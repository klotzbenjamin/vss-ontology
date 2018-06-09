#
# Makefile to generate specifications
#


.PHONY: clean all ttl

all: clean ttl

ttl:
	python vspec2ttl.py -i:../../vehicle_signal_specification/spec/VehicleSignalSpecification.id:1 -I ../../vehicle_signal_specification/spec ../../vehicle_signal_specification/spec/VehicleSignalSpecification.vspec generatedVSSo.ttl

clean:
	rm -f generatedVSSo.ttl generatedVSSoExtension.ttl
