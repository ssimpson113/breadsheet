"""
Build script to create executables for Breadsheet using PyInstaller.
This script automatically detects the platform and builds accordingly.
"""

import os
import sys
import platform
import subprocess


def build_executable():
    """Build the executable for the current platform."""

    print("=" * 60)
    print("Breadsheet Executable Builder")
    print("=" * 60)
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    print()

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("ERROR: PyInstaller is not installed!")
        print("Install it with: pip install pyinstaller")
        sys.exit(1)

    # Determine the separator for --add-data based on platform
    separator = ";" if platform.system() == "Windows" else ":"

    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",           # Single executable file
        "--windowed",          # No console window (GUI only)
        "--name=Breadsheet",   # Name of executable
        f"--add-data=breadsheet{separator}breadsheet",  # Include package
        "--icon=NONE",         # You can add an icon file here
        "app.py"
    ]

    print("Building executable with command:")
    print(" ".join(cmd))
    print()
    print("This may take a few minutes...")
    print()

    # Run PyInstaller
    try:
        result = subprocess.run(cmd, check=True)

        print()
        print("=" * 60)
        print("BUILD SUCCESSFUL!")
        print("=" * 60)
        print()
        print(f"Executable location: {os.path.join('dist', 'Breadsheet')}")
        print()
        print("You can now:")
        print("1. Test the executable in the dist/ folder")
        print("2. Distribute it to users on the same platform")
        print("3. Create a GitHub Release and upload it")
        print()
        print("Note: Executables are platform-specific!")
        print("Build on Windows for Windows, macOS for macOS, etc.")
        print()

    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("BUILD FAILED!")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        print("Troubleshooting:")
        print("1. Make sure all dependencies are installed")
        print("2. Try running: pip install -r requirements.txt")
        print("3. Check that app.py exists in the current directory")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()
