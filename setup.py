from setuptools import setup, find_packages

setup(
    name = "virtaddress",
    version = "0.1.1",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'virt-address = virtaddress.cli:main',
        ]
    },
)
