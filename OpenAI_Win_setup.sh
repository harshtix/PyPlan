# filepaths will start with /mnt/... (ex: /mnt/c/Python36/Scripts/pip.exe)
PY = # absolute path to Python installation directory
GYM = # absolute gym-master directory location (should be in PyPlan)
NUMPY = # absolute filepath to numpy wheel file
SCIPY = # absolute filepath to scipy wheel file

PIP = $PY + '/Scripts/pip.exe'

sudo apt-get update
sudo apt-get install -y python-numpy python-dev cmake zlib1g-dev libjpeg-dev xvfb libav-tools xorg-dev python-opengl libboost-all-dev libsdl2-dev swig

cd $GYM

$PIP install $NUMPY
$PIP install $SCIPY
# $PIP install tensorflow

$PIP install 'gym' .
# $PIP install 'gym[parameter_tuning]'
$PIP install 'gym[classic_control]' . 