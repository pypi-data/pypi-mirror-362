from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="nyz-dynamic-design-builder",
    version="2.0.1",
    description="Dynamic Excel export builder for Django ORM querysets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Niyazi Özaydın",
    author_email="niyazi.ozydn@gmail.com",
    url="https://github.com/niyaziozydn/nyz-dynamic-design-builder",
    license="MIT",
    packages=find_packages(exclude=["tests*", "docs*"]),
    install_requires=[
        "django>=5.1.4"
    ],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)