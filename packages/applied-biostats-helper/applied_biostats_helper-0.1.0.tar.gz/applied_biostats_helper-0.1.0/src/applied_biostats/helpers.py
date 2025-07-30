"""
Core helper functions for Applied Biostats course environment setup.
"""

import os
import sys
import subprocess
import warnings
import zipfile
import requests


def is_colab():
    """
    Detect if running in Google Colab environment.
    
    Returns:
        bool: True if running in Colab, False otherwise
    """
    try:
        import google.colab
        return True
    except ImportError:
        return False


def is_tests_present():
    """
    Check if test directories are present in the current directory.
    Assumes that the test directories are named 'lab-tests' or 'walkthrough-tests'.

    Returns:
        bool: True if tests are present, False otherwise.
    """
    return os.path.isdir('lab-tests') or os.path.isdir('walkthrough-tests')


def ensure_dependencies():
    """
    Ensure required dependencies are installed.
    
    Installs otter-grader if not already present.
    """
    required_packages = ['otter-grader==4.0.0']
    
    for package in required_packages:
        package_name = package.split('==')[0].replace('-', '_')
        try:
            __import__(package_name)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-q', package
            ], check=True)


def download_tests(module_name, repo_url, branch='main'):
    """
    Download and extract test files from GitHub repository.
    
    Args:
        module_name (str): Name of the module (e.g., 'Module02')
        repo_url (str): GitHub repository URL
        branch (str): Git branch to download from (default: 'main')
    
    """
    
    # Clean up repo URL
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    if repo_url.endswith('/'):
        repo_url = repo_url[:-1]

    # Construct download URL for the zip file
    zip_filename = f"{module_name}_files.zip"
    # Adjust based on repo
    #raw/refs/heads/main/
    download_url = f"{repo_url}/raw/refs/heads/{branch}/tests/{zip_filename}"
    
    print(f"Downloading tests from: {download_url}")
    
    try:
        # Download the zip file
        response = requests.get(download_url)
        response.raise_for_status()
        
        # Save zip file
        with open(zip_filename, 'wb') as f:
            f.write(response.content)
        
        # Extract zip file
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall()
        
        # Clean up zip file
        os.remove(zip_filename)
        
        # Return the tests directory path
        assert is_tests_present(), 'Tests directory not found after extraction!'
            
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to download tests: {e}")
    except zipfile.BadZipFile as e:
        raise RuntimeError(f"Invalid zip file: {e}")


def init_grader(assignment_type, colab=None):
    """
    Initialize the otter grader with proper configuration.
    
    Args:
        assignment_type (str): Type of assignment, 'lab' or 'walkthrough'
        colab (bool): Whether running in Colab (auto-detected if None)
    
    Returns:
        otter.Notebook: Configured grader instance
    """
    try:
        import otter
    except ImportError:
        raise ImportError("otter-grader not found. Run ensure_dependencies() first.")
    
    # Auto-detect environment if not specified
    if colab is None:
        colab = is_colab()
    
    print(f"Initializing grader for {assignment_type}")
    print(f"Colab mode: {colab}")
    
    # Initialize grader
    grader = otter.Notebook(colab=colab, tests_dir=f"{assignment_type}-tests")
    
    return grader


def setup_environment(assignment_name, github_repo_url=None, branch='main'):
    """
    One-line setup for Applied Biostats course environments.
    
    This function:
    1. Detects the environment (Colab vs local)
    2. Installs required dependencies
    3. Downloads test files from GitHub
    4. Initializes the otter grader
    
    Args:
        assignment_name (str): Name of the assignment (e.g., 'Module02_walkthrough')
        github_repo_url (str): GitHub repository URL
        branch (str): Git branch to download from (default: 'main')
        tests_dir (str): Directory name containing tests in repo (default: 'tests')
    
    Returns:
        otter.Notebook: Configured grader instance ready for use
    
    Example:
        >>> grader = setup_environment('Module02_walkthrough', 
        ...                           'https://github.com/your-org/applied_biostats')
    """
    # Suppress warnings for cleaner output
    warnings.filterwarnings("ignore")

    if github_repo_url is None:
        github_repo_url = 'https://github.com/DamLabResources/quantitative-reasoning-in-biology'
    
    print(f"Setting up environment for {assignment_name}...")

    module_name, assignment_type = assignment_name.split('_')
    
    # Ensure dependencies are installed
    # ensure_dependencies()
    
    # Check if tests already exist (avoid re-downloading)
    if not is_tests_present():
        # Download and extract tests
        download_tests(module_name, github_repo_url, branch)
    
    # Initialize and return grader
    grader = init_grader(assignment_type)
    
    print("Environment setup complete!")
    return grader


