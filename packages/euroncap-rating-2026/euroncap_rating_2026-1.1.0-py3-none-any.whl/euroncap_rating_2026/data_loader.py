# Copyright 2025, Euro NCAP IVZW
# Created by IVEX NV (https://ivex.ai)
#
# Licensed under the Apache License 2.0.
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

import os, sys
import pandas as pd
import math
from euroncap_rating_2026 import body_region
from euroncap_rating_2026.load_case import LoadCase
from euroncap_rating_2026.body_region import BodyRegion
from euroncap_rating_2026.dummy import Dummy
from euroncap_rating_2026.seat import Seat
import logging
from euroncap_rating_2026.criteria import ColorCriteria, Criteria, CriteriaType
from collections import Counter
import numpy as np
from euroncap_rating_2026 import vru_processing

logger = logging.getLogger(__name__)

# Mapping of sheet names to stage subelements
SHEET_MAPPING = {
    "CP - Frontal Offset": "Offset",
    "CP - Frontal FW": "FW",
    "CP - Frontal Sled & VT": "Sled & VT",
    "CP - Side MDB": "MDB",
    "CP - Side Pole": "Pole",
    "CP - Side Farside": "Farside",
    "CP - Rear Whiplash": "Whiplash",
    "CP - VRU Head Impact": "Head Impact",
    "CP - VRU Pelvis & Leg Impact": "Pelvis & Leg Impact",
}


def generate_vru_points(dfs, param_df):
    vru_params = param_df[param_df["param_code"].str.contains("VRU", na=False)]
    # Extract the "CP - VRU Prediction" sheet from dfs if it exists
    vru_prediction_df = dfs.get("CP - VRU Prediction", None)
    headform_test_points, vru_test_points_all = vru_processing.process_headform_test(
        vru_prediction_df, vru_params
    )
    logger.debug(f"Headform test points: {headform_test_points}")

    legform_test_points = vru_processing.process_legform_test(
        vru_prediction_df, vru_params
    )
    logger.debug(f"Legform test points: {legform_test_points}")
    return headform_test_points, vru_test_points_all, legform_test_points


def generate_vru_loadcases(vru_test_data):
    # Generate the "CP - VRU Head Impact" sheet
    vru_head_impact_loadcases = vru_processing.process_headform_vru_loadcases(
        vru_test_data.headform_test_points
    )

    vru_legform_loadcases = vru_processing.process_legform_vru_loadcases(
        vru_test_data.legform_test_points
    )
    vru_test_data.headform_loadcases = vru_head_impact_loadcases
    vru_test_data.legform_loadcases = vru_legform_loadcases


def get_initials(text):
    if pd.isna(text):
        return ""
    return "".join([word[0].upper() for word in str(text).split()])


def get_first_word(text):
    if pd.isna(text):
        return ""
    return str(text).split()[0]


def get_param_df(dfs):

    # Read the "Input parameters" sheet into a DataFrame and remove it from dfs
    if "Input parameters" in dfs:
        input_parameters_df = dfs.pop("Input parameters")
    else:
        input_parameters_df = None

    if input_parameters_df is None:
        raise ValueError(
            "The Excel file does not contain the required 'Input parameters' sheet."
        )
    # Extract input parameters with their corresponding stage, stage element, and stage subelement
    input_parameters = []
    current_stage = None
    current_stage_element = None
    current_stage_subelement = None

    for _, row in input_parameters_df.iterrows():
        if not pd.isna(row.get("Stage")):
            current_stage = row["Stage"]
        if not pd.isna(row.get("Stage element")):
            current_stage_element = row["Stage element"]
        if not pd.isna(row.get("Stage Subelement")):
            current_stage_subelement = row["Stage Subelement"]
        input_param = row.get("Input parameter")
        input_value = row.get("Value")
        if not pd.isna(input_param) and not pd.isna(input_value):
            input_parameters.append(
                {
                    "Input parameter": input_param,
                    "Stage": current_stage,
                    "Stage element": current_stage_element,
                    "Stage Subelement": current_stage_subelement,
                    "Value": input_value,
                }
            )
    # Create a DataFrame of input parameters
    param_df = pd.DataFrame(input_parameters)

    param_df["param_code"] = (
        param_df["Stage"].apply(get_initials)
        + " - "
        + param_df["Stage element"].apply(get_first_word)
        + " "
        + param_df["Stage Subelement"].astype(str)
    )
    param_df = param_df[["param_code", "Input parameter", "Value"]]
    logger.debug(f"Extracted param_df: {param_df}")
    return param_df


def read_excel_file_to_dfs(input_file):
    # Load the Excel file
    xls = pd.ExcelFile(input_file)

    sheet_names = xls.sheet_names
    if not sheet_names:
        raise ValueError("The Excel file does not contain any sheets.")
    dfs = {}

    for sheet_name in sheet_names:
        dfs[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name, header=0)

    xls.close()

    return dfs


