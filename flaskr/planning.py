import functools

from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import folium
from folium.plugins import MarkerCluster
from .utils import get_distance, get_bounds, find_point
bp = Blueprint('planning', __name__, url_prefix='/map')


@bp.route('/', methods=['GET', 'POST'])
def planning():

    return render_template('planning/base.html')
