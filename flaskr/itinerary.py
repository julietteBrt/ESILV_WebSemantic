from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from .sparql_queries import get_all_routes, get_all_coordinates, get_all_stations, get_stations_around_coord
from .utils import get_distance, interSection
import folium
from folium.plugins import MarkerCluster
from flask_wtf import FlaskForm
import numpy as np
import json

bp = Blueprint('itinerary', __name__, url_prefix='/itinerary')
routes = get_all_routes()
coordinates = get_all_coordinates()

#http://127.0.0.1:5000/itinerary/
@bp.route('/')
def upload_form():
	return render_template('itinerary/journey.html')

@bp.route('/result', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /result is accessed directly. Try going to '/http://127.0.0.1:5000/itinerary' to submit form"
    if request.method == 'POST':
        form_data = request.form
        lat_dStation = 0.0
        long_dStation = 0.0
        lat_aStation = 0.0
        long_aStation = 0.0
        dStation = form_data['dStation']
        aStation = form_data['aStation']
        #print(form_data['aStation'])
        for i in range(len(coordinates)):
            if coordinates[i]['name'].replace("_", " ") == dStation:
                lat_dStation = coordinates[i]['lat']
                long_dStation = coordinates[i]['long']
            if coordinates[i]['name'].replace("_", " ") == aStation:
                lat_aStation = coordinates[i]['lat']
                long_aStation = coordinates[i]['long']
        #print(lat_dStation)
        #print(lat_aStation)
        journeys = {'dRouteLongName': [], 'aRouteLongName': []}
        journeys1 = {'routeLongName': []}
        trips = [] 
        for i in range(len(routes)):
            if routes[i]['lat'] == lat_dStation:
                journeys['dRouteLongName'].append(routes[i]['routeLongName'].replace('_', ' '))
            if routes[i]['lat'] == lat_aStation:
                journeys['aRouteLongName'].append(routes[i]['routeLongName'].replace('_', ' '))
        journeys1['routeLongName'] = np.unique(interSection(journeys['aRouteLongName'], journeys['dRouteLongName']))
        for i in range(len(routes)):
            if routes[i]['routeLongName'].replace('_', ' ') in journeys1['routeLongName']:
                trips.append([routes[i]['routeLongName'].replace('_', ' '), routes[i]['route'], routes[i]['stopTime']])
        routeName = 'None'
        departure = 'None'
        coordinates1 = [c for c in coordinates if get_distance((c['lat'], c['long']), (lat_dStation, long_dStation)) < 100]
        #print(coordinates1)
        coordinates2 = [c for c in coordinates if get_distance((c['lat'], c['long']), (lat_aStation, long_aStation)) < 100]
        map = folium.Map(location = [lat_dStation, long_dStation], zoom_start = 5, control_scale = True)
        for c in coordinates1:
            folium.Marker([c['lat'], c['long']], popup=f'<i>{c["name"].replace("_", " ")}</i>').add_to(map)
        for c in coordinates2:
            folium.Marker([c['lat'], c['long']], popup=f'<i>{c["name"].replace("_", " ")}</i>').add_to(map)
        if(trips):
            routeName = trips[0][0]
            departure = trips[0][2]
            str2 = departure.split('/')
            stopTime = str2[5]
            departure = stopTime[-9:-4]
            return render_template('itinerary/result.html', map=map._repr_html_(), origin = dStation, destination = aStation, routeName = routeName, departure = departure)
        else:
            #print('hello')
            print(get_stations_around_coord(lat_dStation, long_dStation))
            return render_template('itinerary/substitute.html', origin = dStation, destination = aStation, routeName = routeName, departure = departure)


@bp.route('/search', methods=['POST'])
def search():
    term = request.form['q']
    #print ('term: ', term)

    stations = get_all_stations()
    stations = [s.replace('_' , ' ') for s in stations]
    #print(stations[0])

    filtered_dict = [v for v in stations if term in v]
    #print(filtered_dict)

    resp = jsonify(filtered_dict)
    resp.status_code = 200
    return resp


#http://127.0.0.1:5000/planning/coverage/48.864902612482986/2.3429293408796634/10000
"""@bp.route('/coverage/<float:lat>/<float:long>/<int:radius>', methods = ['GET'])
def planning(lat, long, radius):
    routes = get_all_routes()
    origin_coord = [lat, long]
    coordinates = get_all_coordinates()
    coordinates = [c for c in coordinates if get_distance((c['lat'], c['long']), (lat, long)) < radius]
    map = folium.Map(location=origin_coord, zoom_start=1, control_scale=True)
    for c in coordinates:
        folium.Marker([c['lat'], c['long']], popup=f'<i>{c["name"].replace("_", " ")}</i>').add_to(map)
    #return render_template('map/sncf-stops.html', map=map._repr_html_())
    return render_template('planning/planning.html', map=map._repr_html_(), routes = routes)
"""