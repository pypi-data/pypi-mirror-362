from setuptools import setup, find_packages

setup(
    name='mseep-ailice',
    version='0.4.0',
    description='AIlice is a fully autonomous, general-purpose AI agent. This project aims to create a standalone artificial intelligence assistant, similar to JARVIS, based on the open-source LLM.',
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
    install_requires=[],
    keywords=['mseep'],
)
