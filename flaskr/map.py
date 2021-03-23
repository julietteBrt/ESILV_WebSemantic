import functools

from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import folium
from folium.plugins import MarkerCluster
from .sparql_queries import get_all_coordinates
from .utils import get_distance
bp = Blueprint('map', __name__, url_prefix='/map')


@bp.route('/sncf-stops/<float:lat>/<float:long>/<int:radius>', methods=['GET'])
def map(lat, long, radius):
    origin_coord = [lat, long]
    coordinates = get_all_coordinates()
    coordinates = [c for c in coordinates if get_distance((c['lat'], c['long']), (lat, long)) < radius]
    map = folium.Map(location=origin_coord, zoom_start=1, control_scale=True)
    for c in coordinates:
        folium.Marker([c['lat'], c['long']], popup=f'<i>{c["name"].replace("_", " ")}</i>').add_to(map)
    return render_template('map/sncf-stops.html', map=map._repr_html_())
