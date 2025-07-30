import math as mth
import os
import shutil
import tempfile
import urllib
import webbrowser

import astropy.coordinates as coord
import astropy.time
import astropy.units as u
import healpy as hp
import lxml.etree
import numpy as np
from astropy.io.fits import getheader
from ligo.gracedb import rest
from ligo.skymap.io.fits import read_sky_map
from ligo.skymap.postprocess.ellipse import find_ellipse
from ligo.skymap.postprocess.crossmatch import crossmatch

from .jinja import env
import importlib.metadata
__version__ = importlib.metadata.version(__name__)


def authors(authors, service=rest.DEFAULT_SERVICE_URL):
    """Write GCN Circular author list"""
    return env.get_template('authors.jinja2').render(authors=authors).strip()


def guess_skyloc_pipeline(filename):
    skyloc_pipelines_dict = {
        'cwb': 'cWB_AllSky',
        'bayestar': 'BAYESTAR',
        'bilby': 'Bilby',
        'lib': 'LIB',
        'lalinference': 'LALInference',
        'olib': 'oLIB_AllSky',
        'mly': 'MLy_AllSky',
        'rapidpe_rift': 'RapidPE-RIFT',
        'amplfi': 'AMPLFI'
    }
    try:
        return skyloc_pipelines_dict[filename.split('.')[0].lower()]
    except KeyError:
        return filename.split('.')[0]


def text_width(remove_text_wrap):
    """Return width of text wrap based on whether we wish to wrap the lines or
    not."""
    return 9999 if remove_text_wrap else 79


