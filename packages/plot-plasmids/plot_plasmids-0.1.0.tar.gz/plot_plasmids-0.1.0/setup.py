from setuptools import setup, find_packages

setup(
    name="plot-plasmids",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'plot_plasmids = plot_plasmids.main:main',
        ],
    },
    install_requires=[
        "pandas",
        "numpy",
        "scikit-bio",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "adjusttext",
    ],
    author="Jules",
    author_email="jules@example.com",
    description="A tool to generate PCoA or NMDS plots for plasmids.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/example/plot_plasmids",
)
