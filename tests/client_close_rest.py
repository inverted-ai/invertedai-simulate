from iai_common.communications.utils import SensorSettings
import logging
import numpy as np
import argparse
import matplotlib.pyplot as plt
import pygame
import imageio
import inquirer
import cv2

cap = cv2.VideoCapture(0)

logger = logging.getLogger(__name__)
questions = [
    inquirer.List('source',
                message="Which InvertedAI-Simulate?",
                choices=['Cloned Repository', 'Installed Pypi Package'],
            ),
    inquirer.List('remote_host',
                message="Remote Host?",
                choices=["yes", "no"], default="no"
                  ),
    inquirer.Text('server_ip',
                message="Server ip address?",
                  ),
    inquirer.Text('port',
                  message="Server Port", default="5555",
            )
]
answers = inquirer.prompt(questions[:2])
if answers['remote_host'] == 'no':
    server_address='localhost'
    server_port='5555'
else:
    ip_answer = inquirer.prompt(questions[2:])
    server_address = ip_answer['server_ip']
    server_port = ip_answer['port']
    print(f'{server_address}:{server_port}')

if answers['source'] == 'Cloned Repository':
    import sys
    sys.path.append('../invertedai_simulate')
    from utils import Res, SensorSettings, Resolution, PyGameWindow, ClientSideBoundingBoxes
    from interface import IAIEnv, ServerTimeoutError
else:
    from invertedai_simulate.utils import Res, SensorSettings, Resolution, PyGameWindow, ClientSideBoundingBoxes
    from invertedai_simulate.interface import IAIEnv

sensors_dict = {
        'second-front-cam':{
            'sensor_type': 'camera',
            'camera_type': 'rgb-camera',
            'bounding_box': False,
            # 'track_actor_types': 'all', #Actors, # or 'all'
            'track_actor_types': SensorSettings.Available_Tracked_Actors,
            'show_bounding_boxes': False,
            'world_sensor': False,
            'resolution': Res.SD,
            'location': SensorSettings.Location(x=0, z=2.8, y=0),
            'rotation': SensorSettings.Rotation(yaw=0, roll=0, pitch=0),
            'fov': 90.0,
            },
}


fig = plt.figure()
parser = argparse.ArgumentParser()
IAIEnv.add_config(parser)
config = parser.parse_args()
world_parameters = dict(carlatown='Town01', traffic_count=0, pedestrian_count=0)
# world_parameters = dict(carlatown='Town04')
if server_address:
    config.zmq_server_address = f'{server_address}:{server_port}'

env = IAIEnv(config)


action = (0.0, 1.0)
rem_self = 0
how_long = 0

env.render_init(sensors_dict, renderer='pygame', scale=.5)
frames = []
done = False

for l in range(3):
    print(f'Start Env:{l}')
    obs = env.set_scenario('egodriving', world_parameters=world_parameters, sensors=sensors_dict)
    action = (0.0, 1.0)
    for i in range(100):
        obs, reward, done, info = env.step(action)
        action = info['expert_action']
        env.render()
    # env.end_simulation()