def main_dict(gracedb_id, client, raven_coinc=False, update_alert=False,
              cgmi_filename=None):
    """Create general dictionary to pass to compose circular"""

    superevent = client.superevent(gracedb_id).json()
    preferred_event = superevent['preferred_event_data']
    pipeline = preferred_event['pipeline']
    search = preferred_event['search']
    preferred_pipeline_search = f'{pipeline}_{search}'
    early_warning_pipeline_searches = []
    pipeline_searches = []
    gw_events = superevent['gw_events']
    early_warning_alert = False

    for gw_event in gw_events:
        gw_event_dict = client.event(gw_event).json()
        pipeline = gw_event_dict['pipeline']
        search = gw_event_dict['search']
        # Remap MDC to allsky to not double count
        if search == 'MDC':
            search = 'AllSky'
        pipeline_search = f'{pipeline}_{search}'
        # Create separates lists of post merger and early warning pipelines
        if pipeline_search not in pipeline_searches and \
                'EarlyWarning' not in pipeline_search:
            pipeline_searches.append(pipeline_search)
        if 'EarlyWarning' in pipeline_search:
            # Remap MBTA early warning to the all sky citation prior to
            # checking if there is a previous entry
            if 'mbta' in pipeline_search.lower():
                pipeline_search = 'MBTA_AllSky'
            if pipeline_search not in early_warning_pipeline_searches:
                early_warning_pipeline_searches.append(pipeline_search)

    if not pipeline_searches:
        raise ValueError(
            "{} has no post-merger events to generate circulars from.".format(
                gracedb_id))

    # Sort to get alphabetical order
    pipeline_searches.sort(key=str.lower)
    early_warning_pipeline_searches.sort(key=str.lower)

    voevents = client.voevents(gracedb_id).json()['voevents']
    if not voevents:
        raise ValueError(
            "{} has no VOEvent to generate circulars from.".format(
                gracedb_id))

    citation_index = {
        pipeline_search.lower(): pipeline_searches.index(pipeline_search) + 1
        for pipeline_search in pipeline_searches}
    for pipeline_search in early_warning_pipeline_searches:
        if pipeline_search.lower() not in citation_index:
            citation_index[pipeline_search.lower()] = \
                max(citation_index.values()) + 1

    gpstime = float(preferred_event['gpstime'])
    event_time = astropy.time.Time(gpstime, format='gps').utc

    # Grab latest p_astro and em_bright values from lastest VOEvent
    voevent_text_latest = \
        client.files(gracedb_id, voevents[-1]['filename']).read()
    root = lxml.etree.fromstring(voevent_text_latest)
    p_astros = root.find('./What/Group[@name="Classification"]')
    em_brights = root.find('./What/Group[@name="Properties"]')
    classifications = {}
    source_classification = {}
    mchirp_bin = {}
    # Only try to load if present to prevent errors with .getchildren()
    p_astro_pipeline = None
    search_for_cgmi_file = em_brights and not update_alert and \
        cgmi_filename is None

    # Grab logs for either RapidPE checks or chirp mass bins
    if p_astros or search_for_cgmi_file:
        logs = client.logs(gracedb_id).json()['log']

    if p_astros:
        for p_astro in p_astros.getchildren():
            if p_astro.attrib.get('value'):
                classifications[p_astro.attrib['name']] = \
                    float(p_astro.attrib['value']) * 100
        # Figure out which pipeline uploaded p_astro, usually the first one
        # FIXME: Replace with more efficient method in the future
        for message in reversed(logs):
            filename = message['filename']
            if filename and '.p_astro.json' in filename and \
                    filename != 'p_astro.json':
                p_astro = client.files(gracedb_id, filename).json()
                if all(mth.isclose(p_astro[key] * 100, classifications[key])
                       for key in classifications.keys()):
                    p_astro_pipeline = filename.split('.')[0].lower()
                    break
        if p_astro_pipeline == 'rapidpe_rift':
            citation_index['rapidpe_rift'] = max(citation_index.values()) + 1
    if em_brights:
        for em_bright in em_brights.getchildren():
            if em_bright.attrib.get('value'):
                source_classification[em_bright.attrib['name']] = \
                    float(em_bright.attrib['value']) * 100
        if len(source_classification) > 0:
            citation_index['em_bright'] = max(citation_index.values()) + 1

    # Look for CGMI file if a preliminary/inital alert with embright info or
    # if given a filename, usually for an update alert
    if search_for_cgmi_file or cgmi_filename is not None:
        #  chirp mass estimates included when em-bright is
        if cgmi_filename is not None:
            cgmi_json = client.files(gracedb_id, cgmi_filename).json()
        else:
            for message in reversed(logs):
                filename = message['filename']
                # use most recent mchirp estimate
                if filename and 'mchirp_source' in filename and \
                        '.json' in filename:
                    cgmi_json = client.files(gracedb_id, filename).json()
                    break
        # if CGMI file found either way, include in results
        if cgmi_json:
            mchirp_bin_edges = cgmi_json['bin_edges']
            mchirp_probs = cgmi_json['probabilities']
            # find the highest probability bin
            max_prob_idx = np.argmax(mchirp_probs)
            left_bin = mchirp_bin_edges[max_prob_idx]
            right_bin = mchirp_bin_edges[max_prob_idx+1]
            mchirp_bin = left_bin, right_bin

    skymaps = {}
    voevents_text = []
    for voevent in voevents:
        # Don't load latest voevent since already loaded from before
        if voevent == voevents[-1]:
            voevent_text = voevent_text_latest
        # If earlier voevent, load
        else:
            voevent_text = client.files(gracedb_id, voevent['filename']).read()
        root = lxml.etree.fromstring(voevent_text)
        alert_type = root.find(
            './What/Param[@name="AlertType"]').attrib['value'].lower()
        if alert_type == 'earlywarning':
            # Add text for early warning detection if one early warning alert
            early_warning_alert = True
        url = root.find('./What/Group/Param[@name="skymap_fits"]')
        if url is None:
            continue
        url = url.attrib['value']
        _, filename = os.path.split(url)
        skyloc_pipeline = guess_skyloc_pipeline(filename)
        issued_time = astropy.time.Time(root.find('./Who/Date').text).gps
        if filename not in skymaps:
            skymaps[filename] = dict(
                alert_type=alert_type,
                pipeline=skyloc_pipeline,
                filename=filename,
                latency=issued_time-event_time.gps)
            if skyloc_pipeline.lower() not in citation_index:
                citation_index[skyloc_pipeline.lower()] = \
                    max(citation_index.values()) + 1
        voevents_text.append(voevent_text)
    skymaps = list(skymaps.values())

    o = urllib.parse.urlparse(client.service_url)

    kwargs = dict(
        subject='Identification',
        gracedb_id=gracedb_id,
        gracedb_service_url=urllib.parse.urlunsplit(
            (o.scheme, o.netloc, '/superevents/', '', '')),
        update_alert=update_alert,
        cgmi_filename=cgmi_filename,
        group=preferred_event['group'],
        pipeline_search=preferred_pipeline_search,
        post_merger_pipeline_searches=pipeline_searches,
        early_warning_alert=early_warning_alert,
        early_warning_pipeline_searches=early_warning_pipeline_searches,
        gpstime='{0:.03f}'.format(round(float(preferred_event['gpstime']), 3)),
        search=preferred_event.get('search', ''),
        far=preferred_event['far'],
        utctime=event_time.iso,
        instruments=preferred_event['instruments'].split(','),
        skymaps=skymaps,
        prob_has_ns=source_classification.get('HasNS'),
        prob_has_remnant=source_classification.get('HasRemnant'),
        prob_has_massgap=source_classification.get('HasMassGap'),
        prob_has_ssm=source_classification.get('HasSSM'),
        source_classification=source_classification,
        mchirp_bin=mchirp_bin,
        include_ellipse=None,
        classifications=classifications,
        p_astro_pipeline=p_astro_pipeline,
        citation_index=citation_index)

    if skymaps:
        preferred_skymap = skymaps[-1]['filename']
        cls = [50, 90]
        include_ellipse, ra, dec, a, b, pa, area, greedy_area = \
            uncertainty_ellipse(gracedb_id, preferred_skymap, client, cls=cls)
        kwargs.update(
            preferred_skymap=preferred_skymap,
            cl=cls[-1],
            include_ellipse=include_ellipse,
            ra=coord.Longitude(ra*u.deg),
            dec=coord.Latitude(dec*u.deg),
            a=coord.Angle(a*u.deg),
            b=coord.Angle(b*u.deg),
            pa=coord.Angle(pa*u.deg),
            ellipse_area=area,
            greedy_area=greedy_area)
        try:
            distmu, distsig = get_distances_skymap_gracedb(gracedb_id,
                                                           preferred_skymap,
                                                           client)
            kwargs.update(
                distmu=distmu,
                distsig=distsig)
        except TypeError:
            pass

    if raven_coinc:
        kwargs = _update_raven_parameters(superevent, kwargs, client,
                                          voevents_text)
    return kwargs


