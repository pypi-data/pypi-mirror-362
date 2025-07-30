from setuptools import setup, find_packages

setup(
    name='instascraper-pro',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver-manager',
        'easyocr',
        'opencv-python',
        'pandas'
    ],
    entry_points={
        "console_scripts": [
            "instascraper-setup = instascraper.setup_env:main",
        ],
    },
    include_package_data=True,
)
