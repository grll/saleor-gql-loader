from distutils.core import setup
setup(
    name='saleor-gql-loader',
    packages=['saleor_gql_loader'],
    version='0.0.4',
    license='MIT',
    description='A simple gql loader class to create some entities in Saleor',
    author='Guillaume Raille',
    author_email='guillaume.raille@gmail.com',
    url='https://github.com/grll/saleor-gql-loader',
    download_url='https://github.com/grll/saleor-gql-loader/archive/0.0.4.tar.gz',
    keywords=['graphql', 'saleor', 'loader'],
    install_requires=['requests', 'Django', 'requests-toolbelt'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
