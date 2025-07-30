from setuptools import setup, find_packages

setup(
    name='autodevops-cli',
    version='5.0',
    description='AutoDevOps CLI: Automate Git push and simulate CI/CD',
    author='Kannan',
    author_email='kannan@example.com',
    packages=find_packages(),
    install_requires=[
        'click',
        'rich',
        'sh',
        'loguru',
        'python-dotenv',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'autodevops=autodevops_cli.cli:autodevops',
        ],
    },

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
