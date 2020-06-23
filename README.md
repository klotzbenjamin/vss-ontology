# VSSo: the Vehicle Signal Specification Ontology
This repository contains the research project carried out around the development, extension and usage of VSSo. VSSo is an ontology created from [GENIVI's Vehicle Signal Specification](https://github.com/GENIVI/vehicle_signal_specification/). It relies on the [SOSA patterns for observations and actuations](https://www.w3.org/TR/vocab-ssn/).

The VSSo ontology is available in [Turtle](vsso.ttl).

## Folder structure
The repository is structured as follows:
### [docs](docs)
This folder contains the html documentation of VSSo, automatically generated using [WIDOCO](https://github.com/dgarijo/Widoco). The rendered page is available at http://automotive.eurecom.fr/vsso
### [rdf-generation](rdf-generation)
This folder contains the script for extending VSSo according to the priciple of private branches described in the vehicle signal specification.
### [trajectory-annotation](trajectory-annotation)
This folder contains a script for generating semantic trajectories using VSSo, SOSA and STEP. A public demonstrator is available at http://automotive.eurecom.fr/trajectory

## Competency questions for VSSo
We also provide [a list of competency question](competency-questions.md), that served to evaluate VSSo, expressed when possible as SPARQL queries on VSSo datasets.