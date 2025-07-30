from __future__ import print_function
import sys
import csv
import logging
from collections import defaultdict

from .voronoi import TrajectoryVoronoi
from .helpers import top_signature, fraction_with_signature, domain_with_signature, int_to_sign, sign_to_int
from .helpers import _dump as dump
from .core import __version__


__all__ = ['fraction', 'stats', 'clusters', 'spindles', 'gr',
           'sphericity', 'lifetime', 'domains']


def _set_output(fileinp, stdout, suffix):
    if stdout:
        fileout = '/dev/stdout'
    else:
        fileout = fileinp + '.' + suffix
    return fileout


def _neighbors_from_voronoi(s, match):
    """Return a list of list of neighbors matching a condition on the central voronoi cell"""
    neigh = []
    for v in s.voronoi:
        if match(v):
            neigh.append([v.central] + list(v.neighbors))
    return neigh


def _easy_stats(fileinp, comment='# ', ignore=[]):
    # TODO: move to general utils
    import numpy
    # Get column names
    columns = []
    with open(fileinp) as fh:
        for line in fh:
            if 'columns' in line:
                columns = line.split(':')[1].split(',')
                break
    if len(columns) == 0:
        raise ValueError('cannot find columns')
    # Get data
    # TODO: handles a single row
    data = numpy.loadtxt(fileinp, unpack=True, ndmin=1)
    # data = numpy.genfromtxt('data.txt', delimiter=',', dtype=None, unpack=True)
    # Produce stats summary
    txt = comment + "nsamples = %d\n" % (len(data[0]))
    for x, name in zip(data, [c.strip() for c in columns]):
        if name not in ignore:
            txt += comment + "average %s = %g\n" % (name, x.mean())
    for x, name in zip(data, [c.strip() for c in columns]):
        if name not in ignore:
            txt += comment + "variance %s = %g\n" % (name, x.var())
    for x, name in zip(data, [c.strip() for c in columns]):
        if name not in ignore:
            txt += comment + "std %s = %g\n" % (name, x.std())
    return txt


def _stats(fileinp):
    """Statistics of Voronoi polyhedra."""
    stats = defaultdict(int)
    with TrajectoryVoronoi(fileinp) as th:
        for s in th:
            for v in s.voronoi:
                stats[v.signature] += 1
    keys = sorted(stats, key=stats.get, reverse=True)
    return keys, stats


def stats(fileinp, stdout=False, at_most=20):
    """Statistics of most frequent Voronoi polyhedra."""
    keys, db = _stats(fileinp)
    fileout = _set_output(fileinp, stdout, 'stats')
    with open(fileout, 'w') as fh:
        fh.write('# title: fraction of most frequent Voronoi signatures\n')
        fh.write('# columns: signature, fraction\n')
        for x in keys[:at_most]:
            fh.write('%s %s\n' % (int_to_sign(x), float(db[x])/sum(db.values())))


def fraction(stdout=False, at_most=10, include=None, only=None, *files):
    """
    Fraction of most frequent polyhedra as a function of time and
    domains formed by central and connected particles of top Voronoi
    signatures.
    """
    for fileinp in files:
        with TrajectoryVoronoi(fileinp) as th:
            if only is not None:
                sel = [sign_to_int(signature) for signature in only.strip(',').split(',')]
            else:
                top_1 = set(top_signature(th[0].voronoi, at_most))
                top_2 = set(top_signature(th[int(len(th)/2)].voronoi, at_most))
                top_3 = set(top_signature(th[-1].voronoi, at_most))
                top = list(sorted(top_1 & top_2 & top_2))
                if include is not None:
                    # Make sure additional tracked signatures are there
                    inc = [sign_to_int(signature) for signature in include.split(',')]
                    sel = sorted(set(top + inc))
                else:
                    sel = top

            fileout_fraction = _set_output(fileinp, stdout, 'fraction')
            fileout_domains = _set_output(fileinp, stdout, 'domain')

            # with open(fileout_log, 'w') as fh:
            #    for i, signature in enumerate(sel):
            #        fh.write('%d %s\n' % (i+1, signature))

            with open(fileout_fraction, 'w') as fh_fraction, \
                    open(fileout_domains, 'w') as fh_domains:
                sel_str = [int_to_sign(signature) for signature in sel]
                fh_fraction.write(dump('fraction of most frequent Voronoi signatures',
                                       columns=['step'] + sel_str,
                                       version=__version__,
                                       command='voropp.py fraction', parents=fileinp))
                fh_domains.write(dump('domain size of most frequent Voronoi signatures',
                                      columns=['step'] + sel_str,
                                      version=__version__,
                                      command='voropp.py fraction', parents=fileinp))
                for i, s in enumerate(th):
                    # Fractions
                    out = ' '.join([str(fraction_with_signature(s.voronoi, signature))
                                    for signature in sel])
                    fh_fraction.write('%d %s\n' % (th.steps[i], out))
                    # Domains
                    out = ' '.join([str(domain_with_signature(s.voronoi, signature))
                                    for signature in sel])
                    fh_domains.write('%d %s\n' % (th.steps[i], out))

            # Append stats at the end of the file
            with open(fileout_fraction, 'a') as fh_fraction, \
                    open(fileout_domains, 'a') as fh_domains:
                fh_fraction.write(_easy_stats(fileout_fraction, ignore=['step']))
                fh_domains.write(_easy_stats(fileout_domains, ignore=['step']))


