# TODO

## open questions

get noise source from TUI-objects as well?


## input

- [X] receive TUIO
- [X] load object geometries
  - [ ] real geojson?
  - [X] any ID / default gemetry for unknown IDs
- [X] convert TUIO to geometry
    - [X] rotate geometry
      - [X] fix rotation (consider adjacent objets)
- [X] load background GeoJSON
    - [ ] parse more robustly
    - [X] get filename from config.ini
- [ ] fixed scale (1:500?)
- [ ] proper geo-tranformations? (e.g. pyproj)
    - [ ] store projection in Geometry object?

## putput

- [X] convert object geometries to json
- [X] send object geometry json to noise model
- [X] receive noise json from model
- [ ] pygame window (fullscreen, resize, ...)
- [ ] be faster!

## output

- [X] plot background json
- [X] plot object 
    - [ ] plot geometry in real time
- [X] plot noise json
  - [X] read feature properties from file
  - [X] colour iso-polys
    - [X] read colour key from config

## general

- [ ] python3 port?!
- [ ] comment code
- [ ] packaging
    - [ ] config
        - [X] tuio address/port from file
        - [ ] map center / scale (or calculate it from input map?)
    - [ ] put used packages into seperate modules and repos
    - [X] requirements.txt
- [ ] deployment 
    - [ ] start script
    - [ ] install script for used external packages -> requirements.txt
    - [ ] install own modules and dependencies
    - [ ] include external binary software? (TUIO server etc)