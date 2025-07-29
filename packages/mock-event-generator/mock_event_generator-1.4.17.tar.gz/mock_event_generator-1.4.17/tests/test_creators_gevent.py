from __future__ import annotations

import json
from collections.abc import Iterator
from io import BytesIO
from pathlib import Path

# --------------------------------------
# Deprecated: ligo.lw --> igwn_ligolw
# https://git.ligo.org/emfollow/gwcelery/-/merge_requests/1636/diffs
# -------------------------------------
import igwn_ligolw.lsctables
import igwn_ligolw.utils
import lal
import pytest
from astropy.time import Time
from igwn_ligolw.ligolw import Document
from pytest_mock import MockerFixture
from requests import HTTPError

from ligo.gracedb.rest import GraceDb
from mock_event_generator.cache import EventFileCache
from mock_event_generator.creators import (
    PIPELINE_GEVENT_CREATOR_CLASSES,
    AframeEventCreator,
    CBCEventCreator,
    ContentHandler,
    CWBEventCreator,
    ExternalEventCreator,
    GEventCreator,
    filter_uploads,
    filter_uploads_unless,
)
from mock_event_generator.gracedbs import GraceDBAlias, GraceDBWithContext
from mock_event_generator.models import Upload
from pytest_gracedb import PIPELINES

GEVENT_ID = 'G587369'
SOURCE = GraceDBWithContext.meg_from_alias_or_url(GraceDBAlias.MOCKED)
TARGET = GraceDBWithContext.meg_from_alias_or_url(GraceDBAlias.MOCKED)


@pytest.fixture
def cache(mocked_gracedb: None, tmp_path: Path) -> Iterator[EventFileCache]:
    yield EventFileCache(SOURCE, False, tmp_path)


@pytest.mark.xfail
@pytest.mark.parametrize('group', [None, 'Test'])
@pytest.mark.parametrize('search', [None, 'MDC'])
async def test_create_gevent(
    cache: EventFileCache, group: str | None, search: str | None
) -> None:
    creator = GEventCreator.from_id(GEVENT_ID, TARGET, cache)
    gevent = await creator.create(group, search, Time.now().gps, 0)
    expected_group = group or 'Burst'
    expected_search = search or 'BBH'
    assert gevent['group'] == expected_group
    assert gevent['search'] == expected_search


@pytest.mark.xfail
async def test_create_gevent_invalid_request(
    mocker: MockerFixture, cache: EventFileCache
) -> None:
    creator = GEventCreator.from_id(GEVENT_ID, TARGET, cache)
    mocker.patch(
        'pytest_gracedb.gracedb.TestDoubleGraceDB.create_event',
        return_value=(500, {}, '{"detail": "Reason 42"}'),
    )
    with pytest.raises(HTTPError) as excinfo:
        await creator.create(None, None, Time.now().gps, 0)
    exc: HTTPError = excinfo.value
    assert exc.response.status_code == 500
    assert 'Reason 42' in exc.response.text


def test_create_gevent_unknown_pipeline(
    mocker: MockerFixture, cache: EventFileCache
) -> None:
    mocker.patch.dict(PIPELINE_GEVENT_CREATOR_CLASSES, clear=True)
    with pytest.raises(NotImplementedError, match='Cannot re-create G-event'):
        GEventCreator.from_id(GEVENT_ID, TARGET, cache)


@pytest.mark.xfail
async def test_create_gevent_log_invalid_request(
    mocker: MockerFixture, cache: EventFileCache
) -> None:
    creator = GEventCreator.from_id(GEVENT_ID, TARGET, cache)
    mocker.patch(
        'pytest_gracedb.gracedb.TestDoubleGraceDB.create_event_log',
        return_value=(500, {}, '{"detail": "Reason 42"}'),
    )
    with pytest.raises(HTTPError) as excinfo:
        await creator.create(None, None, Time.now().gps, 0)
    exc: HTTPError = excinfo.value
    assert exc.response.status_code == 500
    assert 'Reason 42' in exc.response.text