def clusters(signature, fileinp, conc=None, stdout=False, bin_width=10):
    """
    Statistics of clusters of connected Voronoi polyhedra.

    `signature` must be in the form l_n_m ... where l, n, m, ... are integers.
    """
    import numpy
    import random
    from pyutils.histogram import Histogram
    from .helpers import cluster_analysis
    from .voronoi import sign_to_int

    fout = fileinp + '.cluster-%s' % signature
    if conc is not None:
        fout = map(lambda x: x + '-' + conc, fout)

    hist = Histogram(bin_width=bin_width)
    hist_rand = Histogram(bin_width=bin_width)
    with TrajectoryVoronoi(fileinp) as t:
        keys = ['step', 'largest cluster size', 'cluster size',
                'fraction of non-clusters', 'gyration radius']
        data = []
        for i, s in enumerate(t):
            def _f(hist, sample):
                nn = []
                for v in sample:
                    nn.append([v.central] + [j for j in v.neighbors if s.voronoi[j] in sample])
                clusters = cluster_analysis(nn)
                if len(clusters.clusters[0]) > 0:
                    hist.add([float(len(ci)) for ci in clusters])
                return clusters, hist

            # LFS clusters
            sample = [v for v in s.voronoi if v.signature == sign_to_int(signature)]
            clusters, hist = _f(hist, sample)
            clusters_size = [len(ci) for ci in clusters]

            # Clusters gyration radius
            from atooms.system.particle import gyration_radius
            rg = []
            for cluster in clusters:
                particles = [s.particle[j] for j in cluster]
                rg_n1 = gyration_radius(particles, s.cell, method='N1')
                # rg_n2 = gyration_radius(particles, s.cell, method='N2')
                rg.append(rg_n1)

            # Random sample of particles (same number of LFS)
            randsample = random.sample(s.voronoi, len(sample))
            randclusters, hist_rand = _f(hist_rand, randsample)
            data.append((t.steps[i], max(clusters_size),
                         numpy.average(clusters_size),
                         clusters_size.count(1)/float(sum(clusters_size)),
                         numpy.average(rg)))

    # Write results
    with open(fout, 'w') as fh:
        fh.write(dump('backbone clusters formed by %s voronoi signatures' %
                      signature, columns=keys,
                      version=__version__,
                      command='voropp.py', parents=fileinp))
        csv_writer = csv.writer(fh, delimiter=' ', lineterminator='\n')
        csv_writer.writerows(data)

    # Append stats at the end of the file
    with open(fout, 'a') as fh:
        fh.write(_easy_stats(fout, ignore=['step']))

    # Histogram of cluster size
    with open(fout + '.histogram', 'w') as fh:
        fh.write(dump('histogram of backbone cluster sizes from %s voronoi signatures' %
                      signature, columns=['cluster size', 'probability'],
                      version=__version__,
                      command='voropp.py', parents=[fileinp, fout]))
        fh.write(hist.stats)
        fh.write(str(hist))

    # # Histogram of randomized clusters
    fout = fileinp + '.cluster-%s-random.histogram' % signature
    with open(fout, 'w') as fh:
        fh.write(dump('histogram of randomized backbone cluster sizes from %s voronoi signatures' %
                      signature, columns=['cluster size', 'probability'],
                      version=__version__,
                      command='voropp.py', parents=[fileinp, fout]))
        fh.write(hist_rand.stats)
        fh.write(str(hist_rand))


