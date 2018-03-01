# -*- coding: utf-8 -*-
#import pycurl
import json
import rdflib
from flask import Flask, url_for, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os
from StringIO import StringIO
import requests, time
from requests.auth import HTTPBasicAuth
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, OWL, XSD
from rdflib.namespace import DC, FOAF, Namespace, NamespaceManager,XSD
from time import gmtime, strftime

app = Flask(__name__, template_folder="html")
GoogleMaps(app)


SERVER_URL="http://127.0.0.1:50000/_get_data"


#Definition of prefixes
rdfs=Namespace("http://www.w3.org/2000/01/rdf-schema#")
#vss=Namespace(os.path.dirname(os.path.abspath(__file__))+"/vss.ttl")
vss=Namespace("http://genivi.org/ns/vss#")
ssn=Namespace("http://www.w3.org/ns/ssn/")
sosa=Namespace("http://www.w3.org/ns/sosa/")
otime=Namespace("http://www.w3.org/2006/time#")
geo=Namespace("http://www.opengis.net/ont/geosparql#")
sf=Namespace("http://www.opengis.net/ont/sf#")
qudt11=Namespace("http://www.qudt.org/1.1/schema/qudt#")
qudtunit11=Namespace("http://www.qudt.org/1.1/vocab/unit#")
dbr=Namespace("http://www.dbpedia.org/resource/")
vso=Namespace("http://www.purl.org/vso/ns#")
owl=Namespace("http://www.w3.org/2002/07/owl#")
step=Namespace("http://www.purl.org/net/step#")

#Creation of a graph as a global variable
g = Graph()
MyCar=BNode()
MyTrajectory=BNode()
MyRawTrajectory=BNode()


class Signal(object):
    uri =""
    sensor = ""
    unit = ""
    xsd = ""

    def __init__(self,uri,sensor,unit,xsd):
        self.uri=uri
        self.sensor=sensor
        self.unit=unit
        self.xsd=xsd

def make_signal(uri,sensor,unit,xsd):
    signal = Signal(uri,sensor,unit,xsd)
    return signal

def getShortName(longName):
    return longName.split('.')[-1]

def getConfigNames(carConfig):
    nameList=[]
    for x in carConfig:
        nameList.append(getShortName(x[0]))
    return nameList

def isLinkUnique(urlList):
    return len(set(urlList))<=1

def getCarConfig():
    file=open("Configuration.csv","r")
    rawSignalList= file.read().split('\n')
    signalList=[]
    for signal in rawSignalList:
        if len(signal)>0:
            signalList.append(signal.split(','))
    return signalList

def getVSSold(l):
    gVSS = Graph()
    gVSS.parse("vssLite.ttl",format='turtle')
    output=[]
    for s in l:
        for x,_,_ in gVSS.triples((None, rdfs.subClassOf, vss.Signal)):
            if(str(vss+s)==str(x)):
                sensor = gVSS.value(x,sosa.isObservedBy,None)
                unit =  gVSS.value(x,qudt11.unit,None)
                for y in gVSS.objects(x,rdfs.subClassOf):
                    if y in gVSS.subjects(RDF.type, owl.Restriction):
                        valuesfrom = gVSS.value(y, owl.allValuesFrom)
                        output.append(make_signal(x,sensor,unit,valuesfrom))
    return output



def getVSS(l):
    gVSS = Graph()
    gVSS.parse("vssLite.ttl",format='turtle')
    #print gVSS.serialize(format='turtle')
    output=[]
    for s in l:
        for x,_,_ in gVSS.triples((None, rdfs.subClassOf, vss.Signal)):
            if(str(vss+s)==str(x)):
                #sensor = gVSS.value(x,sosa.isObservedBy,None)
                for y in gVSS.objects(x,rdfs.subClassOf):
                    if y in gVSS.subjects(RDF.type, owl.Restriction):
                        if gVSS.value(y,owl.onProperty,None)==sosa.isObservedBy:
                            sensor = gVSS.value(y, owl.allValuesFrom)
                        if gVSS.value(y,owl.onProperty,None)==qudt11.unit:
                            unit = gVSS.value(y, owl.allValuesFrom)
                        if gVSS.value(y,owl.onProperty,None)==vss.hasValue:
                            datatype = gVSS.value(y, owl.allValuesFrom)
                print sensor
                print unit
                print datatype
                output.append(make_signal(x,sensor,unit,datatype))

    return output


