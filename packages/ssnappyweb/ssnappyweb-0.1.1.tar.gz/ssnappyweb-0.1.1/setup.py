from setuptools import setup, find_packages

setup(
    name='ssnappyweb',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'cryptography',
    ],
    entry_points={
        'console_scripts': [
            'ssnappyweb = ssnappyweb.main:main',
        ],
    },
)
