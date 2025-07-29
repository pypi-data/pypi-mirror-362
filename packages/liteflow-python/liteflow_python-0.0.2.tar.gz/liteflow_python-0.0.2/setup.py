import setuptools
from pathlib import Path

# Load long description from README.md
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8")

# Load requirements from ../app/functions/requirements.txt
requirements_path = Path(__file__).parent / "requirements.txt"
install_requires = requirements_path.read_text(encoding="utf-8").splitlines()

# Filter out empty lines and comments
install_requires = [
    line.strip() for line in install_requires
    if line.strip() and not line.strip().startswith("#")
]

setuptools.setup(
    name="liteflow-python",
    version="0.0.2",
    author="53gf4u1t",
    author_email="nguyenhoanglienson1105@gmail.com",
    description="Build production-grade LLM apps the easy way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/53gf4u1t/liteflow-python",
    # project_urls={
    #     "Bug Tracker": "https://github.com/yourusername/LiteFlow/issues",
    # },
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires='>=3.9',
    install_requires=install_requires,
)
