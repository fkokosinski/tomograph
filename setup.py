import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
        name='tomograph',
        version='0.1',
        author='Filip Kokosinski',
        author_email='filip.kokosinski@gmail.com',
        description='Parametrized cone tomograph simulator',
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=setuptools.find_packages()
)
