import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()


entry_points = {
    'console_scripts': ['tomograph = tomograph.cli:main']
}


setuptools.setup(
    name='tomograph',
    version='0.1',
    author='Filip Kokosinski',
    author_email='filip.kokosinski@gmail.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    description='Parametrized computer tomography simulator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fkokosinski/tomograph',
    install_requires=['click', 'tqdm', 'scikit-image', 'numpy==1.15.*'],
    entry_points=entry_points,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry'
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Development Status :: Alpha',
        'Programming Language :: Python',
        'Programming Language :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
