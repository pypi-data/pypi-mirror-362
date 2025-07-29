#!/usr/bin/env python3
"""
Helper script to build and publish the mareana-k8s-mcp-server package to PyPI.
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def publish_to_pypi(token):
    """Publish directly to PyPI using the provided token."""
    print("\n🚀 Publishing to PyPI...")
    
    # Set the token as environment variable
    env = os.environ.copy()
    env["TWINE_USERNAME"] = "__token__"
    env["TWINE_PASSWORD"] = token
    
    try:
        result = subprocess.run(
            ["uv", "run", "twine", "upload", "dist/*"],
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Successfully published to PyPI!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed to publish to PyPI!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main function to build and publish the package."""
    print("📦 Building and Publishing mareana-k8s-mcp-server")
    print("=" * 55)
    
    # Check if we're in the right directory
    if not os.path.exists("pyproject.toml"):
        print("❌ Error: pyproject.toml not found. Make sure you're in the project root directory.")
        sys.exit(1)
    
    # Clean previous builds
    if not run_command("rm -rf dist/ build/ *.egg-info/", "Cleaning previous builds"):
        sys.exit(1)
    
    # Build the package using uv
    if not run_command("uv run python -m build", "Building package"):
        print("\n💡 Hint: Make sure uv and build tools are installed")
        sys.exit(1)
    
    # Check the built package using uv
    if not run_command("uv run twine check dist/*", "Checking package"):
        sys.exit(1)
    
    print("\n🎯 Package built successfully!")
    print("📁 Files created in dist/ directory:")
    
    # List the created files
    try:
        for file in os.listdir("dist"):
            print(f"   - {file}")
    except OSError:
        pass
    
    # Check if PyPI token is provided as argument
    if len(sys.argv) > 1:
        token = sys.argv[1]
        if token.startswith("pypi-"):
            if publish_to_pypi(token):
                print("\n🎉 Package successfully published to PyPI!")
                print("📦 You can now install it with:")
                print("   pip install mareana-k8s-mcp-server")
                print("   uv add mareana-k8s-mcp-server")
            else:
                sys.exit(1)
        else:
            print("❌ Invalid token format. Token should start with 'pypi-'")
            sys.exit(1)
    else:
        print("\n" + "=" * 55)
        print("🚀 Ready to publish!")
        print("\nTo publish to PyPI, run:")
        print("  python publish.py <your-pypi-token>")
        print("\nOr manually:")
        print("  1. Test on TestPyPI first:")
        print("     uv run twine upload --repository testpypi dist/*")
        print("  2. If everything looks good, upload to PyPI:")
        print("     uv run twine upload dist/*")
        print("\n💡 Make sure you have your PyPI credentials configured!")

if __name__ == "__main__":
    main() 