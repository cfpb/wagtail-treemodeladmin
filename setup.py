from setuptools import find_packages, setup


with open("README.md") as f:
    long_description = f.read()


install_requires = [
    "wagtail>=2.3,<2.11",
]


testing_extras = [
    "mock>=2.0.0",
    "coverage>=3.7.0",
]


setup(
    name="wagtail-treemodeladmin",
    url="https://github.com/cfpb/wagtail-treemodeladmin",
    author="CFPB",
    author_email="tech@cfpb.gov",
    description="TreeModelAdmin for Wagtail",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="CC0",
    version="1.2.1",
    include_package_data=True,
    packages=find_packages(),
    package_data={
        "treemodeladmin": [
            "templates/treemodeladmin/*",
            "templates/treemodeladmin/includes/*",
            "static/treemodeladmin/css/*",
        ]
    },
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={"testing": testing_extras},
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.2",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
