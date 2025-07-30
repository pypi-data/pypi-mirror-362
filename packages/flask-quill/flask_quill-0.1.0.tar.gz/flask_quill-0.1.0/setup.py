from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

with open(here / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="flask_quill",
    version="0.1.0",
    description="FlaskでQuillリッチテキストエディタを簡単に使える拡張",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=3.0.0",
        "Flask-WTF>=1.2.1",
        "WTForms>=3.1.2",
        "Flask-Bootstrap>=3.3.7.1"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 