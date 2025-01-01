from setuptools import setup, find_packages

setup(
    name="harlanbot",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'nltk',
        # 'numpy',
        'tensorflow',
        # 'tflearn @ git+https://github.com/harlansr/tflearn.git@master',
        'pillow==9.5.0'
    ],
    author="HarlanSR",
    description="Create your own custom chatbot",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    package_data={
        'harlanbot': [
            'intents.json'
        ],
    },
    include_package_data=True,
    url="https://github.com/harlansr/harlanbot",
)