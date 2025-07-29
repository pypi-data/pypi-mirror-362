from setuptools import setup, find_packages
from irlpdf import __app_name__,__version__
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()
 
setup(
    name = __app_name__,
    version = __version__,
    author = 'Gauraang Ratnaparik',
    author_email = 'john.doe@foo.com',
    license = 'MIT',
    description = 'CLI tool for pdf related tasks',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/dusa-sai-krishna/irlpdf",
    py_modules = ['my_tool', 'irlpdf'],
    packages = find_packages(),
    install_requires = requirements,
    python_requires='>=3.9',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        irlpdf=my_tool:start
    '''
)