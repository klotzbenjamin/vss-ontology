# Linked data extraction from a simulated vehicle
This folder contains a python scripts that reads data on a car simulation running on a local server, and writes RDF triples that describe the state of the vehicle linked to its trajectory using a combination of the SOSA, STEP and VSS ontologies.
The "VSS ontology" folder contains the Vehicle Signal Specification in a JS file, the JS script that translates it into RDF triples and the output: an ontologized VSS.
## Setup of the vehicle simulator
You will need to install the vehicle simulation, and run it locally
```shell
git clone https://github.com/openxc/openxc-vehicle-simulator
cd leshan openxc-vehicle-simulator-master
./simulator.py

```

You will be able to controll the simulation by opening a web browser on 
```shell
127.0.0.1:50000

```

It will generate a JSON file of signal values available at
```shell
127.0.0.1:50000/_Get_Data

```

## Setup of signal definitions
In Configuration.csv, there is a line for each signal known by the vehicle. You can add more signal following the VSS:
```
https://github.com/GENIVI/vehicle_signal_specification/
```
You can select a VSS ontology between a smal one with only 4 signals for comprehensiveness, and the full one.

## Start the script
Run the car_data_extraction.py script
```shell
python car_data_extraction.py

```

## Attach Attributes to the car
```shell
127.0.0.1:5000/addAttributes
```
Will create RDF triples about sensors and signal using to the Vehicle Sales Ontology for the vehicles features, from the known signals in COnfiguration.csv and enriched with the VSS ontology.

## Observe signals
```shell
127.0.0.1:5000/addObservation/[time span]/[period of requests]/[Signal1,Signal2...]
```
Will add RDF triples about signal values on the existing graph using instances of SOSA:Observations. It will also create an instance of STEP:Trajectory and record fix points for filling the raw trajectory.

## Reduce trajectories
```shell
127.0.0.1:5000/reduce/[Signal1,Signal2...]
```
Will do a SPARQL query on the trajectory graph to produce a reducedTrajectory.csv file with format (latiture, longitude, time, [values])

## Visualize signal variations
You can visualize the variations of a signal values over a recorded trajectory.
```shell
127.0.0.1:5000/variation/[time span]/[period of requests]/[Signal]/[offset]
```
It will create a vehicle graph and add attributes and observation of the given [Signal] with during [time span] seconds with a period of [period of requests]. Then a label is generated for sub-trajectories (is increasing, is decreasing, is constant) depending if the signal value changed by more than [offset] between 2 observations. Each label is associated with a color, red for increasing value yellow if constant, green if decreasing.

## Visualize a driving smoothness label

