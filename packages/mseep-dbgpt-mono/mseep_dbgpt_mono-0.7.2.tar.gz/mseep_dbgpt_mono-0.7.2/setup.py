from setuptools import setup, find_packages

setup(
    name='mseep-dbgpt-mono',
    version='0.7.2',
    description='DB-GPT is an experimental open-source project that uses localized GPT large models to interact with your data and environment. With this solution, you can beassured that there is no risk of data le...',
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
