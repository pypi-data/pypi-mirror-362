from setuptools import setup, find_packages

setup(
    name='mseep-swiftlens',
    version='0.2.14',
    description="SwiftLens is a Model Context Protocol (MCP) server that provides deep, semantic-level analysis of Swift codebases to any AI models. By integrating directly with Apple's SourceKit-LSP, SwiftLens ena...",
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
    install_requires=['mcp>=1.0.0', 'fastmcp>=0.1.0', 'pydantic>=2.0.0', 'fastapi>=0.110.0', 'uvicorn>=0.24.0', 'websockets>=12.0', 'aiosqlite>=0.19.0', 'httpx>=0.25.0', 'swiftlens-core>=0.1.9', 'rpds-py>=0.20.0'],
    keywords=['mseep'],
)
