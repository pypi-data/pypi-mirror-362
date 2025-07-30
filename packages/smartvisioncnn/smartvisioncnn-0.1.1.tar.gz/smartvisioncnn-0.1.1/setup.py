from setuptools import setup, find_packages

setup(
    name='smartvisioncnn',
    version='0.1.1',
    description='A simple CNN wrapper with training, evaluation, and plotting utilities',
    author='Yotcheb kandolo jean',
    author_email='kandoloyotchebjean@gemail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0',
        'numpy',
        'matplotlib',
        'scikit-learn'

    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
