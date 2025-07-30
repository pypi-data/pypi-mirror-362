from setuptools import setup, find_packages

setup(
    name='mseep-google-analytics-mcp',
    version='1.0.11',
    description='Google Analytics 4 MCP Server - Access GA4 data in Claude, Cursor and other MCP clients',
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
    install_requires=['fastmcp>=2.0.0', 'google-analytics-data>=0.16.0'],
    keywords=['mseep', 'google-analytics', 'mcp', 'ai-assistant', 'analytics', 'ga4', 'claude', 'cursor', 'windsurf'],
)
