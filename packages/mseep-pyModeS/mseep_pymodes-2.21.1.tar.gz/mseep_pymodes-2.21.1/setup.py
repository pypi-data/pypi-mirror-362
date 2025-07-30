from setuptools import setup, find_packages

setup(
    name='mseep-pyModeS',
    version='2.21.1',
    description='Python Mode-S and ADS-B Decoder',
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
    install_requires=['numpy>=1.26', 'pyzmq>=24.0'],
    keywords=['mseep'],
)
