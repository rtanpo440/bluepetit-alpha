#!/bin/bash

joycontrol-pluginloader -r $(cat .macaddress) bluepetit-plugins/SendStringPlugin.py -p "$1"
