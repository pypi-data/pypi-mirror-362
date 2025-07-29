import os
from pathlib import Path
import tempfile

import numpy as np
import astropy.units as u
from traitlets.config import Config
import pytest
import tables

from ctapipe.containers import CoordinateFrameType, EventType, PointingMode
from ctapipe.calib.camera.gainselection import ThresholdGainSelector

from ctapipe_io_lst.constants import LST1_LOCATION, N_GAINS, N_PIXELS_MODULE, N_SAMPLES, N_PIXELS
from ctapipe_io_lst import CTAPIPE_GE_0_20, CTAPIPE_GE_0_21, TriggerBits, PixelStatus

test_data = Path(os.getenv('LSTCHAIN_TEST_DATA', 'test_data')).absolute()
test_r0_dir = test_data / 'real/R0/20200218'
test_r0_dvr_dir = test_data / 'real/R0DVR'
test_r0_path = test_r0_dir / 'LST-1.1.Run02006.0004.fits.fz'
test_r0_path_all_streams = test_r0_dir / 'LST-1.1.Run02008.0000_first50.fits.fz'

test_missing_module_path = test_data / 'real/R0/20210215/LST-1.1.Run03669.0000_first50.fits.fz'
test_missing_module_r1v1_path = test_data / 'real/R0/20240310/LST-1.1.Run17016.0000_first10.fits.fz'

test_drive_report = test_data / 'real/monitoring/DrivePositioning/DrivePosition_log_20200218.txt'

calib_version = "ctapipe-v0.17"
calib_path = test_data / 'real/monitoring/PixelCalibration/Cat-A/'
test_calib_path = calib_path / f'calibration/20200218/{calib_version}/calibration_filters_52.Run02006.0000.h5'
test_time_calib_path = calib_path / f'drs4_time_sampling_from_FF/20191124/{calib_version}/time_calibration.Run01625.0000.h5'

# ADC_SAMPLES_SHAPE = (2, 14, 40)


config = Config()
config.LSTEventSouce.EventTimeCalculator.extract_reference = True


def test_loop_over_events():
    from ctapipe_io_lst import LSTEventSource

    n_events = 10
    source = LSTEventSource(
        input_url=test_r0_path,
        max_events=n_events,
        apply_drs4_corrections=False,
        pointing_information=False,
    )

    for i, event in enumerate(source):
        assert event.count == i
        for telid in event.r0.tel.keys():
            n_gains = 2
            n_pixels = source.subarray.tels[telid].camera.geometry.n_pixels
            n_samples = event.lst.tel[telid].svc.num_samples
            waveform_shape = (n_gains, n_pixels, n_samples)
            assert event.r0.tel[telid].waveform.shape == waveform_shape
            assert event.mon.tel[telid].pixel_status.hardware_failing_pixels.shape == (n_gains, n_pixels)

    # make sure max_events works
    assert (i + 1) == n_events


def test_multifile():
    from ctapipe_io_lst import LSTEventSource

    event_count = 0

    with LSTEventSource(
        input_url=test_r0_path_all_streams,
        apply_drs4_corrections=False,
        pointing_information=False,
    ) as source:

        for event in source:
            event_count += 1
            # make sure all events are present and in the correct order
            assert event.index.event_id == event_count

    # make sure we get all events from all streams (50 per stream)
    assert event_count == 200


def test_is_compatible():
    from ctapipe_io_lst import LSTEventSource
    assert LSTEventSource.is_compatible(test_r0_path)


def test_event_source_for_lst_file():
    from ctapipe.io import EventSource

    reader = EventSource(test_r0_path)

    # import here to see if ctapipe detects plugin
    from ctapipe_io_lst import LSTEventSource

    assert isinstance(reader, LSTEventSource)
    assert reader.input_url == test_r0_path


def test_subarray():
    from ctapipe_io_lst import LSTEventSource

    source = LSTEventSource(test_r0_path)
    subarray = source.subarray
    subarray.info()
    subarray.to_table()

    assert source.lst_service.telescope_id == 1
    assert source.lst_service.num_modules == 265

    position = source.subarray.positions[1]
    mc_position = [-6.336, 60.405, 12.5] * u.m

    # mc uses slightly different reference location and z is off
    # so only test x/y distance
    distance = np.linalg.norm(mc_position[:2] - position[:2])
    assert distance < 0.6 * u.m

    with tempfile.NamedTemporaryFile(suffix='.h5') as f:
        subarray.to_hdf(f.name)


