#!/usr/bin/env python3
"""
Test script to verify that the PyPI package includes all necessary files.
This script builds the package and checks the contents.
"""

import os
import sys
import subprocess
import tempfile
import zipfile
import tarfile
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False, result.stderr
    return True, result.stdout

def check_package_contents():
    """Build the package and check its contents"""
    print("=" * 60)
    print("TESTING ESCOBAR PACKAGE CONTENTS")
    print("=" * 60)
    
    # Clean previous builds
    print("\n1. Cleaning previous builds...")
    success, output = run_command("rm -rf dist/ build/ *.egg-info/")
    if not success:
        print("Warning: Could not clean previous builds")
    
    # Build the package
    print("\n2. Building the package...")
    success, output = run_command("python -m build")
    if not success:
        print("ERROR: Failed to build package")
        return False
    
    print("Build completed successfully!")
    
    # Check dist directory
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("ERROR: dist directory not found")
        return False
    
    # Find the wheel and source distribution
    wheel_files = list(dist_dir.glob("*.whl"))
    tar_files = list(dist_dir.glob("*.tar.gz"))
    
    if not wheel_files:
        print("ERROR: No wheel file found")
        return False
    
    if not tar_files:
        print("ERROR: No source distribution found")
        return False
    
    wheel_file = wheel_files[0]
    tar_file = tar_files[0]
    
    print(f"\n3. Checking wheel contents: {wheel_file.name}")
    check_wheel_contents(wheel_file)
    
    print(f"\n4. Checking source distribution contents: {tar_file.name}")
    check_tar_contents(tar_file)
    
    return True

def check_wheel_contents(wheel_file):
    """Check the contents of the wheel file"""
    print(f"Examining wheel: {wheel_file}")
    
    critical_files = [
        "static/oauth-callback.html",
        "schemas/escobar/plugin.json",
        "escobar/labextension/package.json",
        "escobar/labextension/static/style.js"
    ]
    
    icon_files = [
        "lib/icons/key-icon.js",
        "lib/icons/voitta-icon.js"
    ]
    
    with zipfile.ZipFile(wheel_file, 'r') as zf:
        file_list = zf.namelist()
        
        print("\nWheel contents:")
        for file in sorted(file_list):
            print(f"  {file}")
        
        print("\nChecking critical files:")
        for critical_file in critical_files:
            # Look for the file in the wheel (it might be in a subdirectory)
            found_files = [f for f in file_list if critical_file in f]
            if found_files:
                print(f"  ✓ {critical_file} found as: {found_files[0]}")
            else:
                print(f"  ✗ {critical_file} NOT FOUND")
        
        print("\nChecking icon files:")
        for icon_file in icon_files:
            found_files = [f for f in file_list if icon_file in f]
            if found_files:
                print(f"  ✓ {icon_file} found as: {found_files[0]}")
            else:
                print(f"  ✗ {icon_file} NOT FOUND")
        
        # Check if static files are properly included
        static_files = [f for f in file_list if 'static' in f and 'oauth-callback' in f]
        if static_files:
            print(f"\nStatic files found:")
            for sf in static_files:
                print(f"  {sf}")
                # Try to read the content to verify it's the OAuth callback
                try:
                    content = zf.read(sf).decode('utf-8')
                    if 'OAuth Callback' in content and 'GOOGLE_OAUTH_CODE_SUCCESS' in content:
                        print(f"    ✓ Content verified - OAuth callback HTML is correct")
                    else:
                        print(f"    ✗ Content verification failed - not the expected OAuth callback")
                except Exception as e:
                    print(f"    ✗ Could not read content: {e}")
        else:
            print(f"\n✗ No static OAuth callback files found in wheel")

def check_tar_contents(tar_file):
    """Check the contents of the source distribution"""
    print(f"Examining source distribution: {tar_file}")
    
    critical_files = [
        "static/oauth-callback.html",
        "schema/plugin.json",
        "src/icons/key-icon.ts",
        "src/icons/voitta-icon.ts"
    ]
    
    with tarfile.open(tar_file, 'r:gz') as tf:
        file_list = tf.getnames()
        
        print("\nSource distribution contents (first 20 files):")
        for file in sorted(file_list)[:20]:
            print(f"  {file}")
        if len(file_list) > 20:
            print(f"  ... and {len(file_list) - 20} more files")
        
        print("\nChecking critical files in source:")
        for critical_file in critical_files:
            found_files = [f for f in file_list if critical_file in f]
            if found_files:
                print(f"  ✓ {critical_file} found as: {found_files[0]}")
            else:
                print(f"  ✗ {critical_file} NOT FOUND")

def main():
    """Main function"""
    if not Path("pyproject.toml").exists():
        print("ERROR: This script must be run from the project root directory")
        sys.exit(1)
    
    success = check_package_contents()
    
    if success:
        print("\n" + "=" * 60)
        print("PACKAGE CONTENT CHECK COMPLETED")
        print("=" * 60)
        print("Review the output above to ensure all critical files are included.")
        print("Pay special attention to:")
        print("- static/oauth-callback.html (needed for Google auth)")
        print("- schema/plugin.json (needed for JupyterLab settings)")
        print("- Icon files (key-icon.js, voitta-icon.js)")
        print("- JupyterLab extension files in escobar/labextension/")
    else:
        print("\nERROR: Package content check failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
