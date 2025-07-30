from setuptools import setup, find_packages

setup(
    name='mseep-agentops',
    version='0.4.18',
    description='Observability and DevTool Platform for AI Agents',
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
    install_requires=['requests>=2.0.0,<3.0.0', 'psutil>=5.9.8,<7.0.1', 'termcolor>=2.3.0,<2.5.0', 'PyYAML>=5.3,<7.0', 'packaging>=21.0,<25.0', 'httpx>=0.24.0,<0.29.0', "opentelemetry-sdk==1.29.0; python_version<'3.10'", "opentelemetry-sdk>1.29.0; python_version>='3.10'", "opentelemetry-api==1.29.0; python_version<'3.10'", "opentelemetry-api>1.29.0; python_version>='3.10'", "opentelemetry-exporter-otlp-proto-http==1.29.0; python_version<'3.10'", "opentelemetry-exporter-otlp-proto-http>1.29.0; python_version>='3.10'", 'ordered-set>=4.0.0,<5.0.0', 'wrapt>=1.0.0,<2.0.0', "opentelemetry-instrumentation==0.50b0; python_version<'3.10'", "opentelemetry-instrumentation>=0.50b0; python_version>='3.10'", "opentelemetry-semantic-conventions==0.50b0; python_version<'3.10'", "opentelemetry-semantic-conventions>=0.50b0; python_version>='3.10'"],
    keywords=['mseep'],
)
