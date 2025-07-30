from setuptools import setup, find_packages

setup(
    name='mseep-tidal-mcp',
    version='0.1.0',
    description='A package republished under mseep',
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
    install_requires=['flask>=3.1.0', 'mcp[cli]>=1.6.0', 'requests>=2.32.3', 'tidalapi>=0.8.3'],
    keywords=['mseep'],
)
