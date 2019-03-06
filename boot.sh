#!/bin/bash

echo "starting gass"
amixer set PCM 100
/home/osmc/.gvenv/bin/python /home/osmc/assistant/main.py 

