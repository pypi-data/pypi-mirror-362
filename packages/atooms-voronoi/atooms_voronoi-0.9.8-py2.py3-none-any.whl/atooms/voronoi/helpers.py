from collections import defaultdict


def sign_to_int(sign, glue='_'):
    """ Return a tuple of integer representation of a str signature """
    if sign:
        return tuple(map(int, sign.split(glue)))


def int_to_sign(sign, glue="_"):
    """ Return a string representation of an integer signature """
    return glue.join(['%s' % s for s in sign])


def top_signature(vor, maximum=10):
    stats = defaultdict(int)
    for v in vor:
        stats[v.signature] += 1
    skeys = sorted(stats, key=stats.get, reverse=True)
    return skeys[0:maximum]


def indices(v, lps):
    return [i for i, vi in enumerate(v) if vi.signature == lps]


def fraction_with_signature(voronoi, signature):
    """Returns the fraction of given signature of an input system s"""
    return len(indices(voronoi, signature)) / float(len(voronoi))


def fraction_with_composition(voronoi, signature, x=None):
    """Returns the fraction of given signature of an input system s"""
    cnt = 0
    for v in voronoi:
        if v.signature == signature and v.composition == tuple(x):
            cnt += 1
    return cnt / float(len(voronoi))


def spindles(s, hist=None, qmax=14):
    """Spindle statistics"""
    if hist is None:
        # Alternatively use a defaultdict, but this will lead to fluctuating keys
        hist = {q: 0 for q in range(3, qmax)}
    for vi in s.voronoi:
        for nv, nf in enumerate(vi.signature):
            nv += 3
            if nv in hist:
                hist[nv] += nf
            else:
                print('Warning: skipped 1 spindle')
    norm = float(sum(hist.values()))
    for x in hist:
        hist[x] /= norm
    return hist


def spindles_defect(s):
    """See PRL 108, 035701 (2012)."""
    hist = spindles(s)
    c_def = 0
    for q in hist:
        c_def += hist[q] * (q-5)**2
    return c_def


def domain_with_signature(voronoi, signature):
    """Compute fraction of particles in domains formed by a given Voronoi signature."""
    domain = [0] * len(voronoi)
    for i, v in enumerate(voronoi):
        if v.signature == signature:
            domain[i] = 1
            for n in v.neighbors:
                domain[n] = 1
    return float(sum(domain)) / len(voronoi)


def filter_voronoi_signature(system, signature):
    """Callback to change particle identity according to Voronoi signature."""
    from .voronoi import int_to_sign
    for p, v in zip(system.particle, system.voronoi):
        if v.signature == signature:
            p.id = 1
            p.name = int_to_sign(signature)
        else:
            p.id = 2
            p.name = 'O'
    return system


def sphericity(system, voronoi):
    import numpy
    distance = []
    p0 = system.particle[voronoi.central]
    for i in voronoi.neighbors:
        pi = system.particle[i]
        dr = p0.distance(pi, system.cell)
        distance.append(sum(dr*dr)**0.5)
    ave = numpy.average(numpy.array(distance))
    std = numpy.std(numpy.array(distance))
    delta = max(distance) - min(distance)
    return ave, std / ave, delta / ave


def lifetime(data, times=None, mask=None, identity_fct=None,
             steps=None, attribute_fct=None, return_intervals=False):
    """
    Measure largest time for which two clusters (lists) are equal and
    have the same tag (optional function).
    """
    import copy
    if steps is None:
        steps = data.steps
    if times is None:
        times = []
    if return_intervals:
        deltas = []
    if identity_fct is None:
        def identity_fct(p, p0):
            return p == p0
    if attribute_fct is None:
        def attribute_fct(data, i):
            return data[i]
    if mask is not None:
        if len(data) != len(mask):
            raise ValueError('mask length must match input')

    i_next = 0  # starting frame
    while True:
        dt = None
        # We start search from this frame
        i0 = i_next
        p0 = None
        for i in range(i0, len(steps)):
            # print i, p0
            # Look for the starting (matching) frame
            if p0 is None:
                if mask is not None:
                    # If a logical mask is provided we check that it matches
                    # and we continue to do so until a match is found.
                    if mask[i]:
                        i_first = copy.copy(i)
                        p0 = attribute_fct(data, i)
                    else:
                        continue
                else:
                    # Otherwise we start to compare instances of data
                    # to this guy
                    p0 = attribute_fct(data, i0)
                    i_first = copy.copy(i)

            # Determine the lifetime
            p = attribute_fct(data, i)
            if identity_fct(p, p0):
                dt = (steps[i], steps[i_first])
                i_next = i + 1

        # We only append a lifetime is condition is matched at some
        # frame.
        if dt is not None:
            if return_intervals:
                deltas.append(dt)
            times.append(dt[0] - dt[1])
            if i_next >= len(steps):
                break
        else:
            break

    if return_intervals:
        return times, deltas
    else:
        return times


