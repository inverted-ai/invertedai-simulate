#   Product Interface Client

<!-- start elevator-pitch -->
- **Safety Validation**
- **Synthetic Data Generation for Training Autonomous Vehicles** 
- **Real-World Results From Simulation** 
    - Accurate Physics Simulation
    - Photo-Realistic Scenes
    - Accurate Sensor Data
    - Human-Like NPCs

<!-- end elevator-pitch -->



<!-- start quickstart -->
1. Install iai-client in your project environment.

   ```shell
   pip install iai-client
   ```

2. Alternatively, to run the provided examples build the environment with the packages in the 'requirements.txt'.
   ```shell
   pip install -r requirements.txt
   source .venv/bin/activate
   ```
4. Contact us for the server ip address.
3. Run your simulation! 🎉
- For driving run:
  ```shell
   python client_app_driving.py  --zmq_server_address 'x.x.x.x:5555'
  ```
- For data generation run:
   ```shell
   python client_app_trafficlight_data.py --zmq_server_address 'x.x.x.x:5555'
   ```

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
