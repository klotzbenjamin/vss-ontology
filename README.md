# VSSo: as Vehicle Signals and Attribute Ontology
This folder contains the research project carried out around the development, extension and usage of VSSo. 
VSSo is an ontology created from GENIVI's Vehicle Signal Specification and the SOSA patterns for observations and actuations.

## Folder structure
Each project has its own folder. The current structure is as follows
### [docs](https://github.com/klotzbenjamin/vss-ontology/tree/master/docs)
This contains the html documentation about VSSo, automatically generated using WIDOCO.
The rendered page is available at https://klotzbenjamin.github.io/vss-ontology/
### [rdf-generation](https://github.com/klotzbenjamin/vss-ontology/tree/master/rdf-generation)
This contains the script for extending VSSo according to the priciple of private branches in the vehicle signal specification.
### [trajectory-annotation](https://github.com/klotzbenjamin/vss-ontology/tree/master/trajectory-annotation)
This contains a script for generating semantic trajectories with VSSo, SOSA and STEP.
A public demonstrator is available at http://automotive.eurecom.fr/trajectory

## Competency questions for VSSo
Here is a list of competency question, that served to evaluate VSSo, expressed when possible as SPARQL queries on VSSo datasets.

### Car Attributes
#### What are the attributes of this car and what do they express?
```SPARQL
SELECT ?attribute ?branch ?value
WHERE { ?attribute  rdfs:subPropertyOf  vss:attribute.
?branch ?attribute ?value.}
```
#### How many attributes does this car have?
```SPARQL
SELECT (count(distinct ?attribute) as ?nbAttribute)
WHERE{?attribute  rdfs:subPropertyOf  vss:attribute.}
GROUP BY ?x
```
#### What is the model of this car?
```SPARQL
SELECT ?model
WHERE { ?branch vss:model ?model.}
```
#### What is the brand of this car?
```SPARQL
SELECT ?brand
WHERE { ?branch vss:brand ?brand.}
```
#### What is the VIN of this car?
```SPARQL
SELECT ?vin
WHERE { ?branch vss:vin ?vin.}
```
#### How old is this car?
```SPARQL
SELECT ?age
WHERE { ?branch vss:year ?year.
BIND((2018-?year) AS ?age)}
```
#### What are the dimensions of this car?
```SPARQL
SELECT ?length ?width ?height
WHERE { ?branch vss:length ?length;
	vss:width ?width;
	vss:height ?height.}
```
#### What are the characteristics of this car's chassis?
```SPARQL
SELECT ?attribute ?value
WHERE { ?attribute  rdfs:subPropertyOf  vss:attribute.
?chassis a vss:Chassis;
  ?attribute ?value.}
```
#### What type of fuel does this car need?
```SPARQL
SELECT ?fueltype
WHERE {?branch vss:fuelType ?fuelType.}
```
#### What type of transmission does this car have?
```SPARQL
SELECT ?type
WHERE { ?branch vss:transmissionType ?type.}
```
#### What are the characteristics of this engine?
```SPARQL
SELECT ?engine ?attribute ?value
WHERE { ?attribute  rdfs:subPropertyOf  vss:attribute.
?engine a vss:InternalCombustionEngine;
  ?attribute ?value.}
```
#### How many doors does this car contain?
```SPARQL
SELECT ?nbDoor
WHERE { ?branch vss:doorCount ?nbDoor.}
```
#### How many seats do I have this my car?
```SPARQL
SELECT ?nbSeats ?nbRows
WHERE { ?seats a vss:Seat;
	vss:rowCount ?nbRows;
	vss:row1PosCount ?row1Count;
	vss:row2PosCount ?row2Count;
	vss:row3PosCount ?row3Count;
	vss:row4PosCount ?row4Count;
vss:row5PosCount ?row5Count.
BIND((?row1Count + ?row2Count + ?row3Count + ?row4Count + ?row5Count) AS ?nbSeats)}

```
#### On which side is located the steering wheel?
```SPARQL
SELECT ?steeringWheelSide
WHERE { ?wheel a vss:SteeringWheel;
vss:steeringWheelSide ?steeringWheelSide.}
```

