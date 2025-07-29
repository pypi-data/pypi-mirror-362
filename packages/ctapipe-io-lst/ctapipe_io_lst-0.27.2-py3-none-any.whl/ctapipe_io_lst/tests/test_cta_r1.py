import os
import socket
from pathlib import Path
from contextlib import ExitStack

import pytest
import numpy as np
from astropy.time import Time
import astropy.units as u
from traitlets.config import Config

from ctapipe.io import EventSource
from ctapipe.image.toymodel import WaveformModel, Gaussian
from ctapipe.containers import EventType

import protozfits
from protozfits.R1v1_pb2 import CameraConfiguration, Event, TelescopeDataStream
from protozfits.R1v1_debug_pb2 import DebugEvent, DebugCameraConfiguration

try:
    # protozfits < 2.7.1
    from protozfits.any_array_to_numpy import numpy_to_any_array
except ModuleNotFoundError:
    # current protozfits
    from protozfits.anyarray import numpy_to_any_array

from ctapipe_io_lst import LSTEventSource, CTAPIPE_GE_0_21
from ctapipe_io_lst.constants import CLOCK_FREQUENCY_KHZ, TriggerBits
from ctapipe_io_lst.event_time import time_to_cta_high
from ctapipe_io_lst.evb_preprocessing import EVBPreprocessingFlag
from ctapipe_io_lst.anyarray_dtypes import CDTS_AFTER_37201_DTYPE, TIB_DTYPE


test_data = Path(os.getenv('LSTCHAIN_TEST_DATA', 'test_data'))
test_drs4_pedestal_path = test_data / 'real/monitoring/PixelCalibration/LevelA/drs4_baseline/20200218/v0.8.2.post2.dev48+gb1343281/drs4_pedestal.Run02005.0000.h5'


subarray = LSTEventSource.create_subarray(tel_id=1)
GEOMETRY = subarray.tel[1].camera.geometry
pulse_shape = subarray.tel[1].camera.readout.reference_pulse_shape[0]
if CTAPIPE_GE_0_21:
    pulse_shape = pulse_shape[np.newaxis, ...]

waveform_model = WaveformModel(
    reference_pulse=pulse_shape,
    reference_pulse_sample_width=subarray.tel[1].camera.readout.reference_pulse_sample_width,
    sample_width=1 * u.ns,
)


def weighted_average(a, b, weight_a, weight_b):
    return (a * weight_a + b * weight_b) / (weight_a + weight_b)


def create_shower(rng):
    x = rng.uniform(-0.5, 0.5) * u.m
    y = rng.uniform(-0.5, 0.5) * u.m
    width = rng.uniform(0.01, 0.05) * u.m
    length = rng.uniform(2 * width.to_value(u.m), 5 * width.to_value(u.m)) * u.m
    psi = rng.uniform(0, 360) * u.deg


    area = np.pi * (width.to_value(u.m) * length.to_value(u.m))
    intensity = 5e4 * area + 2e6 * area**2

    model = Gaussian(x, y, length, width, psi)
    image, signal, noise = model.generate_image(GEOMETRY, intensity=intensity, nsb_level_pe=3)

    long = (GEOMETRY.pix_x - x) * np.cos(psi) + (GEOMETRY.pix_y - y) * np.sin(psi)

    peak_time = rng.uniform(0, 40, size=len(GEOMETRY))
    signal_peak_time = np.clip(20 + 30 * (long / (3 * u.m)).to_value(u.one), 0, 40)

    mask = signal > 0
    peak_time[mask] = weighted_average(
        peak_time[mask], signal_peak_time[mask], noise[mask], signal[mask]
    )

    return image, peak_time


def create_waveform(image, peak_time, num_samples=40, gains=(86, 5), offset=400):
    r1 = waveform_model.get_waveform(image, peak_time, num_samples)
    if CTAPIPE_GE_0_21:
        r1 = r1[0]
    return np.array([r1 * gain + offset for gain in gains]).astype(np.uint16)


def create_flat_field(rng):
    image = rng.uniform(65, 75, len(GEOMETRY))
    peak_time = rng.uniform(18, 22, len(GEOMETRY))
    return image, peak_time

def create_pedestal(rng):
    image = rng.uniform(-2, 2, len(GEOMETRY))
    peak_time = rng.uniform(0, 40, len(GEOMETRY))
    return image, peak_time



@pytest.fixture(scope="session")
def dummy_cta_r1_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("dummy_cta_r1")


