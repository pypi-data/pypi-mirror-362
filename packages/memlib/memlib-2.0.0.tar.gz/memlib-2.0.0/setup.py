# setup.py
from setuptools import setup
from setuptools.command.install import install
import sys

class CustomInstallCommand(install):
    def run(self):
        try:
            from memlib import show_popup
            show_popup()
        except Exception as e:
            print("失敗:", e)
        install.run(self)

setup(
    name='memlib',
    version='2.0.0',
    description='python module',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='memlib',
    author_email='gymk@gaypan.jp',
    url='https://github.com/memlib/',
    packages=['memlib'],
    cmdclass={
        'install': CustomInstallCommand,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
