from setuptools import setup, find_packages

setup(
    name='async-image-extractor',
    version='0.1.1',
    description='Async Gemini-based image text extractor',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'nest_asyncio',
        'pandas',
        'google-genai',
        'openai',
    ],
    python_requires='>=3.7',
)
