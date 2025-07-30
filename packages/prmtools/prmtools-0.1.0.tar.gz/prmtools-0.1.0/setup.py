from setuptools import setup, find_packages

setup(
    name='prmtools',
    version='0.1.0',
    description='A toolkit for PRM (Parallel Reaction Monitoring) data analysis',
    author='Oluwatosin Daramola',
    author_email='oluwatosindaramola@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'openpyxl',
        # Add any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'prmtools=prmtools.cli:main',
        ],
    },
    python_requires='>=3.7',
)
