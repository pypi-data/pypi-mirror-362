from setuptools import setup, find_packages

setup(
    name='mseep-file-converter-mcp',
    version='0.1.0',
    description='A MCP server that provides file conversion tools',
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
    install_requires=['mcp[cli]', 'docx2pdf', 'pdf2docx', 'pillow', 'pandas', 'pdfkit', 'markdown'],
    keywords=['mseep'],
)
