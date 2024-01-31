from setuptools import setup

setup(
    name='MenSans',
    version='0.1.0',    
    description='MNE based EEg menta health analysis package',
    url='https://github.com/emmanuel-olateju/MenSans',
    author='Emmanuel Olateju',
    author_email='oltejuemmanuel@gmail.com',
    license='BSD 2-clause',
    packages=['Pipeline','signal_processing','visualization'],
    install_requires=[
        'mne==1.6.0',  
        'matplotlib==3.8.2'                  
        ],
    classifiers=[
    ],
)