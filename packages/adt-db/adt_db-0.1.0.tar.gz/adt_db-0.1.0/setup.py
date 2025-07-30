from setuptools import find_packages, setup
import tomllib

with open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="adt_db",
    version="0.1.0",
    description="Agent de Tourisme database manipulation library.",
    package_dir={"": "modules"},
    packages=find_packages(where="modules"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/agent-de-tourisme/adt-juil-db",
    author="Maxime Blanchard, Khadim Fall, Wissem Mejri",
    license="GPL-3",
    install_requires=pyproject["project"]["dependencies"],
    python_requires=pyproject["project"]["requires-python"]
)