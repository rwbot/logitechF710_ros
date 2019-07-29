#!/bin/bash

unalias diffd
unalias holo

alias diffd="roslaunch logitech_f710 diff_drive.launch"
alias holo="roslaunch logitech_f710 holonomic.launch"
