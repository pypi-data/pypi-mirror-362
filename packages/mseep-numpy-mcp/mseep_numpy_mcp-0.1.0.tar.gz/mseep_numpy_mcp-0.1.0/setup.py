from setuptools import setup, find_packages

setup(
    name='mseep-numpy-mcp',
    version='0.1.0',
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
    install_requires=['matplotlib>=3.10.3', 'mcp[cli]>=1.9.2', 'numpy>=2.2.6', 'sympy>=1.14.0', 'typing', 'pydantic'],
    keywords=['mseep'],
)
