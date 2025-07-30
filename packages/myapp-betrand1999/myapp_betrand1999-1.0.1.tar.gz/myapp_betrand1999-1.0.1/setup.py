from setuptools import setup, find_packages

setup(
    name='myapp-betrand1999',
    version='1.0.1', # each new release need update version
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'myapp=myapp.app:main',  # assumes main() exists in app.py
        ],
    },
)
