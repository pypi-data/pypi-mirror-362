from setuptools import setup, find_packages

setup(
    name='myinput',
    version='0.1.0',
    description='A customizable input function that mimics and extends Python’s built-in input()',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Muhammad',
    author_email='sultanmuhammadarslan72@gmail.com',
    url='https://github.com/yourusername/myinput',  # Replace with actual GitHub repo if public
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.6',
)
