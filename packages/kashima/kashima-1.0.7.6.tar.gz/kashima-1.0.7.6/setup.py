from setuptools import setup, find_packages

setup(
    name="kashima",
    version="1.0.7.6",
    author="Alejandro Verri Kozlowski",
    author_email="averri@fi.uba.ar",
    description="Machine Learning Tools for Geotechical Earthquake Engineering.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/averriK/kashima",  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "folium",
        "geopandas",
        "pyproj",
        "requests",
        "branca",
        "geopy",
        "matplotlib",
        "obspy",
        'dataclasses; python_version < "3.7"',
        # 'typing_extensions; python_version < "3.8"',  # Uncomment if needed
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