def compose(gracedb_id, authors=(), mailto=False, remove_text_wrap=False,
            service=rest.DEFAULT_SERVICE_URL, client=None):
    """Compose GCN Circular draft"""

    if client is None:
        client = rest.GraceDb(service)

    kwargs = main_dict(gracedb_id, client=client)
    kwargs.update(authors=authors)
    kwargs.update(change_significance_statement=False)
    kwargs.update(text_width=text_width(remove_text_wrap))

    subject = env.get_template('subject.jinja2').render(**kwargs).strip()
    body = env.get_template('initial_circular.jinja2').render(**kwargs).strip()

    if mailto:
        pattern = 'mailto:emfollow@ligo.org,dac@ligo.org?subject={0}&body={1}'
        url = pattern.format(
            urllib.parse.quote(subject),
            urllib.parse.quote(body))
        webbrowser.open(url)
    else:
        return '{0}\n\n{1}'.format(subject, body)


def compose_raven(gracedb_id, authors=(), remove_text_wrap=False,
                  service=rest.DEFAULT_SERVICE_URL, client=None):
    """Compose EM_COINC RAVEN GCN Circular draft"""

    if client is None:
        client = rest.GraceDb(service)

    kwargs = dict()
    kwargs.update(main_dict(gracedb_id, client=client, raven_coinc=True))
    kwargs.update(text_width=text_width(remove_text_wrap))
    # Add RAVEN citation
    citation_index = kwargs['citation_index']
    citation_index['raven'] = max(citation_index.values()) + 1
    kwargs['citation_index'] = citation_index

    subject = (
        env.get_template('RAVEN_subject.jinja2').render(**kwargs)
        .strip())
    body = (
        env.get_template('RAVEN_circular.jinja2').render(**kwargs)
        .strip())
    return '{0}\n\n{1}'.format(subject, body)


