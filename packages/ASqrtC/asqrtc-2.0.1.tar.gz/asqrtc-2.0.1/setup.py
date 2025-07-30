from setuptools import setup

setup(
    name='ASqrtC',
    version='2.0.1',
    description=
    ('ASqrtC is a fast and accurate square root calculator with no size limit. '
     'It delivers exact results to any specified number of decimal places. '
     'ASqrtC outperforms Python’s built-in math and decimal modules in both speed and accuracy for large and high-precision calculations.'
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
