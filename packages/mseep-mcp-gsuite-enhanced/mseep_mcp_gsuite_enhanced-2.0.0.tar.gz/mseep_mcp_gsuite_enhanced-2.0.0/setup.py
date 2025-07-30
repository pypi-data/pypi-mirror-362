from setuptools import setup, find_packages

setup(
    name='mseep-mcp-gsuite-enhanced',
    version='2.0.0',
    description='Enhanced MCP server for Google Workspace integration with comprehensive Gmail API coverage and advanced email management',
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
    install_requires=['google-api-python-client>=2.171.0', 'mcp>=1.3.0', 'oauth2client>=4.1.3', 'pytz>=2024.2'],
    keywords=['mseep', 'mcp', 'google', 'gmail', 'calendar', 'google-meet', 'email-management', 'labels', 'archive', 'model-context-protocol'],
)