def compose_llama(
        gracedb_id, authors=(), service=rest.DEFAULT_SERVICE_URL,
        icecube_alert=None, remove_text_wrap=False,
        client=None):
    """Compose GRB LLAMA GCN Circular draft.
    Here, gracedb_id will be a GRB superevent ID in GraceDb."""

    if client is None:
        client = rest.GraceDb(service)

    superevent = client.superevent(gracedb_id).json()

    gpstime = float(superevent['t_0'])
    tl, th = gpstime - 500, gpstime + 500
    event_time = astropy.time.Time(gpstime, format='gps').utc
    tl_datetime = str(astropy.time.Time(
                      tl, format='gps').isot).replace('T', ' ')
    th_datetime = str(astropy.time.Time(
                      th, format='gps').isot).replace('T', ' ')

    o = urllib.parse.urlparse(client.service_url)
    kwargs = dict(
        gracedb_service_url=urllib.parse.urlunsplit(
            (o.scheme, o.netloc, '/superevents/', '', '')),
        gracedb_id=gracedb_id,
        llama=True,
        icecube_alert=icecube_alert,
        event_time=event_time,
        tl_datetime=tl_datetime,
        th_datetime=th_datetime,
        authors=authors)
    kwargs.update(text_width=text_width(remove_text_wrap))

    citation_index = {'llama': 1, 'llama_stat': 2}
    kwargs.update(citation_index=citation_index)

    files = client.files(gracedb_id).json()

    llama_stat_filename = 'significance_subthreshold_lvc-i3.json'
    if llama_stat_filename in files:
        llama_stat_file = client.files(gracedb_id, llama_stat_filename).json()
        llama_fap = llama_stat_file["p_value"]
        neutrinos = llama_stat_file["inputs"]["neutrino_info"]
        lines = []
        for neutrino in neutrinos:
            # Build aligned string
            vals = []
            dt = (event_time -
                  astropy.time.Time(neutrino['mjd'],
                                    format='mjd')).to(u.s).value
            vals.append('{:.2f}'.format(dt))
            vals.append('{:.2f}'.format(neutrino['ra']))
            vals.append('{:.2f}'.format(neutrino['dec']))
            vals.append('{:.2f}'.format(neutrino['sigma']))
            vals.append('{:.4f}'.format(llama_fap))
            lines.append(align_number_string(vals, [0, 11, 21, 40, 59]))

        kwargs.update(llama_fap=llama_fap,
                      neutrinos=lines)

    subject = (
        env.get_template('llama_subject.jinja2').render(**kwargs)
        .strip())
    if icecube_alert:
        body = (
            env.get_template('llama_alert_circular.jinja2').render(**kwargs)
            .strip())
    else:
        body = (
            env.get_template('llama_track_circular.jinja2').render(**kwargs)
            .strip())
    return '{0}\n\n{1}'.format(subject, body)


