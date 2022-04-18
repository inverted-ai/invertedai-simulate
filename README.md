#   Product Interface Client
### Building
`python -m build`

### Publishing

Refer to [here](https://packaging.python.org/en/latest/specifications/pypirc/) for setting up your local package indexes
e.g. to publish to testpypi
`python -m twine upload --repository testpypi dist/*`

### Autodoc  
Run `make html` inside `docs/` dir will auto generate the html documentation from the current source files.  
Run `sphinx-apidoc -f -o source/ ../src/iai_client` inside `docs/` dir to regenerate the rst files in `source/`.  
More info regarding autodoc can be found [here](https://docs-python2readthedocs.readthedocs.io/en/master/code-doc.html#)