from setuptools import setup

setup(
    name = 'ASqrtC', 
    version = '1.0.0',
    description = 'ASC was made to be a fast and accurate way of calculating square root. It is 100% accurate and has no size limit.', 
    py_modules = ["ASqrtC"],
    package_dir = {'':'src'},
   # packages = [''],
    author = 'Sebastian Trumbore',
    author_email = 'Trumbore.Sebastian@gmail.com',
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
    url='https://github.com/SebastianTrumbore/ASqrtC',
    include_package_data=True,
    classifiers  = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: BSD License",
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Text Processing',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
    ],
    install_requires = [
        'pandas ~= 1.2.4'
    ],
    keywords = ['Square Root', 'Data Science', 'Exact', 'Sqrt', 'Accurate'],
    
)
