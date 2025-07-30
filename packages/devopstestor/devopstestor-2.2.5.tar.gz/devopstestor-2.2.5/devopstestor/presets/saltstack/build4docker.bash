#!/bin/bash
set -e
set -o pipefail
# If devopstestor is in a container, dockercontroller must be used without volume
sed -i "s/preset_name: saltstack_dockerincontainer/preset_name: saltstack_dockerincontainer_novolume/g" "$DEVOPSTESTOR_PATH/presets/saltstack/config/machine.yml"

# to avoid redundancy disable pillar and salt source accessor because, they can be mount directly with -v en /srv/salt and in /srv/pillar

sed -i "s/undefined: please use --salt_files to set value/srv\/salt/g" "$DEVOPSTESTOR_PATH/presets/saltstack/config/machine.yml"
sed -i "s/undefined: please use --pillar_files to set value/srv\/pillar/g" "$DEVOPSTESTOR_PATH/presets/saltstack/config/machine.yml"

exit $?