"""
Setup script for robot_kinematics library.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A comprehensive robotics kinematics library for Python."

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="robot_kinematics",
    version="1.1.0",
    author="Sherin Joseph Roy",
    author_email="sherin.joseph2217@gmail.com",
    description="A comprehensive robotics kinematics library with URDF and PyBullet integration",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sherin-SEF-AI/robo-kinematics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "nbsphinx>=0.8.0",
        ],
        "visualization": [
            "pybullet>=3.2.0",
            "matplotlib>=3.5.0",
        ],
        "full": [
            "pybullet>=3.2.0",
            "matplotlib>=3.5.0",
            "scipy>=1.8.0",
            "lxml>=4.6.0",
            "xmltodict>=0.12.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="robotics, kinematics, forward-kinematics, inverse-kinematics, jacobian, urdf, pybullet",
    project_urls={
        "Bug Reports": "https://github.com/Sherin-SEF-AI/robo-kinematics/issues",
        "Source": "https://github.com/Sherin-SEF-AI/robo-kinematics",
        "Documentation": "https://robotkinematics.readthedocs.io/",
    },
) 