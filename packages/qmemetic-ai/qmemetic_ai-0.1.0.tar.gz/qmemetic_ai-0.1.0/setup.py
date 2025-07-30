from setuptools import setup, find_packages
import platform
import subprocess

def check_python_version():
    major, minor = platform.python_version_tuple()[:2]
    if int(major) < 3 or int(minor) < 7:
        raise RuntimeError("Q-Memetic AI requires Python 3.7 or higher")

def upgrade_pip():
    try:
        print("Upgrading pip")
        subprocess.check_call(["python", "-m", "pip", "install", "--upgrade", "pip"])
        print("Upgrading pip - Success")
    except subprocess.CalledProcessError:
        print("Upgrading pip - Failed")

def install_requirements():
    try:
        print("Installing dependencies from requirements-prod.txt")
        subprocess.check_call(["pip", "install", "-r", "requirements-prod.txt"])
        print("Installing dependencies from requirements-prod.txt - Success")
    except subprocess.CalledProcessError:
        print("Installing dependencies - Failed")

print("Q-Memetic AI Production Setup")
print("=" * 50)

check_python_version()
upgrade_pip()
install_requirements()

setup(
    name='qmemetic',
    version='0.1.0',
    author='Your Name',
    author_email='your@email.com',
    description='Hybrid Quantum-AI Optimizer Library',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/qmemetic',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Keep this minimal for PyPI; production deps go in requirements-prod.txt
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
