from setuptools import setup, find_packages

setup(
    name='mseep-hh-mcp-comfyui',
    version='2025.07.01.01',
    description='基于Model Context Protocol (MCP)的ComfyUI图像生成服务，通过API调用本地ComfyUI实例生成图片,实现自然语言生图自由',
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
    install_requires=['httpx>=0.28.1', 'mcp[cli]>=1.6.0', 'websockets>=15.0.1', 'websocket-client>=1.8.0', 'aiohttp>=3.9.5', 'aiofiles>=23.2.1'],
    keywords=['mseep'],
)