@pytest.mark.xfail
async def test_create_gevent_label_invalid_request(
    mocker: MockerFixture, cache: EventFileCache
) -> None:
    creator = GEventCreator.from_id(GEVENT_ID, TARGET, cache)
    mocker.patch(
        'pytest_gracedb.gracedb.TestDoubleGraceDB.create_event_label',
        return_value=(500, {}, '{"detail": "Reason 42"}'),
    )
    with pytest.raises(HTTPError) as excinfo:
        await creator.create(None, None, Time.now().gps, 0)
    exc: HTTPError = excinfo.value
    assert exc.response.status_code == 500
    assert 'Reason 42' in exc.response.text


def test_time_shift_cwb() -> None:
    original_content = b"""noise:      6.227334e-24 9.412676e-24 1.561057e-23
segment:    1343218196.0000 1343218396.0000 1343218196.0000 1343218396.0000 1343218196.0000 1343218396.0000
start:      1343218303.7500 1343218303.7500 1343218303.7500
time:       1343218303.7875 1343218303.7939 1343218303.7985
stop:       1343218303.8750 1343218303.8750 1343218303.8750
event_time: 1343218303.7875
inj_time:         0.0000       0.0000       0.0000"""
    delta_time = -1.5
    expected_content = b"""noise:      6.227334e-24 9.412676e-24 1.561057e-23
segment:    1343218194.5000 1343218394.5000 1343218194.5000 1343218394.5000 1343218194.5000 1343218394.5000
start:      1343218302.2500 1343218302.2500 1343218302.2500
time:       1343218302.2875 1343218302.2939 1343218302.2985
stop:       1343218302.3750 1343218302.3750 1343218302.3750
event_time: 1343218302.2875
inj_time:         0.0000       0.0000       0.0000"""
    actual_content = CWBEventCreator._shift_original_data(original_content, delta_time)
    assert actual_content == expected_content


def test_time_shift_aframe() -> None:
    original_content = {
        'gpstime': 1432618323.609375,
        'detection_statistic': 1.7362452,
        'far': 0.0003478098339674524,
        'ifos': 'H1,L1',
        'channels': [
            'H1:GDS-CALIB_STRAIN_CLEAN_INJ1_O4Replay',
            'L1:GDS-CALIB_STRAIN_CLEAN_INJ1_O4Replay',
        ],
    }
    delta_time = -1.5
    expected_content = original_content.copy()
    expected_content['gpstime'] = 1432618323.609375 + delta_time
    expected_content_bytes = json.dumps(expected_content).encode()
    original_content_bytes = json.dumps(original_content).encode()
    actual_content = AframeEventCreator._shift_original_data(
        original_content_bytes, delta_time
    )
    assert actual_content == expected_content_bytes


# -------- To be rewriten ---------------------------
# @pytest.mark.parametrize(
#     'content',
#     [
#         b"""noise:      6.227334e-24 9.412676e-24 1.561057e-23
# segment:    1343218196.0000 1343218396.0000 1343218196.0000 1343218396.0000 1343218196.0000 1343218396.0000
# start:      1343218303.7500 1343218303.7500 1343218303.7500
# stop:       1343218303.8750 1343218303.8750 1343218303.8750
# inj_time:         0.0000       0.0000       0.0000""",
#         b"""noise:      6.227334e-24 9.412676e-24 1.561057e-23
# segment:    1343218196.0000 1343218396.0000 1343218196.0000 1343218396.0000 1343218196.0000 1343218396.0000
# start:      1343218303.7500 1343218303.7500 1343218303.7500
# time:       1343218303.7875
# stop:       1343218303.8750 1343218303.8750 1343218303.8750
# inj_time:         0.0000       0.0000       0.0000""",
#         b"""noise:      6.227334e-24 9.412676e-24 1.561057e-23
# segment:    1343218196.0000 1343218396.0000 1343218196.0000 1343218396.0000 1343218196.0000 1343218396.0000
# start:      1343218303.7500 1343218303.7500 1343218303.7500
# time:       1343218303.7875 1343218303.7939 1343218303.7985 1343218303.7985
# stop:       1343218303.8750 1343218303.8750 1343218303.8750
# inj_time:         0.0000       0.0000       0.0000""",
#     ],
# )
# def test_time_shift_cwb_invalid_original_data1(content: bytes) -> None:
#     with pytest.raises(ValueError, match='Could not extract the event times'):
#         CWBEventCreator._shift_original_data(content, 0)


