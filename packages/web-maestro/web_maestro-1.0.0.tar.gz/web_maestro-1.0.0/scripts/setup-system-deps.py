#!/usr/bin/env python3
"""Setup script for system dependencies required by web-maestro.

This script automatically installs system dependencies like poppler
that are required for PDF processing functionality.
"""

import platform
import shutil
import subprocess
import sys


def run_command(cmd, check=True, shell=False):
    """Run a command and return the result."""
    try:
        if shell:
            result = subprocess.run(  # noqa: S602
                cmd,
                shell=True,
                check=check,
                capture_output=True,
                text=True,  # noqa: S602
            )
        else:
            result = subprocess.run(
                cmd, check=check, capture_output=True, text=True
            )  # noqa: S603
        return result
    except subprocess.CalledProcessError as e:
        if check:
            print(
                f"Error running command: {' '.join(cmd) if isinstance(cmd, list) else cmd}"
            )
            print(f"Exit code: {e.returncode}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            raise
        return e


def check_command_exists(command):
    """Check if a command exists in PATH."""
    return shutil.which(command) is not None


def install_poppler_macos():
    """Install poppler on macOS using Homebrew."""
    print("Installing poppler on macOS...")

    # Check if brew is installed
    if not check_command_exists("brew"):
        print("❌ Homebrew not found. Please install Homebrew first:")
        print(
            '   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        )
        return False

    try:
        # Check if poppler is already installed
        result = run_command(["brew", "list", "poppler"], check=False)
        if result.returncode == 0:
            print("✅ poppler is already installed")
            return True

        # Install poppler
        print("Installing poppler...")
        run_command(["brew", "install", "poppler"])
        print("✅ poppler installed successfully")
        return True

    except subprocess.CalledProcessError:
        print("❌ Failed to install poppler with Homebrew")
        return False


def install_poppler_linux():
    """Install poppler on Linux."""
    print("Installing poppler on Linux...")

    # Try different package managers
    if check_command_exists("apt-get"):
        try:
            print("Using apt-get...")
            run_command(["sudo", "apt-get", "update"])
            run_command(["sudo", "apt-get", "install", "-y", "poppler-utils"])
            print("✅ poppler installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install with apt-get")

    elif check_command_exists("yum"):
        try:
            print("Using yum...")
            run_command(["sudo", "yum", "install", "-y", "poppler-utils"])
            print("✅ poppler installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install with yum")

    elif check_command_exists("dnf"):
        try:
            print("Using dnf...")
            run_command(["sudo", "dnf", "install", "-y", "poppler-utils"])
            print("✅ poppler installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install with dnf")

    elif check_command_exists("pacman"):
        try:
            print("Using pacman...")
            run_command(["sudo", "pacman", "-S", "--noconfirm", "poppler"])
            print("✅ poppler installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install with pacman")

    print("❌ No supported package manager found")
    return False


def install_poppler_windows():
    """Install poppler on Windows."""
    print("❌ Windows poppler installation not automated.")
    print("Please manually install poppler for Windows:")
    print("1. Download from: https://blog.alivate.com.au/poppler-windows/")
    print("2. Extract to a folder (e.g., C:\\poppler)")
    print("3. Add C:\\poppler\\bin to your PATH environment variable")
    print("4. Restart your terminal/IDE")
    return False


def check_poppler_installed():
    """Check if poppler is properly installed."""
    return check_command_exists("pdftoppm") or check_command_exists("pdftocairo")


def main():
    """Main setup function."""
    print("🔧 Setting up system dependencies for web-maestro...")
    print("=" * 50)

    # Check if poppler is already installed
    if check_poppler_installed():
        print("✅ poppler is already installed and available")
        return True

    # Install based on platform
    system = platform.system().lower()
    success = False

    if system == "darwin":
        success = install_poppler_macos()
    elif system == "linux":
        success = install_poppler_linux()
    elif system == "windows":
        success = install_poppler_windows()
    else:
        print(f"❌ Unsupported platform: {system}")
        return False

    if success:
        # Verify installation
        if check_poppler_installed():
            print("✅ All system dependencies installed successfully!")
        else:
            print("⚠️  poppler was installed but not found in PATH")
            print("   You may need to restart your terminal")
    else:
        print("❌ Failed to install system dependencies")
        print("\nManual installation instructions:")
        print("- macOS: brew install poppler")
        print("- Ubuntu/Debian: sudo apt-get install poppler-utils")
        print("- CentOS/RHEL: sudo yum install poppler-utils")
        print("- Windows: Download from https://blog.alivate.com.au/poppler-windows/")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
