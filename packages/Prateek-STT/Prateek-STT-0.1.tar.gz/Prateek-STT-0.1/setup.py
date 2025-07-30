from setuptools import setup,find_packages

setup(
    name='Prateek-STT',
    version='0.1',
    author='Prateek Shakya',
    author_email='prateekshakya251@gmail.com',
    description='This is Speech To Text created by Mr.PRATEEK'
)
packages=find_packages(),
install_requirements=[
    'selenium',
    'webdriver_manager',
]
