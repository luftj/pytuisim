# pytuisim

This project brings noise simulations to a tangible user interface

## setup

Requires
* pygame
* 

Uses
* pytuio
* git@github.com:CityScope/CSL_Hamburg_Noise.git
* 


``` python -m pip install [...] ```


## how it works

1. read TUIO from network
1. create geometry from TUIO objects
1. write geometry as GeoJSON
1. send GeoJSON to noise sim
1. receive GeoJSON from noise sim
1. print received GeoJSON
1. profit

## configuration

### config.json
contains deployment config, e.g. ip:port of TUIO server

### geometry.json
contains geomtries for the different objects