def test_missing_modules():
    from ctapipe_io_lst import LSTEventSource
    source = LSTEventSource(
        test_missing_module_path,
        apply_drs4_corrections=False,
        pointing_information=False,
    )

    assert source.lst_service.telescope_id == 1
    assert source.lst_service.num_modules == 264

    fill = np.iinfo(np.uint16).max
    for event in source:
        # one module missing, so 7 pixels
        assert np.count_nonzero(event.mon.tel[1].pixel_status.hardware_failing_pixels) == N_PIXELS_MODULE * N_GAINS
        assert np.count_nonzero(event.r0.tel[1].waveform == fill) == N_PIXELS_MODULE * N_SAMPLES * N_GAINS

        # 514 is one of the missing pixels
        assert np.all(event.r0.tel[1].waveform[:, 514] == fill)


def test_missing_modules_r1v1():
    from ctapipe_io_lst import LSTEventSource
    source = LSTEventSource(
        test_missing_module_r1v1_path,
        apply_drs4_corrections=False,
        pointing_information=False,
    )

    assert source.lst_service.telescope_id == 1
    assert source.lst_service.num_modules == 264

    n_events = 0
    for event in source:
        n_events += 1
        # one module missing, so 7 pixels
        assert np.count_nonzero(event.mon.tel[1].pixel_status.hardware_failing_pixels) == N_PIXELS_MODULE * N_GAINS
        assert np.count_nonzero(event.r0.tel[1].waveform == 0.0) == N_PIXELS_MODULE * N_SAMPLES * N_GAINS

        missing_gain, missing_pixel = np.nonzero(event.mon.tel[1].pixel_status.hardware_failing_pixels)
        # 514 is one of the missing pixels
        for gain, pixel in zip(missing_gain, missing_pixel):
            np.testing.assert_equal(event.r0.tel[1].waveform[gain, pixel], 0.0)

        if CTAPIPE_GE_0_20:
            np.testing.assert_equal(event.lst.tel[1].evt.pixel_status, event.r1.tel[1].pixel_status)

    assert n_events == 40


def test_gain_selected():
    from ctapipe_io_lst import LSTEventSource

    config = Config(dict(
        LSTEventSource=dict(
            default_trigger_type='tib',  # ucts unreliable in this run
            apply_drs4_corrections=True,
            pointing_information=False,
            use_flatfield_heuristic=True,
            LSTR0Corrections=dict(
                apply_drs4_pedestal_correction=False,
                apply_spike_correction=False,
                apply_timelapse_correction=False,
                offset=400,
            )
        )
    ))

    source = LSTEventSource(
        test_r0_dir / 'LST-1.1.Run02008.0000_first50_gainselected.fits.fz',
        config=config,
    )
    original_source = LSTEventSource(
        test_r0_dir / 'LST-1.1.Run02008.0000_first50.fits.fz',
        config=config,
    )
    gain_selector = ThresholdGainSelector(threshold=3500)
    for event, original_event in zip(source, original_source):
        if event.trigger.event_type in {EventType.FLATFIELD, EventType.SKY_PEDESTAL}:
            assert event.r0.tel[1].waveform is not None
            assert event.r0.tel[1].waveform.shape == (N_GAINS, N_PIXELS, N_SAMPLES)
            assert event.r1.tel[1].waveform is not None
            assert event.r1.tel[1].waveform.shape == (N_GAINS, N_PIXELS, N_SAMPLES - 4)
        else:
            if event.r0.tel[1].waveform is not None:
                assert event.r0.tel[1].waveform.shape == (N_GAINS, N_PIXELS, N_SAMPLES)

            if CTAPIPE_GE_0_21:
                assert event.r1.tel[1].waveform.shape == (1, N_PIXELS, N_SAMPLES - 4)
            else:
                assert event.r1.tel[1].waveform.shape == (N_PIXELS, N_SAMPLES - 4)

            # compare to original file
            selected_gain = gain_selector(original_event.r1.tel[1].waveform)
            pixel_idx = np.arange(N_PIXELS)
            waveform = original_event.r1.tel[1].waveform[selected_gain, pixel_idx]
            assert np.allclose(event.r1.tel[1].waveform, waveform)

    assert event.count == 199



