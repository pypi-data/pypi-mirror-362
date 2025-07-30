from setuptools import setup, find_packages

setup(
    name='mseep-mcp-google-ads',
    version='0.1.0',
    description='Google Ads API integration for Model Context Protocol (MCP)',
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
    install_requires=['google-api-python-client>=2.163.0', 'google-auth-httplib2>=0.2.0', 'google-auth-oauthlib>=1.2.1', 'mcp[cli]>=1.3.0'],
    keywords=['mseep', 'mcp', 'google ads', 'seo', 'sem', 'claude', 'search analytics'],
)
