from setuptools import setup, find_packages

setup(
    name="eduautoml",
    version="0.1",
    packages=find_packages(),  # auto-discovers eduautoml/
    install_requires=[
        "pandas",
        "scikit-learn",
        "matplotlib",
        "typer",
        "gradio"
    ],
    entry_points={
        "console_scripts": [
            "eduautoml=CLI.cli:run"
        ]
    },
)
