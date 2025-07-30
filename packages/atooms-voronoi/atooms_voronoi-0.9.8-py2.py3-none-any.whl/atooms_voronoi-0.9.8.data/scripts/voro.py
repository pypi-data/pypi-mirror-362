#!python

import logging
import argparse
from atooms.trajectory import Trajectory, Sliced
from atooms.voronoi import TrajectoryVoronoi, VoronoiTessellation
from atooms.voronoi.api import stats
from atooms.system.particle import distinct_species

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--percentage',dest='percent', action='store_true', help='first and last in percentages (if set)')
parser.add_argument('-L', '--cellside', dest='L', type=float, default=-1.0, help='side of cell if missing')
parser.add_argument('-S', '--sigma',   dest='sigma', type=float, default=[1.0], nargs='*', help='sigmas')
parser.add_argument('-i', '--input',   dest='inp', default=None, help='input trj type')
parser.add_argument('-f', '--first',   dest='first', type=int, default=0, help='first cfg')
parser.add_argument('-l', '--last',    dest='last', type=int, default=None, help='last cfg [-1 will exclude last one]')
parser.add_argument('-s', '--skip',    dest='skip', type=int, default=1, help='interval between cfg')
parser.add_argument('-t', '--tag',     dest='tag', type=str, default='', help='tag to add before suffix')
parser.add_argument(      '--fmt',     dest='fmt', type=str, default='name,pos,signature,neighbors', help='comma-separated list of voronoi properties to dump')
parser.add_argument(      '--fields',  dest='fmt', type=str, default='name,pos,signature,neighbors', help='comma-separated list of voronoi properties to dump')
parser.add_argument('-F', '--ff',      dest='ff', type=str, default='', help='force field file')
parser.add_argument(      '--stats',   dest='stats', action='store_true', help='add stats file')
parser.add_argument(nargs='+',         dest='file',type=str, help='input files')
args = parser.parse_args()

for finp in args.file:
    sl = slice(args.first, args.last, args.skip)
    t = Sliced(Trajectory(finp, fmt=args.inp), sl)

    # Open Voronoi file for writing
    if len(args.tag) > 0:
        fout = finp + '.voronoi-%s.xyz' % args.tag
    else:
        fout = finp + '.voronoi.xyz'
    tv = TrajectoryVoronoi(fout, 'w', fields=args.fmt.split(','))

    # Loop on samples one by one and feed voro++
    for i, s in enumerate(t):
        if args.L > 0:
            s.cell.side([L, L, L])

        # Voro++ expects some radii for radical tesselletion
        if len(args.sigma) > 1:
            species = distinct_species(s.particle)
            for p in s.particle:
                p.radius = args.sigma[species.index(p.species)]/2

        # Voronoi tessellation. Throw the polyhedra back in the system
        # This can be simplified
        vt = VoronoiTessellation(s, t.filename)
        s.voronoi = vt.polyhedra
        # Finally we can dump the Voronoi trajectory in normal format
        tv.write(s, t.steps[i])

    fout = tv.filename
    tv.close()
    t.close()

    # Compute stats 
    if args.stats:
        stats(fout)
