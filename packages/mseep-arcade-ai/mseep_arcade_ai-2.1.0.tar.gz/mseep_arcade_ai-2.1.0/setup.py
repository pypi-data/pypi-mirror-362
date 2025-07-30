from setuptools import setup, find_packages

setup(
    name='mseep-arcade-ai',
    version='2.1.0',
    description='Arcade.dev - Tool Calling platform for Agents',
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
    install_requires=['arcade-core>=2.0.0,<3.0.0', 'typer==0.10.0', 'rich==13.9.4', 'Jinja2==3.1.6', 'arcadepy==1.5.0', 'tqdm==4.67.1', 'openai==1.82.1', 'click==8.1.8'],
    keywords=['mseep'],
)