@pytest.fixture(scope="session")
def dummy_cta_r1(dummy_cta_r1_dir):
    # with protozfits.File("test_data/real/R0/20200218/LST-1.1.Run02006.0004.fits.fz") as f:
    # old_camera_config = f.CameraConfig[0]

    stream_paths = [
        dummy_cta_r1_dir / "LST-1.1.Run10000.0000.fits.fz",
        dummy_cta_r1_dir / "LST-1.2.Run10000.0000.fits.fz",
        dummy_cta_r1_dir / "LST-1.3.Run10000.0000.fits.fz",
        dummy_cta_r1_dir / "LST-1.4.Run10000.0000.fits.fz",
    ]

    num_samples = 40
    num_pixels = 1855
    num_modules = 265
    ucts_address = np.frombuffer(socket.inet_pton(socket.AF_INET, "10.0.100.123"), dtype=np.uint32)[0]

    run_start = Time("2023-05-16T16:06:31.123")

    # trigger dependent processing definition
    # tdp_type is a list of TriggerBits
    # tdp_action is the bit pattern of pre-processing steps to apply
    # to the corresponding tdp_type. 
    tdp_type = np.zeros(15, dtype=np.uint16)
    tdp_action = np.zeros(16, dtype=np.uint16)

    # tdp_action[0] is the default for unknown trigger bits 
    tdp_action[0] = EVBPreprocessingFlag.BASELINE_SUBTRACTION | EVBPreprocessingFlag.GAIN_SELECTION
    # tdp_action[i] corresponds to tdp_type[i - 1]
    # physics (mono for now)
    tdp_type[0] = TriggerBits.MONO
    tdp_action[1] = EVBPreprocessingFlag.BASELINE_SUBTRACTION | EVBPreprocessingFlag.GAIN_SELECTION
    # flat field events
    tdp_type[1] = TriggerBits.CALIBRATION
    tdp_action[2] = EVBPreprocessingFlag.BASELINE_SUBTRACTION
    tdp_type[2] = TriggerBits.CALIBRATION | TriggerBits.MONO
    tdp_action[3] = EVBPreprocessingFlag.BASELINE_SUBTRACTION
    # pedestal events
    tdp_type[3] = TriggerBits.PEDESTAL
    tdp_action[4] = EVBPreprocessingFlag.BASELINE_SUBTRACTION


    camera_config = CameraConfiguration(
        tel_id=1,
        local_run_id=10000,
        config_time_s=run_start.unix,
        camera_config_id=1,
        num_modules=num_modules,
        num_pixels=num_pixels,
        num_channels=2,
        data_model_version="1.0",
        num_samples_nominal=num_samples,
        pixel_id_map=numpy_to_any_array(np.arange(num_pixels).astype(np.uint16)),
        module_id_map=numpy_to_any_array(np.arange(num_modules).astype(np.uint16)),

        debug=DebugCameraConfiguration(
            cs_serial="???",
            evb_version="evb-dummy",
            cdhs_version="evb-dummy",
            tdp_type=numpy_to_any_array(tdp_type),
            tdp_action=numpy_to_any_array(np.zeros(16, dtype=np.uint16)),
            # at the moment, the tdp_action and ttype_pattern fields are mixed up in EVB
            ttype_pattern=numpy_to_any_array(tdp_action),
        )
    )

    # assume evb did no pe calibration
    data_stream = TelescopeDataStream(sb_id=10000, obs_id=10000, waveform_offset=400, waveform_scale=1)

    rng = np.random.default_rng()

    streams = []
    with ExitStack() as stack:
        for stream_path in stream_paths:
            stream = stack.enter_context(protozfits.ProtobufZOFits(n_tiles=5, rows_per_tile=20, compression_block_size_kb=64 * 1024))
            stream.open(str(stream_path))
            stream.move_to_new_table("DataStream")
            stream.write_message(data_stream)
            stream.move_to_new_table("CameraConfiguration")
            stream.write_message(camera_config)
            stream.move_to_new_table("Events")
            streams.append(stream)

        event_time = run_start
        event_rate = 8000 / u.s

        module_hires_local_clock_counter = np.zeros(num_modules, dtype=np.uint64)
        for event_count in range(100):
            if event_count % 20 == 18:
                # flatfield
                event_type = 0
                trigger_type = 0b0000_0001
                image, peak_time = create_flat_field(rng)
            elif event_count % 20 == 19:
                # pedestal
                event_type = 2
                trigger_type = 0b0100_0000
                image, peak_time = create_pedestal(rng)
            else:
                # air shower
                event_type = 32
                trigger_type = 0b0000_0100
                image, peak_time = create_shower(rng)

            delta = rng.exponential(1 / event_rate.to_value(1 / u.s)) * u.s
            event_time = event_time + delta
            event_time_s, event_time_qns = time_to_cta_high(event_time)

            waveform = create_waveform(image, peak_time, num_samples)

            if event_type == 32:
                num_channels = 1
                pixel_status = rng.choice([0b1000, 0b0100], p=[0.001, 0.999], size=num_pixels).astype(np.uint8)

                low_gain = pixel_status == 0b1000
                gain_selected_waveform = waveform[0].copy()
                gain_selected_waveform[low_gain] = waveform[1, low_gain]
                waveform = gain_selected_waveform
            else:
                num_channels = 2
                pixel_status = np.full(num_pixels, 0b1100, dtype=np.uint8)

            first_cell_id = rng.choice(4096, size=2120).astype(np.uint8)

            jitter = rng.choice([-2, 1, 0, 1, -2], size=num_modules)
            module_hires_local_clock_counter[:] += np.uint64(CLOCK_FREQUENCY_KHZ * delta.to_value(u.ms) + jitter)

            # uint64 unix_tai, whole ns
            timestamp = np.uint64(event_time_s) * np.uint64(1e9) + np.uint64(np.round(event_time_qns / 4.0))
            cdts_data = (
                timestamp,
                ucts_address,
                event_count + 1, # event_counter
                0, # busy_counter
                0, # pps_counter
                0, # clock_counter
                trigger_type, # trigger_type
                0, # white_rabbit_status
                0, # stereo_pattern
                event_count % 10, # num_in_bunch
                1234, # cdts_version
            )
            cdts_data = np.array([cdts_data], dtype=CDTS_AFTER_37201_DTYPE)

            tib_data = (
                event_count + 1,
                0,  # pps_counter
                0,  # tenMHz_counter
                0,  # stereo pattern
                trigger_type,
            )
            tib_data = np.array([tib_data], dtype=TIB_DTYPE)

            event = Event(
                event_id=event_count + 1,
                tel_id=1,
                local_run_id=10000,
                event_type=event_type,
                event_time_s=int(event_time_s),
                event_time_qns=int(event_time_qns),
                num_channels=num_channels,
                num_pixels=num_pixels,
                num_samples=num_samples,
                pixel_status=numpy_to_any_array(pixel_status),
                waveform=numpy_to_any_array(waveform),
                first_cell_id=numpy_to_any_array(first_cell_id),
                module_hires_local_clock_counter=numpy_to_any_array(module_hires_local_clock_counter),
                debug=DebugEvent(
                    module_status=numpy_to_any_array(np.ones(num_modules, dtype=np.uint8)),
                    extdevices_presence=0b011,
                    cdts_data=numpy_to_any_array(cdts_data.view(np.uint8)),
                    tib_data=numpy_to_any_array(tib_data.view(np.uint8)),
                )
            )


            streams[event_count % len(streams)].write_message(event)

    return stream_paths[0]


