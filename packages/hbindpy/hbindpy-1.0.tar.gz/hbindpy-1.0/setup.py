from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='hbindpy',
    version='1.0',
    description='hbindpy',
    long_description=long_description,
    author='huang yi yi',
    author_email='363766687@qq.com',
    packages=find_packages(),
    package_dir={'hbindpy': 'hbindpy'},
    package_data={"hbindpy": ["**"]},
    include_package_data=True,
    install_requires=[
        "colorama",
        "pyinstaller; platform_system=='Windows'",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "hbindpy = hbindpy.__main__:main"
        ]
    },
)