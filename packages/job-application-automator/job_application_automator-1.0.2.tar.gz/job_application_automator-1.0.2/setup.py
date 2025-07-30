from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as fh:
            return fh.read()
    return "Automated job application form extraction and filling with MCP integration"

setup(
    name="job-application-automator",
    version="1.0.2",
    author="Job Automator Team",
    author_email="contact@jobautomator.dev",
    description="Automated job application form extraction and filling with MCP integration",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/jobautomator/job-application-automator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
    ],
    python_requires=">=3.10",
    install_requires=[
        # Core MCP
        "mcp>=1.11.0",
        "pydantic>=2.0.0", 
        "typing-extensions>=4.8.0",
        
        # Form automation
        "playwright>=1.40.0",
        "undetected-playwright>=0.3.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "requests>=2.28.0",
        "httpx",
        
        # Location and utilities
        "geocoder>=1.38.1",
    ],
    entry_points={
        "console_scripts": [
            "job-automator-mcp=job_application_automator.mcp_server:main",
            "job-automator-setup=job_application_automator.setup_claude:main",
        ],
    },
    include_package_data=True,
    package_data={
        "job_application_automator": ["*.md", "*.txt", "*.json"],
        "job_application_automator.mcp": ["*.md", "*.json"],
    },
    zip_safe=False,
)
