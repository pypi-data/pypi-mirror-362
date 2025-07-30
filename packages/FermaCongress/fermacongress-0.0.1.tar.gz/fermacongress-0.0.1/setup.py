from setuptools import setup, find_packages

setup(
    name='FermaCongress',
    version='0.0.1',
    author='Ferma Team',
    author_email='hema.murapaka@zoomrx.com',
    description='A short description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.7'
)