import setuptools

PACKAGE_NAME = 'variable-local'
package_dir = PACKAGE_NAME.replace('-', '_')

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.116',  # https://pypi.org/project/variable-local
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles variable Local/Remote Python",
    long_description="PyPI Package for Circles variable Local/Remote Python",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'logger-local>=0.0.135',
        'language-remote>=0.0.20',
        'database-mysql-local>=0.0.290',
        'smartlink-local>=0.0.34',
        'smartlink-remote-restapi',
        'fields-local>=0.0.9'
    ],
)
