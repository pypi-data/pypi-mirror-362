#!/bin/bash
set -e
set -o pipefail

## Preparation du systeme
apt-get update \
    && apt-get install -y \
        systemd procps apt iputils-ping

mkdir /etc/bash_completion.d


# pre-requis testauto
apt -y install python3-pytest python3-testinfra python3-coloredlogs curl python3-dateutil python3-pip python3-dotenv

python3 -m pip install --break-system-packages devopstestor
# Mise a jour du system
apt -y dist-upgrade

# Installation de Saltstack
curl -fsSL -o /etc/apt/keyrings/salt-archive-keyring-2023.gpg https://repo.saltproject.io/salt/py3/debian/12/amd64/SALT-PROJECT-GPG-PUBKEY-2023.gpg
echo "deb [signed-by=/etc/apt/keyrings/salt-archive-keyring-2023.gpg arch=amd64] https://repo.saltproject.io/salt/py3/debian/12/amd64/latest bookworm main" | tee /etc/apt/sources.list.d/salt.list
apt update
apt -y install salt-master
apt -y install salt-minion
systemctl enable salt-master
systemctl enable salt-minion

echo 'master: 127.0.0.1' >> /etc/salt/minion
echo 'master_alive_interval: 50' >> /etc/salt/minion

# Integration des sources
mkdir /srv/salt
mkdir /srv/pillar
mkdir /srv/pillar-auto

exit 0
