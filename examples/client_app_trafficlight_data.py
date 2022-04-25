from invertedai_client.utils import Res, Resolution, PyGameWindow, ClientSideBoundingBoxes
# from iai_client.utils import Res, SensorSettings, Resolution, PyGameWindow, ClientSideBoundingBoxes
# from iai_client.interface import IAIEnv
from invertedai_client.interface import IAIEnv
from iai_common.communications.utils import SensorSettings
import numpy as np
import argparse
import matplotlib.pyplot as plt
import pygame

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
env = IAIEnv(config)
# obs = env.set_scenario('corl2017')
# obs = env.set_scenario('nocrash', sensors=sensors_dict)
# obs = env.set_scenario('egodriving', sensors=sensors_dict)
obs = env.set_scenario('worlddataset', world_parameters=world_parameters, scenario_parameters=scenario_parameters, sensors=sensors_dict)
action = (0.0, 1.0)
_, reward, done, info = env.step(action)
# env.visualize_fig(fig)
rem_self = 0
how_long = 0

pygame.init()

widths = [sensors_dict[sns]['resolution'].width for sns in sensors_dict if 'resolution' in sensors_dict[sns].keys()]
heights = [sensors_dict[sns]['resolution'].height for sns in sensors_dict if 'resolution' in sensors_dict[sns].keys()]
if len(heights) > 0:
    width = np.sum(widths)
    height = np.max(heights)
    full_res = Resolution(width, height)
    main_display = PyGameWindow(full_res)
##
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
            # obs = env.set_scenario('worlddataset', world_parameters=world_parameters, sensors=sensors_dict)
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
    # env.render(fig)
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

    # if len(heights) > 0:
    #     bb2d = ClientSideBoundingBoxes.get_2D_bbox(obs['sensor_data']['boundingbox_ego']['bounding_boxes'], None, None, 90.0, Res.MD, None, None, coordinate_system='sensor')
    #     img = obs['sensor_data']['front-cam']['image']
    #     obs['sensor_data']['front-cam']['image'] = ClientSideBoundingBoxes.draw_bounding_boxes_on_array(img, bb2d)

    if len(heights) > 0:
        disp_img = np.concatenate(list(
            obs['sensor_data'][name]['image'] for name in sensors_dict if 'image' in obs['sensor_data'][name].keys()),
                                  axis=1)
        main_display.render(disp_img)
        pygame.display.update()
#

print(f'Episode Done, Reward:{reward}')
# env.get_map()
##
