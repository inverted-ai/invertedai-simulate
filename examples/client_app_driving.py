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
                choices=['Cloned Repository', 'Latest Published Pypi Package'],
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
        # 'top-cam': {
        #     'sensor_type': 'camera',
        #     'camera_type': 'rgb-camera',
        #     'bounding_box': True,
        #     'track_actor_types': Sensor_Settings.Available_Tracked_Actors,
        #     'show_bounding_boxes': True,
        #     'world_sensor': True,
        #     'resolution': Res.MD,
        #     'location': Sensor_Settings.Location(x=0.0, z=80.0, y=0.0),
        #     'rotation': Sensor_Settings.Rotation(yaw=90.0, pitch=-90.0, roll=0.0),
        #     'fov': 90,
        #     'radius': 200,
        #     },
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
        # 'boundingbox_ego': {
        #     'sensor_type': 'boundingbox',
        #     'track_actor_types': SensorSettings.Available_Tracked_Actors,  # or 'all'
        #     'world_sensor': False, # if True returns the coordinates in the global frame of reference
        #     'attach_to_actor': 'ego',
        #     'radius': 20,
        #     },
        'boundingbox_cam': {
            'sensor_type': 'boundingbox',
            'track_actor_types': SensorSettings.Available_Tracked_Actors,  # or 'all'
            'world_sensor': False, # if True returns the coordinates in the global frame of reference
            'attach_to_actor': 'second-front-cam',
            'occlusion': True,
            },
        'side-cam':{
            'sensor_type': 'camera',
            'camera_type': 'rgb-camera',
            'bounding_box': False,
            # 'track_actor_types': 'all', #Actors, # or 'all'
            'track_actor_types': SensorSettings.Available_Tracked_Actors,
            'show_bounding_boxes': False,
            'world_sensor': False,
            'resolution': Res.SD,
            'location': SensorSettings.Location(x=0, z=2.8, y=0),
            'rotation': SensorSettings.Rotation(yaw=90, roll=0, pitch=0),
            'fov': 90.0,
            },
        # 'boundingbox_side_cam': {
        #     'sensor_type': 'boundingbox',
        #     'track_actor_types': SensorSettings.Available_Tracked_Actors,  # or 'all'
        #     'world_sensor': False, # if True returns the coordinates in the global frame of reference
        #     'attach_to_actor': 'side-cam',
        #     'radius': 20,
        #     'occlusion': True,
        #     },
        # 'back-cam':{
        #     'sensor_type': 'camera',
        #     'camera_type': 'rgb-camera',
        #     'bounding_box': False,
        #     # 'track_actor_types': 'all', #Actors, # or 'all'
        #     'track_actor_types': SensorSettings.Available_Tracked_Actors,
        #     'show_bounding_boxes': False,
        #     'world_sensor': False,
        #     'resolution': Res.SD,
        #     'location': SensorSettings.Location(x=0, z=2.8, y=0),
        #     'rotation': SensorSettings.Rotation(yaw=180, roll=0, pitch=0),
        #     'fov': 90.0,
        #     },
        # 'boundingbox_back_cam': {
        #     'sensor_type': 'boundingbox',
        #     'track_actor_types': SensorSettings.Available_Tracked_Actors,  # or 'all'
        #     'world_sensor': False, # if True returns the coordinates in the global frame of reference
        #     'attach_to_actor': 'back-cam',
        #     'radius': 20,
        #     'occlusion': True,
        #     },
}


fig = plt.figure()
parser = argparse.ArgumentParser()
IAIEnv.add_config(parser)
config = parser.parse_args()
world_parameters = dict(carlatown='Town01')
# world_parameters = dict(carlatown='Town04')
if server_address:
    config.zmq_server_address = f'{server_address}:{server_port}'

env = IAIEnv(config)
obs = env.set_scenario('egodriving', world_parameters=world_parameters, sensors=sensors_dict)


action = (0.0, 1.0)
_, reward, done, info = env.step(action)
rem_self = 0
how_long = 0

env.render_init(sensors_dict, renderer='pygame', scale=.5)
# env.render_init(sensors_dict, renderer='cv', scale=.5)
frames = []
done = False
while not done:
    # env.get_map()
    # valid_actions = env.get_actions()
##
    prev_action = obs['prev_action']
    print(f'Previous Actions: {prev_action}')
    if rem_self < how_long:
        action = info['expert_action']
        obs, reward, done, info = env.step(action)
        rem_self += 1
    else:
        cmd = input('Enter a Command or the Steering angle:')
        if cmd == 'reset':
            obs = env.reset()
        elif cmd == 'self':
            how_long = int(input('How many steps:'))
            rem_self = 0
        elif cmd == 'server':
            # Server Driving
            message = env.get_actions()
            print(message)
        elif cmd == 'init':
            obs = env.set_scenario('egodriving', world_parameters=world_parameters, sensors=sensors_dict)
        elif cmd == 'end':
            print(env.end_simulation())
            env.close()
            break
        else:
            angle = float(cmd)
            acceleration = float(input('Enter Acceleration:'))
            action = (acceleration, angle)
        # action = int(input('Enter Action:'))
            obs, reward, done, info = env.step(action)

    for name in sensors_dict:
        if (sensors_dict[name]['sensor_type'] == 'boundingbox'):
            if (sensors_dict[name]['attach_to_actor'] != 'ego'):
                attached_sensor = sensors_dict[name]['attach_to_actor']
                bb2d = ClientSideBoundingBoxes.get_2d_bbox(obs['sensor_data'][name]['bounding_boxes'], sensors_dict[attached_sensor]['location'], sensors_dict[attached_sensor]['rotation'], sensors_dict[attached_sensor]['fov'], sensors_dict[attached_sensor]['resolution'], obs['compact_vector'][:3], obs['compact_vector'][3:6], coordinate_system='attached_sensor', occlusion=True)
                img = obs['sensor_data'][attached_sensor]['image']
                obs['sensor_data'][attached_sensor]['image'] = ClientSideBoundingBoxes.draw_bounding_boxes_on_array(img, bb2d, draw2d=True, occlusion=True)


    frames.append(env.render())


print(f'Episode Done, Reward:{reward}')
# file_name= 'script_sensor_video.mp4'
# imageio.mimwrite(file_name, frames, fps=15, quality=7)
