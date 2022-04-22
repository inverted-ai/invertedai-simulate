# Quickstart
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

<!-- ```{include} ../README.md -->
<!-- :start-after: <\!-- start quickstart -\-> -->
<!-- :end-before: <\!-- end quickstart -\-> -->
<!-- ``` -->
