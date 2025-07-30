from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

import typer
from module_qc_data_tools import (
    __version__,
    load_json,
    outputDataFrame,
    qcDataFrame,
    save_dict_list,
)

from module_qc_analysis_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)
from module_qc_analysis_tools.utils.misc import (
    get_inputs,
)

app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def main(
    input_meas: Path = OPTIONS["input_meas"],
    base_output_dir: Path = OPTIONS["output_dir"],
    verbosity: LogLevel = OPTIONS["verbosity"],
):
    log = logging.getLogger(__name__)
    log.setLevel(verbosity.value)

    log.info("")
    log.info(" ===============================================")
    log.info(" \tPerforming HV_LV_TEST analysis")
    log.info(" ===============================================")
    log.info("")

    test_type = Path(__file__).stem

    time_start = round(datetime.timestamp(datetime.now()))
    output_dir = base_output_dir.joinpath(test_type).joinpath(f"{time_start}")
    output_dir.mkdir(parents=True, exist_ok=False)

    allinputs = get_inputs(input_meas)

    for filename in sorted(allinputs):
        log.info("")
        log.info(f" Loading {filename}")

        inputDFs = load_json(filename)
        log.info(
            f" There are results from {len(inputDFs)} module(s) stored in this file"
        )

        with Path(filename).open(encoding="utf-8") as f:
            jsonData = json.load(f)

        for j, inputDF in zip(jsonData, inputDFs):
            d = inputDF.to_dict()

            results = j[0].get("results")
            props = results.get("property")
            metadata = results.get("metadata")
            # measurement = metadata.get("Measurement")

            operator = ""
            props["OPERATOR"] = operator  # operator!

            if metadata is None:
                metadata = results.get("Metadata")

            # Extract relevant information
            serial_number = d.get("serialNumber")

            # results = data["results"]
            # metadata = results["metadata"]

            # Additional parameters from the new JSON structure
            vin_drop = metadata.get("Measurement", {}).get("VIN_DROP[V]")
            gnd_drop = metadata.get("Measurement", {}).get("GND_DROP[V]")
            # vin_resistance = metadata.get("Measurement", {}).get("VIN_RESISTANCE[mOhm]")
            # gnd_resistance = metadata.get("Measurement", {}).get("GND_RESISTANCE[mOhm]")
            eff_resistance = metadata.get("Measurement", {}).get(
                "EFFECTIVE_RESISTANCE[mOhm]"
            )
            hv_leakage = metadata.get("Measurement", {}).get("HV_LEAKAGE[mV]")
            leakage_current = metadata.get("Measurement", {}).get("LEAKAGE_CURRENT[nA]")
            ntc_voltage = metadata.get("Measurement", {}).get("NTC_VOLTAGE[V]")
            ntc_value = metadata.get("Measurement", {}).get("NTC_VALUE[kOhm]")
            humidity = metadata.get("Measurement", {}).get("HUMIDITY[RH%]")
            temperature = metadata.get("Measurement", {}).get("TEMPERATURE")
            r1_hv_resistor = metadata.get("Measurement", {}).get("R1_HV_RESISTOR")
            duration = metadata.get("Measurement", {}).get("TEST_DURATION[min]")

            # Fill values from metadatas
            results["VIN_DROP"] = vin_drop
            results["GND_DROP"] = gnd_drop
            # results["VIN_RESISTANCE"] = vin_resistance
            # results["GND_RESISTANCE"] = gnd_resistance
            results["EFFECTIVE_RESISTANCE"] = eff_resistance
            results["HV_LEAKAGE"] = hv_leakage
            results["LEAKAGE_CURRENT"] = leakage_current
            results["NTC_VOLTAGE"] = ntc_voltage
            results["NTC_VALUE"] = ntc_value
            results["TEMPERATURE"] = temperature
            results["DAMAGE_COMMENT"] = ""
            results["R1_HV_RESISTOR"] = r1_hv_resistor
            results["RELATIVE_HUMIDITY"] = humidity
            props["TEST_DURATION"] = int(duration)

            passes_qc = (
                # (vin_resistance <= 12)
                # and (gnd_resistance <= 12)
                (eff_resistance <= 12) and (leakage_current <= 20)
            )

            # Output a json file
            outputDF = outputDataFrame()
            outputDF.set_test_type(test_type)

            qc_data = qcDataFrame()
            qc_data._meta_data.update(metadata)

            # qc_data.add_property("SERIAL_NUMBER", serial_number)
            # Other properties remain the same
            # ...

            # Handle 'property' from results

            # Pass-through properties in input

            for key, value in props.items():
                qc_data.add_property(key, value)

            # Add analysis version
            qc_data.add_property(
                "ANALYSIS_VERSION",
                __version__,
            )

            # Pass-through measurement parameters
            for key, value in results.items():
                if key in [
                    "property",
                    "metadata",
                    "Metadata",
                    "Measurements",
                    "comment",
                ]:
                    continue

                qc_data.add_parameter(key, value)

            results_property = results.get("property", {})
            for key, value in results_property.items():
                qc_data.add_property(key, value)

            outputDF.set_results(qc_data)
            outputDF.set_pass_flag(passes_qc)

            outfile = output_dir.joinpath(f"{serial_number}.json")
            log.info(f" Saving output of analysis to: {outfile}")
            # out = outputDF.to_dict(True)
            out = outputDF.to_dict(True)
            out.update({"serialNumber": serial_number})
            save_dict_list(outfile, [out])


if __name__ == "__main__":
    typer.run(main)