def test_is_compatible(dummy_cta_r1):
    from ctapipe_io_lst import LSTEventSource
    assert LSTEventSource.is_compatible(dummy_cta_r1)


def test_no_calibration(dummy_cta_r1):
    with EventSource(dummy_cta_r1, apply_drs4_corrections=False, pointing_information=False) as source:
        n_events = 0
        for e in source:
            n_events += 1
        assert n_events == 100


def test_drs4_calibration(dummy_cta_r1):
    config = Config({
        'LSTEventSource': {
            'pointing_information': False,
            'LSTR0Corrections': {
                'drs4_pedestal_path': test_drs4_pedestal_path,
            },
        },
    })

    with EventSource(dummy_cta_r1, config=config) as source:
        n_events = 0
        for e in source:
            if e.trigger.event_type is EventType.SUBARRAY:
                n_channels = 1
            else:
                n_channels = 2

            assert e.r0.tel[1].waveform.dtype == np.uint16
            assert e.r0.tel[1].waveform.shape == (n_channels, 1855, 40)

            assert e.r1.tel[1].waveform.dtype == np.float32
            if e.trigger.event_type is EventType.SUBARRAY:
                if CTAPIPE_GE_0_21:
                    assert e.r1.tel[1].waveform.shape == (1, 1855, 36)
                else:
                    assert e.r1.tel[1].waveform.shape == (1855, 36)
            else:
                assert e.r1.tel[1].waveform.shape == (2, 1855, 36)

            n_events += 1
        assert n_events == 100


test_files = [
    "20231214/LST-1.1.Run16102.0000_first50.fits.fz",  # has only baseline enabled
    "20231218/LST-1.1.Run16231.0000_first50.fits.fz",  # baseline + gain selection for physics
    "20231219/LST-1.1.Run16255.0000_first50.fits.fz",  # all corrections + gain selection for physics
]


@pytest.mark.parametrize("test_file", test_files)
def test_read_real_files(test_file):
    config = Config({
        'LSTEventSource': {
            'pointing_information': False,
            'apply_drs4_corrections': False,
        },
    })

    with EventSource(test_data / "real/R0" / test_file, config=config) as source:
        n_read = 0
        for _ in source:
            n_read += 1

        assert n_read == 200
