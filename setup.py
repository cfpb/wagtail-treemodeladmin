from setuptools import find_packages, setup

install_requires = [
    "wagtail>=2.7,<2.11",
]

testing_extras = ["coverage>=3.7.0"]

setup(
    name="wagtail-treemodeladmin",
    url="https://github.com/cfpb/wagtail-treemodeladmin",
    author="CFPB",
    author_email="tech@cfpb.gov",
    description="TreeModelAdmin for Wagtail",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="CC0",
    version="1.2.2",
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
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.1",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
