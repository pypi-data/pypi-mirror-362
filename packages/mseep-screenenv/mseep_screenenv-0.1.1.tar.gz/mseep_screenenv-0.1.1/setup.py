from setuptools import setup, find_packages

setup(
    name='mseep-screenenv',
    version='0.1.1',
    description='A powerful Python library for creating and managing isolated desktop environments using Docker containers',
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
    install_requires=['pydantic>=2.11.7', 'psutil>=7.0.0', 'docker>=7.1.0', 'filelock>=3.18.0', 'playwright>=1.52.0', 'fastapi>=0.115.13', 'requests>=2.32.4', 'uvicorn>=0.15.0', 'mcp>=1.9.4', 'smolagents[openai]==1.15.0', 'huggingface_hub==0.33.1', 'openai==1.91.0', 'prompt-toolkit==3.0.51'],
    keywords=['mseep', 'docker', 'automation', 'gui', 'sandbox', 'desktop', 'playwright'],
)
