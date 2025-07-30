from setuptools import setup
import os


def readme():
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(parent_dir, "README.md")) as f:
        return f.read()


setup(
    name="chart-studio-figlinq",
    version="0.2.9",
    author="figlinq.com",
    author_email="info@figlinq.com",
    maintainer="figlinq.com",
    maintainer_email="info@figlinq.com",
    url="https://github.com/figlinq/chart-studio-figlinq",
    project_urls={
        "Github": "https://github.com/figlinq/chart-studio-figlinq",
    },
    description="Utilities for interfacing with Plotly's Chart Studio and figlinq.com",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    license="MIT",
    packages=[
        "chart_studio",
        "chart_studio.api",
        "chart_studio.api.v2",
        "chart_studio.dashboard_objs",
        "chart_studio.grid_objs",
        "chart_studio.plotly",
        "chart_studio.plotly.chunked_requests",
        "chart_studio.presentation_objs",
        "chart_studio.figlinq",
    ],
    package_data={
        "chart_studio": ["templates/*.json"],  # Include JSON files in the "data" folder
    },
    include_package_data=True,
    install_requires=[
        "plotly>=6.0.1",
        "requests>=2.30.0",
        "retrying>=1.3.3",
        "six",
        "cairosvg",
    ],
    zip_safe=False,
)
