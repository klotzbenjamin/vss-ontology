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
#### What are the attributes of my car and what do they express?
```SPARQL
SELECT ?attribute ?branch ?value
WHERE { ?attribute  rdfs:subPropertyOf  vss:attribute.
?branch ?attribute ?value.}
```
#### How many attributes does my car have?
```SPARQL
SELECT (count(distinct ?attribute) as ?count)
WHERE {?attribute  rdfs:subPropertyOf  vss:attribute.}
GROUP BY ?x
```
#### What is the model of this car?
```SPARQL
SELECT ?model
WHERE { ?branch vss:model ?model.}
```
#### What is the brand of my car?
```SPARQL
SELECT ?brand
WHERE { ?branch vss:brand ?brand.}
```
#### What is the VIN of my car?
```SPARQL
SELECT ?vin
WHERE { ?branch vss:vin ?vin.}
```
#### How old is my car?
```SPARQL
SELECT ?age
WHERE { ?branch vss:year ?year.
BIND((2018-?year) AS ?age)}
```
#### What are the dimensions of my car?
```SPARQL
SELECT ?length ?width ?height
WHERE { ?branch vss:length ?length;
	vss:width ?width;
	vss:height ?height.}
```
#### What type of fuel does my car need?
```SPARQL
SELECT ?fueltype
WHERE {?branch vss:fuelType ?fuelType.}
```
#### What type of transmission does my car have?
```SPARQL
SELECT ?type
WHERE { ?branch vss:transmissionType ?type.}
```
#### What are the characteristics of my engine?
```SPARQL
SELECT ?engine ?attribute ?value
WHERE { ?attribute  rdfs:subPropertyOf  vss:attribute.
?engine a vss:InternalCombustionEngine;
  ?attribute ?value.}
```
#### How many doors does my car contain?
```SPARQL
SELECT ?attributes (count(distinct ?attributes) as ?count)
WHERE{?attribute  rdfs:subPropertyOf  vss:attribute.
?door a vss:Door.
{?door ?attribute ?value}
UNION
{?branch vss:partOf ?door;
  ?branch ?attribute ?value}}
```
#### How many seats do I have in my car?
```SPARQL
SELECT ?seats (count(distinct ?seats) as ?count)
WHERE { ?row1  a  vss:row1PosCount.
?row2  a  vss:row2PosCount.
?row3  a  vss:row3PosCount.
?row4  a  vss:row4PosCount.
?row5  a  vss:row5PosCount.
?branch ?row1 ?row1Count.
?branch ?row2 ?row2Count.
?branch ?row3 ?row3Count.
?branch ?row4 ?row4Count.
?branch ?row5 ?row5Count.
BIND((?row1+?row2+?row3+?row4+?row5) AS ?seats)}
```
#### On which side is located the steering wheel?
```SPARQL
SELECT ?side
WHERE { ?attribute  a  vss:steeringWheelSide.
?branch ?attribute ?side.}
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
#### Which signals are both observable and actuable?
```SPARQL
SELECT ?signal ?sensor ?actuator
WHERE { ?actuator  vss:consumes ?signal.
  ?sensor sosa:observes ?signal.
  ?signal a vss:ActuatableSignal, vss:ObservableSignal.}
```
#### How many sensors does my car contain?
```SPARQL
SELECT ?sensor (count(distinct ?sensor) as ?count)
WHERE { ?sensor sosa:observes ?signal.
  ?signal a vss:ObservableSignal.}
```
#### How many different speedometers does my car contain?
```SPARQL
SELECT ?sensor (count(distinct ?sensor) as ?count)
WHERE { ?sensor a vss:Speedometer.}
```
#### In which part of my car is produced the signal vss:LongitudinalAcceleration?
```SPARQL
SELECT ?branch
WHERE { ?branch  a  vss:Branch.
?branch vss:hasSignal vss:LongitudinalAcceleration.
FILTER NOT EXIST{?x vss:partOf ?p}
}
```
#### Which signals measure a temperature, and in which part of my car?
```SPARQL
SELECT ?signal ?branch
WHERE { ?branch  a  vss:Branch.
?branch vss:hasSignal ?signal.
?signal a vss:AmbientAirTemperature.
FILTER NOT EXIST{?x vss:partOf ?p}
}
```
#### What unit type does the signal vss:VehicleYaw use?
```SPARQL
SELECT ?unitsystem
WHERE { ?yaw  a vss:VehicleYaw;
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
#### What are the values of all signals representing the speed of my car?
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
#### Which windows are open?
```SPARQL
SELECT ?position
WHERE {?windowPosition a vss:WindowPosition.
?window vss:hasSignal ?windowPosition.
?obs a sosa:Observation;
	sosa:observedProperty ?windowPosition;
	sosa:hasResult ?result;
	sosa:PhenomenonTime ?time.
?result qudt:numericValue ?value.
FILTER(?value < 100)
?window vss:position ?position.
}
ORDER BY DESC(?time)
```
#### What is the local temperature on the driver side?
```SPARQL
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

