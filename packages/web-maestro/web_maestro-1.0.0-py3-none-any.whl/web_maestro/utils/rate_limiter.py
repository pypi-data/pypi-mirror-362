"""Enhanced rate limiting utilities for API and web requests.

This module provides enhanced rate limiting with:
- Exponential backoff with jitter
- API rate limit detection and handling
- Batch processing with rate control
- Token bucket and sliding window algorithms
"""

import asyncio
from dataclasses import dataclass
from enum import Enum
import logging
import random
import time
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class RateLimitStrategy(Enum):
    """Rate limiting strategies."""

    EXPONENTIAL_BACKOFF = "exponential_backoff"
    FIXED_INTERVAL = "fixed_interval"
    TOKEN_BUCKET = "token_bucket"  # noqa: S105
    SLIDING_WINDOW = "sliding_window"


@dataclass
class RateLimitResult:
    """Result of a rate-limited operation."""

    success: bool
    result: Any = None
    error: Optional[str] = None
    attempts: int = 0
    total_wait_time: float = 0.0
    rate_limited: bool = False


class RateLimiter:
    """Advanced rate limiter with multiple strategies and backoff."""

    def __init__(
        self,
        max_requests_per_second: float = 1.0,
        max_requests_per_minute: float = 60.0,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        jitter: bool = True,
        strategy: RateLimitStrategy = RateLimitStrategy.EXPONENTIAL_BACKOFF,
    ):
        """Initialize rate limiter.

        Args:
            max_requests_per_second: Maximum requests per second
            max_requests_per_minute: Maximum requests per minute
            max_retries: Maximum retry attempts
            base_delay: Base delay between retries (seconds)
            max_delay: Maximum delay between retries (seconds)
            backoff_factor: Exponential backoff factor
            jitter: Whether to add random jitter to delays
            strategy: Rate limiting strategy to use
        """
        self.max_requests_per_second = max_requests_per_second
        self.max_requests_per_minute = max_requests_per_minute
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter
        self.strategy = strategy

        # Track request history
        self.request_times: list[float] = []
        self.last_request_time = 0.0

        # Token bucket for rate limiting
        self.tokens = max_requests_per_second
        self.last_token_update = time.time()

        # Semaphore for concurrent request limiting
        self.semaphore = asyncio.Semaphore(int(max_requests_per_second * 2))

    async def execute(
        self,
        func: Callable,
        *args,
        detect_rate_limit: Optional[Callable[[Exception], bool]] = None,
        **kwargs,
    ) -> RateLimitResult:
        """Execute a function with rate limiting and retry logic.

        Args:
            func: Function to execute (can be sync or async)
            *args: Function arguments
            detect_rate_limit: Function to detect if exception is rate limit error
            **kwargs: Function keyword arguments

        Returns:
            RateLimitResult with execution results
        """
        time.time()
        attempts = 0
        total_wait_time = 0.0

        async with self.semaphore:
            while attempts <= self.max_retries:
                attempts += 1

                try:
                    # Wait for rate limit if needed
                    wait_time = await self._wait_for_rate_limit()
                    total_wait_time += wait_time

                    # Execute function
                    if asyncio.iscoroutinefunction(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = await asyncio.to_thread(func, *args, **kwargs)

                    # Update request tracking
                    self._update_request_tracking()

                    return RateLimitResult(
                        success=True,
                        result=result,
                        attempts=attempts,
                        total_wait_time=total_wait_time,
                    )

                except Exception as e:
                    # Check if this is a rate limit error
                    is_rate_limit = False
                    if detect_rate_limit:
                        is_rate_limit = detect_rate_limit(e)
                    else:
                        is_rate_limit = self._is_rate_limit_error(e)

                    if is_rate_limit:
                        logger.warning(
                            f"Rate limit detected, attempt {attempts}/{self.max_retries + 1}"
                        )

                        if attempts <= self.max_retries:
                            # Calculate backoff delay
                            delay = self._calculate_backoff_delay(attempts)
                            total_wait_time += delay

                            logger.info(f"Backing off for {delay:.2f} seconds")
                            await asyncio.sleep(delay)
                            continue

                    # Non-rate-limit error or max retries exceeded
                    return RateLimitResult(
                        success=False,
                        error=str(e),
                        attempts=attempts,
                        total_wait_time=total_wait_time,
                        rate_limited=is_rate_limit,
                    )

        # Should not reach here
        return RateLimitResult(
            success=False,
            error="Max retries exceeded",
            attempts=attempts,
            total_wait_time=total_wait_time,
            rate_limited=True,
        )

    async def _wait_for_rate_limit(self) -> float:
        """Wait for rate limit based on strategy."""
        if self.strategy == RateLimitStrategy.TOKEN_BUCKET:
            return await self._wait_token_bucket()
        elif self.strategy == RateLimitStrategy.SLIDING_WINDOW:
            return await self._wait_sliding_window()
        else:
            return await self._wait_fixed_interval()

    async def _wait_token_bucket(self) -> float:
        """Wait based on token bucket algorithm."""
        current_time = time.time()

        # Add tokens based on time elapsed
        time_elapsed = current_time - self.last_token_update
        self.tokens = min(
            self.max_requests_per_second,
            self.tokens + time_elapsed * self.max_requests_per_second,
        )
        self.last_token_update = current_time

        # If we have tokens, use one
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return 0.0

        # Wait until we have a token
        wait_time = (1.0 - self.tokens) / self.max_requests_per_second
        await asyncio.sleep(wait_time)
        self.tokens = 0.0

        return wait_time

    async def _wait_sliding_window(self) -> float:
        """Wait based on sliding window algorithm."""
        current_time = time.time()

        # Remove old requests from tracking
        cutoff_time = current_time - 60.0  # 1 minute window
        self.request_times = [t for t in self.request_times if t > cutoff_time]

        # Check if we're under the minute limit
        if len(self.request_times) >= self.max_requests_per_minute:
            # Wait until oldest request falls out of window
            wait_time = self.request_times[0] + 60.0 - current_time
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                return wait_time

        # Check per-second rate
        second_cutoff = current_time - 1.0
        recent_requests = [t for t in self.request_times if t > second_cutoff]

        if len(recent_requests) >= self.max_requests_per_second:
            wait_time = recent_requests[0] + 1.0 - current_time
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                return wait_time

        return 0.0

    async def _wait_fixed_interval(self) -> float:
        """Wait based on fixed interval between requests."""
        current_time = time.time()
        min_interval = 1.0 / self.max_requests_per_second

        if self.last_request_time > 0:
            elapsed = current_time - self.last_request_time
            if elapsed < min_interval:
                wait_time = min_interval - elapsed
                await asyncio.sleep(wait_time)
                return wait_time

        return 0.0

    def _update_request_tracking(self):
        """Update request tracking after successful request."""
        current_time = time.time()
        self.last_request_time = current_time
        self.request_times.append(current_time)

        # Keep only recent requests for memory efficiency
        cutoff_time = current_time - 60.0
        self.request_times = [t for t in self.request_times if t > cutoff_time]

    def _calculate_backoff_delay(self, attempt: int) -> float:
        """Calculate backoff delay for retry attempt."""
        if self.strategy == RateLimitStrategy.EXPONENTIAL_BACKOFF:
            delay = self.base_delay * (self.backoff_factor ** (attempt - 1))
        else:
            delay = self.base_delay

        # Apply jitter
        if self.jitter:
            jitter_amount = delay * 0.1  # 10% jitter
            delay += random.uniform(-jitter_amount, jitter_amount)  # noqa: S311

        # Cap at max delay
        delay = min(delay, self.max_delay)

        return max(0.1, delay)  # Minimum 100ms delay

    def _is_rate_limit_error(self, error: Exception) -> bool:
        """Detect if error is a rate limit error."""
        error_str = str(error).lower()

        # Common rate limit indicators
        rate_limit_indicators = [
            "rate limit",
            "too many requests",
            "429",
            "quota exceeded",
            "throttled",
            "rate exceeded",
            "request limit",
            "api limit",
        ]

        return any(indicator in error_str for indicator in rate_limit_indicators)

    def get_stats(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        current_time = time.time()

        # Count recent requests
        recent_requests_1s = len(
            [t for t in self.request_times if current_time - t <= 1.0]
        )

        recent_requests_1m = len(
            [t for t in self.request_times if current_time - t <= 60.0]
        )

        return {
            "strategy": self.strategy.value,
            "max_requests_per_second": self.max_requests_per_second,
            "max_requests_per_minute": self.max_requests_per_minute,
            "recent_requests_1s": recent_requests_1s,
            "recent_requests_1m": recent_requests_1m,
            "available_tokens": (
                self.tokens if self.strategy == RateLimitStrategy.TOKEN_BUCKET else None
            ),
            "total_tracked_requests": len(self.request_times),
        }


class RateLimitedBatchManager:
    """Manager for processing batches with rate limiting."""

    def __init__(
        self, rate_limiter: RateLimiter, max_concurrent: int = 5, batch_size: int = 10
    ):
        """Initialize batch manager.

        Args:
            rate_limiter: Rate limiter instance
            max_concurrent: Maximum concurrent operations
            batch_size: Size of each batch
        """
        self.rate_limiter = rate_limiter
        self.max_concurrent = max_concurrent
        self.batch_size = batch_size
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def process_batch(
        self,
        items: list[Any],
        func: Callable,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        error_callback: Optional[Callable[[Any, Exception], None]] = None,
    ) -> list[RateLimitResult]:
        """Process a batch of items with rate limiting.

        Args:
            items: List of items to process
            func: Function to apply to each item
            progress_callback: Optional progress callback
            error_callback: Optional error callback

        Returns:
            List of RateLimitResult objects
        """
        if not items:
            return []

        results = []
        processed = 0

        # Process in chunks
        for i in range(0, len(items), self.batch_size):
            batch = items[i : i + self.batch_size]

            # Process batch concurrently with rate limiting
            tasks = []
            for item in batch:
                task = self._process_single_item(item, func, error_callback)
                tasks.append(task)

            # Wait for batch completion
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for j, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    # Create error result
                    error_result = RateLimitResult(
                        success=False, error=str(result), attempts=1
                    )
                    results.append(error_result)

                    if error_callback:
                        error_callback(batch[j], result)
                else:
                    results.append(result)

                processed += 1

                # Call progress callback
                if progress_callback:
                    progress_callback(processed, len(items))

        return results

    async def _process_single_item(
        self, item: Any, func: Callable, error_callback: Optional[Callable]
    ) -> RateLimitResult:
        """Process a single item with rate limiting."""
        async with self.semaphore:
            try:
                return await self.rate_limiter.execute(func, item)
            except Exception as e:
                if error_callback:
                    error_callback(item, e)

                return RateLimitResult(success=False, error=str(e), attempts=1)

    def get_stats(self) -> dict[str, Any]:
        """Get batch manager statistics."""
        return {
            "max_concurrent": self.max_concurrent,
            "batch_size": self.batch_size,
            "rate_limiter_stats": self.rate_limiter.get_stats(),
        }
