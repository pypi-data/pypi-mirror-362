from __future__ import print_function
import os
import numpy
import tempfile
import subprocess

from atooms.trajectory import TrajectoryXYZ
from atooms.trajectory.base import TrajectoryBase
from atooms.system.particle import Particle, composition
from atooms.system import System
from atooms.core.utils import rmd

from .helpers import sign_to_int, int_to_sign


def _update_signature(particle, data, meta):
    particle.signature = sign_to_int(data[0])
    return data[1:]


def _update_neighbors(particle, data, meta):
    particle.neighbors = [int(i) for i in data[0].split(',')]
    return data[1:]


def _update_neighbors_star(particle, data, meta):
    if data:
        particle.neighbors = [int(i) for i in data[0:]]
    return None


class VoronoiPolyhedron:

    def __init__(self, signature, central, composition=None, neighbors=None, distance=None, volume=None):
        self.central = central
        # Make sure they are tuples (mutable can't be dict keys)
        self.signature = tuple(signature)
        self.neighbors = neighbors
        self.distance = distance
        self.volume = volume
        if composition:
            self.composition = tuple(composition)
            # Check that that composition includes the central particle
            if sum(self.composition.values()) != len(self.neighbors)+1:
                raise ValueError('Something wrong with neighbors and or composition')


class VoronoiTessellation:

    def __init__(self, system, fout):
        # Internal conversion to voro++ input format
        tmp = tempfile.mkdtemp()
        fvpp = os.path.join(tmp, os.path.basename(fout) + '.inp')
        fmt = '%i, %q, %A, %v, %f, %n'
        with TrajectoryVoroPP(fvpp, 'w', fmt=fmt) as tvpp:
            tvpp.write(system, 0)

        # Setup voro++ command line options
        if system.cell is None:
            periodic = ''
            box = ''
            for axis in range(system.number_of_dimensions):
                r_min = 1.001 * numpy.min([p.position[axis] for p in system.particle])
                r_max = 1.001 * numpy.max([p.position[axis] for p in system.particle])
                box += '{} {} '.format(r_min, r_max)
        else:
            periodic = '-p'
            box = ''
            for L in system.cell.side:
                box += '%g %g ' % (-L/2, L/2)

        # Execute voro++
        cmd = f'voro++ -c "{fmt}" -r {periodic} -l 1 -o {box} {fvpp}'
        subprocess.check_call(cmd, shell=True)
        # Transform custom v++ output file into voronoi file with neighbors
        fvpp = os.path.join(tmp, os.path.basename(fout) + '.inp.vol')
        with TrajectoryVoroPP(fvpp, fmt=fmt) as tvpp:
            tvpp.steps.append(0)
            self.polyhedra = tvpp[0].voronoi
        rmd(tmp)


