"""
Superevents:
S1234: BNS
S2468: Burst
S2469: CWB BBH
S3456: Low significance NSBH
S5678: BNS update
S6789: SSM
S2376: Aframe only

External events:
E1122: Swift GRB for PyGRB and X-pipeline
E1133: SNEWS
E1134: Fermi GRB for PyGRB
E1234: Swift GRB for PyGRB and X-pipeline
E1235: INTEGRAL GRB
E2244: Fermi GRB
E5678: Fermi SubGRBTargeted
E5679: Vetoed Swift SubGRBTargeted

Mock events:
M1122: Burst CWB
M1123: CWB BBH
M1234: CBC gstlal
M1235: CBC gstlal early warning
M2376: CBC aframe
M2468: CBC pycbc
M2469: CBC pycbc early warning
M5566: Burst oLIB
M5678: CBC MBTA
M5679: CBC MBTA early warning
M5680: CBC MBTA early warning

The template numbers below correspond to the various templates in:
https://dcc.ligo.org/LIGO-P2300108
"""
import ligo.followup_advocate
from ligo.followup_advocate.test.test_tool import MockGraceDb


mockgracedb = MockGraceDb('https://gracedb.invalid/api/')
path = "ligo/followup_advocate/test/templates/"


def test_cbc_compose():
    """Template 1: Standard CBC BNS initial text"""
    text = ligo.followup_advocate.compose(
               'S1234', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'cbc_compose.txt', 'r') as file:
        assert text == file.read()


def test_burst_compose():
    """"Template 2: Standard unmodeled Burst initial text"""
    text = ligo.followup_advocate.compose(
               'S2468', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'burst_compose.txt', 'r') as file:
        assert text == file.read()


def test_cwb_burst_compose():
    """"Template 3: CWB BBH preferred event initial text"""
    text = ligo.followup_advocate.compose(
               'S2469', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'cwb_burst_compose.txt', 'r') as file:
        assert text == file.read()


def test_cbc_aframe_compose():
    """"Template 4: Aframe preferred event initial text"""
    text = ligo.followup_advocate.compose(
               'S2376', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'cbc_compose_aframe.txt', 'r') as file:
        assert text == file.read()


def test_skymap_update():
    """"Template 4: Update with only new sky map"""
    text = ligo.followup_advocate.compose_update(
               'S5678', client=mockgracedb, remove_text_wrap=False,
               update_types=['sky_localization'])
    with open(path + 'skymap_update.txt', 'r') as file:
        assert text == file.read()


def test_raven_update():
    """"Template 5: Update with only new external coincidence"""
    text = ligo.followup_advocate.compose_update(
               'S5678', client=mockgracedb, remove_text_wrap=False,
               update_types=['raven'])
    with open(path + 'raven_update.txt', 'r') as file:
        assert text == file.read()


def test_general_update():
    """"Template 6: Update on every possible choice"""
    text = ligo.followup_advocate.compose_update(
               'S5678', client=mockgracedb, remove_text_wrap=False,
               update_types=['sky_localization', 'p_astro',
                             'em_bright', 'raven'],
               cgmi_filename='mchirp_source_PE.json')
    with open(path + 'general_update.txt', 'r') as file:
        assert text == file.read()


def test_classification_update():
    """"Template 7: Update on em_bright and p_astro"""
    text = ligo.followup_advocate.compose_update(
               'S5678', client=mockgracedb, remove_text_wrap=False,
               update_types=['p_astro', 'em_bright'],
               cgmi_filename='mchirp_source_PE.json')
    with open(path + 'classification_update.txt', 'r') as file:
        assert text == file.read()


def test_ssm_compose():
    """"Template 8: SSM preferred initial text"""
    text = ligo.followup_advocate.compose(
               'S6789', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'ssm_compose.txt', 'r') as file:
        assert text == file.read()


def test_raven_with_initial_circular():
    """"Template 9: RAVEN GRB coincidence with BNS"""
    text = ligo.followup_advocate.compose_raven(
               'S1234', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'raven_with_initial_circular.txt', 'r') as file:
        assert text == file.read()


def test_raven_with_snews():
    """"Template 10: RAVEN SNEWS coindience with Burst"""
    text = ligo.followup_advocate.compose_raven(
               'S2468', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'raven_with_snews.txt', 'r') as file:
        assert text == file.read()


def test_raven_without_initial_circular():
    """"Template 11: RAVEN subthreshold GRB with low significance NSBH"""
    text = ligo.followup_advocate.compose_raven(
               'S3456', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'raven_without_initial_circular.txt', 'r') as file:
        assert text == file.read()


def test_medium_latency_cbc_only_detection():
    """"Template 12: PyGRB CBC initial text"""
    text = ligo.followup_advocate.compose_grb_medium_latency(
               'E1235', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'medium_latency_cbc_only_detection.txt', 'r') as file:
        assert text == file.read()


def test_medium_latency_cbc_detection():
    """"Template 13: PyGRB and X-pipeline CBC initial text"""
    text = ligo.followup_advocate.compose_grb_medium_latency(
               'E1234', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'medium_latency_cbc_detection.txt', 'r') as file:
        assert text == file.read()


def test_medium_latency_cbc_burst_detection():
    """"Template 14: PyGRB and X-pipeline Burst initial text"""
    text = ligo.followup_advocate.compose_grb_medium_latency(
               'E1122', client=mockgracedb, remove_text_wrap=False,
               use_detection_template=True)
    with open(path + 'medium_latency_cbc_burst_detection.txt', 'r') as file:
        assert text == file.read()


def test_medium_latency_cbc_exclusion():
    """"Template 15: PyGRB CBC non-detection"""
    text = ligo.followup_advocate.compose_grb_medium_latency(
               'E1134', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'medium_latency_cbc_exclusion.txt', 'r') as file:
        assert text == file.read()


def test_medium_latency_cbc_burst_exclusion():
    """"Template 16: PyGRB and X-pipeline Burst non-detection"""
    text = ligo.followup_advocate.compose_grb_medium_latency(
               'E2244', client=mockgracedb, remove_text_wrap=False,
               use_detection_template=True)
    with open(path + 'medium_latency_cbc_burst_exclusion.txt', 'r') as file:
        assert text == file.read()


def test_llama_neutrino_track():
    """"Template 17: LLAMA neutrio track with Burst"""
    text = ligo.followup_advocate.compose_llama(
               'S2468', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'llama_neutrino_track.txt', 'r') as file:
        assert text == file.read()


def test_llama_icecube_alert():
    """"Template 18: LLAMA burst with Burst"""
    text = ligo.followup_advocate.compose_llama(
               'S2468', client=mockgracedb, remove_text_wrap=False,
               icecube_alert='IceCubeCascade-230430a')
    with open(path + 'llama_icecube_alert.txt', 'r') as file:
        assert text == file.read()


def test_retraction():
    """"Template 19: General retraction"""
    text = ligo.followup_advocate.compose_retraction(
               'S1234', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'retraction.txt', 'r') as file:
        assert text == file.read()


def test_retraction_early_warning():
    """"Template 20: Retraction of early warning candidate"""
    text = ligo.followup_advocate.compose_retraction(
               'S5678', client=mockgracedb, remove_text_wrap=False)
    with open(path + 'retraction_early_warning.txt', 'r') as file:
        assert text == file.read()