# Generation of a graph representing the vehicle with its attributes and existing features
@app.route('/addattributes/')
def addattributes():
    
    carConfig=getCarConfig()
    embeddedSignals=getConfigNames(carConfig)

    url=SERVER_URL

    #Binding of namespaces
    namespace_manager=NamespaceManager(Graph())
    namespace_manager.bind("rdfs",rdfs,override=False)
    #namespace_manager.bind("vss",vss,override=False)
    namespace_manager.bind("ssn",ssn,override=False)
    namespace_manager.bind("sosa",sosa,override=False)
    namespace_manager.bind("geo",geo,override=False)
    namespace_manager.bind("sf",sf,override=False)
    namespace_manager.bind("qudt-1-1",qudt11,override=False)
    namespace_manager.bind("qudt-unit-1-1",qudtunit11,override=False)
    namespace_manager.bind("dbr",dbr,override=False)
    namespace_manager.bind("vso",vso,override=False)
    namespace_manager.bind("step",step,override=False)
    namespace_manager.bind("time",otime,override=False)
    g.namespace_manager=namespace_manager

    #Creation of triples about the car
    g.add((MyCar, RDF.type, sosa.FeatureOfInterest))
    g.add((MyCar, RDF.type, vso.Automobile))
    g.add((MyCar, RDF.type, geo.Feature))

    #For every sensor provided as an input, if it is known, its is attached to a sensorType (from DBpedia), a unit and an observable property.
    for signal in getVSS(embeddedSignals):
        sensorType=signal.sensor
        unit=signal.unit
        observableProperty=signal.uri.split('#')[-1]

        Sensor=BNode()
        ObservableProperty=signal.uri
        g.add((Sensor, RDF.type, vso.FeatureValue))
        g.add((Sensor, RDF.type, sensorType))
        g.add((MyCar, vso.feature, Sensor))
        g.add((Sensor, sosa.observes, ObservableProperty))
        g.add((ObservableProperty, rdfs.label, Literal(observableProperty)))
        g.add((ObservableProperty, RDF.type, sosa.ObservableProperty))
        g.add((ObservableProperty, qudt11.Unit, unit))

    #The graph is stored
    file=open("outputFile.ttl","w")
    file.write(g.serialize(format='turtle'))
    file.close()
    #Return the graph
    #TO DO: check the missing prefixes
    return g.serialize(format='turtle') 




