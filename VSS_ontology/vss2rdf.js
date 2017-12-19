
var $rdf = require('rdf-ext');
var $n3 = require('rdf-serializer-n3');

var vssns = 'https://raw.githubusercontent.com/klotzbenjamin/VSSontology/master/VSS_ontology/VSS.ttl/'; /* note: namespace IRI not fixed */

var RDF = {
  type: new $rdf.NamedNode('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
}

var RDFS = {
  comment: new $rdf.NamedNode('http://www.w3.org/2000/01/rdf-schema#comment'),
  subClassOf: new $rdf.NamedNode('http://www.w3.org/2000/01/rdf-schema#subClassOf'),
  Class: new $rdf.NamedNode('http://www.w3.org/2000/01/rdf-schema#Class')
}

var OWL = {
  Ontology: new $rdf.NamedNode('http://www.w3.org/2002/07/owl#Ontology'),
  ObjectProperty: new $rdf.NamedNode('http://www.w3.org/2002/07/owl#ObjectProperty'),
  DatatypeProperty: new $rdf.NamedNode('http://www.w3.org/2002/07/owl#DatatypeProperty'),
  FunctionalProperty: new $rdf.NamedNode('http://www.w3.org/2002/07/owl#FunctionalProperty'),
  TransitiveProperty: new $rdf.NamedNode('http://www.w3.org/2002/07/owl#TransitiveProperty'),
  Restriction: new $rdf.NamedNode('http://www.w3.org/2002/07/owl#Restriction'),
  onProperty: new $rdf.NamedNode('http://www.w3.org/2002/07/owl#onProperty'),
  onClass: new $rdf.NamedNode('http://www.w3.org/2002/07/owl#onClass'),
  allValuesFrom: new $rdf.NamedNode('http://www.w3.org/2002/07/owl#allValuesFrom'),
  someValuesFrom: new $rdf.NamedNode('http://www.w3.org/2002/07/owl#someValuesFrom'),
  qualifiedCardinality: new $rdf.NamedNode('http://www.w3.org/2002/07/owl#qualifiedCardinality')
}

var VSS = {
  hasValue: new $rdf.NamedNode('http://genivi.org/ns/vss#hasValue'),
  Attribute: new $rdf.NamedNode('http://genivi.org/ns/vss#Attribute'),
  hasAttribute: new $rdf.NamedNode('http://genivi.org/ns/vss#hasAttribute'),
  Signal: new $rdf.NamedNode('http://genivi.org/ns/vss#Signal'),
  hasSignal: new $rdf.NamedNode('http://genivi.org/ns/vss#hasSignal'),
  VehiclePart: new $rdf.NamedNode('http://genivi.org/ns/vss#VehiclePart'),
  isPartOf: new $rdf.NamedNode('http://genivi.org/ns/vss#isPartOf')
}

var QUDT = {
  unit: new $rdf.NamedNode('http://www.qudt.org/1.1/schema/qudt#Unit')
}

var SOSA = {
  isObservedBy: new $rdf.NamedNode('http://www.w3.org/ns/sosa/isObservedBy')
}

/* type string (from FrancaIDL) to XSD built-in type */
var type2xsd = {
  'UInt8': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#unsignedByte'),
  'Int8': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#byte'),
  'UInt16': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#unsignedShort'),
  'Int16': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#short'),
  'UInt32': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#unsignedInt'),
  'Int32': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#int'),
  'UInt64': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#unsignedLong'),
  'Int64': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#long'),
  'Boolean': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#boolean'),
  'Float': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#float'),
  'Double': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#double'),
  'String': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#string'),
  /* note: no accurate mapping available for ByteBuffer */
  'ByteBuffer': new $rdf.NamedNode('http://www.w3.org/2001/XMLSchema#hexBinary')
}

/* unit string (SI?) to QUDT term */
var unit2qudt = {
  // TODO: improve
  'A': new $rdf.NamedNode('http://qudt.org/vocab/unit#Ampere'),
  'Nm': new $rdf.NamedNode('http://qudt.org/vocab/unit#NewtonMeter'),
  'V': new $rdf.NamedNode('http://qudt.org/vocab/unit#Volt'), 
  'celsius': new $rdf.NamedNode('http://qudt.org/vocab/unit#DegreeCelsius'),
  'cm/s': new $rdf.NamedNode('http://qudt.org/vocab/unit#CentimeterPerSecond'),
  'degree': new $rdf.NamedNode('http://qudt.org/vocab/unit#DegreeAngle'),
  'degrees/s': new $rdf.NamedNode('http://qudt.org/vocab/unit#DegreePerSecond'),
//'g/s': new $rdf.NamedNode('http://qudt.org/vocab/unit#Ampere'), set g/s from kg/s
  'inch': new $rdf.NamedNode('http://qudt.org/vocab/unit#Inch'),
  'kW': new $rdf.NamedNode('http://qudt.org/vocab/unit#Kilowatt'),
  'kilometer': new $rdf.NamedNode('http://qudt.org/vocab/unit#Kilometer'),
  'km': new $rdf.NamedNode('http://qudt.org/vocab/unit#Kilometer'),
  'km/h': new $rdf.NamedNode('http://qudt.org/vocab/unit#KilometerPerHour'),
  'kpa': new $rdf.NamedNode('http://qudt.org/vocab/unit#KiloPascal'),
'l': new $rdf.NamedNode('http://qudt.org/vocab/unit#Liter'),
//'l/h': new $rdf.NamedNode('http://qudt.org/vocab/unit#Ampere'),
'm': new $rdf.NamedNode('http://qudt.org/vocab/unit#Meter'),
'm/s': new $rdf.NamedNode('http://qudt.org/vocab/unit#MeterPerSecond'),
'mbar': new $rdf.NamedNode('http://qudt.org/vocab/unit#Millibar'),
'min': new $rdf.NamedNode('http://qudt.org/vocab/unit#MinuteTime'),
//'ml': new $rdf.NamedNode('http://qudt.org/vocab/unit#Ampere'),
//'ml/100km': new $rdf.NamedNode('http://qudt.org/vocab/unit#Ampere'),
'mm': new $rdf.NamedNode('http://qudt.org/vocab/unit#Millimeter'),
'mps': new $rdf.NamedNode('http://qudt.org/vocab/unit#MeterPerSecond'),
'pa': new $rdf.NamedNode('http://qudt.org/vocab/unit#Pascal'),
'percent': new $rdf.NamedNode('http://qudt.org/vocab/unit#Percent'),
'percentage': new $rdf.NamedNode('http://qudt.org/vocab/unit#Percent'),
'ratio': new $rdf.NamedNode('http://qudt.org/vocab/unit#Unitless'),
'rpm': new $rdf.NamedNode('http://qudt.org/vocab/unit#RevolutionPerMinute'),
's': new $rdf.NamedNode('http://qudt.org/vocab/unit#Second'),
}

/* output OWL (Lite) ontology */
var graph = new $rdf.Graph();

function isIndexed(name) {
  // name convention: if several instances, names are (1-based) indexed
  return name && name.match(/\D\d+/);
}

function stem(name) {
  // removes index from name if present
  if (name) {
    return name.match(/(\D+)\d*/)[1];
  }
  return name;
}

function addDataRestriction(subcls, prop, datatype) {
  var cls = new $rdf.BlankNode();
  graph.add(new $rdf.Triple(subcls, RDFS.subClassOf, cls));
  graph.add(new $rdf.Triple(cls, RDF.type, OWL.Restriction));
  graph.add(new $rdf.Triple(cls, OWL.onProperty, prop));
  graph.add(new $rdf.Triple(cls, OWL.allValuesFrom, datatype));
}

function addExistentialRestriction(subcls, prop, othercls) {
  var cls = new $rdf.BlankNode();
  graph.add(new $rdf.Triple(subcls, RDFS.subClassOf, cls));
  graph.add(new $rdf.Triple(cls, RDF.type, OWL.Restriction));
  graph.add(new $rdf.Triple(cls, OWL.onProperty, prop));
  graph.add(new $rdf.Triple(cls, OWL.someValuesFrom, othercls));
  // FIXME if several classes involved, should define a union
}

/* JSON objec to subclass of VehiclePart (OWL), also denoted branch in VSS */
function obj2branch(name, obj, parent) {
  name = stem(name);
  parent = stem(parent);
  var part;
  if (VSS[name]) {
    part = VSS[name];
  } else {
    part = new $rdf.NamedNode(vssns + name);
    VSS[name] = part;
    graph.add(new $rdf.Triple(part, RDFS.subClassOf, VSS.VehiclePart));
  }
  if (obj.description) {
    var desc = new $rdf.Literal(obj.description);
    graph.add(new $rdf.Triple(part, RDFS.comment, desc));
  }
  if (parent) {
    addExistentialRestriction(part, VSS.isPartOf, VSS[parent]);
  }
}

/* JSON object to subclass of Attribute or Signal (OWL) */
function obj2leaf(name, obj, branch, type) {
  if (obj.type === 'branch') {
    obj2branch(name, obj, branch);
    if (obj.children) {
      for (var child in obj.children) {
        obj2leaf(child, obj.children[child], name, type);
      }
    }
  } else {
    var attr;
    if (VSS[name] && isIndexed(branch)) {
      attr = VSS[name];
    } else if (VSS[branch + name]) {
      attr = VSS[branch + name];
    } else {
      if (VSS[name]) {
        // prepend branch name to avoid name collision
        attr = new $rdf.NamedNode(vssns + branch + name);
        VSS[branch + name] = attr;
      } else {
        attr = new $rdf.NamedNode(vssns + name);
        VSS[name] = attr;
      }
      graph.add(new $rdf.Triple(attr, RDFS.subClassOf, type));
      if (obj.description) {
        var desc = new $rdf.Literal(obj.description);
        graph.add(new $rdf.Triple(attr, RDFS.comment, desc));
      }
      var datatype = type2xsd[obj.type];
      if (datatype) {
        addDataRestriction(attr, VSS.hasValue, datatype);
      }
      if (obj.enum) {
        // TODO OWL class + individuals
      }
      var unit = unit2qudt[obj.unit]
      if (unit) {
      //console.log(obj.unit) 
      addDataRestriction(attr,QUDT.unit,unit);
      }
      
      if (obj.sensor) {
      //console.log(obj.unit) 
      var sensor = new $rdf.NamedNode(vssns + obj.sensor);
      addDataRestriction(attr,SOSA.isObservedBy,sensor);
      }
      if (type === VSS.Signal && obj.range) {
        // note: can't be expressed in OWL Lite
        // TODO OWL DL?
      }
    }
    if (branch) {
      var prop = type === VSS.Signal ? VSS.hasSignal : VSS.hasAttribute;
      branch = stem(branch);
      addExistentialRestriction(VSS[branch], prop, attr);
    }
  }
}

/* Root JSON object to meta-model/schema for VSS */
function obj2meta(obj) {
  var vssiri = vssns.substr(0, vssns.length - 1);
  graph.add(new $rdf.Triple(new $rdf.NamedNode(vssiri), RDF.type, OWL.Ontology));
  graph.add(new $rdf.Triple(VSS.VehiclePart, RDF.type, RDFS.Class));
  graph.add(new $rdf.Triple(VSS.isPartOf, RDF.type, OWL.ObjectProperty));
  //graph.add(new $rdf.Triple(VSS.isPartOf, RDF.type, OWL.FunctionalProperty));
  graph.add(new $rdf.Triple(VSS.isPartOf, RDF.type, OWL.TransitiveProperty));
  graph.add(new $rdf.Triple(VSS.hasValue, RDF.type, OWL.DatatypeProperty));
  graph.add(new $rdf.Triple(VSS.hasValue, RDF.type, OWL.FunctionalProperty));
  if (obj.Attribute) {
    var desc = new $rdf.Literal(obj.Attribute.description);
    graph.add(new $rdf.Triple(VSS.Attribute, RDF.type, RDFS.Class));
    graph.add(new $rdf.Triple(VSS.Attribute, RDFS.comment, desc));
    graph.add(new $rdf.Triple(VSS.hasAttribute, RDF.type, OWL.ObjectProperty));
  }
  if (obj.Signal) {
    var desc = new $rdf.Literal(obj.Signal.description);
    graph.add(new $rdf.Triple(VSS.Signal, RDF.type, RDFS.Class));
    graph.add(new $rdf.Triple(VSS.Signal, RDFS.comment, desc));
    graph.add(new $rdf.Triple(VSS.hasSignal, RDF.type, OWL.ObjectProperty));
  }
}

/* Vehicle Signal Specification (VSS) to RDF graph */
function vss2rdf(spec) {
  obj2meta(spec);
  if (spec.Attribute) {
    for (var attr in spec.Attribute.children) {
      obj2leaf(attr, spec.Attribute.children[attr], null, VSS.Attribute);
    }
  }
  if (spec.Signal) {
    for (var signal in spec.Signal.children) {
      obj2leaf(signal, spec.Signal.children[signal], null, VSS.Signal);
    }
  }
}

var spec = require('./vss.js');
var fs=require('fs')
vss2rdf(spec);
$n3.serialize(graph).then(function(ttl) {
  console.log(ttl);
  fs.writeFile("generatedVSS.ttl", ttl, function(err) {
    if(err) {
        return console.log(err);
    }

    console.log("The file was saved!");
}); 
}).catch(function(err) {
  console.log(err);
});
