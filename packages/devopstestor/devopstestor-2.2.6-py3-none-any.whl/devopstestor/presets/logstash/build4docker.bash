#!/bin/bash
set -e
set -o pipefail
# If devopstestor is in a container, dockercontroller must be used without volume
sed -i "s/preset_name: logstash/preset_name: logstash_novolume/g" "$DEVOPSTESTOR_PATH/presets/logstash/config/machine.yml"

exit $?