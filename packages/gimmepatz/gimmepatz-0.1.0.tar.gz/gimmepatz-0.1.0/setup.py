from setuptools import setup, find_packages

setup(
    name='gimmepatz',
    version='0.1.0',
    author='6mile',
    author_email='6mile@linux.com',
    description=' GitHub Personal Access Token (PAT) recon tool',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
