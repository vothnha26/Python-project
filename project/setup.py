from setuptools import setup, find_packages

setup(
    name='my_python_project',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'setuptools',
        'pandas',
        'numpy',
        'requests',
        'matplotlib',
        'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            'my_project=src.main:main',
        ],
    }
)