def compose_grb_medium_latency(
        gracedb_id, authors=(), service=rest.DEFAULT_SERVICE_URL,
        use_detection_template=None, remove_text_wrap=False, client=None):
    """Compose GRB Medium Latency GCN Circular draft.
    Here, gracedb_id will be a GRB external trigger ID in GraceDb."""

    if client is None:
        client = rest.GraceDb(service)

    event = client.event(gracedb_id).json()
    search = event['search']

    if search != 'GRB':
        return

    group = event['group']
    pipeline = event['pipeline']
    external_trigger = event['extra_attributes']['GRB']['trigger_id']

    o = urllib.parse.urlparse(client.service_url)
    kwargs = dict(
        gracedb_service_url=urllib.parse.urlunsplit(
            (o.scheme, o.netloc, '/events/', '', '')),
        gracedb_id=gracedb_id,
        group=group,
        grb=True,
        pipeline=pipeline,
        external_trigger=external_trigger,
        exclusions=[],
        detections=[])
    kwargs.update(text_width=text_width(remove_text_wrap))

    files = client.files(gracedb_id).json()

    citation_index = {}
    index = 1
    xpipeline_fap_file = 'false_alarm_probability_x.json'
    if xpipeline_fap_file in files:
        xpipeline_fap = client.files(gracedb_id, xpipeline_fap_file).json()
        online_xpipeline_fap = xpipeline_fap.get('Online Xpipeline')
        # Create detection/exclusion circular based on given argument
        # Use default cutoff if not provided
        xpipeline_detection = (use_detection_template if use_detection_template
                               is not None else online_xpipeline_fap < 0.001)
        if xpipeline_detection:
            kwargs['detections'].append('xpipeline')
            kwargs.update(online_xpipeline_fap=online_xpipeline_fap)
        else:
            kwargs['exclusions'].append('xpipeline')
            xpipeline_distances_file = 'distances_x.json'
            xpipeline_distances = client.files(gracedb_id,
                                               xpipeline_distances_file).json()
            burst_exclusion = xpipeline_distances.get('Burst Exclusion')
            kwargs.update(burst_exclusion=burst_exclusion)
        citation_index['xpipeline'] = index
        index += 1

    pygrb_fap_file = 'false_alarm_probability_pygrb.json'
    if pygrb_fap_file in files:
        pygrb_fap = client.files(gracedb_id, pygrb_fap_file).json()
        online_pygrb_fap = pygrb_fap.get('Online PyGRB')
        # Create detection/exclusion circular based on given argument
        # Use default cutoff if not provided
        pygrb_detection = (use_detection_template if use_detection_template
                           is not None else online_pygrb_fap < 0.01)
        if pygrb_detection:
            kwargs['detections'].append('pygrb')
            kwargs.update(online_pygrb_fap=online_pygrb_fap)
        else:
            kwargs['exclusions'].append('pygrb')
            pygrb_distances_file = 'distances_pygrb.json'
            pygrb_distances = client.files(gracedb_id,
                                           pygrb_distances_file).json()
            nsns_exclusion = pygrb_distances.get('NSNS Exclusion')
            nsbh_exclusion = pygrb_distances.get('NSBH Exclusion')
            kwargs.update(nsbh_exclusion=nsbh_exclusion,
                          nsns_exclusion=nsns_exclusion)
        citation_index['pygrb'] = index

    kwargs.update(citation_index=citation_index)

    subject = (
        env.get_template('medium_latency_grb_subject.jinja2').render(**kwargs)
        .strip())
    body = (
        env.get_template('medium_latency_grb_circular.jinja2').render(**kwargs)
        .strip())
    return '{0}\n\n{1}'.format(subject, body)


