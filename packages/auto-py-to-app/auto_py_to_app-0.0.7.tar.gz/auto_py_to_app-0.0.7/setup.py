#!/usr/bin/python
#coding = utf-8

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto-py-to-app", # Replace with your own username
    version="0.0.7",
    author="Syuya_Murakami",
    author_email="wxy135@mail.ustc.edu.cn",
    description="auto-py-to-app is a cx-Freeze GUI to package .py into .exe or excutable files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://auto-py-to-app-doc.readthedocs.io/zh/latest/",
    project_urls={
        "Bug Tracker": "https://auto-py-to-app-doc.readthedocs.io/zh/latest/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    keywords=['gui', 'executable'],
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    install_requires=['Eel==0.14.0', 'cx-Freeze>=6.15.0'],
    python_requires=">=3.9",
    entry_points={
        'console_scripts': [
            'autopytoapp=auto_py_to_app.__main__:run',
            'auto-py-to-app=auto_py_to_app.__main__:run'
        ]
    }
)
