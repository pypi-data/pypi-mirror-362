from setuptools import setup, find_packages

setup(
    name='mseep-pyserini',
    version='1.2.0',
    description='A Python toolkit for reproducible information retrieval research with sparse and dense representations',
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
    install_requires=['tqdm', 'pyyaml', 'requests', 'Cython>=0.29.21', 'numpy>=1.18.1', 'pandas>=1.4.0', 'pyjnius>=1.6.0', 'scikit-learn>=0.22.1', 'scipy>=1.4.1', 'transformers>=4.6.0', 'torch>=2.4.0', 'onnxruntime>=1.8.1', 'openai>=1.0.0', 'sentencepiece>=0.2', 'tiktoken>=0.4.0', 'flask>3.0', 'pillow>=10.2.0', 'fastapi>=0.70.0', 'uvicorn>=0.13.0', 'mcp>=1.9.4'],
    keywords=['mseep'],
)
