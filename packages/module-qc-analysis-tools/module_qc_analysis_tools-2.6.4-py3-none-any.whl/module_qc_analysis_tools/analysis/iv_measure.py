from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
from module_qc_data_tools import (
    get_sensor_type_from_layer,
)

from module_qc_analysis_tools import data as data_path
from module_qc_analysis_tools.utils.analysis import (
    depletion_voltage_default,
    find_breakdown_and_current,
    make_iv_plots,
    module_sensor_area,
    normalise_current,
    operation_voltage,
    perform_qc_analysis,
    update_iv_cuts,
)
from module_qc_analysis_tools.utils.misc import (
    bcolors,
    get_qc_config,
)

TEST_TYPE = Path(__file__).stem.upper()

log = logging.getLogger("analysis")


def analyse(
    iv_array,
    depl_volt,
    module_sn,
    layer,
    ref=None,
    temp=None,
    qc_criteria_path=None,
):
    sensor_type = get_sensor_type_from_layer(layer)
    is3Dmodule = "3D" in sensor_type
    cold = False
    qc_config = get_qc_config(
        qc_criteria_path or data_path / "analysis_cuts.json", TEST_TYPE
    )

    #  check input IV array
    for key in ["voltage", "current", "sigma current"]:
        iv_array[key] = [abs(value) for value in iv_array[key]]

    normalised_current = []

    if len(iv_array["voltage"]) == len(iv_array["temperature"]):
        normalised_current = normalise_current(
            iv_array["current"], iv_array["temperature"]
        )
        cold = np.average(iv_array["temperature"]) < 0
    elif len(iv_array["temperature"]) > 0:
        normalised_current = normalise_current(
            iv_array["current"],
            len(iv_array["current"]) * [np.average(iv_array["temperature"])],
        )
        cold = np.average(iv_array["temperature"]) < 0
    elif temp is not None:
        log.warning(
            bcolors.WARNING
            + f" No temperature array recorded, using {temp}degC."
            + bcolors.ENDC
        )
        normalised_current = normalise_current(
            iv_array["current"], len(iv_array["current"]) * [temp]
        )
        cold = temp < 0
    else:
        log.warning(
            bcolors.WARNING
            + " No temperature recorded, cannot normalise to 20 degC."
            + bcolors.ENDC
        )

    if cold:
        normalised_current = iv_array["current"]

    #  check reference IV data
    if ref is not None:
        try:
            ref["reference_IVs"]
        except Exception as fail:
            log.warning(
                bcolors.WARNING + f" No reference IVs found: {fail}" + bcolors.ENDC
            )

            if is3Dmodule and len(ref["reference_IVs"]) == 3:
                log.debug(" Found 3 bare single IVs for triplet.")
            elif not is3Dmodule and len(ref["reference_IVs"]) == 1:
                log.debug(" Found one bare quad IV.")
            else:
                log.error(
                    bcolors.ERROR
                    + " Incorrect number of reference IVs found \U0001F937"
                    + bcolors.ENDC
                )

            for item in ref["reference_IVs"]:
                if not (
                    item["Vbd"]
                    and item["Vfd"]
                    and item["temperature"]
                    and item["IV_ARRAY"]
                ):
                    log.error(
                        bcolors.ERROR
                        + ' Key words missing in "reference_IVs"'
                        + bcolors.ENDC
                    )

    #  get values
    area = module_sensor_area(layer)

    #  depletion voltage, operation voltage
    ## sensor measurement range is 0V to 200V (planar)
    Vdepl = 0
    if depl_volt is not None and abs(depl_volt) > 0 and abs(depl_volt) < 200:
        Vdepl = abs(depl_volt)
        log.info(f" Using manual input depletion voltage {Vdepl}V.")
    elif ref is not None:
        try:
            tmp_vfd = max(abs(v["Vfd"]) for v in ref["reference_IVs"])
            if 0 < tmp_vfd < 200:
                Vdepl = tmp_vfd
                log.info(f" Found depletion voltage from sensor data: {Vdepl}V.")
            else:
                log.warning(
                    bcolors.WARNING
                    + f" Depletion voltage provided in the bare module IV is not valid: {tmp_vfd}V. Proceed using default value!"
                    + bcolors.ENDC
                )
        except KeyError:
            depl_volt = None
            log.warning(
                bcolors.WARNING
                + " No depletion voltage found in bare module IV."
                + bcolors.ENDC
            )

    if Vdepl == 0:
        Vdepl = depletion_voltage_default(is3Dmodule)
        log.warning(
            bcolors.WARNING
            + f" No valid depletion voltage provided, proceed using default value of {Vdepl}V."
            + bcolors.ENDC
        )

    ## same for sensor and module
    Vop = operation_voltage(Vdepl, is3Dmodule)

    #  breakdown voltage and leakage current at operation voltage from previous stage
    ## *0 values are from previous stage (bare module reception)
    Vbd0 = None  ## get from bare module stage below
    Ilc0 = 0

    if ref is not None:
        Vbd0 = min(v["Vbd"] for v in ref["reference_IVs"])
        for iv in ref["reference_IVs"]:
            for index, v in enumerate(iv["IV_ARRAY"]["voltage"]):
                if v >= Vop:
                    temperatures = iv["IV_ARRAY"]["temperature"] or []
                    voltages = iv["IV_ARRAY"]["voltage"]
                    _temp = 23
                    if not temperatures:
                        log.warning(
                            f" No temperature array found for bare module {iv['component_sn']}"
                        )
                        try:
                            _temp: float = (
                                temperatures[index]
                                if len(temperatures) == len(voltages)
                                else iv["temperature"]
                            )
                        except Exception:
                            _temp: float = iv["temperature"]

                    Ilc0 += normalise_current(
                        iv["IV_ARRAY"]["current"][index], _temp
                    )  ## += for triplets

                    break

        log.debug(f"Ilc0: {Ilc0}uA at {Vop}V")

    #  breakdown voltage and leakage current at operation voltage
    Vbd = -999  ## -999V if no breakdown occurred during the measurement
    Ilc = 0

    # Finding breakdown voltage and leakage current at operation voltage
    Vbd, Ilc = find_breakdown_and_current(
        iv_array["voltage"], normalised_current, Vdepl, Vop, is3Dmodule
    )

    fig = make_iv_plots(module_sn, iv_array, normalised_current, Vbd, temp, cold, ref)

    qc_config = update_iv_cuts(qc_config, layer, Vdepl)

    # # "IV_ARRAY", "IV_IMG", "BREAKDOWN_VOLTAGE", "LEAK_CURRENT", "MAXIMUM_VOLTAGE", "NO_BREAKDOWN_VOLTAGE_OBSERVED"
    results = {}
    results["IV_ARRAY"] = iv_array
    # results["IV_IMG"] ?? ## Required for sensor but not for module
    results["BREAKDOWN_VOLTAGE"] = Vbd
    results["BREAKDOWN_REDUCTION"] = Vbd0 - Vbd if Vbd0 else -999

    results["NO_BREAKDOWN_VOLTAGE_OBSERVED"] = True
    if Vbd != -999:
        results["NO_BREAKDOWN_VOLTAGE_OBSERVED"] = False
    results["MAXIMUM_VOLTAGE"] = max(iv_array["voltage"])
    results["LEAK_CURRENT"] = Ilc
    results["LEAK_INCREASE_FACTOR"] = Ilc / Ilc0 if Ilc0 else -999
    results["LEAK_PER_AREA"] = Ilc / area

    passes_qc, summary, rounded_results = perform_qc_analysis(
        TEST_TYPE, qc_config, layer, results
    )

    return rounded_results, passes_qc, summary, fig
