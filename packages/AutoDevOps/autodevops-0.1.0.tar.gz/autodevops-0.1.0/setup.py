from setuptools import setup, find_packages

setup(
    name='AutoDevOps',
    version='0.1.0',
    description='CLI tool to automate Git workflow',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'AutoDevOps=auto_devops.cli:git_auto',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
