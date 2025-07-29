import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="secmind",
    version="1.5.15",
    author="SecMind xPAM",
    author_email="service@wandoutech.com",
    description="Automation library for xPAM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wandoutech",
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    install_requires=[
        "selenium>=3.141.0", "paramiko>=3.0.0", "pywinrm>=0.5.0", "ddddocr>=1.5.5", "chardet==4.0.0", "dill==0.4.0"
    ],
    python_requires=">=3",
)
