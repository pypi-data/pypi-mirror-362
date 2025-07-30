from setuptools import setup, find_packages

setup(
    name='mseep-optuna-mcp',
    version='1.0.0',
    description='Optuna MCP Server operates, manages, and visualizes Optuna studies.',
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
    install_requires=['kaleido==0.2.1', 'mcp[cli]>=1.5.0', 'optuna>=4.2.1', 'optuna-dashboard>=0.18.0', 'pandas>=2.2.3', 'plotly>=6.0.1', 'torch>=2.7.0', 'bottle>=0.13.4'],
    keywords=['mseep'],
)
