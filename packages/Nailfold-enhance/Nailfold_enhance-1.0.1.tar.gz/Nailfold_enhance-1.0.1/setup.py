# setup.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='nailfold-image-enhance',
    version='1.0.0',
    author='ZhouBin_FOSU',
    author_email='wuyanxiong@fosu.edu.cn',
    description='Nailfold image and video enhancement SDK',
    long_description=open('README.md', encoding='utf-8').read(),
    license='MIT',


    packages=find_packages(include=['nailfold_image_enhance', 'nailfold_image_enhance.*']),

    # Dependencies required for the package to function
    install_requires=[
        'opencv-python>=4.8.0',  # OpenCV for image/video processing
        'numpy>=1.21.0',  # NumPy for numerical operations
    ],

    # Classifiers for categorizing the package on PyPI
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Multimedia :: Video :: Conversion',
    ],

    # Minimum Python version required
    python_requires='>=3.7',

    # Optional dependencies for development and testing
    extras_require={
        'dev': [
            'pytest>=7.0',  # Testing framework
            'flake8>=6.0',  # Code linter
            'sphinx>=6.2',  # Documentation generator
        ],
    },

    # Include non-code files (e.g., configuration, data files)
    package_data={
        'nailfold_image_enhance': ['data/*.txt'],  # Example: include text files in data/
    },
)