def compose_update(gracedb_id, authors=(),
                   service=rest.DEFAULT_SERVICE_URL,
                   update_types=['sky_localization', 'p_astro',
                                 'em_bright', 'raven'],
                   remove_text_wrap=False,
                   client=None,
                   cgmi_filename=None):
    """Compose GCN update circular"""
    if client is None:
        client = rest.GraceDb(service)

    kwargs = main_dict(gracedb_id, client=client,
                       raven_coinc='raven' in update_types,
                       update_alert=True,
                       cgmi_filename=cgmi_filename)
    kwargs.pop('citation_index', None)
    kwargs.update(text_width=text_width(remove_text_wrap))

    if isinstance(update_types, str):
        update_types = update_types.split(',')

    # Adjust files for update type alert
    citation_index = {}
    skymaps = []
    index = 1

    updated_skymap = kwargs.get('skymaps')[-1]
    kwargs.update(updated_skymap=updated_skymap)
    skymaps = [updated_skymap]
    if cgmi_filename:
        update_types.append('cgmi')
    if 'sky_localization' in update_types:
        citation_index[updated_skymap['pipeline'].lower()] = index
        index += 1
    if 'p_astro' in update_types and \
            kwargs.get('p_astro_pipeline') == 'rapidpe_rift':
        citation_index['rapidpe_rift'] = index
        index += 1
    if 'em_bright' in update_types:
        # If not already cited, cite sky map pipeline for em_bright
        if updated_skymap['pipeline'].lower() not in citation_index.keys():
            citation_index[updated_skymap['pipeline'].lower()] = index
            index += 1
        citation_index['em_bright'] = index
        index += 1
    if 'raven' in update_types:
        citation_index['raven'] = index

    kwargs.update(skymaps=skymaps,
                  citation_index=citation_index,
                  post_merger_pipeline_searches=[],
                  update_alert=True)

    kwargs.update(authors=authors)
    kwargs.update(change_significance_statement=False)
    kwargs.update(subject='Update')
    kwargs.update(update_types=update_types)

    subject = env.get_template('subject.jinja2').render(**kwargs).strip()
    body = env.get_template(
               'update_circular.jinja2').render(**kwargs).strip()
    return '{0}\n\n{1}'.format(subject, body)


def compose_retraction(gracedb_id, authors=(), remove_text_wrap=False,
                       service=rest.DEFAULT_SERVICE_URL, client=None):
    """Compose GCN retraction circular"""
    if client is None:
        client = rest.GraceDb(service)
    event = client.superevent(gracedb_id).json()
    preferred_event = event['preferred_event_data']
    labels = event['labels']
    earlywarning = \
        ('EARLY_WARNING' in labels and
         {'EM_SelectedConfident', 'SIGNIF_LOCKED'}.isdisjoint(labels))

    kwargs = dict(
                 subject='Retraction',
                 gracedb_id=gracedb_id,
                 group=preferred_event['group'],
                 earlywarning=earlywarning,
                 authors=authors
             )
    kwargs.update(text_width=text_width(remove_text_wrap))

    subject = env.get_template('subject.jinja2').render(**kwargs).strip()
    body = env.get_template('retraction.jinja2').render(**kwargs).strip()
    return '{0}\n\n{1}'.format(subject, body)


def read_map_gracedb(graceid, filename, client):
    with tempfile.NamedTemporaryFile(mode='w+b') as localfile:
        remotefile = client.files(graceid, filename, raw=True)
        shutil.copyfileobj(remotefile, localfile)
        localfile.flush()
        return read_sky_map(localfile.name, moc=True)


def get_distances_skymap_gracedb(graceid, filename, client):
    with tempfile.NamedTemporaryFile(mode='w+b') as localfile:
        remotefile = client.files(graceid, filename, raw=True)
        shutil.copyfileobj(remotefile, localfile)
        localfile.flush()
        header = getheader(localfile.name, 1)
        try:
            return header['distmean'], header['diststd']
        except KeyError:
            pass


def read_map_from_path(path, client):
    return read_map_gracedb(*path.split('/'), client)[0]


def align_number_string(nums, positions):
    positions.append(len(nums[-1]))
    gen = (val + ' ' * (positions[i+1]-positions[i]-len(val))
           for i, val in enumerate(nums))
    return ''.join(gen)


def mask_cl(p, level=90):
    pflat = p.ravel()
    i = np.flipud(np.argsort(p))
    cs = np.cumsum(pflat[i])
    cls = np.empty_like(pflat)
    cls[i] = cs
    cls = cls.reshape(p.shape)
    return cls <= 1e-2 * level


