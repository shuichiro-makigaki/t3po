#! /bin/bash -eu

set -o pipefail

mkdir ~/.ssh
chmod 700 ~/.ssh
cat > ~/.ssh/private
chmod 600 ~/.ssh/private
echo 'Host login.t3.gsic.titech.ac.jp' >> ~/.ssh/config
echo "User ${T3_LOGIN_USERNAME}" >> ~/.ssh/config
echo 'StrictHostKeyChecking=no' >> ~/.ssh/config
echo 'IdentityFile ~/.ssh/private' >> ~/.ssh/config

python t3po.py
