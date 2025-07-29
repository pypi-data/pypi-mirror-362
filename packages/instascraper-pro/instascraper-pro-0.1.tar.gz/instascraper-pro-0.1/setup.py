from setuptools import setup, find_packages

setup(
    name='instascraper-pro',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver-manager',
        'easyocr',
        'opencv-python',
        'pandas'
    ]
)
