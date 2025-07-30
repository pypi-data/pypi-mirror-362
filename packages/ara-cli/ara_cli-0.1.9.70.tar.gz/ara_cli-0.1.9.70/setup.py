from setuptools import setup, find_packages

# Import version number
version = {}
with open("./ara_cli/version.py") as fp:
    exec(fp.read(), version)

with open("./docker/base/requirements.txt", "r") as pip_reqs_file:
    reqs = [line.strip() for line in pip_reqs_file.readlines()]

setup(
    name="ara_cli",
    version=version['__version__'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ara = ara_cli.__main__:cli",
        ],
    },
    install_requires=reqs,
)
