#!/usr/bin/env python3
#
# Code modified from https://github.com/OlafenwaMoses/ImageAI
#
# Copyright (c) 2020 Recognition Designs Ltd, Colin Twigg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# for use with DDL/Anki's Vector Robot: https://www.anki.com/en-us/vector
    
import anki_vector
from anki_vector.util import degrees, Angle
from imageai.Prediction import ImagePrediction
import os
from PIL import Image, ImageStat

robot = anki_vector.Robot()
robot.connect()
robot.behavior.set_lift_height(0)
robot.behavior.set_head_angle(degrees(12.0))

robot.behavior.say_text("Show me the item to identify. 3, 2, 1, SNAPP")
image = robot.camera.capture_single_image()
#change the path to where you want the picture to be saved
image.raw_image.save('capture.jpeg', 'JPEG')

#object detection code below
prediction = ImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath("resnet50_weights_tf_dim_ordering_tf_kernels.h5")
prediction.loadModel()

#change the path to where you picture is saved. result_count returns number of possible results from 1-1000
predictions, percentage_probabilities = prediction.predictImage ("capture.jpeg", result_count=1)
for index in range(len(predictions)):
    s = (predictions[index])
    print(s.replace('_', ' ') , " : " , percentage_probabilities[index])
 
    if (percentage_probabilities[index] >= 90):
        print("That is definitely a {}".format(s.replace('_', ' ')))
        robot.anim.play_animation_trigger('GreetAfterLongTime')
        robot.behavior.say_text("That is definitely a {}".format(s.replace('_', ' ')))

    if (percentage_probabilities[index] <= 89) and (percentage_probabilities[index] >= 60):
        print("That looks like a {}".format(s.replace('_', ' ')))
        robot.behavior.say_text("That looks like a {}".format(s.replace('_', ' ')))

    if (percentage_probabilities[index] <= 59) and (percentage_probabilities[index] >= 30):
        print("I'm not sure but that looks like a {}".format(s.replace('_', ' ')))
        robot.behavior.say_text("I'm not sure but that looks like a {}".format(s.replace('_', ' ')))

    if (percentage_probabilities[index] <= 29) and (percentage_probabilities[index] >= 0):
        print("Thats tricky, is it a {}".format(s.replace('_', ' ')))
        robot.anim.play_animation_trigger('CubePounceLoseSession')
        robot.behavior.say_text("Thats tricky, is it a {}".format(s.replace('_', ' ')))
        
    robot.disconnect()
