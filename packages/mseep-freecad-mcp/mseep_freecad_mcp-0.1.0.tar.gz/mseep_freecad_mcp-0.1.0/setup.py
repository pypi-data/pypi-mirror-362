from setuptools import setup, find_packages

setup(
    name='mseep-freecad-mcp',
    version='0.1.0',
    description='FreeCAD integration through the Model Context Protocol',
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
    install_requires=['mcp-server>=1.2.0', 'httpx>=0.24.1'],
    keywords=['mseep'],
)
