from setuptools import setup, find_packages

requirements = []
with open("requirements.txt", "r") as fh:
    for line in fh:
        requirements.append(line.strip())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ironflock",
    version="1.0.4",
    description="SDK to integrate your IronFlock Industry 4 Apps with the IronFlock Data Infrastructure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RecordEvolution/ironflock-py",
    author="Record Evolution GmbH",
    author_email="marko.petzold@record-evolution.de",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.8",
    install_requires=requirements,
    classifiers=[],
)
