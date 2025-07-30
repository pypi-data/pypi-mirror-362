from setuptools import setup, find_packages

setup(
    name='balestrine-nexus-suite',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['balestrine-dashboard=balestrine_nexus_suite.cli:main']
    },
    install_requires=[
        'fastapi', 'uvicorn[standard]', 'openai', 'boto3', 'google-cloud-storage',
        'azure-identity', 'apscheduler', 'requests'
    ]
)
