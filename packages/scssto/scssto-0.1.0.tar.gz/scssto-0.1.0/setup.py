from setuptools import setup, find_packages

setup(
    name="scssto",
    version="0.1.0",
    description="Compile all .scss files from a folder into .css",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Axmadjon Qaxxorov",
    author_email="qaxxorovc.work@gmail.com",
    url="https://taplink.cc/qaxxorovc",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "scsscompile=scsscompile.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
