import json
import os

# import astropy.utils.data
from importlib import resources
import pytest

from ..tool import main
from . import data


class MockGraceDb(object):

    def __init__(self, service):
        assert service == 'https://gracedb.invalid/api/'
        self.service_url = service

    def _open(self, graceid, filename):
        if '.fits.gz' in filename:
            filename = os.path.join(graceid, filename)
            return resources.files(data).joinpath(filename).open('rb')
        else:
            filename = os.path.join(graceid, filename)
            if 'bayestar-gbm' in filename:
                filename += '.gz'
                return resources.files(data).joinpath(filename).open('rb')

            elif '.fits' in filename or 'xml' in filename:
                return resources.files(data).joinpath(filename).open('rb')
            else:
                f = resources.files(data).joinpath(filename).open('r')

                def get_json():
                    return json.load(f)

                f.json = get_json
                return f

    def superevent(self, graceid):
        return self._open(graceid, 'superevent.json')

    def event(self, graceid):
        return self._open(graceid, 'event.json')

    def logs(self, graceid):
        return self._open(graceid, 'logs.json')

    def voevents(self, graceid):
        return self._open(graceid, 'voevents.json')

    def files(self, graceid, filename=None, raw=True):
        if filename is None:
            return self._open(graceid, 'files.json')
        else:
            return self._open(graceid, os.path.join('files', filename))


def remove_nones(list):
    return [x for x in list if x is not None]


@pytest.fixture
def mock_gracedb(monkeypatch):
    return monkeypatch.setattr('ligo.gracedb.rest.GraceDb', MockGraceDb)


@pytest.fixture
def mock_webbrowser_open(mocker):
    return mocker.patch('webbrowser.open')


def test_cbc_compose(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose', 'S1234']))


def test_burst_compose(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose', 'S2468']))


def test_cwb_burst_compose(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose', 'S2469']))


def test_cbc_compose_aframe(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose', 'S2376']))


def test_skymap_update(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_update', 'S5678', ['sky_localization']]))


def test_raven_update(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_update', 'S5678', ['raven']]))


def test_general_update(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_update', 'S5678',
                      ['sky_localization', 'p_astro', 'em_bright', 'raven'],
                      '--cgmi_filename', 'mchirp_source_PE.json']))


def test_classification_update(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_update', 'S5678', ['p_astro', 'em_bright'],
                       '--cgmi_filename', 'mchirp_source_PE.json']))


def test_ssm_compose(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose', 'S6789']))


def test_compose_mailto(mock_gracedb, mock_webbrowser_open):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose', '--mailto', 'S1234']))
    mock_webbrowser_open.assert_called_once()


def test_raven_with_initial_circular(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_raven', 'S1234']))


def test_raven_with_snews(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_raven', 'S2468']))


def test_raven_without_initial_circular(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_raven', 'S5678']))


def test_medium_latency_cbc_only_detection(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_grb_medium_latency', 'E1235']))


def test_medium_latency_cbc_detection(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_grb_medium_latency', 'E1234']))


def test_medium_latency_cbc_burst_detection(mock_gracedb,):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_grb_medium_latency', 'E1122',
                       '--use_detection_template']))


def test_medium_latency_cbc_exclusion(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_grb_medium_latency', 'E1134']))


def test_medium_latency_cbc_burst_exclusion(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_grb_medium_latency', 'E2244',
                       '--use_exclusion_template']))


def test_llama_neutrino_track(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_llama', 'S2468']))


def test_llama_icecube_alert(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_llama', 'S2468',
                       '--icecube_alert', 'IceCubeCascade-230430a']))


def test_retraction(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_retraction', 'S1234']))


def test_retraction_early_warning(mock_gracedb):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/',
                       '--remove_text_wrap',
                       'compose_retraction', 'S5678']))
