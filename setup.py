import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt') as file:
    required = file.read().splitlines()

setuptools.setup(
    name='psi-cli',
    version='0.0.3',
    author='juju',
    author_email='gliheng@live.com',
    description='flutter-rs devtool',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=required,
    url='https://github.com/flutter-rs/psi-cli',
    packages=setuptools.find_packages(),
    entry_points ={ 
        'console_scripts': [ 
          'psi = psi.psi:main'
        ] 
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
)