def test_dvr():
    from ctapipe_io_lst import LSTEventSource

    config = Config(dict(
        LSTEventSource=dict(
            default_trigger_type='tib',  # ucts unreliable in this run
            apply_drs4_corrections=True,
            pointing_information=False,
            use_flatfield_heuristic=True,
            LSTR0Corrections=dict(
                apply_drs4_pedestal_correction=False,
                apply_spike_correction=False,
                apply_timelapse_correction=False,
                offset=400,
            )
        )
    ))

    dvr_source = LSTEventSource(
        test_r0_dvr_dir / 'LST-1.1.Run02008.0100_first50.fits.fz',
        config=config,
    )
    original_source = LSTEventSource(
        test_r0_dir / 'LST-1.1.Run02008.0100_first50.fits.fz',
        config=config,
    )
    gain_selector = ThresholdGainSelector(threshold=3500)
    for dvr_event, original_event in zip(dvr_source, original_source):
        if dvr_event.trigger.event_type in {EventType.FLATFIELD, EventType.SKY_PEDESTAL}:
            assert dvr_event.r0.tel[1].waveform is not None
            assert dvr_event.r0.tel[1].waveform.shape == (N_GAINS, N_PIXELS, N_SAMPLES)
            assert dvr_event.r1.tel[1].waveform is not None
            assert dvr_event.r1.tel[1].waveform.shape == (N_GAINS, N_PIXELS, N_SAMPLES - 4)
        else:
            if dvr_event.r0.tel[1].waveform is not None:
                assert dvr_event.r0.tel[1].waveform.shape == (N_GAINS, N_PIXELS, N_SAMPLES)

            if CTAPIPE_GE_0_21:
                assert dvr_event.r1.tel[1].waveform.shape == (1, N_PIXELS, N_SAMPLES - 4)
            else:
                assert dvr_event.r1.tel[1].waveform.shape == (N_PIXELS, N_SAMPLES - 4)

            # compare to original file
            selected_gain = gain_selector(original_event.r1.tel[1].waveform)
            pixel_idx = np.arange(N_PIXELS)
            waveform = original_event.r1.tel[1].waveform[selected_gain, pixel_idx]

            readout_pixels = (dvr_event.lst.tel[1].evt.pixel_status & np.uint8(PixelStatus.DVR_STATUS)) > 0

            if CTAPIPE_GE_0_21:
                assert np.allclose(dvr_event.r1.tel[1].waveform[:, readout_pixels], waveform[readout_pixels])
            else:
                assert np.allclose(dvr_event.r1.tel[1].waveform[readout_pixels], waveform[readout_pixels])

    assert dvr_event.count == 199


def test_pointing_info():

    from ctapipe_io_lst import LSTEventSource

    # test source works when not requesting pointing info
    with LSTEventSource(
        test_r0_dir / 'LST-1.1.Run02008.0000_first50.fits.fz',
        apply_drs4_corrections=False,
        pointing_information=False,
        max_events=1
    ) as source:
        for e in source:
            assert np.isnan(e.pointing.tel[1].azimuth)

    # test we get an error when requesting pointing info but nor drive report given
    with pytest.raises(ValueError):
        with LSTEventSource(
            test_r0_dir / 'LST-1.1.Run02008.0000_first50.fits.fz',
            apply_drs4_corrections=False,
            max_events=1
        ) as source:
            next(iter(source))


    config = {
        'LSTEventSource': {
            'apply_drs4_corrections': False,
            'max_events': 1,
            'PointingSource': {
                'drive_report_path': str(test_drive_report)
            },
        },
    }

    with LSTEventSource(
        test_r0_dir / 'LST-1.1.Run02008.0000_first50.fits.fz',
        config=Config(config),
    ) as source:

        sb = source.scheduling_blocks[2008]
        assert sb.sb_id == 2008
        assert sb.pointing_mode is PointingMode.TRACK

        obs = source.observation_blocks[2008]
        assert u.isclose(obs.subarray_pointing_lon, 83.6296 * u.deg)
        assert u.isclose(obs.subarray_pointing_lat, 22.0144 * u.deg)
        assert obs.subarray_pointing_frame is CoordinateFrameType.ICRS
        assert obs.producer_id == "LST-1"
        assert obs.obs_id == 2008
        assert obs.sb_id == 2008

        for e in source:
            assert u.isclose(e.pointing.array_ra, 83.6296 * u.deg)
            assert u.isclose(e.pointing.array_dec, 22.0144 * u.deg)

            expected_alt = (90 - 7.03487) * u.deg
            assert u.isclose(e.pointing.tel[1].altitude.to(u.deg), expected_alt, rtol=1e-2)

            expected_az = 197.318 * u.deg
            assert u.isclose(e.pointing.tel[1].azimuth.to(u.deg), expected_az, rtol=1e-2)



