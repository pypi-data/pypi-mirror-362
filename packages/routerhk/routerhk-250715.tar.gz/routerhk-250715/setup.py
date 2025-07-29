from setuptools import setup, find_packages

setup(
    name='routerhk',
    version='250715',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='API client for router.hk API requests.',
    author='Sammy Fung',
    author_email='sammy@sammy.hk',
    url='https://github.com/routerhk/routerhk',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
