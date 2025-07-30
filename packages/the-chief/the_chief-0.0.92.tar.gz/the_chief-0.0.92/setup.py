from setuptools import setup, find_packages

setup(
    name="the_chief",
    version="0.0.92",
    packages=find_packages(),
    install_requires=[],
    author="Jie Xiong",
    author_email="363692146@qq.com",
    description="",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    package_data={
        'the_chief.member': ['prompt.jinja'],
    },
)
