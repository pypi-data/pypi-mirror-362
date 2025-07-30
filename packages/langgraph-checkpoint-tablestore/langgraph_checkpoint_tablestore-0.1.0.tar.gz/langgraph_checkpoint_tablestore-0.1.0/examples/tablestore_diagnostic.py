"""
Aliyun Table Store Python SDK Diagnostic Script
Used to check Python Tablestore SDK installation status and import issues
"""

import sys
import importlib

def check_python_version():
    """Check Python version"""
    print(f"Python Version: {sys.version}")
    version_info = sys.version_info
    
    if version_info.major == 3 and version_info.minor >= 9:
        print("✓ Python version supported")
        return True
    else:
        print("✗ Python version not supported, Python 3.9+ is required")
        return False

def check_tablestore_installation():
    """Check if tablestore package is installed"""
    try:
        import tablestore # pyright: ignore
        print(f"✓ tablestore installed, Version: {getattr(tablestore, '__version__', 'Unknown')}")
        print(f"✓ tablestore path: {tablestore.__file__}")
        return True
    except ImportError as e:
        print(f"✗ tablestore import failed: {e}")
        return False

def check_protobuf():
    """Check protobuf version"""
    try:
        import google.protobuf
        print(f"✓ protobuf version: {google.protobuf.__version__}")
        return True
    except ImportError:
        print("✗ protobuf not installed")
        return False

def check_dependencies():
    """Check other dependencies"""
    dependencies = [
        'urllib3',
        'six',
        'certifi',
        'future',
        'flatbuffers',
        'numpy',
        'google.protobuf'
    ]
    
    print("\nChecking dependencies:")
    for dep in dependencies:
        try:
            module = importlib.import_module(dep)
            version = getattr(module, '__version__', 'Unknown')
            print(f"✓ {dep}: {version}")
        except ImportError:
            print(f"✗ {dep}: Not installed")

def test_basic_import():
    """Test basic imports"""
    print("\nTesting basic imports:")
    test_imports = [
        'tablestore',
        'tablestore.metadata',
        'tablestore.aggregation',
        'tablestore.group_by',
        'tablestore.error',
        'tablestore.retry',
        'tablestore.credentials',
        'tablestore.const_module',
    ]

    for module_name in test_imports:
        try:
            importlib.import_module(module_name)
            print(f"✓ {module_name}")
        except ImportError as e:
            print(f"✗ {module_name}: {e}")

def test_client_creation():
    """Test client creation"""
    print("\nTesting client creation:")
    try:
        from tablestore import OTSClient # pyright: ignore
        # Test client creation with dummy configuration
        client = OTSClient(
            end_point='https://test.cn-hangzhou.ots.aliyuncs.com',
            access_key_id='test',
            access_key_secret='test',
            instance_name='test',
        )
        print(f"✓ OTSClient created successfully: {client}")
        return True
    except Exception as e:
        print(f"✗ OTSClient creation failed: {e}")
        return False


def main():
    """Main function"""
    print("Aliyun Table Store Python SDK Diagnostic Tool")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check tablestore installation
    tablestore_ok = check_tablestore_installation()
    
    # Check protobuf
    check_protobuf()
    
    # Check dependencies
    check_dependencies()
    
    if tablestore_ok:
        # Test basic imports
        test_basic_import()
        
        # Test client creation
        test_client_creation()


if __name__ == "__main__":
    main()