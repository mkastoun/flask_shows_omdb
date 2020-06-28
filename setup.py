from setuptools import find_packages, setup

setup(
    name='shows_management',
    version='1.1.2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'PyMysql>=0.9.3',
        'SQLAlchemy>=1.3.18',
        'pandas>=1.0.5',
        'omdb>=0.10.1',
        'mariadb>=1.0.0',
        'reportlab>=3.5.44',
        'Flask-SQLAlchemy>=2.4.3',
        'Flask-DebugToolbar >=0.11.0',
        'xlrd>=1.2.0'
    ],
)