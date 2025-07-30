from setuptools import setup, find_packages

setup(
    name='mseep-fast-agent-mcp',
    version='0.2.43',
    description='Define, Prompt and Test MCP enabled Agents and Workflows',
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
    install_requires=['fastapi>=0.115.6', 'mcp==1.10.1', 'opentelemetry-distro>=0.50b0', 'opentelemetry-exporter-otlp-proto-http>=1.29.0', 'pydantic-settings>=2.7.0', 'pydantic>=2.10.4', 'pyyaml>=6.0.2', 'rich>=13.9.4', 'typer>=0.15.1', 'anthropic>=0.55.0', 'openai>=1.93.0', 'azure-identity>=1.14.0', 'boto3>=1.35.0', 'prompt-toolkit>=3.0.50', 'aiohttp>=3.11.13', "opentelemetry-instrumentation-openai>=0.40.14; python_version >= '3.10' and python_version < '4.0'", "opentelemetry-instrumentation-anthropic>=0.40.14; python_version >= '3.10' and python_version < '4.0'", "opentelemetry-instrumentation-mcp>=0.40.14; python_version >= '3.10' and python_version < '4.0'", 'google-genai', 'opentelemetry-instrumentation-google-genai>=0.2b0', 'tensorzero>=2025.6.3', 'deprecated>=1.2.18', 'a2a-sdk>=0.2.9', 'email-validator>=2.2.0'],
    keywords=['mseep'],
)
