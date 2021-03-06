"""Contains all the configuration for the package on pip"""
import setuptools

def get_content(*filename:str) -> str:
    """ Gets the content of a file or files and returns
    it/them as a string
    Parameters
    ----------
    filename : (str)
        Name of file or set of files to pull content from 
        (comma delimited)
    
    Returns
    -------
    str:
        Content from the file or files
    """
    content = ""
    for file in filename:
        with open(file, "r") as full_description:
            content += full_description.read()
    return content

setuptools.setup(
    name = "ezshortcut",
    version = "0.1.0",
    author = "Kieran Wood",
    author_email = "kieran@canadiancoding.ca",
    description = "Generate shortcuts to executables and/or folders",
    long_description = get_content("README.md", "CHANGELOG.md"),
    long_description_content_type = "text/markdown",
    project_urls = {
        "API Docs"  :      "https://kieranwood.ca/ez-shortcut",
        "Source" :         "https://github.com/Descent098/ez-shortcut",
        "Bug Report":      "https://github.com/Descent098/ez-shortcut/issues/new?assignees=Descent098&labels=bug&template=bug_report.md&title=%5BBUG%5D",
        "Feature Request": "https://github.com/Descent098/ez-shortcut/issues/new?labels=enhancement&template=feature_request.md&title=%5BFeature%5D",
        "Roadmap":         "https://github.com/Descent098/ez-shortcut/projects"
    },
    include_package_data = True,
    py_modules = ["ezshortcut"],
    install_requires = [
    "pywin32", 
    "winshell", 
        ],
    extras_require = {
        "dev" : ["pytest",  # Used to run the test code in the tests directory
                ],
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Beta"
    ],
)