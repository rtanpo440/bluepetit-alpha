#!/bin/bash

echo "Bluepetit: セットアップをはじめます..."

: \
&& apt update \
&& apt install git libhidapi-hidraw0 \
&& git clone https://github.com/mart1nro/joycontrol.git \
&& pip3 install joycontrol \
&& git clone --recursive https://github.com/Almtr/joycontrol-pluginloader.git \
&& pip3 install joycontrol-pluginloader \
&& echo "Bluepetit: セットアップが完了しました" \
|| echo "Bluepetit: セットアップに失敗しました"
