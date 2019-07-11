# TODO

## open questions

get noise source from TUI-objects as well?


## input

- [X] receive TUIO
- [X] load object geometries
  - [ ] real geojson?
  - [X] any ID / default geometry for unknown IDs
- [X] convert TUIO to geometry
    - [X] rotate geometry
      - [X] fix rotation (consider adjacent objets)
- [X] load background GeoJSON
    - [ ] parse more robustly
    - [X] get filename from config.ini
- [X] fixed scale (1:500?)
  - [X] from config
  - [ ] seperate model scale from physical display PPI scale
- [ ] proper geo-tranformations? (e.g. pyproj)
    - [ ] store projection in Geometry object?
- [ ] allow raster background map

## putput

- [X] convert object geometries to json
- [X] send object geometry json to noise model
- [X] receive noise json from model
- [X] pygame window (fullscreen, ...)
- [ ] be faster!
  - [ ] update tracking exactly as often as necessary
  - [X] optimise drawing
  - [X] noise sim
  - [X] line simplification

## output

- [X] plot background json
- [X] plot object 
    - [X] plot geometry in real time? Shouldn't be necessary, when tracking is fast enough
    - [ ] halo effect?
- [X] plot noise json
  - [X] read feature properties from file
  - [X] colour iso-polys
    - [X] read colour key from config
- [X] indicate computation in process
- [ ] show colour legend

## general

- [ ] python3 port?!
- [ ] comment code
- [ ] packaging
    - [ ] config
        - [X] tuio address/port from file
        - [ ] map center / scale (or calculate it from input map?)
        - [ ] "invert" option, for different camera setups?
    - [ ] put used packages into seperate modules and repos
    - [X] requirements.txt
- [ ] deployment 
    - [X] start script win
    - [ ] start script linux
    - [X] install script for used external packages -> requirements.txt
    - [ ] install own modules and dependencies
    - [ ] include external binary software? (TUIO server etc)