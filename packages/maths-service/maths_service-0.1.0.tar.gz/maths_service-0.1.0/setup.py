from setuptools import setup, find_packages

setup(
    name='maths-service',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
    ],
    description='A reusable Django maths service',
    author='Lakshmanaselvan V',
    author_email='lakshmanaselvan.v@icanio.com',
    url='https://github.com/lakshmanaselvan/django-maths-service',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
)