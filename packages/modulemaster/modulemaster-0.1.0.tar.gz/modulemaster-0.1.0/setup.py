from setuptools import setup, find_packages

setup(
    name='modulemaster', # Renamed package name
    version='0.1.0', 
    py_modules=['modulemaster'], # Renamed module file
    description='A simple Python module to automatically check and install missing dependencies by analyzing import statements.',
    long_description=open('README.txt').read(), # Assumes README.txt is present
    long_description_content_type='text/plain',
    author='Your Name', # Replace with your name
    author_email='your.email@example.com', # Replace with your email
    url='https://github.com/yourusername/modulemaster', # Optional: Link to your project's repository
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', # Or your chosen license
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Installation/Setup',
    ],
    python_requires='>=3.8', # Specify minimum Python version
    install_requires=[
        # modulemaster itself needs setuptools to function (for pkg_resources)
        'setuptools', 
        # ast, subprocess, sys, importlib, os, time are all standard library modules
    ],
)
