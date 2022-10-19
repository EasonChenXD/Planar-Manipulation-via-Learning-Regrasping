'''
coding  :utf-8
@Project:RUT_pro_01
@Time   :2022/10/17 11:19
@Author :Zhiyuan Chen
@Desc   :

'''

import numpy as np
import pandas as pd
import os, sys, glob
from scipy.spatial.transform import Rotation as Rot
import pybullet as p
import pybullet_data
import time

def enable_physics():
    p.setTimeStep(1 / 240.0)
    p.setGravity(0, 0, -9.81)

def get_material(mode):

    if mode == 'rand':
        urdf_list = glob.glob('../dataset/MCB_A_total/MCB_A_URDF_Recon_Show/*/*/*.urdf')
    elif mode == 'test' or mode == 'train':
        urdf_list = glob.glob('../dataset/MCB_A_total/MCB_A_URDF_Recon_Show/{}/*/*.urdf'.format(mode))
    else:
        print('the mode is wrong !')

    urdf_path = np.random.choice(urdf_list,1)[0]
    obj_code = urdf_path.split('/')[-1][:-5]
    obj_name = urdf_path.split('/')[-2]
    gt_path = glob.glob('../dataset/MCB_A_total/simu_data_stablePO_general/*/*/*{}*'.format(obj_code))[0]
    f = pd.read_csv(gt_path, sep=' ')
    print('Object name: {}\nObject code: {}'.format(obj_name,obj_code))

    return urdf_path,f

def pick_single_stable_placement(f):
    index = np.random.randint(0, len(f))
    ini = f.iloc[[index]]
    ini_pos = np.array(ini[['objectPosX', 'objectPosY', 'objectPosZ']])[0]
    ini_orn = np.array(ini[['objectOrnR', 'objectOrnP', 'objectOrnY']])[0]
    ini_quat = Rot.from_euler('xyz', ini_orn).as_quat()
    print('The {}th stable poses:\nPosition: {}\nOrientation: {}'.format(index,ini_pos,ini_orn))

    return ini_pos,ini_quat

def progress():

    physicsClient = p.connect(p.GUI, options="--background_color_red=1 "
                                            "--background_color_blue=1 "
                                            "--background_color_green=1"
                                             "--width=1920 --height=1640")
    enable_physics()
    p.resetDebugVisualizerCamera(cameraDistance=0.4,
                                 cameraYaw=0,
                                 cameraPitch=-50,
                                 cameraTargetPosition=[0, -0.1, 0.1])
    # load the plane
    planePath = pybullet_data.getDataPath()
    planeId = p.loadURDF(os.path.join(planePath, 'plane.urdf'))

    # load the object
    urdf_path, gt = get_material(mode)
    obj = p.loadURDF(urdf_path)

    while True:
        # randomly pick a position and orientation in the ground-truth
        ini_pos, ini_quat = pick_single_stable_placement(gt)
        p.resetBasePositionAndOrientation(obj, ini_pos, ini_quat)

        time.sleep(5)#stop 5 seconds for watching




if __name__ == '__main__':
    mode = 'rand'
    # rand - randomly pick an object in the dataset
    # train - randomly pick an object in the training set
    # test - randomly pick an object in the test set
    progress()
