from setuptools import setup
from setuptools import find_packages


setup(
    name = 'pywheels',
    version = '0.1.6',
    packages = find_packages(),
    description = 'debug',
    author = 'parkcai',
    author_email = 'sun_retailer@163.com',
    url = 'https://github.com/parkcai/pywheels',
    include_package_data=True,  # 必须
    package_data={
        'pywheels': ['locales/**/LC_MESSAGES/*.mo'],  # 指定相对路径，确保包含.mo
    },
)