def domains(signature, fileinp, conc=None, stdout=False, bin_width=10):
    """
    Statistics of domains of Voronoi polyhedra.

    `signature` must be in the form l_n_m ... where l, n, m, ... are integers.
    """
    import numpy
    import random
    from pyutils.histogram import Histogram
    from .helpers import cluster_analysis
    from .voronoi import sign_to_int

    fout = fileinp + '.domains-%s' % signature
    if conc is not None:
        fout = map(lambda x: x + '-' + conc, fout)

    hist = Histogram(bin_width=bin_width)
    hist_rand = Histogram(bin_width=bin_width)
    with TrajectoryVoronoi(fileinp) as t:
        keys = ['step', 'largest domain size', 'domain size',
                'domain gyration radius']
        data = []
        import progressbar
        bar = progressbar.ProgressBar(widgets=[  # '[', progressbar.Timer(), '] ',
            ' ', progressbar.AnimatedMarker(), progressbar.Percentage(),
            ' (', progressbar.AdaptiveETA(), ')'])
        for i, s in bar(enumerate(t), len(t)):
            # TODO: refactor. This is the difference wrt cluster
            def _f(hist, sample):
                nn = []
                for v in sample:
                    nn.append([v.central] + [j for j in v.neighbors])
                clusters = cluster_analysis(nn)
                if len(clusters[0]) > 0:
                    hist.add([float(len(ci)) for ci in clusters])
                return clusters, hist

            # LFS domains
            sample = [v for v in s.voronoi if v.signature == sign_to_int(signature)]
            continue
            clusters, hist = _f(hist, sample)
            clusters_size = [len(ci) for ci in clusters]

            # Clusters gyration radius
            from atooms.system.particle import gyration_radius
            rg = []
            for cluster in clusters:
                particles = [s.particle[j] for j in cluster]
                rg_n1 = gyration_radius(particles, s.cell, method='N1')
                # rg_n2 = gyration_radius(particles, s.cell, method='N2')
                rg.append(rg_n1)

            # # Random sample of particles (same number of LFS)
            # randsample = random.sample(s.voronoi, len(sample))
            # randclusters, hist_rand = _f(hist_rand, randsample)
            data.append((t.steps[i], max(clusters_size),
                         numpy.average(clusters_size),
                         numpy.average(rg)))

    # Write results
    with open(fout, 'w') as fh:
        fh.write(dump('domains formed by %s voronoi signatures' %
                      signature, columns=keys,
                      version=__version__,
                      command='voropp.py', parents=fileinp))
        csv_writer = csv.writer(fh, delimiter=' ', lineterminator='\n')
        csv_writer.writerows(data)

    # Append stats at the end of the file
    with open(fout, 'a') as fh:
        fh.write(_easy_stats(fout, ignore=['step']))

    # Histogram of cluster size
    with open(fout + '.histogram', 'w') as fh:
        fh.write(dump('histogram of domain sizes from %s voronoi signatures' %
                      signature, columns=['domain size', 'probability'],
                      version=__version__,
                      command='voropp.py', parents=[fileinp, fout]))
        fh.write(hist.stats)
        fh.write(str(hist))


def spindles(fileinp, stdout=False):
    """Compute spindles statistics."""
    from .helpers import spindles, spindles_defect
    fout = fileinp + '.spindles'
    hist = {i: 0 for i in range(3, 14)}
    with TrajectoryVoronoi(fileinp) as t:
        with open(fout, 'w') as fh:
            fh.write('# columns: step, spindles defect concentration\n')
            for i, s in enumerate(t):
                hist = spindles(s, hist)
                fh.write('%d %s' % (t.steps[i],
                                    spindles_defect(s)))
    # do_stats(fout)
    fout = fileinp + '.spindles.histogram'
    with open(fout, 'w') as fh:
        fh.write('# columns: spindle, average\n')
        for key in hist:
            fh.write('%s %s\n' % (key, hist[key]))


