from setuptools import setup, find_packages

setup(
    name='mseep-omcp',
    version='0.1.0',
    description='Model Context Protocol Server for the Observational Medical Outcomes Partnership (OMOP) Common Data Model',
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
    install_requires=['ibis-framework>=10.5.0', 'mcp[cli]>=1.6.0'],
    keywords=['mseep', 'claude', 'ibis', 'llm', 'mcp server', 'ohdsi', 'omop', 'python'],
)
