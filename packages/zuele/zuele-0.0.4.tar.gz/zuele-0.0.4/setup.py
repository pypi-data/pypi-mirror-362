from setuptools import setup, find_packages

setup(
    name='zuele',
    version='0.0.4',
    author='ikun',
    author_email='2206490823@qq.com',
    description='Jieba in economy',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={'zuele': ['data/*.txt']},
    include_package_data=True,
    python_requires='>=3.8',
)