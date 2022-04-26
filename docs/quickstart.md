# Quickstart
```{include} ../README.md
:start-after: <!-- start quickstart --> 
:end-before: <!-- end quickstart -->
```

1. Install iai-client in your project environment.

   ```shell
   pip install iai-client
   ```

2. Alternatively, to run the provided examples build the environment with the packages in the 'requirements.txt'.
   ```shell
   pip install -r requirements.txt
   source .venv/bin/activate
   ```
3. Contact us for the server ip address.
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
