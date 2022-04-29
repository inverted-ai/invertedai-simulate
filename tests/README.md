


After starting the EC2 instance with ip address: 'x.x.x.x'

$ pip install -r requirements.txt
$ source .venv/bin/activate


run the driving client app with:
$ python client_app_driving.py  --zmq_server_address 'x.x.x.x:5555'

run the client app with:
$ python client_app_trafficlight_data.py --zmq_server_address 'x.x.x.x:5555'

