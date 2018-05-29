#Generation of a private extension of VSSo

## Setup
Put the vehicle signal specification and this repo in a common folder. 
### Get the vehicle signal specification

```shell
git clone https://github.com/GENIVI/vehicle_signal_specification
```
### Get the VSSo repo
```shell
git clone https://github.com/klotzbenjamin/vss-ontology
cd VSSontology/rdf-generation
```

## Functions usage
### Extend VSS
TODO

### Generate an extension
```shell
make
cd ..
```
The Makefile will call the generation script, which will generate an extension of VSSo.
