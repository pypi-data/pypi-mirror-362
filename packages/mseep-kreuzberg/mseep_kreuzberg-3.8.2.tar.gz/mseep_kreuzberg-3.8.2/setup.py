from setuptools import setup, find_packages

setup(
    name='mseep-kreuzberg',
    version='3.8.2',
    description='Document intelligence framework for Python - Extract text, metadata, and structured data from diverse file formats',
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
    install_requires=['anyio>=4.9.0', 'chardetng-py>=0.3.4', "exceptiongroup>=1.2.2; python_version<'3.11'", 'html-to-markdown[lxml]>=1.8.0', 'mcp>=1.11.0', 'msgspec>=0.18.0', 'playa-pdf>=0.6.1', 'psutil>=7.0.0', 'pypdfium2==4.30.0', 'python-calamine>=0.3.2', 'python-pptx>=1.0.2', "typing-extensions>=4.14.0; python_version<'3.12'"],
    keywords=['mseep', 'async', 'document-analysis', 'document-intelligence', 'document-processing', 'extensible', 'information-extraction', 'mcp', 'metadata-extraction', 'model-context-protocol', 'ocr', 'pandoc', 'pdf-extraction', 'pdfium', 'plugin-architecture', 'rag', 'retrieval-augmented-generation', 'structured-data', 'table-extraction', 'tesseract', 'text-extraction'],
)