class TrajectoryVoronoi(TrajectoryXYZ):

    # TrajectoryVoronoi assumes neighbors are indexed using Fortran convention
    # However, internally it will convert to C indexing. Experience shows that
    # keeping a double convention in python code is a nightmare.

    def __init__(self, filename, mode='r', fields=None):
        super(TrajectoryVoronoi, self).__init__(filename, mode, fields=fields)
        # TODO: fmt should be read from comment line if possible when mode=r
        # Fix parsing of other fields.
        if mode == 'w':
            if fields is None:
                self.fields = ['species', 'position', 'signature', 'neighbors']
        self._offset = 1
        self.callback_read['signature'] = _update_signature
        self.callback_read['neighbors'] = _update_neighbors
        self.callback_read['neighbors*'] = _update_neighbors_star

    def read_system(self, frame):
        """Store Voronoi polyhedra directly in system object to adhere with Trajectory interface"""
        # Note: neighbors start indexing from 1. We should offset that when exposing neighbors to atooms
        _super = super(TrajectoryVoronoi, self)
        system = _super.read_system(frame)

        # Make sure we read radii if they are present
        # TODO: this should be done in xyz
        # TODO: all this should be recoded in terms of read callback! :-(
        # TODO: fix reading of radii 20.01.2017
        # for i, p in enumerate(s.particle):
        #     try:
        #         p.radius = float(self._sampledata[i]['radius'])
        #     except:
        #         pass

        # Store voronoi data in a voronoi list
        system.voronoi = []
        for ipart, p in enumerate(system.particle):
            # TODO: what if we put voronoi objects inside particles?
            vi = VoronoiPolyhedron([None], ipart)
            if hasattr(p, 'signature'):
                vi.signature = p.signature
            if hasattr(p, 'faces'):
                vi.faces = [float(x) for x in p.faces.split(',')]
            if hasattr(p, 'volume'):
                vi.volume = float(p.volume)
            if hasattr(p, 'neighbors'):
                # At this stage, neighbors have Fortran indexing
                p.neighbors = [ni-1 for ni in p.neighbors]
                vi.neighbors = p.neighbors
                db = composition([p] + [system.particle[n-1] for n in vi.neighbors])
                vi.composition = tuple([db[x] for x in sorted(db)])
            else:
                vi.neighbors = []
                vi.composition = None
            system.voronoi.append(vi)
        return system

    def read_sample(self, frame):
        self.read_system(frame)

    def write_system(self, system, step):
        # We expect system to contain Voronoi polyhedra
        # This way we reuse write() logic from base class.
        # TODO: what if we put voronoi objects inside particles?
        self._cell = system.cell
        ndim = len(system.particle[0].position)
        n = len(system.particle)
        self._file.write("%8i\n" % len(system.particle))
        self._file.write(self._comment(step, system) + '\n')
        for i, p in enumerate(system.particle):
            # TODO: refactor with xyz patterns
            data = ""
            for fmt_entry in self.fields:
                if fmt_entry in ['name', 'species', 'id', 'particle.species']:
                    data += " " + p.species.strip()
                if fmt_entry in ['pos', 'position', 'particle.position', 'x']:  # we ignore y and z
                    data += " " + " ".join(["%.6f" % x for x in p.position])
                if fmt_entry == 'signature':
                    data += " " + int_to_sign(system.voronoi[i].signature)
                if fmt_entry == 'volume':
                    data += " %g" % system.voronoi[i].volume
                if fmt_entry == 'radius':
                    data += " %g" % p.radius
                if fmt_entry == 'neighbors*':
                    data += " " + int_to_sign(map(lambda x: x+1, system.voronoi[i].neighbors), " ")
                if fmt_entry == 'neighbors':
                    data += " " + ','.join([str(x+1) for x in system.voronoi[i].neighbors])
                if fmt_entry == 'faces':
                    data += " " + ','.join([str(x) for x in system.voronoi[i].faces])
            data += "\n"
            self._file.write(data)

    def write_sample(self, system, step):
        self.write_system(system, step)

class TrajectoryVoroPP(TrajectoryBase):

    # TODO: check that voro++ starts indexing from 1

    """Voro++ file format"""

    suffix = '.v++'

    def __init__(self, filename, mode='r', fmt='%i, %q, %A, %v, %n'):
        TrajectoryBase.__init__(self, filename, mode)
        self.fmt = fmt

    def write_sample(self, system, step):
        ndim = len(system.particle[0].position)
        n = len(system.particle)
        with open(self.filename, 'w') as fh:
            for i, p in enumerate(system.particle):
                fmt = "%d" + ndim*" %.6f" + " %g\n"
                fh.write(fmt % tuple([i+1] + list(p.position) + [p.radius]))

    def read_sample(self, sample):
        # Does not adhere to trj interface
        # Note: sample is ignored
        p = []
        v = []
        # This must match the one used to write of course
        fmt = [x.strip() for x in self.fmt.split(',')]
        with open(self.filename, 'r') as fh:
            for central, line in enumerate(fh):
                for i, data in enumerate(line.split(',')):
                    if fmt[i] == '%q':
                        pi = Particle(position=map(float, data.split()))
                    elif fmt[i] == '%A':
                        vi = VoronoiPolyhedron(map(int, data.split()[3:]), central)
                    elif fmt[i] == '%n':
                        vi.neighbors = map(int, data.split())
                        vi.neighbors = [i-1 for i in vi.neighbors]
                    elif fmt[i] == '%f':
                        vi.faces = map(float, data.split())
                    elif fmt[i] == '%v':
                        vi.volume = float(data)
                v.append(vi)
        # Voro++ does not provide cell nor species info
        # This should be added by the caller.
        s = System()
        s.voronoi = v
        return s


class FilterVoronoi:

    """ Decorate a trajectory by filtering according to selected polyhedra """

    def __new__(cls, component, lps):
        cls = type('FilterVoronoi', (FilterVoronoi, component.__class__), component.__dict__)
        return object.__new__(cls)

    def __init__(self, component, lps):
        self._grandcanonical = True  # for sure this is going to be GC
        self.lps = tuple(lps)  # make sure it's a tuple

    def read_sample(self, sample):
        self.read_sample(sample)
        
    def read_system(self, sample):
        _super = super(FilterVoronoi, self)
        s = _super.read_system(sample)
        # Select only particles that belong to LPS domains
        p_lps = []
        for i, v in enumerate(s.voronoi):
            if v.signature == self.lps:
                p_lps.append(s.particle[i])
                for j in v.neighbors:
                    if not s.particle[j] in p_lps:
                        p_lps.append(s.particle[i])

        s.particle = p_lps
        return s
