from setuptools import find_packages, setup

package_name = "square_database_structure"

setup(
    name=package_name,
    version="2.5.9",
    packages=find_packages(),
    package_data={
        package_name: ["**/**/stored_procedures_and_functions/*.sql"],
    },
    install_requires=[
        "sqlalchemy>=2.0.23",
        "psycopg2-binary>=2.9.9",
        "pytest>=8.0.0",
    ],
    author="thePmSquare",
    author_email="thepmsquare@gmail.com",
    description="database layer for my personal server.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url=f"https://github.com/thepmsquare/{package_name}",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
