from setuptools import setup, find_packages

setup(
    name             = 'pygifgenerator_testver',
    version          = '1.0.0',
    description      = 'Test package for distribution',
    author           = 'Monstro',
    author_email     = '',
    url              = '',
    download_url     = '',
    install_requires = ['pillow'],
	include_package_data=True,
	packages=find_packages(),
    keywords         = ['GIFGENERATOR', 'gifgenerator'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
) 