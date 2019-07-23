#!/bin/bash

sudo cp ~/catkin_ws/src/logitech_f710/udev/10-all-js-f710.rules /etc/udev/rules.d/
sudo service udev restart
sudo udevadm control --reload-rules && sudo service udev restart && sudo udevadm trigger
exit
$SHELL