def gr(input_file, signature=None):
    import postprocessing
    from .helpers import filter_voronoi_signature
    from .voronoi import sign_to_int
    with TrajectoryVoronoi(input_file) as th:
        th._grandcanonical = True
        th.register_callback(filter_voronoi_signature, sign_to_int(signature))
        cf = postprocessing.Partial(postprocessing.RadialDistributionFunction, [signature, None], th)
        cf.do()


def sphericity(fileinp, stdout=False):
    """Sphericity of Voronoi polyhedra."""
    from .helpers import sphericity
    if stdout:
        fh = sys.stdout
    else:
        fh = open(fileinp + '.sphericity.xyz', 'w')

    with TrajectoryVoronoi(fileinp) as th:
        for i, s in enumerate(th):
            step = th.steps[i]
            fh.write('%s\n' % len(s.particle))
            fh.write('step:%d columns:%s\n' % (step, 'signature,sphericity_std,sphericity_ratio,sphericity_ave'))
            print(dump('sphericity', columns=['signature',
                                              'sphericity_std',
                                              'sphericity_ratio',
                                              'sphericity_ave'],
                       version=__version__,
                       command='voropp.py',
                       parents=fileinp,
                       inline=True,
                       comment='',
                       extra_fields=[('step', step)]))
            for v in s.voronoi:
                out = sphericity(s, v)
                fh.write('%s %g %g %g\n' % (int_to_sign(v.signature), out[1], out[2], out[0]))
    fh.close()


def lifetime(fileinp, stdout=False, signature=None, top=10, fmt=None, exclude=None):
    """Lifetime of Voronoi polyhedra."""
    import numpy
    from pyutils.histogram import Histogram
    from .helpers import sign_to_int
    from .helpers import lifetime as life_time

    if signature is None:
        signature = [int_to_sign(x) for x in _stats(fileinp)[0][:top]]
        if None in signature:
            raise ValueError('No signatures found in voronoi file')
    else:
        signature = signature.split(',')

    if stdout:
        fh = sys.stdout
    else:
        fh = open(fileinp + '.lifetime', 'w')

    def f_match(p0, p):
        if p0.signature == p.signature and \
           sorted(p0.neighbors) == sorted(p.neighbors):
            return True
        else:
            return False

    with TrajectoryVoronoi(fileinp) as th:
        if fmt is not None:
            th.fmt = fmt.split(',')  # ['name', 'pos', 'signature', 'neighbors*']
        npart = len(th[0].particle)
        particle = th[0].particle

        # Put data into a big list
        from collections import namedtuple
        Voro = namedtuple('Voro', ['signature', 'neighbors'])
        voronoi_list = []
        for j in range(npart):
            voronoi_list.append([])
        for _, s in enumerate(th):
            for i in range(npart):
                voronoi_list[i].append(Voro(s.voronoi[i].signature,
                                            s.voronoi[i].neighbors))
        # Compute life time
        fh.write('# lifetime calculation of top %s voronoi signatures\n' % top)
        fh.write('# columns: lifetime, start_frame, end_frame, particle, signature\n')
        stats_data = {}
        for focused_signature in signature:
            times = []
            for i in range(npart):
                if exclude is not None:
                    if particle[i].name == exclude:
                        continue
                dt, deltas = life_time(voronoi_list[i], steps=th.steps, identity_fct=f_match, return_intervals=True,
                                       mask=[v.signature == sign_to_int(focused_signature) for v in voronoi_list[i]])
                times += dt
                for x, y in zip(dt, deltas):
                    fh.write('%s %s %s %s %s\n' % (x, y[0], y[1], i, focused_signature))
            stats_data[focused_signature] = (numpy.mean(times), numpy.std(times))
        for focus in signature:
            fh.write('# mean lifetime %s = %s\n' % (focus, stats_data[focus][0]))
        # for focus in stats_data:
        #     fh.write('# std lifetime %s = %s\n' % (focus, stats_data[focus][1]))
