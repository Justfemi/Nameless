import os 

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-ajibadeolufemiscrummy',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description="A scrummy app",
    long_description=README,
    url='https://github.com/justfemi',
    author="Justfemi",
    author_email="justfemi@outlook.com",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 3.0.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
