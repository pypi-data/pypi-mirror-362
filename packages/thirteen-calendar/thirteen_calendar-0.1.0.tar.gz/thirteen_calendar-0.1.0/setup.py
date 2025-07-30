from setuptools import setup, find_packages

setup(
    name='thirteen_calendar',
    version='0.1.0',
    author='Gemini',
    description='A custom calendar and clock system with 13 months, 26 hours, and astronomical calculations.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
