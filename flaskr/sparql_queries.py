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
