from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='codicent-py',
    version='1.3.5',
    author='Johan',
    author_email='johan@example.com',
    description='Python interface to the Codicent API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/izaxon/codicent-py',
    project_urls={
        'Bug Tracker': 'https://github.com/izaxon/codicent-py/issues',
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        'requests>=2.25.0',
    ],
)