def generate_vru_test_points(input_file):
    """
    Load and process VRU test points from an Excel file.

    This function reads the VRU test points from the specified Excel file and processes them according to the parameters
    defined in the input parameters DataFrame.

    Args:
        input_file (str): The path to the input Excel file.
        param_df (DataFrame): A DataFrame containing the input parameters.

    Returns:
        list: A list of VRU test points.
    """
    dfs = read_excel_file_to_dfs(input_file)
    param_df = get_param_df(dfs)
    headform_test_points, vru_test_points_all, legform_test_points = (
        generate_vru_points(dfs, param_df)
    )
    vru_test_data = vru_processing.VruTestData(
        prediction_df=dfs.get("CP - VRU Prediction", pd.DataFrame()),
        headform_test_points=headform_test_points,
        legform_test_points=legform_test_points,
        vru_test_points_all=vru_test_points_all,
    )
    return vru_test_data


def load_data(input_file):
    """ """

    dfs = read_excel_file_to_dfs(input_file)

    sheet_dict = {}
    valid_sheet_names = list(SHEET_MAPPING.keys())

    param_df = get_param_df(dfs)

    # Process each sheet in the Excel file
    for sheet_name, df in dfs.items():

        if sheet_name in valid_sheet_names:
            logger.debug(f"Loading sheet {sheet_name}")
            print(f"   Processing {sheet_name}..")
        else:
            logger.debug(f"Skipping sheet {sheet_name}")
            continue

        # Get current params by using sheet_name to access all the matching rows in param_df
        current_params = param_df[
            param_df["param_code"].str.contains(sheet_name, na=False)
        ]
        logger.debug(f"Current params for {sheet_name}: {current_params}")

        loadcase_list_with_index = [
            (index, loadcase)
            for index, loadcase in enumerate(df["Loadcase"])
            if pd.notna(loadcase)
        ]
        logger.debug(f"loadcase_list_with_index: {loadcase_list_with_index}")

        load_cases = []
        for loadcase_index, loadcase_name in loadcase_list_with_index:
            logger.debug(f"Current loadcase name: %s ", loadcase_name)
            load_case, _ = LoadCase.get_loadcase_from_row(loadcase_index, df)
            load_cases.append(load_case)
        if sheet_name == "CP - Rear Whiplash":
            # Get torso_angle_value from param_df
            torso_angle_row = param_df[
                (param_df["Input parameter"] == "Torso angle (rear)")
                & (param_df["param_code"].str.contains(sheet_name, na=False))
            ]
            if not torso_angle_row.empty:
                torso_angle_value = float(torso_angle_row.iloc[0]["Value"])
                logger.debug(f"Torso angle (rear) value: {torso_angle_value}")
            else:
                raise ValueError(
                    f"Missing mandatory parameter: 'Torso angle (rear)' in input parameters for sheet {sheet_name}."
                )

            # Set the torso angle for the load case
            for load_case in load_cases:
                if load_case.name == "Static-Rear":
                    for seat in load_case.seats:
                        dummy = seat.dummy
                        if dummy.name == "HRMD":
                            neck_body_region = dummy.get_body_region("Neck")
                            for criteria in neck_body_region._criteria:
                                if criteria.name in [
                                    "Backset - Lowest",
                                    "Backset - Mid",
                                ]:
                                    criteria.hpl = 7.128 * torso_angle_value + 153.0
                                    criteria.lpl = 7.128 * torso_angle_value + 153.0
                                    criteria.calculate_color_score()
                                    logger.debug(
                                        f"Updated criteria '{criteria.name}' in Neck body region: hpl={criteria.hpl}, lpl={criteria.lpl}, full criteria: {vars(criteria)}"
                                    )

        sheet_dict[sheet_name] = load_cases

        # Handle specific operations for CP - Side Farside sheet
        if sheet_name == "CP - Side Farside":
            # Get countermeasure and red line from param_df
            # Extract "Countermeasure?" parameter
            match_countermeasure = param_df[
                (param_df["Input parameter"] == "Countermeasure?")
                & (param_df["param_code"].str.contains(sheet_name, na=False))
            ]
            if not match_countermeasure.empty:
                countermeasure_param = match_countermeasure.iloc[0]["Value"]
            else:
                raise ValueError(
                    f"Missing mandatory parameter: 'Countermeasure?' in input parameters for sheet '{sheet_name}'."
                )

            # Extract "Red line >125 mm outboard of the orange line" parameter
            match_redline = param_df[
                (
                    param_df["Input parameter"]
                    == "Red line >125 mm outboard of the orange line"
                )
                & (param_df["param_code"].str.contains(sheet_name, na=False))
            ]
            if not match_redline.empty:
                redline_param = match_redline.iloc[0]["Value"]
            else:
                raise ValueError(
                    f"Missing mandatory parameter: 'Red line >125 mm outboard of the orange line' in input parameters for sheet '{sheet_name}'."
                )

            logger.debug(
                f"Countermeasure param: {countermeasure_param}, Redline param: {redline_param}"
            )

            farside_loadcase_color_dict = {}
            farside_loadcase_score_dict = {}
            last_loadcase = None
            for index, row in df.iterrows():
                if not pd.isna(row["Loadcase"]):
                    last_loadcase = row["Loadcase"]
                if "Robustness" not in last_loadcase:
                    if row.Criteria == "Farside excursion" and not pd.isna(row.Value):
                        cc = ColorCriteria(
                            name=row.Criteria,
                            color=row.Value.lower(),
                            countermeasure=countermeasure_param,
                            redline_above_125mm=redline_param,
                        )
                        if "Main-AEMD" in last_loadcase:
                            last_loadcase_key = "AEMD"
                        elif "Main-Pole" in last_loadcase:
                            last_loadcase_key = "Pole"
                        farside_loadcase_color_dict[last_loadcase_key] = cc.color
                        farside_loadcase_score_dict[last_loadcase] = cc.score
                        logger.debug(f"ColorCriteria created: {cc}")
                else:
                    if "AEMD" in last_loadcase:
                        actual_test_color = farside_loadcase_color_dict["AEMD"]
                    elif "Pole" in last_loadcase:
                        actual_test_color = farside_loadcase_color_dict["Pole"]
                    else:
                        actual_test_color = None
                    if row.Criteria == "Farside excursion" and not pd.isna(row.Value):
                        virtual_test_color = row["Value"].lower()
                        logger.debug(
                            f"Virtual test color: {virtual_test_color}, Actual test color: {actual_test_color}"
                        )
                        virtual_score = None
                        result = None
                        if actual_test_color == virtual_test_color or (
                            (
                                actual_test_color == "green"
                                and virtual_test_color == "yellow"
                            )
                            or (
                                actual_test_color == "yellow"
                                and virtual_test_color == "green"
                            )
                            or (
                                actual_test_color == "yellow"
                                and virtual_test_color == "orange"
                            )
                            or (
                                actual_test_color == "orange"
                                and virtual_test_color == "yellow"
                            )
                            or (
                                actual_test_color == "orange"
                                and virtual_test_color == "brown"
                            )
                            or (
                                actual_test_color == "brown"
                                and virtual_test_color == "orange"
                            )
                        ):
                            result = "PASS"
                            virtual_score = 100.0
                        else:
                            result = "FAIL"
                            virtual_score = 0.0

                        farside_loadcase_score_dict[last_loadcase] = virtual_score
                        logger.debug(f"Comparison result: {result}")
                        logger.debug(f"virtual_score: {virtual_score}")

    logger.debug(f"farside_loadcase_color_dict: {farside_loadcase_color_dict}")
    logger.debug(f"farside_loadcase_score_dict: {farside_loadcase_score_dict}")

    # For "CP - Frontal Sled & VT", add Lower Leg, Foot & Ankle body region to Virtual- loadcases
    if "CP - Frontal Sled & VT" in sheet_dict:
        sled_vt_loadcases = sheet_dict["CP - Frontal Sled & VT"]
        for load_case in sled_vt_loadcases:
            if load_case.name.startswith("Virtual-"):
                for seat in load_case.seats:
                    dummy = seat.dummy
                    # Only add if not already present
                    if not any(
                        br.name == "Lower Leg, Foot & Ankle"
                        for br in dummy.body_region_list
                    ):
                        lower_leg_br = BodyRegion(name="Lower Leg, Foot & Ankle")
                        dummy.body_region_list.append(lower_leg_br)

    # Special handling for "CP - Rear Whiplash": keep only the dummy (Driver or Front Passenger) with the lowest score, rename to "Front"
    if "CP - Rear Whiplash" in sheet_dict:
        whiplash_loadcases = sheet_dict["CP - Rear Whiplash"]
        for load_case in whiplash_loadcases:
            if load_case.name == "Static-Front":
                # Get both dummies and their scores
                load_case.raw_seats = load_case.seats.copy()
                seat1, seat2 = load_case.seats
                dummy1, dummy2 = seat1.dummy, seat2.dummy
                # Instead of computing bodyregion score, sum all criteria scores in that body region
                neck1 = dummy1.get_body_region("Neck")
                neck2 = dummy2.get_body_region("Neck")
                if neck1 is not None:
                    score1 = min(100.0, sum(c.get_score() for c in neck1._criteria))
                else:
                    score1 = float("inf")
                if neck2 is not None:
                    score2 = min(100.0, sum(c.get_score() for c in neck2._criteria))
                else:
                    score2 = float("inf")

                logger.debug(f"Load case name: {load_case.name}")
                logger.debug(f"1) S: {seat1} D: {dummy1} - score: {score1}")
                logger.debug(f"2) S: {seat2} D: {dummy2} - score: {score2}")

                # Keep the seat/dummy with the lowest score
                if score1 <= score2:
                    # Create a new Seat with name "Front" and the selected dummy
                    new_seat = Seat(name="Front", dummy=dummy1)
                    load_case.seats = [new_seat]
                    new_seat.dummy.get_body_region("Neck").set_bodyregion_score(score1)
                else:
                    # Create a new Seat with name "Front" and the selected dummy
                    new_seat = Seat(name="Front", dummy=dummy2)
                    load_case.seats = [new_seat]
                    new_seat.dummy.get_body_region("Neck").set_bodyregion_score(score2)
                break

    # Dynamically generate VRU test data from the processed sheet_dict
    vru_test_data = vru_processing.VruTestData.from_sheet_dict(sheet_dict)
    vru_test_data.get_vru_points_from_file(input_file)
    # Log each VRU point in vru_test_data.vru_test_points_all
    for vru_point in vru_test_data.vru_test_points_all:
        logger.debug(f"VRU point: {vru_point}")
    vru_test_data.compute_vru_bodyregion_score()

    legform_max_scores = {}
    legform_inspection = {}

    # Read the data from the "CP - Body Region Scores" sheet
    df_body_region_scores = pd.read_excel(
        input_file, sheet_name="CP - Body Region Scores", header=0
    )

    current_stage_element = None
    current_stage_subelement = None
    current_load_case_name = None
    current_seat_name = None
    current_dummy_name = None

    farside_virtual_aemb_max_score = None
    farside_virtual_aemb_inspection = None
    farside_virtual_pole_max_score = None
    farside_virtual_pole_inspection = None

    lower_leg_bodyregion_scores = []
    # Iterate through each row in df_body_region_scores
    for index, row in df_body_region_scores.iterrows():

        if not pd.isna(row["Stage element"]):
            current_stage_element = row["Stage element"]
        logger.debug("current_stage_element: %s", current_stage_element)

        if not pd.isna(row["Stage subelement"]):
            current_stage_subelement = row["Stage subelement"]
        logger.debug("current_stage_subelement: %s", current_stage_subelement)

        if not pd.isna(row["Stage element"]):
            current_stage_element = (
                row["Stage element"].replace("Impact", "").replace(" ", "")
            )
        logger.debug("current_stage_element: %s", current_stage_element)
        current_stage_subelement = current_stage_subelement.strip()

        sheet_name = "CP - " + current_stage_element + " " + current_stage_subelement

        if sheet_name not in valid_sheet_names:
            logger.debug(f"Skipping sheet {sheet_name}")
            continue

        logger.debug("sheet_name: %s", sheet_name)

        if not pd.isna(row["Loadcase"]):
            current_load_case_name = row["Loadcase"]
        if not pd.isna(row["Seat position"]):
            current_seat_name = row["Seat position"]
        if not pd.isna(row["Dummy"]):
            current_dummy_name = row["Dummy"]

        body_region_name = row["Body Region"]

        max_score = row["Max Score"]
        if pd.isna(max_score):
            max_score = None
        else:
            max_score = float(round(max_score, 5))
        inspection = row["Inspection [%]"]
        if pd.isna(inspection):
            inspection = None

        logger.debug("current_load_case_name: %s", current_load_case_name)
        logger.debug("current_seat_name: %s", current_seat_name)
        logger.debug("current_dummy_name: %s", current_dummy_name)
        logger.debug("body_region_name: %s", body_region_name)

        if current_load_case_name == "Robustness-AEMDB":
            farside_virtual_aemb_max_score = max_score
            farside_virtual_aemb_inspection = inspection
        elif current_load_case_name == "Robustness-Pole":
            farside_virtual_pole_max_score = max_score
            farside_virtual_pole_inspection = inspection

        load_cases = sheet_dict[sheet_name]

        # Special handling for VRU Pelvis & Leg Impact: merge Knee and Tibia into "Knee & Tibia"
        if (
            sheet_name == "CP - VRU Pelvis & Leg Impact"
            and current_load_case_name == "Lower Leg"
            and dummy.name == "aPLI"
            and body_region_name == "Knee & Tibia"
        ):
            legform_max_scores[body_region_name] = max_score
            legform_inspection[body_region_name] = inspection

        # Find the corresponding load_case, seat, and dummy
        for load_case in load_cases:
            if load_case.name == current_load_case_name:
                for seat in load_case.seats:
                    if seat.name == current_seat_name:
                        dummy = seat.dummy
                        if dummy.name == current_dummy_name:
                            for body_region in dummy.body_region_list:
                                if body_region.name == body_region_name:
                                    if (
                                        sheet_name == "CP - Rear Whiplash"
                                        and current_load_case_name == "Static-Front"
                                        and dummy.name == "HRMD"
                                        and body_region.name == "Neck"
                                    ):
                                        body_region.set_max_score(max_score)
                                        body_region.set_inspection(inspection)
                                        body_region.compute_score()

                                        bodyregion_score = (
                                            body_region.get_bodyregion_score()
                                        )
                                        computed_score = body_region.get_score()
                                    elif sheet_name == "CP - Side Farside":
                                        if (
                                            current_load_case_name
                                            in farside_loadcase_score_dict
                                        ):
                                            bodyregion_score = (
                                                farside_loadcase_score_dict.get(
                                                    current_load_case_name, 0.0
                                                )
                                            )
                                            body_region.set_bodyregion_score(
                                                bodyregion_score
                                            )
                                        if (
                                            current_load_case_name == "Robustness-AEMDB"
                                            and body_region_name == "Head"
                                        ):
                                            body_region.set_bodyregion_score(
                                                farside_loadcase_score_dict.get(
                                                    "Robustness-AEMDB", 0.0
                                                )
                                            )
                                            body_region.set_measurement_list(
                                                dummy.get_body_region(
                                                    "Pelvis"
                                                )._measurement
                                            )
                                        elif (
                                            current_load_case_name == "Robustness-Pole"
                                            and body_region_name == "Head"
                                        ):
                                            body_region.set_bodyregion_score(
                                                farside_loadcase_score_dict.get(
                                                    "Robustness-Pole", 0.0
                                                )
                                            )
                                            body_region.set_measurement_list(
                                                dummy.get_body_region(
                                                    "Pelvis"
                                                )._measurement
                                            )

                                        body_region.set_max_score(max_score)
                                        body_region.set_inspection(inspection)
                                        body_region.compute_score()
                                        computed_score = body_region.get_score()
                                        logger.debug(
                                            f"Body Region: {body_region_name}, "
                                            f"Bodyregion Score: {body_region.get_bodyregion_score()}, "
                                            f"Max Score: {body_region.get_max_score()}, "
                                            f"Inspection: {body_region.get_inspection()}, "
                                            f"Measurement: {body_region._measurement}, "
                                            f"Score: {computed_score}"
                                        )
                                    elif sheet_name == "CP - VRU Head Impact":
                                        # body_region.set_max_score(max_score)
                                        body_region.set_inspection(0.0)
                                        body_region.compute_score()
                                        computed_score = body_region.get_score()
                                    elif sheet_name == "CP - VRU Pelvis & Leg Impact":
                                        logger.debug(
                                            f"Current body_region_name: {body_region_name}"
                                        )
                                        logger.debug(
                                            f"Legform_final_scores: {vru_test_data.legform_scores}"
                                        )
                                        if (
                                            body_region_name
                                            in vru_test_data.legform_scores
                                        ):
                                            legform_max_scores[body_region_name] = (
                                                max_score
                                            )
                                            legform_inspection[body_region_name] = (
                                                inspection
                                            )
                                    else:
                                        if (
                                            "Virtual" in current_load_case_name
                                            and body_region_name
                                            == "Lower Leg, Foot & Ankle"
                                        ):
                                            if any(
                                                x == 0
                                                for x in lower_leg_bodyregion_scores
                                                if x is not None
                                            ):
                                                body_region.set_bodyregion_score(0.0)
                                            else:
                                                body_region.set_bodyregion_score(100.0)

                                            body_region.set_max_score(max_score)
                                            body_region.set_inspection(inspection)
                                            body_region.compute_score()

                                            bodyregion_score = (
                                                body_region.get_bodyregion_score()
                                            )
                                            computed_score = body_region.get_score()

                                        else:
                                            if (
                                                body_region_name
                                                == "Lower Leg, Foot & Ankle"
                                            ):
                                                lower_leg_bodyregion_scores.append(
                                                    body_region.get_bodyregion_score()
                                                )

                                            # Update the max score and inspection for the body region
                                            body_region.set_max_score(max_score)
                                            body_region.set_inspection(inspection)
                                            body_region.compute_bodyregion_score()
                                            body_region.compute_score()
                                            bodyregion_score = (
                                                body_region.get_bodyregion_score()
                                            )
                                            computed_score = body_region.get_score()

                                    logger.debug(
                                        f"####### Updated body region '{body_region_name}' with max score '{max_score}' and inspection '{inspection}'. Bodyregion_score {bodyregion_score} - Computed score {computed_score}"
                                    )
                                    break

    # Special rule for "CP - Frontal Sled & VT": if "Virtual" in load case name and all bodyregion scores except Lower Leg, Foot & Ankle are None, set Lower Leg, Foot & Ankle bodyregion score to 0
    if "CP - Frontal Sled & VT" in sheet_dict:
        sled_vt_loadcases = sheet_dict["CP - Frontal Sled & VT"]
        for load_case in sled_vt_loadcases:
            if "Virtual" in load_case.name:
                for seat in load_case.seats:
                    dummy = seat.dummy
                    lower_leg_br = None
                    body_region_only_none = False
                    other_values = []
                    for br in dummy.body_region_list:
                        if br.name == "Lower Leg, Foot & Ankle":
                            lower_leg_br = br
                        else:
                            # Collect all criteria values for this body region
                            crit_values = [crit.get_value() for crit in br._criteria]
                            other_values.extend(crit_values)
                            # If all values for this body region are None, add a marker
                            if all(pd.isna(val) for val in crit_values):
                                body_region_only_none = True

                    logger.debug(f"Other bodyregion values: {other_values}")
                    logger.debug(f"body_region_only_none: {body_region_only_none}")
                    # If all other bodyregion scores are None
                    if body_region_only_none:
                        logger.debug(
                            f"There is a body region with all None values, setting Lower Leg, Foot & Ankle bodyregion score to None"
                        )
                        lower_leg_br.set_bodyregion_score(0.0)
                        lower_leg_br.compute_score()

    # Add new load cases for "CP - Side Farside"
    if "CP - Side Farside" in sheet_dict:
        farside_load_cases = sheet_dict["CP - Side Farside"]
        # Remove load cases starting with "Robustness-Pole" or "Robustness-AEMDB"
        farside_load_cases = [
            load_case
            for load_case in farside_load_cases
            if not (
                load_case.name.startswith("Robustness-Pole")
                or load_case.name.startswith("Robustness-AEMDB")
            )
        ]

        # Create Robustness-AEMBD load case
        aembd_head_bodyregion = BodyRegion(name="Head")
        aembd_head_bodyregion.set_bodyregion_score(
            min(
                value
                for key, value in farside_loadcase_score_dict.items()
                if "Robustness-AEMDB" in key
            )
        )
        aembd_head_bodyregion.set_max_score(farside_virtual_aemb_max_score)
        aembd_head_bodyregion.set_inspection(farside_virtual_aemb_inspection)
        aembd_head_bodyregion.compute_score()
        aembd_head_bodyregion_list = [aembd_head_bodyregion]
        virtual_aembd_dummy = Dummy(
            name="WorldSID-50", body_region_list=aembd_head_bodyregion_list
        )

        virtual_aembd_seat = Seat(name="Driver", dummy=virtual_aembd_dummy)
        aembd_seats = [virtual_aembd_seat]
        virtual_aembd_load_case = LoadCase(name="Robustness-AEMDB", seats=aembd_seats)

        farside_load_cases.append(virtual_aembd_load_case)
        # Create Robustness-Pole load case
        pole_head_bodyregion = BodyRegion(name="Head")
        pole_head_bodyregion.set_bodyregion_score(
            min(
                value
                for key, value in farside_loadcase_score_dict.items()
                if "Robustness-Pole" in key
            )
        )
        pole_head_bodyregion.set_max_score(farside_virtual_pole_max_score)
        pole_head_bodyregion.set_inspection(farside_virtual_pole_inspection)
        pole_head_bodyregion.compute_score()
        pole_head_bodyregion_list = [pole_head_bodyregion]
        virtual_pole_dummy = Dummy(
            name="WorldSID-50", body_region_list=pole_head_bodyregion_list
        )

        virtual_pole_seat = Seat(name="Driver", dummy=virtual_pole_dummy)
        pole_seats = [virtual_pole_seat]
        virtual_pole_load_case = LoadCase(name="Robustness-Pole", seats=pole_seats)

        farside_load_cases.append(virtual_pole_load_case)

        sheet_dict["CP - Side Farside"] = farside_load_cases

    # Special rule for "CP - Rear Whiplash": for "Rear-Mid" and "Rear-High" loadcases, set Neck bodyregion score as average of all criteria scores (not min)
    if "CP - Rear Whiplash" in sheet_dict:
        whiplash_loadcases = sheet_dict["CP - Rear Whiplash"]
        for load_case in whiplash_loadcases:
            if load_case.name in ["Rear-Mid", "Rear-High"]:
                for seat in load_case.seats:
                    dummy = seat.dummy
                    neck = dummy.get_body_region("Neck")
                    if neck is not None and neck._criteria:
                        # Compute average of all criteria scores
                        scores = [
                            c.get_score()
                            for c in neck._criteria
                            if c.get_score() is not None
                        ]
                        logger.debug(
                            f"[CP - Rear Whiplash] Neck body region criteria scores to be avg: {scores}"
                        )
                        if scores:
                            prev_bodyregionscore = neck.get_bodyregion_score()
                            prev_score = neck.get_score()
                            avg_score = sum(scores) / len(scores)
                            neck.set_bodyregion_score(avg_score)
                            neck.compute_score()
                            logger.debug(
                                f"[CP - Rear Whiplash] Neck body region updated bodyregion score: {neck.get_bodyregion_score()} (was {prev_bodyregionscore}), score: {neck.get_score()} (was {prev_score})"
                            )
    if "CP - VRU Pelvis & Leg Impact" in sheet_dict:

        # Add new load case for "Upper Legform" with body region: Pelvis
        upper_leg_bodyregion = BodyRegion(name="Pelvis")
        upper_leg_bodyregion.set_bodyregion_score(
            vru_test_data.legform_scores.get("Pelvis", 0.0)
        )
        upper_leg_bodyregion.set_max_score(legform_max_scores.get("Pelvis", None))
        upper_leg_bodyregion.set_inspection(legform_inspection.get("Pelvis", None))

        upper_leg_bodyregion.compute_score()
        upper_leg_bodyregion_list = [upper_leg_bodyregion]
        upper_leg_dummy = Dummy(
            name="Upper legform", body_region_list=upper_leg_bodyregion_list
        )
        upper_leg_seat = Seat(name="Driver", dummy=upper_leg_dummy)
        upper_leg_load_case = LoadCase(name="Upper Leg", seats=[upper_leg_seat])
        sheet_dict["CP - VRU Pelvis & Leg Impact"].append(upper_leg_load_case)

        # Add new load case for "Lower Legform" with body regions: Pelvis, Knee, Tibia
        lower_legform_bodyregions = []
        for br_name in ["Femur", "Knee & Tibia"]:
            br = BodyRegion(name=br_name)
            br.set_bodyregion_score(vru_test_data.legform_scores.get(br_name, 0.0))
            br.set_inspection(legform_inspection.get(br_name, None))
            br.set_max_score(legform_max_scores.get(br_name, None))
            br.compute_score()
            lower_legform_bodyregions.append(br)
        lower_leg_dummy = Dummy(name="aPLI", body_region_list=lower_legform_bodyregions)
        lower_leg_seat = Seat(name="Driver", dummy=lower_leg_dummy)
        lower_leg_load_case = LoadCase(name="Lower Leg", seats=[lower_leg_seat])
        sheet_dict["CP - VRU Pelvis & Leg Impact"].append(lower_leg_load_case)

    # Read the data from the "CP - Dummy Scores" sheet
    df_dummy_scores = pd.read_excel(
        input_file, sheet_name="CP - Dummy Scores", header=0
    )

    current_stage_element = None
    current_stage_subelement = None
    current_load_case_name = None
    current_seat_name = None
    current_dummy_name = None

    lower_leg_bodyregion_scores = []

    vru_headform_dummy_max_scores = {}

    # Sum body region max scores for Adult Headform and Child Headform
    for sheet_name, load_cases in sheet_dict.items():
        if sheet_name == "CP - VRU Head Impact":
            for load_case in load_cases:
                for seat in load_case.seats:
                    dummy = seat.dummy
                    if load_case.name == "Headform" and dummy.name in [
                        "Adult Headform",
                        "Child Headform",
                    ]:
                        total_max_score = 0.0
                        for body_region in dummy.body_region_list:
                            max_score = body_region.get_max_score()
                            if max_score is not None:
                                total_max_score += max_score
                        vru_headform_dummy_max_scores[dummy.name] = total_max_score
    logger.debug(f"vru_headform_dummy_max_scores: {vru_headform_dummy_max_scores}")
    # Iterate through each row in df_dummy_scores
    for index, row in df_dummy_scores.iterrows():

        if not pd.isna(row["Stage element"]):
            current_stage_element = row["Stage element"]

        if not pd.isna(row["Stage subelement"]):
            current_stage_subelement = row["Stage subelement"]

        logger.debug("current_stage_subelement: %s", current_stage_subelement)

        if not pd.isna(row["Stage element"]):
            current_stage_element = (
                row["Stage element"].replace("Impact", "").replace(" ", "")
            )
        logger.debug("current_stage_element: %s", current_stage_element)
        sheet_name = "CP - " + current_stage_element + " " + current_stage_subelement

        if sheet_name not in valid_sheet_names:
            logger.debug(f"Skipping sheet {sheet_name}")
            continue
        logger.debug("sheet_name: %s", sheet_name)

        if not pd.isna(row["Loadcase"]):
            current_load_case_name = row["Loadcase"]
        if not pd.isna(row["Seat position"]):
            current_seat_name = row["Seat position"]

        if not pd.isna(row["Seat position"]):
            current_seat_name = " ".join(
                word.capitalize() for word in row["Seat position"].split()
            )

        current_dummy_name = row["Dummy"]

        max_score = row["Max score"]
        if pd.isna(max_score):
            max_score = None
        else:
            max_score = float(round(max_score, 5))
        logger.debug("current_load_case_name: %s", current_load_case_name)
        logger.debug("current_seat_name: %s", current_seat_name)
        logger.debug("current_dummy_name: %s", current_dummy_name)

        load_cases = sheet_dict[sheet_name]

        # Find the corresponding load_case, seat, and dummy
        for load_case in load_cases:
            if load_case.name == current_load_case_name:
                for seat in load_case.seats:
                    if seat.name == current_seat_name:
                        dummy = seat.dummy
                        if dummy.name == current_dummy_name:
                            if (
                                load_case.name == "Headform"
                                and current_dummy_name in vru_headform_dummy_max_scores
                            ):
                                # If the dummy is Adult Headform or Child Headform, use the precomputed max score
                                max_score = vru_headform_dummy_max_scores[
                                    current_dummy_name
                                ]
                                dummy.set_max_score(max_score)
                            else:
                                dummy.set_max_score(max_score)

                            dummy.compute_capping()
                            capping = dummy.get_capping()
                            dummy.compute_score()
                            computed_score = dummy.get_score()

                            logger.debug(
                                f"####### Updated dummy '{current_dummy_name}' with max score '{max_score}'. Capping {capping} - Computed score {computed_score}"
                            )
                            break

    # Read the "Input parameters" sheet into a DataFrame and remove it from dfs
    if "Test Scores" in dfs:
        test_scores_df = dfs.pop("Test Scores")
    else:
        test_scores_df = None

    if test_scores_df is None:
        raise ValueError(
            "The Excel file does not contain the required 'Test Scores' sheet."
        )

    test_score_inspections = []
    current_stage = None
    current_stage_element = None
    current_stage_subelement = None

    for _, row in test_scores_df.iterrows():
        if not pd.isna(row.get("Stage")):
            current_stage = row["Stage"]
        if not pd.isna(row.get("Stage element")):
            current_stage_element = row["Stage element"]
        if not pd.isna(row.get("Stage Subelement")):
            current_stage_subelement = row["Stage Subelement"]
        input_inspection = row.get("Inspection [%]")
        if not pd.isna(input_inspection):
            test_score_inspections.append(
                {
                    "Stage": current_stage,
                    "Stage element": current_stage_element,
                    "Stage Subelement": current_stage_subelement,
                    "Inspection [%]": input_inspection,
                }
            )
    # Create a DataFrame of test_scores inspections
    test_score_inspection_df = pd.DataFrame(test_score_inspections)

    test_score_inspection_df["sheet_code"] = (
        test_score_inspection_df["Stage"].apply(get_initials)
        + " - "
        + test_score_inspection_df["Stage element"].apply(get_first_word)
        + " "
        + test_score_inspection_df["Stage Subelement"].astype(str)
    )
    test_score_inspection_df = test_score_inspection_df[
        ["sheet_code", "Inspection [%]"]
    ]
    test_score_inspection = dict(
        zip(
            test_score_inspection_df["sheet_code"],
            test_score_inspection_df["Inspection [%]"],
        )
    )
    logger.debug(f"test_scores_inspection: {test_score_inspection_df}")
    return sheet_dict, test_score_inspection


