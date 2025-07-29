from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="talk2db",
    version="0.1.0",
    author="Akash Gunasekar",
    author_email="akashpersonal18@gmail.com",
    description="Natural Language Query Interface for CQL and SQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Akash-Gunasekar/talk2db",
    packages=find_packages(),
    keywords="natural language processing, sql, cypher, database, query, nlp",
    entry_points={
        "console_scripts": [
            "talk2db=talk2db.cli:main",
        ]
    },
)