### Static Signals
#### Is there a signal measuring the steering wheel angle?
```SPARQL
SELECT ?signal
WHERE { ?signal a vss:SteeringWheelAngle.}
```
#### Which signals are controllable?
```SPARQL
SELECT ?signal ?actuator
WHERE { ?actuator  vss:consumes ?signal.
  ?signal a vss:ActuatableSignal.}
```
#### Which signals are both observable and actuatable?
```SPARQL
SELECT ?signal ?sensor ?actuator
WHERE { ?actuator  vss:consumes ?signal.
?sensor sosa:observes ?signal.
?signal a vss:ActuatableSignal, vss:ObservableSignal.}
```
#### How many sensors does this car contain?
```SPARQL
SELECT (count(distinct ?sensor) as ?nbSensor)
WHERE { ?sensor sosa:observes ?signal.
	?signal a vss:ObservableSignal.}
```
#### How many different speedometers does this car contain?
```SPARQL
SELECT (count(distinct ?sensor) as ?nbSpeedSensors)
WHERE { ?sensor a vss:Speedometer.}
```
#### In which part of thismy car is produced the signal vss:LongitudinalAcceleration?
```SPARQL
SELECT ?branch ?branchType
WHERE { ?branch  a  ?branchType;
	vss:hasSignal ?signal.
?signal a vss:LongitudinalAcceleration.
}
```
#### Which signals measure a temperature, and in which part of this car?
```SPARQL
SELECT ?signal ?branch
WHERE { ?branch vss:hasSignal ?signal.
?signal a vss:AmbientAirTemperature.
}
```
#### What unit type does the signals of type vss:VehicleYaw use?
```SPARQL
SELECT ?signal ?unitsystem
WHERE { ?signal  a vss:VehicleYaw;
qudt:unit ?unitsystem.}
```
#### What are the characteristics of the sensor producing the signal “TravelledDistance” in the OBD branch?
```SPARQL
SELECT ?sensor ?p ?o
WHERE { ?sensor  a ?sensor;
  vss:observes ?signal;
  ?p ?o.
?signal a vss:TravelledDistance.}
```
#### What are the maximum values allowed for all signals from car part “Vehicle”?
```SPARQL
```

### Dynamic signals
#### What is the current gear?
```SPARQL
SELECT ?signal ?result ?time
WHERE {?signal a vss:CurrentGear.
?obs a sosa:Observation;
	sosa:observedProperty ?signal;
	sosa:hasSimpleResult ?result;
	sosa:phenomenonTime ?time.
}
ORDER BY DESC(?time)
LIMIT 1
```
#### What are the values of all signals representing the speed of this car now?
```SPARQL
SELECT ?signal ?result ?time
WHERE {?signal a vss:VehicleSpeed.
?obs a sosa:Observation;
	sosa:observedProperty ?signal;
	sosa:hasSimpleResult ?result;
	sosa:phenomenonTime ?time.
}
ORDER BY DESC(?time)
```
#### Which windows are currently open?
```SPARQL
SELECT ?position ?value ?time
WHERE {?signal a vss:WindowPosition.
?window vss:hasSignal ?signal.
?obs a sosa:Observation;
	sosa:observedProperty ?signal;
	sosa:hasSimpleResult ?value;
	sosa:phenomenonTime ?time.
?window vss:position ?position.
}
ORDER BY DESC(?time)
```
#### What is the local current temperature on the driver side?
```SPARQL
SELECT DISTINCT ?localTemperature ?value ?position ?time
WHERE { ?wheel a vss:SteeringWheel;
vss:steeringWheelSide ?steeringWheelSide.
?branch a vss:LocalHVAC;
vss:position ?position;
vss:hasSignal ?localTemperature.
?localTemperature a vss:LocalTemperature.
FILTER regex(str(?steeringWheelSide),str(?position))

?obs a sosa:Observation;
	sosa:observedProperty ?localTemperature;
	sosa:hasSimpleResult ?value;
	sosa:phenomenonTime ?time.
}
ORDER BY DESC(?time)
LIMIT 1
```
#### What are the current values of signals defining the driver seat position?
```SPARQL
```
#### When was the last time the speed was over 100 km/h?
```SPARQL
```
#### Where was the last time the driver door was unlocked?
```SPARQL
```
#### What was the maximal speed reached by the car?
```SPARQL
```

