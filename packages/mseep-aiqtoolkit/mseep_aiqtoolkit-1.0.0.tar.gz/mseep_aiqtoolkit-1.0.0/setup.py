from setuptools import setup, find_packages

setup(
    name='mseep-aiqtoolkit',
    version='1.0.0',
    description='NVIDIA Agent Intelligence toolkit',
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
    install_requires=['aioboto3>=11.0.0', 'click~=8.1', 'colorama~=0.4.6', 'expandvars~=1.0', 'fastapi~=0.115.5', 'httpx~=0.27', 'jinja2~=3.1', 'jsonpath-ng~=1.7', 'mcp~=1.10', 'networkx~=3.4', 'numpy~=1.26', 'openinference-semantic-conventions~=0.1.14', 'openpyxl~=3.1', 'pkginfo~=1.12', 'platformdirs~=4.3', 'pydantic==2.10.*', 'pymilvus~=2.4', 'PyYAML~=6.0', 'ragas~=0.2.14', 'rich~=13.9', 'tabulate~=0.9', 'uvicorn[standard]~=0.32.0', 'wikipedia~=1.4'],
    keywords=['mseep', 'ai', 'rag', 'agents'],
)