def compare_skymaps(paths, service=rest.DEFAULT_SERVICE_URL, client=None):
    """Produce table of sky map overlaps"""
    if client is None:
        client = rest.GraceDb(service)
    filenames = [path.split('/')[1] for path in paths]
    pipelines = [guess_skyloc_pipeline(filename) for filename in filenames]
    probs = [read_map_from_path(path, client) for path in paths]
    npix = max(len(prob) for prob in probs)
    nside = hp.npix2nside(npix)
    deg2perpix = hp.nside2pixarea(nside, degrees=True)
    probs = [hp.ud_grade(prob, nside, power=-2) for prob in probs]
    masks = [mask_cl(prob) for prob in probs]
    areas = [mask.sum() * deg2perpix for mask in masks]
    joint_areas = [(mask & masks[-1]).sum() * deg2perpix for mask in masks]

    kwargs = dict(params=zip(filenames, pipelines, areas, joint_areas))

    return env.get_template('compare_skymaps.jinja2').render(**kwargs)


def uncertainty_ellipse(graceid, filename, client, cls=[50, 90],
                        ratio_ellipse_cl_areas=1.35):
    """Compute uncertainty ellipses for a given sky map

    Parameters
    ----------
    graceid: str
        ID of the trigger used by GraceDB
    filename: str
        File name of sky map
    client: class
        REST API client for HTTP connection
    cls: array-like
        List of percentage of minimal credible area used to check whether the
        areas are close to an ellipse, returning the values of the final item
    ratio_ellipse_cl_areas: float
        Ratio between ellipse area and minimal credible area from cl
    """
    if filename.endswith('.gz'):
        # Try using the multi-res sky map if it exists
        try:
            new_filename = filename.replace('.fits.gz', '.multiorder.fits')
            skymap = read_map_gracedb(graceid, new_filename, client)
        except (IOError, rest.HTTPError):
            skymap = read_map_gracedb(graceid, filename, client)
    else:
        skymap = read_map_gracedb(graceid, filename, client)

    # Convert to an array if necessary
    if np.isscalar(cls):
        cls = [cls]
    cls = np.asarray(cls)

    # Pass array of contour inteverals to get areas
    result = crossmatch(skymap, contours=cls / 100)
    greedy_areas = np.asarray(result.contour_areas)
    ra, dec, a, b, pa, ellipse_areas = find_ellipse(skymap, cl=cls)
    a, b = np.asarray(a), np.asarray(b)

    # Only use ellipse if every confidence interval passes
    use_ellipse = \
        np.all(ellipse_areas <= ratio_ellipse_cl_areas * greedy_areas)
    return (use_ellipse, ra, dec, a[-1], b[-1], pa, ellipse_areas[-1],
            greedy_areas[-1])