@pytest.mark.parametrize('pipeline_name', ['gstlal', 'mbta', 'pycbc', 'spiir'])
def test_time_shift_cbc(mocked_gracedb: None, pipeline_name: str) -> None:
    pipeline = PIPELINES[pipeline_name]
    data = GraceDb().files(pipeline.gevent_id, pipeline.files[0]).read()
    delta_time = 1.5
    doc: Document = igwn_ligolw.utils.load_fileobj(
        BytesIO(data), contenthandler=ContentHandler
    )
    new_doc: Document = igwn_ligolw.utils.load_fileobj(
        BytesIO(data), contenthandler=ContentHandler
    )
    CBCEventCreator._shift_original_document(new_doc, delta_time)

    table = igwn_ligolw.lsctables.CoincInspiralTable.get_table(doc)
    new_table = igwn_ligolw.lsctables.CoincInspiralTable.get_table(new_doc)
    for row, new_row in zip(table, new_table):
        assert new_row.end == row.end + delta_time

    table = igwn_ligolw.lsctables.SnglInspiralTable.get_table(doc)
    new_table = igwn_ligolw.lsctables.SnglInspiralTable.get_table(new_doc)
    for row, new_row in zip(table, new_table):
        assert new_row.end == row.end + delta_time
        assert new_row.end_time_gmst == lal.GreenwichMeanSiderealTime(
            row.end + delta_time
        )

    arrays = doc.getElementsByTagName('LIGO_LW')
    new_arrays = new_doc.getElementsByTagName('LIGO_LW')
    for array, new_array in zip(arrays, new_arrays):
        if not hasattr(array, 'Name') or array.Name != 'COMPLEX8TimeSeries':
            continue
        assert new_array.childNodes[0].pcdata == array.childNodes[0].pcdata + delta_time


def test_time_shift_external() -> None:
    content = b"""<?xml version='1.0' encoding='UTF-8'?>
<voe:VOEvent xmlns:voe="http://www.ivoa.net/xml/VOEvent/v2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2019-08-17T21:21:20.05_584812348_1-240-TESTEVENT" role="observation" version="2.0" xsi:schemaLocation="http://www.ivoa.net/xml/VOEvent/v2.0  http://www.ivoa.net/xml/VOEvent/VOEvent-v2.0.xsd">
  <Who>
    <AuthorIVORN>ivo://nasa.gsfc.tan/gcn</AuthorIVORN>
    <Author>
      <shortName>Fermi (via VO-GCN)</shortName>
      <contactName>Julie McEnery</contactName>
      <contactPhone>+1-301-286-1632</contactPhone>
      <contactEmail>Julie.E.McEnery@nasa.gov</contactEmail>
    </Author>
    <Date>2022-03-17T14:37:25.840</Date>
    <Description>This VOEvent message was created with GCN VOE version: 1.42 11jun19</Description>
  </Who>
  <WhereWhen>
    <ObsDataLocation>
      <ObservatoryLocation id="GEOLUN"/>
      <ObservationLocation>
        <AstroCoordSystem id="UTC-FK5-GEO"/>
        <AstroCoords coord_system_id="UTC-FK5-GEO">
          <Time unit="s">
            <TimeInstant>
              <ISOTime>2022-03-17T14:37:25.840</ISOTime>
            </TimeInstant>
          </Time>
          <Position2D unit="deg">
            <Name1>RA</Name1>
            <Name2>Dec</Name2>
            <Value2>
              <C1>45.7900</C1>
              <C2>-28.0000</C2>
            </Value2>
            <Error2Radius>0.001</Error2Radius>
          </Position2D>
        </AstroCoords>
      </ObservationLocation>
    </ObsDataLocation>
  <Description>The RA,Dec coordinates are of the type: unavailable/inappropriate.</Description>
  </WhereWhen>
</voe:VOEvent>
"""
    new_content = ExternalEventCreator._shift_original_data(content, 15.0)
    assert b'<Date>2022-03-17T14:37:40.840</Date>' in new_content
    assert b'<ISOTime>2022-03-17T14:37:40.840</ISOTime>' in new_content