# Completion of an existing graph with regular observations of a  given set of sensors
@app.route('/addobservations/<int:duration>/<int:period>/<string:signalList>')
def addobservation_simulator(duration,period,signalList):
    observedSignals=signalList.split(',')
    url=SERVER_URL 
    carConfig=getCarConfig()
    embeddedSignals=getConfigNames(carConfig)

    urlList=[]
    localNames=[]
    xsdList=[]
    sensorList=[]
    signalList=[]
    shortCarConfig=[]

    for x in carConfig:
        if getShortName(x[0]) in observedSignals:
            urlList.append(x[1])
            localNames.append(x[2])
            xsdList.append(getVSS([getShortName(x[0])])[0].xsd)
            sensorList.append(g.value(None,sosa.observes,getVSS([getShortName(x[0])])[0].uri))
            signalList.append(getVSS([getShortName(x[0])])[0].uri)
            shortCarConfig.append(getShortName(x[0]))


    g.add((MyCar,RDF.type,step.Agent))
    g.add((MyCar,step.hasTrajectory,MyTrajectory))
    g.add((MyTrajectory,step.hasRawTrajectory,MyRawTrajectory))
    g.add((MyTrajectory,RDF.type,step.Trajectory))
    g.add((MyRawTrajectory,RDF.type,step.RawTrajectory))

    if isLinkUnique(urlList):
        #Loop of nmax observations
        #TO DO: improve the loop
        n=0
        nmax=duration/period
        while n<=nmax:
            #Data requested on the vehicle server
            
            r = requests.get(url)
            resp=json.loads(r.content)
            

            start_time=time.time()
            MyFix=BNode()
            g.add((MyRawTrajectory,step.hasFix,MyFix))
            g.add((MyFix,otime.Instant,Literal(str(strftime("%Y-%m-%dT%H:%M:%S", gmtime())),datatype=XSD.dateTime)))
            g.add((MyFix,sf.Point,Literal("POINT("+str(resp['latitude'])+" "+str(resp['longitude'])+")",datatype=sf.WktLiteral)))
            g.add((MyFix,RDF.type,step.Fix))
            #g.add((MyFix,sf.Point,MyPoint))
            for x in observedSignals:
                if x not in shortCarConfig:
                    return "signal "+x+ " not in the Configuration of the vehicle"
                i=observedSignals.index(x)
                Observation=BNode()
                Result=BNode()

                g.add((Observation, geo.lat, Literal(str(resp['latitude']),datatype=XSD.long)))
                g.add((Observation, geo.long, Literal(str(resp['longitude']),datatype=XSD.long)))
                g.add((Observation, sosa.hasFeatureOfInterest, MyCar))
                g.add((Observation, RDF.type, sosa.Observation))
                g.add((Observation, sosa.hasResult, Result))
                g.add((Observation, sosa.PhenomenonTime, Literal(str(strftime("%Y-%m-%dT%H:%M:%S", gmtime())),datatype=XSD.datetime)))
                g.add((Observation,rdfs.seeAlso,MyFix))
                g.add((Result, RDF.type, qudt11.QuantityValue))
                print "value"
                print resp[localNames[i]]
                g.add((Result, qudt11.numericValue, Literal(str(resp[localNames[i]]), datatype=XSD.double )))#TODO: check datatype
                g.add((Observation, sosa.madeBySensor, sensorList[i]))
                g.add((MyTrajectory,step.hasFeature,signalList[i]))
                g.add((Observation,sosa.observedProperty,signalList[i]))
                g.add((signalList[i],RDF.type,step.FeatureOfInterest))
            

            #print g.serialize(format='turtle')
            
            #Time between observations
            elapsedTime = time.time()-start_time
            time.sleep(period-elapsedTime)
            n=n+1
    else:
        #TO DO consider the case of different sources
        print "At least one link is different in the configuration file"

    # graph stored locally
    file=open("outputFile.ttl","w")
    file.write(g.serialize(format='turtle'))
    file.close()

    return g.serialize(format='turtle') 


#Generation of a reduced view for trajectory analysis
#The user gives a unique signal as input (e.g. Speed, TravelledDistance) 
#Output is a file containing a line per observation-time with the format (latitude longitude time [observations])
@app.route('/reduce/<string:signalList>')
def reduce(signalList):
    reducedSignals=signalList.split(',')
    print reducedSignals
    gReduce = Graph()
    gReduce.parse("outputFile.ttl",format='turtle')
    toWrite=''
    r=gReduce.query("""SELECT DISTINCT ?lat ?lon ?t WHERE{
        ?obs geo:lat ?lat;
            geo:long ?lon;
            sosa:PhenomenonTime ?t.
        }ORDER BY(?t) """)
    rawSignals=[None]*len(reducedSignals)
    for row in r:
        signalsToReduce=""
        print row
        
        for x in gReduce.subjects(sosa.PhenomenonTime,row[2]):
            print x
            sig= gReduce.value(x,sosa.observedProperty,None)
            print sig.split('#')[1]
            for y in gReduce.objects(x,sosa.hasResult):
                for z in gReduce.objects(y,qudt11.numericValue):
                    print z
                    print rawSignals
                    print reducedSignals
                    print sig.split('#')[1]
                    rawSignals[reducedSignals.index(sig.split('#')[1])]=z
                    #signalsToReduce=signalsToReduce+","+z
        print rawSignals
        for x in rawSignals:
            print x
            signalsToReduce=signalsToReduce+","+x
        toWrite=toWrite+"%s"%row[0]+','+"%s"%row[1]+','+"%s"%row[2]+signalsToReduce+'\n'
        
        #print float("%s"%row[2])
    '''
    for x in gReduce.subjects(rdfs.label,Literal(signal)):
        for y in gReduce.subjects(sosa.observes,x):
            for z in gReduce.subjects(sosa.madeBySensor,y):
                t=gReduce.value(z,sosa.PhenomenonTime,None)
                lat=gReduce.value(z,geo.lat,None)
                lon=gReduce.value(z,geo.long,None)
                for r in gReduce.objects(z, sosa.hasResult):
                    val = gReduce.value(r,qudt11.numericValue,None)
                    toWrite=toWrite + lat+','+lon+','+t+','+val+' \n'
                    '''
    file=open("ReducedTrajectory.csv","w")
    file.write(toWrite)
    file.close()
    return toWrite