def _update_raven_parameters(superevent, kwargs, client, voevents_text):
    """Update kwargs with parameters for RAVEN coincidence"""

    gracedb_id = superevent['superevent_id']

    if 'EM_COINC' not in superevent['labels']:
        raise ValueError("No EM_COINC label for {}".format(
            gracedb_id))

    preferred_event = superevent['preferred_event_data']
    group = preferred_event['group']
    gpstime = float(preferred_event['gpstime'])
    event_time = astropy.time.Time(gpstime, format='gps').utc
    em_event_id = superevent['em_type']

    # FIXME: Grab more info from the latest VOEvent if deemed suitable
    em_event = client.event(em_event_id).json()
    external_pipeline = em_event['pipeline']
    # Get all other pipelines
    ext_events = [client.event(id).json() for id
                  in superevent['em_events']]
    # Remove duplicates and vetoed events
    other_ext_pipelines = \
        [*set(event['pipeline'] for event in ext_events
              if 'NOT_GRB' not in event['labels'])]
    # Remove preferred pipeline if present
    # This is to cover a corner case where NOT_GRB gets added to a preferred
    # external event after RAVEN_ALERT is applied
    if external_pipeline in other_ext_pipelines:
        other_ext_pipelines.remove(external_pipeline)
    # FIXME in GraceDb: Even SNEWS triggers have an extra attribute GRB.
    external_trigger_id = em_event['extra_attributes']['GRB']['trigger_id']
    snews = (em_event['pipeline'] == 'SNEWS')
    grb = (em_event['search'] in ['GRB', 'SubGRB', 'SubGRBTargeted', 'MDC']
           and not snews)
    subthreshold = em_event['search'] in ['SubGRB', 'SubGRBTargeted']
    subthreshold_targeted = em_event['search'] == 'SubGRBTargeted'
    far_grb = em_event['far']

    voevent_text_latest = voevents_text[-1]
    root = lxml.etree.fromstring(voevent_text_latest)
    time_diff = \
        root.find('./What/Group/Param[@name="Time_Difference"]')
    time_diff = float(time_diff.attrib['value'])

    o = urllib.parse.urlparse(client.service_url)
    kwargs.update(
        gracedb_service_url=urllib.parse.urlunsplit(
            (o.scheme, o.netloc, '/superevents/', '', '')),
        gracedb_id=gracedb_id,
        group=group,
        external_pipeline=external_pipeline,
        external_trigger=external_trigger_id,
        snews=snews,
        grb=grb,
        subthreshold=subthreshold,
        subthreshold_targeted=subthreshold_targeted,
        other_ext_pipelines=sorted(other_ext_pipelines),
        far_grb=far_grb,
        latency=abs(round(time_diff, 1)),
        beforeafter='before' if time_diff < 0 else 'after')

    if grb:
        # Grab GRB coincidence FARs
        time_coinc_far = superevent['time_coinc_far']
        space_time_coinc_far = superevent['space_coinc_far']
        kwargs.update(
            time_coinc_far=time_coinc_far,
            space_time_coinc_far=space_time_coinc_far,
            ext_ra=em_event['extra_attributes']['GRB']['ra'],
            ext_dec=em_event['extra_attributes']['GRB']['dec'],
            ext_error=em_event['extra_attributes']['GRB']['error_radius'])

        # Find combined sky maps for GRB
        combined_skymaps = {}
        for i, voevent_text in enumerate(voevents_text):
            root = lxml.etree.fromstring(voevent_text)
            alert_type = root.find(
                './What/Param[@name="AlertType"]').attrib['value'].lower()
            # Check if significant GW alert already queued or sent
            change_significance_statement = \
                {'EM_SelectedConfident', 'SIGNIF_LOCKED'}.isdisjoint(
                    superevent['labels'])
            url = root.find('./What/Group/Param[@name="joint_skymap_fits"]')
            if url is None:
                continue
            url = url.attrib['value']
            _, filename = os.path.split(url)
            issued_time = astropy.time.Time(
                              root.find('./Who/Date').text).gps
            if filename not in combined_skymaps:
                combined_skymaps[filename] = dict(
                    alert_type=alert_type,
                    filename=filename,
                    latency=issued_time-event_time.gps)

        if combined_skymaps:
            combined_skymaps = list(combined_skymaps.values())
            combined_skymap = combined_skymaps[-1]['filename']
            cls = [50, 90]
            include_ellipse, ra, dec, a, b, pa, area, greedy_area = \
                uncertainty_ellipse(gracedb_id, combined_skymap, client,
                                    cls=cls)
            kwargs.update(
                combined_skymap=combined_skymap,
                combined_skymaps=combined_skymaps,
                cl=cls[-1],
                combined_skymap_include_ellipse=include_ellipse,
                combined_skymap_ra=coord.Longitude(ra*u.deg),
                combined_skymap_dec=coord.Latitude(dec*u.deg),
                combined_skymap_a=coord.Angle(a*u.deg),
                combined_skymap_b=coord.Angle(b*u.deg),
                combined_skymap_pa=coord.Angle(pa*u.deg),
                combined_skymap_ellipse_area=area,
                combined_skymap_greedy_area=greedy_area,
                change_significance_statement=change_significance_statement)

    return kwargs
