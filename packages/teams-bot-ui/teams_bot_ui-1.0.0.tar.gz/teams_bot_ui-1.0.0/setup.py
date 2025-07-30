from setuptools import setup, find_packages
import os


# Read version from the package
def get_version():
    """Get version from __init__.py"""
    version_file = os.path.join(
        os.path.dirname(__file__), "teams_bot_ui", "__init__.py"
    )
    with open(version_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"


# Read the README file
def get_long_description():
    """Get long description from README.md"""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as fh:
            return fh.read()
    return ""


# Read requirements
def get_requirements():
    """Get requirements from requirements.txt"""
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(req_path):
        with open(req_path, "r", encoding="utf-8") as fh:
            return [
                line.strip() for line in fh if line.strip() and not line.startswith("#")
            ]
    return ["botbuilder-core>=4.14.0"]


setup(
    name="teams-bot-ui",
    version=get_version(),
    author="Shubham Shinde",
    author_email="shubhamshinde7995@gmail.com",
    description="A comprehensive Python library for creating rich Microsoft Teams bot cards with Adaptive Cards support",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/shubhamshinde7995/teams-bot-ui",
    project_urls={
        "Bug Tracker": "https://github.com/shubhamshinde7995/teams-bot-ui/issues",
        "Documentation": "https://github.com/shubhamshinde7995/teams-bot-ui#readme",
        "Source": "https://github.com/shubhamshinde7995/teams-bot-ui",
        "Download": "https://pypi.org/project/teams-bot-ui/",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Conferencing",
        "Topic :: Software Development :: User Interfaces",
        "Environment :: Console",
        "Natural Language :: English",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=get_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0",
            "mypy>=0.950",
            "flake8>=4.0",
            "twine>=4.0.0",
            "build>=0.7.0",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "pytest-cov>=3.0.0",
        ],
    },
    keywords=[
        "microsoft teams",
        "bot",
        "adaptive cards",
        "ui",
        "chatbot",
        "assistant",
        "conversation",
        "bot framework",
        "teams bot",
        "cards",
        "interactive",
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        # Add console scripts if needed in the future
    },
)
