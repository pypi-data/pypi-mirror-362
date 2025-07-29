import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pluginspy",
    version="0.2.19",
    author="zengjf",
    author_email="zengjf42@163.com",
    description="Plugins Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FolderLevel/PluginsPy",
    project_urls={
        "Bug Tracker": "https://github.com/FolderLevel/PluginsPy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
    include_package_data=True,
    install_requires=[
        "windows-curses;platform_system=='Windows'",
        "PyQt5",
        "VisualLog>=0.0.16",
    ],
    entry_points={"console_scripts": ["pluginspy=PluginsPy:main"]},
)
