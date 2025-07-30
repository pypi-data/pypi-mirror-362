from setuptools import setup, find_packages

setup(
    name='mseep-pdf2zh',
    version='1.9.11',
    description='Latex PDF Translator',
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
    install_requires=['requests', 'pymupdf<1.25.3', 'tqdm', 'tenacity', 'numpy', 'ollama', 'xinference-client', 'deepl', 'openai>=1.0.0', 'azure-ai-translation-text<=1.0.1', 'gradio<5.36', 'huggingface_hub', 'onnx', 'onnxruntime', 'opencv-python-headless', 'tencentcloud-sdk-python-tmt', 'pdfminer-six==20250416', 'gradio_pdf>=0.0.21', 'pikepdf', 'peewee>=3.17.8', 'fontTools', 'babeldoc>=0.1.22, <0.3.0', 'rich'],
    keywords=['mseep'],
)
