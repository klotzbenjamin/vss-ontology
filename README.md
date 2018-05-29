# VSSo: as Vehicle Signals and Attribute Ontology
This folder contains the research project carried out around the development, extension and usage of VSSo. 
VSSo is an ontology created from GENIVI's Vehicle Signal Specification and the SOSA patterns for observations and actuations.

## Folder structure
Each project has its own folder. The current structure is as follows
### [https://github.com/klotzbenjamin/vss-ontology/tree/master/docs docs]
This contains the html documentation about VSSo, automatically generated using WIDOCO.
The rendered page is available at https://klotzbenjamin.github.io/vss-ontology/
### [https://github.com/klotzbenjamin/vss-ontology/tree/master/rdf-generation rdf-generation]
This contains the script for extending VSSo according to the priciple of private branches in the vehicle signal specification.
### [https://github.com/klotzbenjamin/vss-ontology/tree/master/trajectory-annotation trajectory-annotation]
This contains a script for generating semantic trajectories with VSSo, SOSA and STEP.
A public demonstrator is available at http://automotive.eurecom.fr/trajectory


## Setup
### Get the vehicle signal specification

```shell
git clone https://github.com/genivi...
```
### Get VSSo
...

## Functions usage

### Generate a private extension of VSSo

## Competency questions

### Car Attributes
#### What are the attributes of my car?
#### How many attributes does my car have?
#### What is the model of this car?
#### What is the brand of my car?
#### What is the VIN of my car?
#### How old is my car?
#### What are the dimensions of my car?
#### What type of fuel does my car need?
#### What type of transmission does my car have?
#### What are the characteristics of my engine?
#### How many doors does my car contain?
#### How many seats do I have in my car?
#### On which side is located the steering wheel?

### Static Signals
#### Is there a signal measuring the steering wheel angle?
#### Which signals are controllable?
#### Which signals are both observable and actuable?
#### How many sensors does my car contain?
#### How many different speedometers does my car contain?
#### In which part of my car is produced the signal vss:LongitudinalAcceleration?
#### Which signals measure a temperature, and in which part of my car?
#### What unit type does the signal vss:VehicleYaw use?
#### What are the characteristics of the sensor producing the signal “TravelledDistance” in the OBD branch?
#### What are the maximum values allowed for all signals from car part “Vehicle”?

### Dynamic signals
#### What is the current gear?
#### What are the values of all signals representing the speed of my car?
#### Which windows are open?
#### What is the local temperature on the driver side?
#### What are the current values of signals defining the driver seat position?