# Add dump() from medepy for portability.
# This should be dropped in the future.
def _dump(title, columns=None, command=None, version=None,
          description=None, note=None, parents=None, inline=False,
          comment='# ', extra_fields=None):
    """
    Return a string of comments filled with metadata.
    """
    import datetime
    import os
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if columns is not None:
        columns_string = ', '.join(columns)

    try:
        author = os.getlogin()
    except OSError:
        author = None

    # Checksums of parent files
    # Make sure parents is list
    # Disable parents because we have issues with directories
    if parents:
        parents = None
        checksums = []
    if parents is not None and not hasattr(parents, '__iter__'):
        parents = [parents]
    if parents is not None and len([os.path.isfile(f) for f in parents]) > 0:
        # Compute checksum
        checksums = []
        size_limit = 1e9
        if max([os.path.getsize(f) for f in parents]) < size_limit:
            for parentpath in parents:
                try:
                    import md5
                    tag = md5.md5(open(parentpath).read()).hexdigest()
                except ImportError:
                    tag = ''
                checksums.append(tag)
            checksums = ', '.join(checksums)
        else:
            checksums = None
        # Convert to string
        parents = ', '.join([os.path.basename(p) for p in parents])

    metadata = [('title', title),
                ('columns', columns_string),
                ('date', date),
                ('author', author),
                ('command', command),
                ('version', version),
                ('parents', parents),
                ('checksums', checksums),
                ('description', description),
                ('note', note)]

    if extra_fields is not None:
        metadata += extra_fields

    if inline:
        fmt = '{}: {};'
        txt = comment + ' '.join([fmt.format(key, value) for key,
                                  value in metadata if value is not None])
    else:
        txt = ''
        for key, value in metadata:
            if value is not None:
                txt += comment + '{}: {}\n'.format(key, value)
    return txt


def cluster_analysis(neighbors):
    """
    Compute clusters based on neighbors. `neighbors` is a list of lists of neighbors.

    Return: the `clusters` as a list of sets of clusters
    """
    # TODO: what if we have missing items? Do we expect a list with empty neighbor list?
    clusters = []
    my_cluster = {}
    first = 0

    # Neighbors is empty, return an empty list of clusters
    if len(neighbors) == 0:
        return [[]]

    # No clusters yet, add the first. This iteration could be done before the loop
    if len(clusters) == 0:
        first = 1
        clusters = [set(neighbors[0])]
        for i in neighbors[0]:
            my_cluster[i] = clusters[0]

    # Elements in list are labelled according to the cluster they belong
    # Every time a new element is found is added to label with None as cluster.
    for ne in neighbors[first:]:
        found = None
        # Loop over all elements (neighbors) in ne
        for e in ne:
            for cl in clusters:
                if e in cl:
                    found = cl
                    break
            if found:
                break

        if not found:
            # This is a new cluster
            clusters.append(set(ne))
            for e in ne:
                my_cluster[e] = clusters[-1]
        else:
            # At least one particle belongs to a cluster that is already there
            # We are about to connect to this clusters all elements in ne.
            # We look for each element in ne and if this is already connected to a cluster
            # distinct from the one we just found, we merge the former to the latter.
            for e in ne:
                # Check if this item is connected to previously found clusters
                already_there = e in my_cluster.keys()
                # First loop over all elements in connected clusters and reassign them.
                if already_there:
                    distinct = not my_cluster[e] == found
                    if distinct:
                        # Add former cluster into new one
                        found.update(my_cluster[e])
                        # Remove cluster from list
                        clusters.remove(my_cluster[e])
                    # Update labels now
                    for ee in my_cluster[e]:
                        my_cluster[ee] = found

                # Now we can update the cluster label of central item
                my_cluster[e] = found

            # Now we add all elements in set
            found.update(ne)

    return clusters
