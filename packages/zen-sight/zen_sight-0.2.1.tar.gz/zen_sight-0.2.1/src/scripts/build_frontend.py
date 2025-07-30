#!/usr/bin/env python3
"""Build the React frontend with Vite and copy to package"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def build_frontend():
    # Get paths
    script_path = Path(__file__).resolve()
    src_dir = script_path.parent.parent
    frontend_dir = src_dir / "frontend"
    build_dir = frontend_dir / "dist"  # Vite outputs to 'dist' instead of 'build'
    target_dir = src_dir / "zen_sight" / "static"

    print(f"Frontend dir: {frontend_dir}")
    print(f"Build dir: {build_dir}")
    print(f"Target dir: {target_dir}")

    # Check if npm is installed
    try:
        result = subprocess.run(
            ["npm", "--version"], check=True, capture_output=True, text=True
        )
        print(f"npm version: {result.stdout.strip()}")
    except:
        print("Error: npm is not installed. Please install Node.js and npm.")
        sys.exit(1)

    # Check if frontend directory exists
    if not frontend_dir.exists():
        print(f"Error: Frontend directory {frontend_dir} does not exist.")
        sys.exit(1)

    # Change to frontend directory
    os.chdir(frontend_dir)

    # Install dependencies if needed
    if not (frontend_dir / "node_modules").exists():
        print("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], check=True)

    # Build frontend with Vite
    print("Building React frontend with Vite...")
    subprocess.run(["npm", "run", "build"], check=True)

    # Check if build directory was created
    if not build_dir.exists():
        print(f"Error: Build directory {build_dir} was not created.")
        print("Make sure 'npm run build' completed successfully.")
        sys.exit(1)

    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy build files to static directory
    print(f"Copying build files from {build_dir} to {target_dir}")

    # Remove old static files
    for item in target_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    # Copy new files
    for item in build_dir.iterdir():
        if item.is_dir():
            shutil.copytree(item, target_dir / item.name)
        else:
            shutil.copy2(item, target_dir)

    print("Frontend build complete!")

    # List files in static directory to confirm
    print("\nFiles in static directory:")
    for item in target_dir.rglob("*"):
        if item.is_file():
            print(f"  {item.relative_to(target_dir)}")


if __name__ == "__main__":
    build_frontend()
