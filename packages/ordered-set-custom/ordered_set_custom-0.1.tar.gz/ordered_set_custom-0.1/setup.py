from setuptools import setup

setup(
    name='ordered-set-custom',
    version='0.1',
    description='A utility to create ordered sets from iterables',
    py_modules=["ordered_utils"],
    package_dir={'': '.'},
    author='Priyanshu Singh',
    author_email='priyanshu3303@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
