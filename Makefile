#
# Makefile to generate specifications
#

.PHONY: clean ttl

all: clean tll

ttl:
	./rdf-generation/vspec2csv.py -i:..vehicle-signal-specification/spec/VehicleSignalSpecification.id:1 -I ..vehicle-signal-specification/spec ..vehicle-signal-specification/spec/VehicleSignalSpecification.vspec VSSo_extended_$$(cat VERSION).ttl

clean:
	rm -f VSSo_extended_$$(cat VERSION).ttl
