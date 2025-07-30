#!python

"""Post processing script for Voronoi data."""

import argh
from atooms.voronoi.api import fraction, stats, clusters, spindles, gr, sphericity, lifetime, domains

argh.dispatch_commands([fraction, stats, clusters, spindles, gr, sphericity, lifetime, domains])
