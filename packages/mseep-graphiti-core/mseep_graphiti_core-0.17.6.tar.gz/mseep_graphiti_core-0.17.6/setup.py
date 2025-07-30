from setuptools import setup, find_packages

setup(
    name='mseep-graphiti-core',
    version='0.17.6',
    description='A temporal graph building library',
    long_description="Package managed by MseeP.ai",
    long_description_content_type="text/plain",
    author='mseep',
    author_email='support@skydeck.ai',
    maintainer='mseep',
    maintainer_email='support@skydeck.ai',
    url='https://github.com/mseep',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['pydantic>=2.11.5', 'neo4j>=5.26.0', 'diskcache>=5.6.3', 'openai>=1.91.0', 'tenacity>=9.0.0', 'numpy>=1.0.0', 'python-dotenv>=1.0.1', 'posthog>=3.0.0'],
    keywords=['mseep'],
)
