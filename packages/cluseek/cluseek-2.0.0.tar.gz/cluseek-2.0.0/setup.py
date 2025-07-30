from setuptools import setup

setup(name="cluseek",
    version="2.0.0",
    description="A GUI application for the discovery and analysis of gene clusters.",
    url="",
    author="OndrejHrebicek",
    author_email="cluseek@biomed.cas.cz",
    license="MIT",
    packages=["cluseek"],
    install_requires=[
        "biopython==1.79",
        "matplotlib",
        "openpyxl==3.0.10",
        "PySide2==5.15.2.1",
        "networkx==3.2.1"],
    entry_points = {
        "console_scripts": ["cluseek=cluseek.__main__:main"]
    },
    zip_safe=False,
    include_package_data=True)
