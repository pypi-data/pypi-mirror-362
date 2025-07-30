from setuptools import setup

setup(
    name='ordered-set-custom',
    version='0.3',  
    description='A utility to create ordered sets from iterables',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    py_modules=["ordered_utils"],
    package_dir={'': '.'},
    author='Priyanshu Singh',
    author_email='your_email@example.com',
    url='https://github.com/PriyanshuSingh44/ordered-set-custom',
    project_urls={
        'Source': 'https://github.com/PriyanshuSingh44/ordered-set-custom',
        'Tracker': 'https://github.com/PriyanshuSingh44/ordered-set-custom/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
