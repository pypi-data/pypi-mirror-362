# setup.py
import sys
from setuptools import setup, find_packages

try:
    setup(
        name="py-import-scanner",
        version="0.1.1",
        description="CLI tool to list and classify Python imports in a project.",
        long_description=open("README.md", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        author="Harshmeet Singh",
        author_email="harshmeetsingh010@gmail.com",
        url="https://github.com/harshmeet-1029/importscanner",
        packages=find_packages(),
        install_requires=["stdlib-list>=0.8.0", "setuptools>=42", "wheel"],
        entry_points={
            "console_scripts": [
                "list-imports=importscanner.cli:main",
            ],
        },
        python_requires=">=3.7",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        include_package_data=True,
    )
except Exception as e:
    print("❌ Failed to run setup. Reason:", str(e))
    sys.exit(1)