def get_score(sheet_dict, test_score_inspection):
    """
    Computes the overall and final scores for each load case.

    Args:
        sheet_dict (dict): A dictionary where the keys are sheet names and the values are lists of LoadCase objects.

    Returns:
        tuple: A tuple containing the overall score, overall maximum score, final scores, and final maximum scores.
    """
    final_scores = {}
    final_max_scores = {}

    for sheet_name, load_cases in sheet_dict.items():
        logger.info(sheet_name)

        # Get inspection value for this sheet_name from test_score_inspection_df
        inspection_value = test_score_inspection.get(sheet_name, 0.0)
        logger.info(f"Inspection value for {sheet_name}: {inspection_value}")

        total_score = 0.0
        total_max_score = 0.0
        for load_case in load_cases:
            for seat in load_case.seats:
                dummy = seat.dummy
                dummy_score = dummy.get_score()
                if dummy is not None and dummy_score is not None:
                    total_score += dummy_score
                    total_max_score += dummy.get_max_score()
        logger.info(f"Total score {total_score} - Total max score {total_max_score}")
        total_score = max(total_score - inspection_value * total_max_score / 100, 0.0)
        logger.info(f"Total score {total_score} - Total max score {total_max_score}")
        mapped_value = SHEET_MAPPING[sheet_name]
        if mapped_value not in final_scores:
            final_scores[mapped_value] = 0.0
            final_max_scores[mapped_value] = 0.0

        logger.info(f"Total score {total_score}")
        final_scores[mapped_value] += round(float(total_score), 3)
        final_max_scores[mapped_value] += round(float(total_max_score), 3)

    overall_score = float(math.floor(sum(final_scores.values())))
    overall_max_score = float(sum(final_max_scores.values()))

    return overall_score, overall_max_score, final_scores, final_max_scores
