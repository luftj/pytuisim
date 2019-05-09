# pytuisim

This project brings noise simulations to a tangible user interface

## setup

Requires
* pygame
* pyshp
For noise simulation:
* Java Runtime
* geomet
* psycopg2
* numpy


Uses
* [pytuio](https://code.google.com/archive/p/pytuio/) -- put it in ```tuio``` directory
* [noise simulation](git@github.com:CityScope/CSL_Hamburg_Noise.git) -- put it in ```CSL_Hamburg_Noise``` directory
  


``` python -m pip install requirements.txt ```
Linux: ```java -cp 'bin/*:bundle/*:sys-bundle/*' org.h2.tools.Server -pg``` in the ```CSL_Hamburg_Noise``` directory
Windows: ```java -cp 'bin/*;bundle/*;sys-bundle/*' org.h2.tools.Server -pg``` in the ```CSL_Hamburg_Noise``` directory


## how it works

1. read TUIO from network
2. create geometry from TUIO objects
3. write geometry as GeoJSON
4. send GeoJSON to noise sim
5. receive GeoJSON from noise sim
6. plot received GeoJSON
7. profit

## configuration

### config.json
contains deployment config: ip:port of TUIO server and filepath to underlying background map (as GeoJSON)

### geometry.json
contains geomtries for the different objects, see the provided sample for syntax
the rotational centre is at (0,0)
use the ID 0 to provide a default geometry for all not specifically described TUIO objects