#Write a new value in an actuator
#TO DO: improve the simulation to work with compatible names
@app.route('/write/<string:sensorName>/<string:value>')
def write_openxc(sensorName,value):
    knownSensors=['speedometer', 'tachometer', 'odometer','gear_lever_position','parking_brake_status']
    if sensorName in knownSensors:
        payload={'name':sensorName,'value':value}
        r=requests.post("http://127.0.0.1:50000/_set_data", data=payload)
        print r.text

    return g.serialize(format='turtle') 


#Example of use with annotation of type "isAccelerating" and "isDecelerating"
#TO DO: add triples with the STEP ontology

@app.route('/variation/<int:duration>/<int:period>/<string:observedSignal>/<int:offset>')
def variation_openxc(duration,period,observedSignal,offset):
    addattributes()
    #observedSignal="Angle"#"Speed"
    addobservation_simulator(duration,period,observedSignal)
    reduce(observedSignal)
    return variationSegmentmap(offset)
    #return g.serialize(format='turtle') 

@app.route('/smoothdriving/<int:duration>/<int:period>/<int:offset1>/<int:offset2>')
def smooth_openxc(duration,period,offset1,offset2):
    addattributes()
    observedSignal='Speed,Angle'
    addobservation_simulator(duration,period,observedSignal)
    reduce(observedSignal)
    return smoothSegmentmap(offset1,offset2)
    #return g.serialize(format='turtle') 

def readReducedTrajectory(numberOutput):
    file=open("ReducedTrajectory.csv","r")
    rawSignalList= file.read().split('\n')
    pointList=[]
    for point in rawSignalList:
        if len(point)>0:
            #print point
            x=point.split(',')
            if numberOutput==2:
                pointList.append((x[0],x[1]))
            elif numberOutput==3:
                pointList.append((x[0],x[1],x[2]))
            elif numberOutput==4:
                pointList.append([x[0],x[1],x[2],x[3]])

    return pointList
#print pointList

def reducedTrajectoryToTuple(numberOutput):
    file=open("ReducedTrajectory.csv","r")
    rawSignalList= file.read().split('\n')
    pointList=[]
    for point in rawSignalList:
        if len(point)>0:
            #print point
            x=point.split(',')
            currentPoint=[]
            for i in range(0,numberOutput+3):
                currentPoint.append(x[i])
            print currentPoint
            pointList.append(tuple(currentPoint))
    return pointList

def reducedTrajectoryToList(numberOutput):
    file=open("ReducedTrajectory.csv","r")
    rawSignalList= file.read().split('\n')
    pointList=[]
    for point in rawSignalList:
        if len(point)>0:
            #print point
            x=point.split(',')
            currentPoint=[]
            for i in range(0,numberOutput+3):
                currentPoint.append(x[i])
            print currentPoint
            pointList.append(currentPoint)
    return pointList

@app.route('/plotpoints')
def pointmap():
    pointList=reducedTrajectoryToTuple(0)
    print pointList
    fullmap = Map(
        identifier="fullmap",
        varname="fullmap",
        style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
        lat=42.3,
        lng=-83.2,
        markers=pointList

    )
    return render_template('example_fullmap.html', fullmap=fullmap)



#To DO: generalize the signal used as step:FeatureOfInterest 
@app.route('/variationsegments/<int:offset>')
def variationSegmentmap(offset):
    pointList=reducedTrajectoryToList(1)
    gV = Graph()
    gV.parse("outputFile.ttl",format='turtle') 
    data=[]
    segmentType=''
    currentSegmentType=''
    for i in range(0,len(pointList)-1):
        segment=[]
        if len(pointList[i+1])>0:
            x=pointList[i]
            y=pointList[i+1]
            for row in gV.subjects(otime.Instant, Literal(x[2],datatype=XSD.dateTime)): #FIX instance
                pointFix=row

            if float(x[3])-float(y[3])<-offset:
                segmentType='increasing value'
                color="#f41f1f"
            elif float(x[3])-float(y[3])>offset:
                segmentType='decreasing value'
                color="#19d238"
            else:
                segmentType='constant value'
                color="#b4d219"

            if currentSegmentType!=segmentType:
                Episode=BNode()
                gV.add((vss.Speed,step.hasEpisode,Episode))#TODONOW!
                gV.add((Episode,step.hasSemanticDescription,Literal(segmentType)))
            gV.add((Episode,step.hasExtent,pointFix))

            currentSegmentType=segmentType
            segment.append((float(x[0]),float(x[1])))
            segment.append((float(y[0]),float(y[1])))
            polySegment = {
                'stroke_color': color,
                'stroke_opacity': 1.0,
                'stroke_weight': 3,
                'path': segment
            }
            data.append(polySegment)

    plinemap = Map(
            identifier="plinemap",
            varname="plinemap",
            lat=42.3,
            lng=-83.2,
            polylines=[x for x in data],
            zoom=14,
            style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
        )
    file=open("outputFile.ttl","w")
    file.write(gV.serialize(format='turtle'))
    file.close()
    return render_template('example_polymap.html', plinemap=plinemap)


    #return g.serialize(format='turtle')




