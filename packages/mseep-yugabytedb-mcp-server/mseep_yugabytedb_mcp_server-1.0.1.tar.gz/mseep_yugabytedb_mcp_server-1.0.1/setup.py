from setuptools import setup, find_packages

setup(
    name='mseep-yugabytedb-mcp-server',
    version='1.0.1',
    description='Add your description here',
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
    install_requires=['mcp[cli]>=1.9.4', 'httpx~=0.28.0', 'fastapi>=0.115.12', "psycopg2-yugabytedb>=2.9.3.5; sys_platform == 'darwin'", "psycopg2-yugabytedb-binary>=2.9.3.5; sys_platform != 'darwin'"],
    keywords=['mseep'],
)
