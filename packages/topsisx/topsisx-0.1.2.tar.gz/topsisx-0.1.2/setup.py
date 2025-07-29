from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="topsisx",
    version="0.1.2",
    author="Your Name",
    author_email="your_email@example.com",
    description="A Python library for Multi-Criteria Decision Making (TOPSIS, AHP, VIKOR, etc.)",
    long_description=long_description,  # ✅ This adds the README
    long_description_content_type="text/markdown",  # ✅ For Markdown rendering
    url="https://github.com/<your-username>/topsisx",  # 🔗 Update your GitHub URL
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "fpdf",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "topsisx=topsisx.cli:main",  # Update if you have CLI
        ],
    },
)