@app.route('/smoothsegments/<int:offset1>/<int:offset2>')
def smoothSegmentmap(offset1, offset2):
    pointList=reducedTrajectoryToList(2)
    gV = Graph()
    gV.parse("outputFile.ttl",format='turtle') 
    data=[]
    segmentType=''
    currentSegmentType=''
    smoothness=0

    FOI=BNode()
    for row in g.subjects(RDF.type, step.Trajectory):
        gV.add((row, step.hasFeature, FOI))
        gV.add((FOI,step.hasSemanticDescription,Literal('Driving smoothness on segments')))



    for i in range(0,len(pointList)-1):
        segment=[]
        if len(pointList[i+1])>0:
            x=pointList[i]
            y=pointList[i+1]
            for row in gV.subjects(otime.Instant, Literal(x[2],datatype=XSD.dateTime)): #FIX instance
                pointFix=row

            if abs(float(x[3])-float(y[3]))<offset1 and abs(float(x[4])-float(y[4]))<offset2:
                smoothness=smoothness+1
                segmentType='smooth'
                color="#ffffff"
            else:
                segmentType='not smooth'
                color="#000000"

            if currentSegmentType!=segmentType:
                Episode=BNode()
                gV.add((FOI,step.hasEpisode,Episode))
                gV.add((Episode,step.hasSemanticDescription,Literal(segmentType)))
            gV.add((Episode,step.hasExtent,pointFix))

            currentSegmentType=segmentType
            segment.append((float(x[0]),float(x[1])))
            segment.append((float(y[0]),float(y[1])))
            polySegment = {
                'stroke_color': color,
                'stroke_opacity': 1.0,
                'stroke_weight': 3,
                'path': segment
            }
            data.append(polySegment)

    plinemap = Map(
            identifier="plinemap",
            varname="plinemap",
            lat=42.3,
            lng=-83.2,
            polylines=[x for x in data],
            zoom=14,
            style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
        )

    smoothnessPercentage=100*float(smoothness)/float(len(pointList))
    Episode=BNode()
    SemanticDescription=BNode()
    gV.add((FOI,step.hasEpisode,Episode))
    gV.add((Episode,step.hasSemanticDescription,Literal("General smoothness")))
    gV.add((Episode,step.hasSemanticDescription, SemanticDescription))
    gV.add((SemanticDescription,step.hasValue,Literal(smoothnessPercentage,datatype=XSD.long)))
    gV.add((SemanticDescription,step.hasUnit,qudtunit11.Percent))

    file=open("outputFile2.ttl","w")
    file.write(gV.serialize(format='turtle'))
    file.close()
    return render_template('example_polymap.html', plinemap=plinemap)




