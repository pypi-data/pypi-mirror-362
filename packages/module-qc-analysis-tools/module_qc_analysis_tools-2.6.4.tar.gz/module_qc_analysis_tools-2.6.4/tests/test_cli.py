from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from module_qc_analysis_tools.cli import app
from typer.testing import CliRunner


@pytest.fixture()
def base_path():
    return Path() / "module-qc-tools" / "emulator" / "outputs" / "Measurements"


@pytest.fixture()
def data_path():
    return Path() / "src" / "module_qc_analysis_tools" / "data"


@pytest.fixture()
def runner():
    return CliRunner(mix_stderr=False)


def test_data_transmission(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "data-transmission",
            "-i",
            base_path.joinpath("DATA_TRANSMISSION/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? True" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_adc_calibration(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "adc-calibration",
            "-i",
            base_path.joinpath("ADC_CALIBRATION/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? False" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_analog_readback(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "analog-readback",
            "-i",
            base_path.joinpath("ANALOG_READBACK/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? False" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_vcal_calibration(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "vcal-calibration",
            "-i",
            base_path.joinpath("VCAL_CALIBRATION/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? True" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_sldo(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "sldo",
            "-i",
            base_path.joinpath("SLDO/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? False" in caplog.text
        ), f"Failure for chip {chip_id}"


@pytest.mark.parametrize(
    ("measurement", "chip_names", "passes"),
    [
        (
            "Measurements/SLDO/Ishunt0/",
            ["0x14d42", "0x14b6e", "0x14b4d"],
            ["False", "False", "False"],
        )
    ],
    ids=["Ishunt0"],
)
def test_sldo_extra(runner, data_path, caplog, measurement, chip_names, passes):
    """
    Tests additional examples of e.g. bad measurements located under `data_path`
    """
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "sldo",
            "-i",
            data_path / measurement,
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for index, chip_name in enumerate(chip_names):
        assert (
            f"Chip {chip_name} passes QC? {passes[index]}" in caplog.text
        ), f"Failure for chip {chip_name}"


def test_injection_capacitance(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "injection-capacitance",
            "-i",
            base_path.joinpath("INJECTION_CAPACITANCE/1000000001/"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? False" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_lp_mode(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "lp-mode",
            "-i",
            base_path.joinpath("LP_MODE/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? False" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_ov_protection(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "overvoltage-protection",
            "-i",
            base_path.joinpath("OVERVOLTAGE_PROTECTION/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? True" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_undershunt_protection(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "undershunt-protection",
            "-i",
            base_path.joinpath("UNDERSHUNT_PROTECTION/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? True" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_minimum_health(runner, data_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "min-health-test",
            "-i",
            data_path.joinpath("example_scans/info_TEST.json"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert (
        caplog.text.count("Saving output of analysis to") == 4
    ), "Minimum health test failed."


def test_tuning(runner, data_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "tuning",
            "-i",
            data_path.joinpath("example_scans/info_TEST.json"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert caplog.text.count("Saving output of analysis to") == 4, "Tuning test failed."


def test_pixel_failure(runner, data_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "pixel-failure-analysis",
            "-i",
            data_path.joinpath("example_scans/info_TEST.json"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert (
        caplog.text.count("Saving output of analysis to") == 4
    ), "Pixel failure analysis test failed."


@pytest.mark.parametrize(
    ("measurement"),
    [
        pytest.param("1000000001"),
        pytest.param("1000000002"),
        pytest.param("1000000003"),
        pytest.param("1000000004"),
    ],
    ids=["module", "sensor", "nonelec-gui_input", "nonelec-gui_output"],
)
def test_iv_measure(runner, base_path, caplog, tmp_path, measurement):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "iv-measure",
            "-i",
            base_path / "IV_MEASURE" / measurement,
            "-r",
            "src/module_qc_analysis_tools/data/dummy/baremodule_iv.json",
            "-v",
            "DEBUG",
            "-o",
            f"{tmp_path}",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert (
        "Module 20UPGXM1234567 passes QC?" in caplog.text
    ), "Success for module 20UPGXM1234567"


def test_iv_measure_no_ref(runner, base_path, caplog, tmp_path):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "iv-measure",
            "-i",
            base_path.joinpath("IV_MEASURE/1000000001//"),
            "-v",
            "DEBUG",
            "-o",
            f"{tmp_path}",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert (
        "Module 20UPGXM1234567 passes QC?" in caplog.text
    ), "Success for module 20UPGXM1234567"


def test_iv_measure_bareIVNone(runner, base_path, caplog, tmp_path):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "iv-measure",
            "-i",
            base_path.joinpath("IV_MEASURE/1000000001//"),
            "-r",
            "src/module_qc_analysis_tools/data/dummy/baremodule_iv_None.json",
            "-v",
            "DEBUG",
            "-o",
            f"{tmp_path}",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert (
        "Module 20UPGXM1234567 passes QC?" in caplog.text
    ), "Success for module 20UPGXM1234567"


@pytest.mark.parametrize(
    ("fname", "passes"),
    [
        ("20UPGM22110015_pass.json", True),
        ("20UPGM22110015_fail.json", False),
        ("mqt_emulator_v2.2.5rc3.json", True),
    ],
    ids=["20UPGM22110015_pass", "20UPGM22110015_fail", "emulator_pass"],
)
def test_long_term_stability_dcs(runner, datadir, tmp_path, caplog, fname, passes):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "long-term-stability-dcs",
            "-i",
            datadir.joinpath(fname),
            "-v",
            "DEBUG",
            "-o",
            f"{tmp_path}",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert f"passes QC? {passes}" in caplog.text


@pytest.mark.parametrize(
    ("fname", "passes"),
    [
        (
            "FLATNESS_pass.json",
            "True",
        ),
        (
            "FLATNESS_fail.json",
            "False",
        ),
    ],
)
def test_flatness(runner, datadir, tmpdir, caplog, fname, passes):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "flatness",
            "-i",
            datadir.joinpath(fname),
            "-v",
            "DEBUG",
            "-o",
            tmpdir,
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert f"passes QC? {passes}" in caplog.text


def test_flatness_wrong_units(runner, datadir, tmpdir):
    with pytest.raises(AssertionError, match="flatness in μm"):
        runner.invoke(
            app,
            args=[
                "analysis",
                "flatness",
                "-i",
                datadir.joinpath("FLATNESS_fail_units.json"),
                "-v",
                "DEBUG",
                "-o",
                tmpdir,
            ],
            catch_exceptions=False,
        )


def test_no_vddd_saturation(runner, datadir, tmpdir, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "analog-readback",
            "-i",
            datadir.joinpath("VDDD_Saturation_pass.json"),
            "-o",
            tmpdir,
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert (
        "AR_VDDD_SATURATION      :         -1.0        :" in caplog.text
    ), f"Expected 'ARR_VDDD_SATURATION: -1.0' in log, but got : {caplog.text}"


def test_yes_vddd_saturation(runner, datadir, tmpdir, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "analog-readback",
            "-i",
            datadir.joinpath("VDDD_Saturation_fail.json"),
            "-o",
            tmpdir,
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert (
        "AR_VDDD_SATURATION      :         12.0        :" in caplog.text
    ), f"Expected 'AR_VDDD_SATURATION : 12.0 :' in log, but got: {caplog.text}"


@pytest.mark.parametrize(
    ("fname", "passes"),
    [
        (
            "WP_ENVELOPE_pass.json",
            "True",
        ),
        (
            "WP_ENVELOPE_fail.json",
            "False",
        ),
        (
            "20UPGM22211222_WP_ENVELOPE_MODULE-WIREBOND_PROTECTION_RAW.json",
            "True",
        ),
    ],
)
def test_wp_envelope(runner, datadir, tmpdir, caplog, fname, passes):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "wp-envelope",
            "-i",
            datadir.joinpath(fname),
            "-o",
            tmpdir,
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert f"passes QC? {passes}" in caplog.text


@pytest.mark.parametrize(
    ("fname", "passes"),
    [
        (
            "20UPGM23210676_MODULE__WIREBONDING_WIREBOND_PULL_TEST_2025Y06m17d__18_47_50+0000_.json",
            "True",
        ),
    ],
)
def test_wirebond_pull_test(runner, datadir, tmpdir, caplog, fname, passes):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "wirebond-pull-test",
            "-i",
            datadir.joinpath(fname),
            "-o",
            tmpdir,
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert f"passes QC? {passes}" in caplog.text

    match = re.search(r"Saving output of analysis to: (/.+?\.json)", caplog.text)
    assert match, "Could not find the output path in logs."

    json_path = Path(match.group(1))
    assert json_path.exists(), f"File does not exist: {json_path}"

    result = json.loads(json_path.read_text(encoding="utf-8"))

    for key in [
        "WIRE_PULLS",
        "PULL_STRENGTH",
        "PULL_STRENGTH_ERROR",
        "WIRE_BREAKS_5G",
        "PULL_STRENGTH_MIN",
        "PULL_STRENGTH_MAX",
        "HEEL_BREAKS_ON_FE_CHIP",
        "HEEL_BREAKS_ON_PCB",
        "BOND_PEEL",
        "LIFT_OFFS_LESS_THAN_7G",
        # "WIRE_PULLS_WITHOUT_ERROR",
        # "BOND_PEEL_ON_FE_CHIP",
        # "BOND_PEEL_ON_PCB",
        # "MIDSPAN",
        # "WITH_ERROR",
    ]:
        assert isinstance(
            result[0]["results"][key], (float, int)
        ), f"{key} should be numeric"

    assert isinstance(
        result[0]["results"]["DATA_UNAVAILABLE"], bool
    ), "DATA_UNAVAILABLE should be bool type"

    assert isinstance(
        result[0]["results"]["PULL_STRENGTH_DATA"], list
    ), "PULL_STRENGTH_DATA should be list type"
