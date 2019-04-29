# TODO

## open questions

get noise source from TUI-objects as well?


## input

- [X] receive TUIO
- [X] load object geometries
- [X] convert TUIO to geometry
    - [X] rotate geometry
- [X] load background GeoJSON
    - [ ] parse more robustly
    - [X] get filename from config.ini
- [ ] fixed scale (1:500?)
- [ ] proper geo-tranformations? (e.g. pyproj)
    - [ ] store projection in Geometry object

## putput

- [X] convert object geometries to json
- [ ] send object geometry json to noise model
- [ ] receive noise json from model

## output

- [X] plot background json
- [X] plot object 
    - [ ] plot geometry
- [ ] plot noise json

## general

- [ ] python3 port?!
- [ ] packaging
    - [ ] config
        - [ ] tuio address/port from file (rewrite ot pytuio necessary)
    - [ ] put used packages into seperate modules and repos
    - [ ] requirements.txt
- [ ] deployment 
    - [ ] install script for used external packages
    - [ ] install own modules and dependencies
    - [ ] include external binary software (TUIO server etc)