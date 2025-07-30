import setuptools

with open("README.md", "r") as f:
    description = f.read()

setuptools.setup(
    name="AppCategorizer",
    version="1.0.0",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "beautifulsoup4",
        "pandas",
        "requests",
        "selenium",
        "transformers"
    ],
    entry_points={
        "console_scripts": [
            "AppCategorizer=AppCategorizer.main:main",
        ],
    },
    author= "Zain Ramzan",
    description="Application categorization tool using rule-based and AI methods",
    long_description=description,
    long_description_content_type="text/markdown"
)