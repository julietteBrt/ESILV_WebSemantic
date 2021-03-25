from SPARQLWrapper import SPARQLWrapper, JSON
from textwrap import dedent


def get_prefixes():
    return dedent("""
    PREFIX gtfs: <http://vocab.gtfs.org/terms#>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX schema: <http://schema.org/>
    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
    PREFIX time: <http://www.w3.org/2006/time#>
    PREFIX uom: <http://www.opengis.net/def/uom/OGC/1.0/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """)


def build_query(string):
    return get_prefixes() + dedent(string)


def query_fuseki(query):
    sparql = SPARQLWrapper('http://localhost:3030/gtfs/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def get_all_coordinates():
    query = build_query("""
    SELECT ?name ?lat ?long
    WHERE {
        ?id foaf:name ?name .
        ?id geo:long ?long .
        ?id geo:lat ?lat .
    }
    GROUP BY ?name ?lat ?long
    """)
    query_results = query_fuseki(query)['results']['bindings']
    results = []
    for row in query_results:
        name = row['name']['value']
        lat = float(row['lat']['value'])
        long = float(row['long']['value'])
        results.append({'name': name, 'lat': lat, 'long': long})
    return results

def get_all_stations():
    query = build_query("""
    SELECT ?name
    WHERE {
        ?id foaf:name ?name .
    }
    GROUP BY ?name
    """)
    query_results = query_fuseki(query)['results']['bindings']
    results = []
    for row in query_results:
        name = row['name']['value']
        results.append(name)
    return results

def get_all_routes():
    query = build_query("""
    SELECT DISTINCT ?route ?routeLongName ?lat ?long ?stopTime WHERE {
	?route a gtfs:Route .
  	OPTIONAL { ?route gtfs:shortName ?routeShortName . }
	OPTIONAL { ?route gtfs:longName ?routeLongName . }
  
  	?trip a gtfs:Trip .  
	?trip gtfs:service ?service .
	?trip gtfs:route ?route .
  	?stopTime a gtfs:StopTime . 
	?stopTime gtfs:trip ?trip . 
	?stopTime gtfs:stop ?stop . 
	
	?stop a gtfs:Stop . 
	?stop geo:lat ?lat .
   	?stop geo:long ?long .
    } GROUP BY ?route ?routeLongName ?lat ?long ?stopTime
    """)
    query_results = query_fuseki(query)['results']['bindings']
    results = []
    #print(query_results)
    for row in query_results:
        route = row['route']['value']
        lat = float(row['lat']['value'])
        long = float(row['long']['value'])
        routeLongName = row['routeLongName']['value']
        stopTime = row['stopTime']['value']
        #print(routeLongName)
        #print(stopTime)
        results.append({'route': route, 'lat': lat, 'long': long, 'routeLongName': routeLongName, 'stopTime': stopTime})
    return results

def get_stations_around_coord(lat, long):
    max_lat = lat + 0.1
    max_long = long + 0.1
    lat, long, max_lat, max_long = str(lat), str(long), str(max_lat), str(max_long)    
    query = build_query("""SELECT * WHERE {
        ?stop a gtfs:Stop .
        ?stop foaf:name ?name .
        ?stop geo:lat ?lat . 
        ?stop geo:long ?long .
        FILTER (?lat >= '%s' && ?lat <= '%s' && ?long >= '%s' && ?long <='%s') .		
    }"""%(lat, max_lat, long, max_long) # latitude et longitude sont des string donc à parser pour récup celles qui nous intéressent
    )
    #print(query)
    query_results = query_fuseki(query)['results']['bindings']
    results = []
    for row in query_results:
        name = row['name']['value']
        stop = row['stop']['value']
        lat = row['lat']['value']
        long = row['long']['value']
        results.append({'stop': stop, 'lat': lat, 'long': long, 'name': name})
    return results
