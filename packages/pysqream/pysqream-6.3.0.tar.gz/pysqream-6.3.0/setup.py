from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup_params = dict(
    name='pysqream',
    setup_requires=["setuptools-scm"],
    use_scm_version={
        "version_scheme": "only-version",
        "local_scheme": "no-local-version",
    },
    description='DB-API connector for SQream DB',
    long_description=long_description,
    url="https://github.com/SQream/pysqream",
    author="SQream",
    author_email="info@sqream.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    keywords='database db-api sqream sqreamdb',
    python_requires='>=3.9,<=3.13.1',
    install_requires=["numpy<=2.3.0", "packaging<=25.0", "pyarrow<=20.0.0",
                      "pandas<=2.3.0", "Faker<=37.3.0", "numexpr<=2.10.2", "setuptools-scm==8.3.1"]
)

if __name__ == '__main__':
    setup(**setup_params)
