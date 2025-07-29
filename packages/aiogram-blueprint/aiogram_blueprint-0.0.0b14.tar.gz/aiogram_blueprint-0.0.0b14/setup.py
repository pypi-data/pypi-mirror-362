from setuptools import setup, find_packages

setup(
    name="aiogram-blueprint",
    version="0.0.0b14",
    packages=find_packages(include=[
        "aiogram_blueprint",
        "aiogram_blueprint.*",
    ]),
    include_package_data=True,
    install_requires=[
        "click~=8.2.1",
        "Jinja2~=3.1.6",
        "InquirerPy~=0.3.4",
    ],
    entry_points={
        "console_scripts": [
            "aiogram-blueprint=aiogram_blueprint.__main__:cli",
        ],
    },
    package_data={
        "aiogram_blueprint": [
            "template/**/*",
            "template/**/.gitkeep",
            "template/.env.j2",
            "template/**/*.j2",
            "template/**/*.py",
            "template/**/*.yaml",
            "template/**/*.ini",
            "template/**/*.txt",
            "template/**/*.mako",
        ],
    },
)
