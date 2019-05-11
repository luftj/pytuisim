#! /bin/sh

# !!! careful: this is unsafe! This will compromise access control to your X-server
# !!! use at your own risk!

docker build -t pytuisim .
xhost +local:root
docker run -it \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    pytuisim
xhost -local:root