from iai_common.communications.utils import SensorSettings
import numpy as np
import argparse
import matplotlib.pyplot as plt
import imageio
import pygame
import logging
import inquirer
logger = logging.getLogger(__name__)
questions = [
    inquirer.List('source',
                message="Which InvertedAI-Simulate?",
                choices=['Cloned Repository', 'Installed Pypi Package'],
            ),
    inquirer.List('remote_host',
                message="Remote Server?",
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

num_cams = 2
sensors_dict = {
    f'cam_{ind}': {
        'sensor_type': 'camera',
        'camera_type': 'rgb-camera',
        'resolution': Res.SD,
        'radius': 20,
        'occlusion': True,
        'fov': 90.0,
    } for ind in range(num_cams)}

fig = plt.figure()
parser = argparse.ArgumentParser()
IAIEnv.add_config(parser)
config = parser.parse_args()

# world_parameters = dict(carlatown='Town01')
world_parameters = dict(carlatown='Town04')
scenario_parameters = dict(camera_location_variation=SensorSettings.Location(x=1, z=1, y=1),
                           camera_rotation_variation=SensorSettings.Rotation(yaw=10, pitch=10, roll=10))
if server_address:
    config.zmq_server_address = f'{server_address}:{server_port}'

env = IAIEnv(config)
obs = env.set_scenario('worlddataset', world_parameters=world_parameters, scenario_parameters=scenario_parameters, sensors=sensors_dict)


action = (0.0, 1.0)
_, reward, done, info = env.step(action)
# env.visualize_fig(fig)
rem_self = 0
how_long = 0

env.render_init(sensors_dict, renderer='pygame', scale=.5)
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
            obs = env.set_scenario('worlddataset', world_parameters=world_parameters, scenario_parameters=scenario_parameters, sensors=sensors_dict)
        elif cmd == 'end':
            print(env.end_simulation())
            env.close()
            break
        else:
            angle = float(cmd)
            acceleration = float(input('Enter Acceleration:'))
            action = (acceleration, angle)
            obs, reward, done, info = env.step(action)
    for attached_sensor in sensors_dict:
        name = 'boundingbox_' + attached_sensor
        if (name in obs['sensor_data']):
            bb2d = ClientSideBoundingBoxes.get_2d_bbox(obs['sensor_data'][name]['bounding_boxes'], 0, 0,
                                                       sensors_dict[attached_sensor]['fov'],
                                                       sensors_dict[attached_sensor]['resolution'],
                                                       obs['compact_vector'][:3], obs['compact_vector'][3:6],
                                                       coordinate_system='attached_sensor', occlusion=True)
            img = obs['sensor_data'][attached_sensor]['image']
            obs['sensor_data'][attached_sensor]['image'] = ClientSideBoundingBoxes.draw_bounding_boxes_on_array(img,
                                                                                                                bb2d,
                                                                                                                draw2d=False,
                                                                                                                occlusion=True)
    frame = env.render()
    frames.append(frame)
print(f'Episode Done, Reward:{reward}')
# file_name= 'script_sensor_video.mp4'
# imageio.mimwrite(file_name, frames, fps=15, quality=7)
# env.get_map()
##
