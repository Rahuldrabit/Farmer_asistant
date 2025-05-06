import importlib.util
import sys

def check_package(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"❌ {package_name} is NOT installed")
        return False
    else:
        package = importlib.import_module(package_name)
        if hasattr(package, '__version__'):
            print(f"✅ {package_name} is installed (version: {package.__version__})")
        else:
            print(f"✅ {package_name} is installed (version unknown)")
        return True

# Check essential packages
packages = ["fastapi", "uvicorn", "transformers", "torch", "PIL"]
all_installed = True

print("Checking package installations...")
for package in packages:
    if not check_package(package):
        all_installed = False

if all_installed:
    print("\nAll required packages are installed! Your environment is ready.")
else:
    print("\n⚠️ Some packages are missing. Please install them using:")
    print("pip install -r requirements.txt")