def test_time_shift_external_missing() -> None:
    content = b"""<?xml version='1.0' encoding='UTF-8'?>
<voe:VOEvent xmlns:voe="http://www.ivoa.net/xml/VOEvent/v2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2019-08-17T21:21:20.05_584812348_1-240-TESTEVENT" role="observation" version="2.0" xsi:schemaLocation="http://www.ivoa.net/xml/VOEvent/v2.0  http://www.ivoa.net/xml/VOEvent/VOEvent-v2.0.xsd">
  <Who>
    <AuthorIVORN>ivo://nasa.gsfc.tan/gcn</AuthorIVORN>
    <Author>
      <shortName>Fermi (via VO-GCN)</shortName>
      <contactName>Julie McEnery</contactName>
      <contactPhone>+1-301-286-1632</contactPhone>
      <contactEmail>Julie.E.McEnery@nasa.gov</contactEmail>
    </Author>
    <Date>2022-03-17T14:37:25.840</Date>
    <Description>This VOEvent message was created with GCN VOE version: 1.42 11jun19</Description>
  </Who>
</voe:VOEvent>
"""
    with pytest.raises(
        ValueError,
        match=r"No element specified by '\./WhereWhen/ObsDataLocation/ObservationLocation/AstroCoords/Time/TimeInstant/ISOTime'",
    ):
        ExternalEventCreator._shift_original_data(content, 0.0)


def test_filter_uploads_include_all_files() -> None:
    uploads = [Upload('', set(), 'file.txt', 0.0)]
    assert filter_uploads_unless(uploads, True) == uploads


@pytest.mark.parametrize(
    'upload',
    [
        Upload('', {'em_bright'}, 'em_bright.json,0', 0.0),
        Upload('', {'p_astro'}, 'p_astro.json,0', 0.0),
        Upload('', {'sky_loc'}, 'localization.fits,0', 0.0),
        Upload('', {'sky_loc'}, 'localization.fits.gz,0', 0.0),
        Upload('', {'em_bright'}, 'em_bright.json,1', 0.0),
        Upload('', {'p_astro'}, 'p_astro.json,1', 0.0),
        Upload('', {'sky_loc'}, 'localization.fits,1', 0.0),
        Upload('', {'sky_loc'}, 'localization.fits.gz,1', 0.0),
        Upload('', {'em_bright'}, 'file.json,0', 0.0),
        Upload('', {'p_astro'}, 'file.json,0', 0.0),
        Upload('', {'sky_loc'}, 'file.txt,0', 0.0),
        Upload('', {'sky_loc'}, 'file.txt.gz,0', 0.0),
    ],
)
def test_filter_uploads_in(upload: Upload) -> None:
    uploads = [Upload('', set(), 'original_data.txt,0', 0.0), upload]
    assert filter_uploads(uploads) == uploads


@pytest.mark.parametrize(
    'upload',
    [
        Upload('', {'A'}, 'file.txt,0', 0.0),
        Upload('', {'em_bright'}, 'em_bright.png,0', 0.0),
        Upload('', {'p_astro'}, 'p_astro.png,0', 0.0),
        Upload('', {'sky_loc'}, 'localization.png,0', 0.0),
    ],
)
def test_filter_uploads_out(upload: Upload) -> None:
    uploads = [Upload('', set(), 'original_data.txt,0', 0.0), upload]
    assert filter_uploads(uploads) == [uploads[0]]
