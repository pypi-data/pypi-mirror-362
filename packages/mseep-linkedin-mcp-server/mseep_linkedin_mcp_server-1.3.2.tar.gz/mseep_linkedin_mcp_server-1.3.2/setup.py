from setuptools import setup, find_packages

setup(
    name='mseep-linkedin-mcp-server',
    version='1.3.2',
    description='MCP server for LinkedIn profile, company, and job scraping with Claude AI integration. Supports direct profile/company/job URL scraping with secure credential storage.',
    long_description="Package managed by MseeP.ai",
    long_description_content_type="text/plain",
    author='mseep',
    author_email='support@skydeck.ai',
    maintainer='mseep',
    maintainer_email='support@skydeck.ai',
    url='https://github.com/mseep',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['fastmcp>=2.10.1', 'inquirer>=3.4.0', 'keyring>=25.6.0', 'linkedin-scraper', 'pyperclip>=1.9.0'],
    keywords=['mseep'],
)
