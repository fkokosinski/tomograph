import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

entry_points = {
        'console_scripts': ['tomograph = tomograph.scripts.cli:main']
}

setuptools.setup(
        name='tomograph',
        version='0.1',
        author='Filip Kokosinski',
        author_email='filip.kokosinski@gmail.com',
        packages=setuptools.find_packages(),
        include_package_data=True,
        description='Parametrized computer tomography simulator',
        install_requires=['click', 'tqdm', 'scikit-image', 'numpy==1.15.*'],
        long_description=long_description,
        long_description_content_type='text/markdown',
        entry_points=entry_points
)
