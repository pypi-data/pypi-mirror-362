from setuptools import setup, find_packages

setup(
    name="pyservinit",
    version="0.1.3",
    description="CLI to scaffold a default Python service structure",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Aditya Thiyyagura",
    author_email="thiyyaguraadityareddy@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pyservinit = pyservinit.scaffolder:main"
        ]
    },
    package_data={
        "pyservinit": ["templates/*.template"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
