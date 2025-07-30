from setuptools import setup, find_packages

setup(
    name='mseep-basic-memory',
    version='1.0.0',
    description='Local-first knowledge management combining Zettelkasten with knowledge graphs',
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
    install_requires=['sqlalchemy>=2.0.0', 'pyyaml>=6.0.1', 'typer>=0.9.0', 'aiosqlite>=0.20.0', 'greenlet>=3.1.1', 'pydantic[email,timezone]>=2.10.3', 'icecream>=2.1.3', 'mcp>=1.2.0', 'pydantic-settings>=2.6.1', 'loguru>=0.7.3', 'pyright>=1.1.390', 'markdown-it-py>=3.0.0', 'python-frontmatter>=1.1.0', 'rich>=13.9.4', 'unidecode>=1.3.8', 'dateparser>=1.2.0', 'watchfiles>=1.0.4', 'fastapi[standard]>=0.115.8', 'alembic>=1.14.1', 'pillow>=11.1.0', 'pybars3>=0.9.7', 'fastmcp==2.10.2', 'pyjwt>=2.10.1', 'python-dotenv>=1.1.0', 'pytest-aio>=1.9.0'],
    keywords=['mseep'],
)
