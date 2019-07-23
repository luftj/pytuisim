# pytuisim

This project brings noise simulations to a tangible user interface

## setup

### Requires
* Python2 (tested with 2.7)
* pygame
* pyshp
#### For noise simulation:
* Java Runtime
* geomet
* psycopg2
* numpy


### Uses
* [pytuio](https://code.google.com/archive/p/pytuio/) -- put it in ```tuio``` directory
* [noise simulation](https://github.com/CityScope/CSL_Hamburg_Noise) -- submodule in ```CSL_Hamburg_Noise``` directory
  

```python -m pip install -r requirements.txt CSL_Hamburg_Noise/requirements.txt```

## Usage

### Start noise simulation database:
Linux: ```java -cp 'bin/*:bundle/*:sys-bundle/*' org.h2.tools.Server -pg``` in the ```CSL_Hamburg_Noise``` directory

Windows (cmd.exe): ```java -cp bin/*;bundle/*;sys-bundle/* org.h2.tools.Server -pg``` in the ```CSL_Hamburg_Noise``` directory
Windows (powershell.exe): ```java -cp 'bin/*;bundle/*;sys-bundle/*' org.h2.tools.Server -pg``` in the ```CSL_Hamburg_Noise``` directory

### Start interactive tool:
``` python main.py ```

1. Use WASD to fine-tune the map view to show your desired area.
2. Place TUIO objects.
3. Press RETURN to start calculating the resulting noise map for the current situation. This might take a while.
4. Behold the flashy colours.

## how it works

1. read TUIO from network (e.g. from [reacTIVision](http://reactivision.sourceforge.net/#files) server)
2. create geometry from TUIO objects
3. write geometry as GeoJSON
4. send GeoJSON to noise sim
5. receive GeoJSON from noise sim
6. plot received GeoJSON
7. profit

## configuration

### config.json
Contains deployment config: 
* ip:port of TUIO server (you can also pass it over the commandline like this: ```python main.py --ip 127.0.0.0 --port 3333```).
* filepath to underlying background map (as GeoJSON). The geodata should be in a metric projection, e.g. EPSG:25832.
* The scale as a constant in pixel/meter. This of course has to be calculated from the desired model scale (e.g. 1:500) and the display pixel density.
* The geo-coordinates to center the camera on.
* colour coding key for noise output. in 5 dB(A) steps from 0 = <45 to 6 = >75dB(A).

### geometry.json
Contains geomtries for the different objects, see the provided sample for syntax. All units are in metres. Positive Y is east, positive Y is north (when camera is below table)
The rotational centre is at (0,0).
Use the ID 0 to provide a default geometry for all not specifically described TUIO objects