def test_pedestal_events(tmp_path):
    from ctapipe_io_lst import LSTEventSource

    path = tmp_path / 'pedestal_events.h5'
    with tables.open_file(path, 'w') as f:
        data = np.array([(2008, 5), (2008, 11)], dtype=[('obs_id', int), ('event_id', int)])
        f.create_table('/', 'interleaved_pedestal_ids', obj=data)

    with LSTEventSource(
        test_r0_dir / 'LST-1.1.Run02008.0000_first50.fits.fz',
        pedestal_ids_path=path,
        apply_drs4_corrections=False,
        pointing_information=False,
    ) as source:
        for event in source:
            if event.index.event_id in {5, 11}:
                assert event.trigger.event_type == EventType.SKY_PEDESTAL
            else:
                assert event.trigger.event_type != EventType.SKY_PEDESTAL

            if CTAPIPE_GE_0_20:
                assert event.r1.tel[1].event_type == event.trigger.event_type


@pytest.mark.parametrize(
    "trigger_bits,expected_type",
    [
        (TriggerBits.MONO, EventType.SUBARRAY),
        (TriggerBits.MONO | TriggerBits.STEREO, EventType.SUBARRAY),
        (TriggerBits.MONO | TriggerBits.PEDESTAL, EventType.UNKNOWN),
        (TriggerBits.STEREO, EventType.SUBARRAY),
        (TriggerBits.CALIBRATION, EventType.FLATFIELD),
        (TriggerBits.CALIBRATION | TriggerBits.PEDESTAL, EventType.UNKNOWN),
        (TriggerBits.CALIBRATION | TriggerBits.MONO, EventType.FLATFIELD),
        (TriggerBits.PEDESTAL, EventType.SKY_PEDESTAL),
    ]
)
def test_trigger_bits_to_event_type(trigger_bits, expected_type):
    from ctapipe_io_lst import LSTEventSource

    event_type = LSTEventSource._event_type_from_trigger_bits(trigger_bits)
    assert event_type == expected_type



def test_reference_position():
    from ctapipe_io_lst import LSTEventSource
    from ctapipe.coordinates import GroundFrame

    subarray = LSTEventSource.create_subarray()

    ground = GroundFrame(*subarray.positions[1], reference_location=subarray.reference_location)
    position = ground.to_earth_location()

    assert u.isclose(position.lat, LST1_LOCATION.lat)
    assert u.isclose(position.lon, LST1_LOCATION.lon)
    assert u.isclose(position.height, LST1_LOCATION.height)


@pytest.mark.parametrize("timeshift", (-5, 70))
def test_time_correction(timeshift):
    from ctapipe_io_lst import LSTEventSource
    config = {
        'LSTEventSource': {
            'input_url': test_r0_path_all_streams,
            'apply_drs4_corrections': False,
            'pointing_information': False,
            'max_events': 5,
        },
    }

    original = LSTEventSource(config=Config(config))
    shifted = LSTEventSource(config=Config(config), event_time_correction_s=timeshift)

    with original, shifted:
        for event, event_shifted in zip(original, shifted):
            dt = event_shifted.trigger.time - event.trigger.time
            dt_tel = event_shifted.trigger.tel[1].time - event.trigger.tel[1].time
            assert u.isclose(dt.to_value(u.s), timeshift)
            assert u.isclose(dt_tel.to_value(u.s), timeshift)


def test_evb_calibrated_data():
    from ctapipe_io_lst import LSTEventSource
    input_url = test_data / 'real/R0/20231219/LST-1.1.Run16255.0000_first50.fits.fz'

    config = {
        'LSTEventSource': {
            "pointing_information": False,
            'LSTR0Corrections': {
                'drs4_time_calibration_path': str(test_time_calib_path),
                'calibration_path': str(test_calib_path),
            },
        },
    }

    with LSTEventSource(input_url, config=Config(config)) as source:
        read_events = 0
        for e in source:
            read_events += 1
            assert np.all(e.calibration.tel[1].dl1.time_shift != 0)

        assert read_events == 200


def test_arbitrary_filename(tmp_path):
    from ctapipe_io_lst import LSTEventSource
    path = tmp_path / "some_name_not_matching_the_lst_pattern.fits.fz"
    path.write_bytes(test_r0_path_all_streams.read_bytes())

    assert LSTEventSource.is_compatible(path)

    with LSTEventSource(path, pointing_information=False, apply_drs4_corrections=False) as source:
        n_read = 0
        for _ in source:
            n_read += 1
        assert n_read == 50
