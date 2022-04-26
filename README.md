#   Product Interface Client

<!-- start elevator-pitch -->
- **Safety Validation**
- **Synthetic Data Generation** 
- **Training and Testing**
- **Real-World Results From Simulation** 
<!-- end elevator-pitch -->



<!-- start quickstart -->

1. Contact us for the server ip address.
2. Install iai-client in your project environment.

   ```shell
   pip install iai-client
   ```

2. Alternatively, to run the provided examples build the environment with the packages in the 'requirements.txt'.
   ```shell
   pip install -r requirements.txt
   source .venv/bin/activate
   ```
4. Run your simulation! 🎉
- For driving run:
  ```shell
   python client_app_driving.py  --zmq_server_address 'x.x.x.x:5555'
  ```
- For data generation run:
   ```shell
   python client_app_trafficlight_data.py --zmq_server_address 'x.x.x.x:5555'
   ```
5. Jupyter-notebooks are also provided in Google Colab:

- For driving run:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inverted-ai/iai-client/blob/main/examples/demo-driving.ipynb)

- For data generation run:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inverted-ai/iai-client/blob/main/examples/demo-datageneration.ipynb)

- For data generation as a pytorch dataloader run:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inverted-ai/iai-client/blob/main/examples/demo-dataloader.ipynb)
<!-- end quickstart -->

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