@app.route('/smoothsegmentsolg/<int:offset1>/<int:offset2>')
def smoothSegmentmapolg(offset1,offset2):

    pointList=reducedTrajectoryToList(2)
    data=[]
    smoothness=0
    for i in range(0,len(pointList)-1):
        segSmooth=[]
        segOther=[]
        if len(pointList[i+1])>0:
            x=pointList[i]
            y=pointList[i+1]
            if float(x[3])-float(y[3])<offset1 and float(x[4])-float(y[4])<offset2:
                smoothness=smoothness+1
                segSmooth.append((float(x[0]),float(x[1])))
                segSmooth.append((float(y[0]),float(y[1])))
                polySmooth = {
                    'stroke_color': '#FFFFFF',
                    'stroke_opacity': 1.0,
                    'stroke_weight': 3,
                    'path': segSmooth
                }
                data.append(polySmooth)
            else:
                segOther.append((float(x[0]),float(x[1])))
                segOther.append((float(y[0]),float(y[1])))
                polyOther = {
                    'stroke_color': '#000000',
                    'stroke_opacity': 1.0,
                    'stroke_weight': 6,
                    'path': segOther
                }
                data.append(polyOther)
    smoothnessPercentage=float(smoothness)/float(len(pointList))
    FOI=BNode()
    Episode=BNode()
    SemanticDescription=BNode()
    for x in g.subjects(RDF.type, step.Trajectory):
        print x
        g.add((x, step.hasFeature, FOI))
        g.add((FOI,step.hasEpisode,Episode))
        g.add((Episode,step.hasSemanticDescription,Literal("Smoothness")))
        g.add((Episode,step.hasSemanticDescription, SemanticDescription))
        g.add((SemanticDescription,step.hasValue,Literal(smoothnessPercentage,datatype=XSD.long)))
        g.add((SemanticDescription,step.hasUnit,qudtunit11.Percent))

    print 'Smoothness: '+str(float(smoothness)/float(len(pointList)))
    file=open("outputFile.ttl","w")
    file.write(g.serialize(format='turtle'))
    file.close()
    plinemap = Map(
        identifier="plinemap",
        varname="plinemap",
        lat=42.3,
        lng=-83.2,
        polylines=[x for x in data],
        zoom=14,
        style=(
        "height:100%;"
        "width:100%;"
        "top:0;"
        "left:0;"
        "position:absolute;"
        "z-index:200;"
    ),
    )
    return render_template('example_polymap.html', plinemap=plinemap)

@app.route('/segmentsold/<int:offset>')
def segmentmapold(offset):

    file=open("ReducedTrajectory.csv","r")
    rawSignalList= file.read().split('\n')
    pointList2=[]
    data=[]
    for i in range(0,len(rawSignalList)-1):
        segAcc=[]
        segDec=[]
        segCst=[]
        if len(rawSignalList[i+1])>0:
            x=rawSignalList[i].split(',')
            y=rawSignalList[i+1].split(',')
            if float(x[3])-float(y[3])>offset:
                segDec.append((float(x[0]),float(x[1])))
                segDec.append((float(y[0]),float(y[1])))
                polyDec = {
                    'stroke_color': '#FFFFFF',
                    'stroke_opacity': 1.0,
                    'stroke_weight': 3,
                    'path': segDec
                }
                data.append(polyDec)
            elif float(x[3])-float(y[3])<-offset:
                segAcc.append((float(x[0]),float(x[1])))
                segAcc.append((float(y[0]),float(y[1])))
                polyAcc = {
                    'stroke_color': '#000000',
                    'stroke_opacity': 1.0,
                    'stroke_weight': 3,
                    'path': segAcc
                }
                data.append(polyAcc)
            else:
                segCst.append((float(x[0]),float(x[1])))
                segCst.append((float(y[0]),float(y[1])))
                polyCst = {
                    'stroke_color': '#FF0077',
                    'stroke_opacity': 1.0,
                    'stroke_weight': 3,
                    'path': segCst
                }
                data.append(polyCst)

    plinemap = Map(
        identifier="plinemap",
        varname="plinemap",
        lat=42.3,
        lng=-83.2,
        polylines=[x for x in data],
        zoom=10,
        style=(
        "height:100%;"
        "width:100%;"
        "top:0;"
        "left:0;"
        "position:absolute;"
        "z-index:200;"
    ),
    )
    return render_template('example_polymap.html', plinemap=plinemap)


if __name__ == '__main__':
    if ("SERVER_URL" in os.environ.keys()):
            SERVER_URL = os.environ["SERVER_URL"]
            print "Server url set: %s" % (SERVER_URL) 
    if ("ENDPOINT" in os.environ.keys()):
            ENDPOINT = os.environ["ENDPOINT"]
            print "Endpoint set: %s" % (ENDPOINT)
    if ("SERVER_CREDENTIALS" in os.environ.keys()):
            SERVER_CREDENTIALS = os.environ["SERVER_CREDENTIALS"]
            print "Credentials set: %s" % (SERVER_CREDENTIALS)
    app.run(host="0.0.0.0",port="5000")
