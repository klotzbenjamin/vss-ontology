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
VSS comes with an extension mechnism, where new private concepst are included in the "Private" repository. This methods has the benefit of separating the core model from the private concepts. The script vspec2ttl.py will generate an extension generatedVSSoExtension if the private branch is included. See https://github.com/GENIVI/vehicle_signal_specification for more details.

The other solution consists in modifying directly VSS concepts. It is not recommended. For this case, an ontology generatedVSSo will be produced.

### Generate an extension
```shell
make
```
The Makefile will call the generation script, which will generate an extension of VSSo.
