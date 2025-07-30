from setuptools import setup, find_packages

setup(
    name='mseep-frontend-dev-assistant-mcp',
    version='0.1.0',
    description='前端开发提示词智能助手 MCP服务器 - 专为前端团队设计的AI开发助手',
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
    install_requires=['mcp>=0.3.0', 'pydantic>=2.0.0', 'typing-extensions>=4.0.0', 'aiofiles>=23.0.0', 'pathlib2>=2.3.0'],
    keywords=['mseep'],
)
