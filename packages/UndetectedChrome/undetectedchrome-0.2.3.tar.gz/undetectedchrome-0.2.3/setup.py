from setuptools import setup, find_packages

setup(
    name="UndetectedChrome",
    version="0.2.3",
    description="A comprehensive browser automation class using nodriver.",
    author="guocity",
    author_email="your.email@example.com",
    packages=find_packages(include=["UndetectedChrome*"], exclude=["tests", "tests.*"]),
    install_requires=[
        "nodriver",
        "websockets"
    ],
    python_requires=">=3.7",
    include_package_data=True,
    url="https://github.com/guocity/UndetectedChrome",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'uc=UndetectedChrome.cli:main',
        ],
    },
)
