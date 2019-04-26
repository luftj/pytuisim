# TODO

## open questions

get noise source from TUI-objects as well?


## input

[X] receive TUIO
[ ] load object geometries
[ ] convert TUIO to geometry
[X] load background GeoJSON
    [ ] parse more robustly
    [X] get filename from config.ini

## putput

[ ] convert object geometries to json
[ ] send object geometry json to noise model
[ ] receive noise json from model

## output

[X] plot background json
[X] plot object 
    [ ] plot geometry
[ ] plot noise json

## general

[ ] packaging
    [ ] put used packages into seperate modules and repos
[ ] deployment 
    [ ] install script for used external packages
    [ ] install own modules and dependencies
    [ ] include external binary software (TUIO server etc)