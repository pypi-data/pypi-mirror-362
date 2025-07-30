from setuptools import setup

setup(
    name='ASqrtC',
    version='3.1.1',
    description=
    (
     'ASqrtC is a fast square root calculator with 100% accuracy. '
     'It delivers exact results to any specified number of decimal places. '
     'ASqrtC outperforms Python’s built-in math and decimal modules in speed when calculating less then ~5000 decimal places.'
    ),
    py_modules=["ASqrtC"],
    package_dir={'': 'src'},
    author='Sebastian Trumbore',
    author_email='Trumbore.Sebastian@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/SebastianTrumbore/ASqrtC',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
    keywords=[
        'square root', 'sqrt', 'math', 'numerical methods', 'accurate',
        'precision', 'high precision', 'exact decimal', 'arbitrary precision',
        'fast math', 'root calculator', 'big number math',
        'scientific computing', 'math utilities', 'python3', 'educational',
        'lightweight'
    ],
)
