import sys
import pandas as pd
import numpy as np
from collections import Counter
import logging
import os
import random
from dataclasses import dataclass, field
from enum import Enum

from euroncap_rating_2026.load_case import LoadCase
from euroncap_rating_2026.seat import Seat
from euroncap_rating_2026.dummy import Dummy
from euroncap_rating_2026.body_region import BodyRegion
from euroncap_rating_2026.criteria import Criteria, CriteriaType
import openpyxl

logger = logging.getLogger(__name__)

HEADFORMS_START_ROW_INDEX = 0
HEADFORMS_END_ROW_INDEX = 21
LEGFORMS_START_ROW_INDEX = 23
LEGFORMS_END_ROW_INDEX = 28


class VruPredictionColor(str, Enum):
    BLUE = "blue"
    BROWN = "brown"
    D_RED = "d red"
    GREEN = "green"
    GREEN_20 = "green-20"
    GREEN_30 = "green-30"
    GREEN_40 = "green-40"
    GREY = "grey"
    ORANGE = "orange"
    RED = "red"
    YELLOW = "yellow"


VRU_PREDICTION_COLOR_MAP = {
    VruPredictionColor.BLUE: (0 / 255, 102 / 255, 204 / 255),
    VruPredictionColor.BROWN: (150 / 255, 75 / 255, 0 / 255),
    VruPredictionColor.D_RED: (139 / 255, 0 / 255, 0 / 255),  # dark red
    VruPredictionColor.GREEN: (0 / 255, 153 / 255, 51 / 255),
    VruPredictionColor.GREEN_20: (
        204 / 255,
        255 / 255,
        221 / 255,
    ),  # light green (20% green)
    VruPredictionColor.GREEN_30: (
        153 / 255,
        255 / 255,
        187 / 255,
    ),  # lighter green (30% green)
    VruPredictionColor.GREEN_40: (
        102 / 255,
        255 / 255,
        153 / 255,
    ),  # even lighter green (40% green)
    VruPredictionColor.GREY: (128 / 255, 128 / 255, 128 / 255),
    VruPredictionColor.ORANGE: (255 / 255, 153 / 255, 51 / 255),
    VruPredictionColor.RED: (255 / 255, 51 / 255, 51 / 255),
    VruPredictionColor.YELLOW: (255 / 255, 221 / 255, 51 / 255),
}


@dataclass
class VruTestPoint:
    """
    Represents a VRU test point with its coordinates and color.
    """

    row: int
    col: int
    color: VruPredictionColor = None
    loadcase_name: str = None

    @property
    def body_region(self):
        if 18 >= self.row >= 12:
            return "Cyclist"
        elif 11 >= self.row >= 6:
            return "Adult"
        elif 5 >= self.row >= 0:
            return "Child"
        else:
            return None


@dataclass
class LegformTestPoint:
    """
    Represents a legform test point with its coordinates and color.
    """

    row: int
    col: int
    color: VruPredictionColor = None
    loadcase_name: str = None


@dataclass
class VruScore:
    """
    Represents a VRU score with its name and value.
    """

    name: str
    predicted_score: float = 0.0
    blue_points: float = 0.0
    a_pillar: float = 0.0
    max_points: float = 0.0

    COLOR_WEIGHTS = {
        VruPredictionColor.GREEN: 1.0,
        VruPredictionColor.YELLOW: 0.75,
        VruPredictionColor.ORANGE: 0.5,
        VruPredictionColor.BROWN: 0.25,
    }

    def compute_blue_points(self, loadcases):
        blue_scores = 0
        for load_case in loadcases:
            for seat in load_case.seats:
                dummy = seat.dummy
                for body_region in dummy.body_region_list:
                    if body_region.name == self.name:
                        for criteria in body_region._criteria:
                            if criteria.prediction.lower() == "blue":
                                logger.debug(
                                    f"[CP - VRU Head Impact] Found blue prediction in {body_region}: {criteria}"
                                )
                                blue_scores += criteria.get_score()

        self.blue_points = blue_scores / 100.0

    def compute_a_pillar(self, loadcases):
        # Implement weighted sum for Green-40, Green-30, Green-20
        green_40_sum = 0
        green_30_sum = 0
        green_20_sum = 0
        for load_case in loadcases:
            for seat in load_case.seats:
                dummy = seat.dummy
                for body_region in dummy.body_region_list:
                    if body_region.name == self.name:
                        for criteria in body_region._criteria:
                            pred = criteria.prediction.lower()
                            score = criteria.get_score()
                            if pred == "green-40":
                                green_40_sum += score
                            elif pred == "green-30":
                                green_30_sum += score
                            elif pred == "green-20":
                                green_20_sum += score
        weighted_sum = green_40_sum * 3 + green_30_sum * 2 + green_20_sum * 1
        self.a_pillar = weighted_sum / 100.0


def loadcases_to_rows(load_cases):
    """
    Converts a list of load cases to a list of rows for DataFrame creation.

    Args:
    load_cases (list): A list of LoadCase objects.

    Returns:
    list: A list of lists, each representing a row.
    """
    rows = []
    for load_case in load_cases:
        for seat in load_case.seats:
            dummy = seat.dummy
            first_row = True
            for body_region in dummy.body_region_list:
                for criteria in body_region._criteria:
                    if first_row:
                        row = [
                            load_case.name,
                            seat.name,
                            dummy.name,
                        ]
                        first_row = False
                    else:
                        row = ["", "", ""]
                    row += [
                        body_region.name,
                        criteria.test_point,
                        criteria.name,
                        criteria.hpl,
                        criteria.lpl,
                        criteria.capping_value,
                        criteria.prediction,
                        criteria.value,
                    ]
                    rows.append(row)
    # Remove duplicated content in col0 (Loadcase), skip "" cells
    last_non_nan = None
    for idx in range(len(rows)):
        if rows[idx][0] and pd.notna(rows[idx][0]):
            if rows[idx][0] == last_non_nan:
                rows[idx][0] = ""
            else:
                last_non_nan = rows[idx][0]
        elif last_non_nan is not None:
            rows[idx][0] = ""
    # Remove duplicated content in col3 (Body Region), skip "" cells
    last_non_nan_col3 = None
    for idx in range(len(rows)):
        if rows[idx][3] and pd.notna(rows[idx][3]):
            if rows[idx][3] == last_non_nan_col3:
                rows[idx][3] = ""
            else:
                last_non_nan_col3 = rows[idx][3]
        elif last_non_nan_col3 is not None:
            rows[idx][3] = ""
    return rows


def pretty_print_loadcases(loadcases):
    logger.info("pretty_print_loadcases:")
    for lc in loadcases:
        logger.info(f"LoadCase: {lc.name}")
        for seat in lc.seats:
            logger.info(f"  Seat: {seat.name}")
            dummy = seat.dummy
            logger.info(f"    Dummy: {dummy.name}")
            for body_region in getattr(dummy, "body_region_list", []):
                logger.info(f"      BodyRegion: {body_region.name}")
                for criteria in getattr(body_region, "_criteria", []):
                    logger.info(
                        f"        Criteria: {criteria.name}, HPL: {getattr(criteria, 'hpl', None)}, "
                        f"LPL: {getattr(criteria, 'lpl', None)}, "
                        f"Capping: {getattr(criteria, 'capping_value', None)}, "
                        f"Prediction: {getattr(criteria, 'prediction', None)}, "
                        f"Value: {getattr(criteria, 'value', None)}, "
                        f"Score: {getattr(criteria, 'score', None)}, "
                        f"Color: {getattr(criteria, 'color', None)}, "
                        f"Test Point: {getattr(criteria, 'test_point', None)}"
                    )


@dataclass
class VruTestData:
    """
    Represents a collection of VRU test data.
    """

    prediction_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    headform_test_points: list[VruTestPoint] = field(default_factory=list)
    legform_test_points: list[LegformTestPoint] = field(default_factory=list)

    headform_loadcases: list[LoadCase] = field(default_factory=list)
    legform_loadcases: list[LoadCase] = field(default_factory=list)

    headform_scores: dict[str, VruScore] = field(default_factory=dict)
    legform_scores: dict[str, VruScore] = field(default_factory=dict)

    loadcase_dict: dict[str, list[LoadCase]] = field(default_factory=dict)
    df_dict: dict[str, pd.DataFrame] = field(default_factory=dict)

    vru_test_points_all: list[VruTestPoint] = field(default_factory=list)

    def populate_loadcase_dict(self):
        """
        Populates the loadcase_dict with headform and legform loadcases.
        """
        self.loadcase_dict["CP - VRU Head Impact"] = self.headform_loadcases
        self.loadcase_dict["CP - VRU Pelvis & Leg Impact"] = self.legform_loadcases
        self.loadcase_dict["CP - VRU Prediction"] = self.prediction_df
        logger.info(
            f"Loadcase dict populated with {len(self.headform_loadcases)} headform and {len(self.legform_loadcases)} legform loadcases."
        )

    def get_vru_test_points(self):
        """
        Returns a combined list of all VRU test points.
        """
        return self.headform_test_points + self.legform_test_points

    def generate_vru_df(self):
        for vru_sheet in ["CP - VRU Head Impact", "CP - VRU Pelvis & Leg Impact"]:
            loadcase_list = self.loadcase_dict[vru_sheet]
            df_rows = loadcases_to_rows(loadcase_list)
            df = pd.DataFrame(
                df_rows,
                columns=[
                    "Loadcase",
                    "Seat position",
                    "Dummy",
                    "Body Region",
                    "Test Point",
                    "Criteria",
                    "HPL",
                    "LPL",
                    "Capping",
                    "OEM.Prediction",
                    "Value",
                ],
            )
            self.df_dict[vru_sheet] = df  # Store the DataFrame for later use

        self.df_dict["CP - VRU Prediction"] = self.prediction_df

    @staticmethod
    def from_sheet_dict(sheet_dict):
        """
        Creates and returns a VruTestData instance populated from a sheet_dict containing DataFrames for
        "CP - VRU Head Impact" and "CP - VRU Pelvis & Leg Impact".
        """
        vru_test_data = VruTestData()
        # Headform test points and loadcases
        vru_test_data.headform_loadcases = sheet_dict.get("CP - VRU Head Impact", [])
        vru_test_data.headform_test_points = []

        # Build headform test points from headform_loadcases
        for load_case in vru_test_data.headform_loadcases:
            for seat in load_case.seats:
                dummy = seat.dummy
                for body_region in dummy.body_region_list:
                    for criteria in body_region._criteria:
                        test_point_str = getattr(criteria, "test_point", None)
                        if not test_point_str or pd.isna(test_point_str):
                            continue
                        try:
                            row_idx, col_idx = map(int, str(test_point_str).split(","))
                        except Exception:
                            continue
                        color_str = getattr(criteria, "prediction", None)
                        color = None
                        if isinstance(color_str, str):
                            color = next(
                                (
                                    k
                                    for k in VruPredictionColor
                                    if k.value.lower() == color_str.lower()
                                ),
                                VruPredictionColor.GREY,
                            )
                        vtp = VruTestPoint(
                            row=row_idx,
                            col=col_idx,
                            color=color,
                            loadcase_name=load_case.name,
                        )
                        vru_test_data.headform_test_points.append(vtp)

        # Legform test points and loadcases
        vru_test_data.legform_loadcases = sheet_dict.get(
            "CP - VRU Pelvis & Leg Impact", []
        )
        vru_test_data.legform_test_points = []
        for load_case in vru_test_data.legform_loadcases:
            for seat in load_case.seats:
                dummy = seat.dummy
                for body_region in dummy.body_region_list:
                    for criteria in body_region._criteria:
                        test_point_str = getattr(criteria, "test_point", None)
                        if not test_point_str or pd.isna(test_point_str):
                            continue
                        try:
                            row_idx, col_idx = map(int, str(test_point_str).split(","))
                        except Exception:
                            continue
                        color_str = getattr(criteria, "prediction", None)
                        color = None
                        if isinstance(color_str, str):
                            color = next(
                                (
                                    k
                                    for k in VruPredictionColor
                                    if k.value.lower() == color_str.lower()
                                ),
                                VruPredictionColor.GREY,
                            )
                        ltp = LegformTestPoint(
                            row=row_idx,
                            col=col_idx,
                            color=color,
                            loadcase_name=load_case.name,
                        )
                        vru_test_data.legform_test_points.append(ltp)

        # Update criteria.score for all criteria in headform and legform loadcases
        for load_case in (
            vru_test_data.headform_loadcases + vru_test_data.legform_loadcases
        ):
            for seat in load_case.seats:
                dummy = seat.dummy
                for body_region in dummy.body_region_list:
                    for criteria in body_region._criteria:
                        color = criteria.color
                        if load_case.name == "Upper Leg":
                            logger.debug(
                                f"Setting score for criteria at test_point={getattr(criteria, 'test_point', None)}, color={color}"
                            )
                        if color is not None:
                            score = (
                                VruScore.COLOR_WEIGHTS.get(str(color).lower(), 0.0)
                                * 100
                            )
                            criteria.score = score

        return vru_test_data

    def get_vru_points_from_file(self, file_path):
        # Process headform_matrix to initialize vru_test_points_all
        # Read the "CP - VRU Prediction" tab from the Excel file at file_path
        vru_prediction_df = pd.read_excel(file_path, sheet_name="CP - VRU Prediction")

        # Try to read the cell background color as RGB using openpyxl
        wb = openpyxl.load_workbook(file_path, data_only=True)
        ws = wb["CP - VRU Prediction"]

        if not vru_prediction_df.empty:
            # Use the same logic as in process_headform_test to extract all cells
            headforms_matrix = vru_prediction_df.iloc[
                HEADFORMS_START_ROW_INDEX:HEADFORMS_END_ROW_INDEX, :
            ].reset_index(drop=True)
            headforms_matrix = headforms_matrix.iloc[2:, 4:].astype(str).values.tolist()
            for i in range(len(headforms_matrix)):
                for j in range(len(headforms_matrix[0])):

                    cell = ws.cell(
                        row=HEADFORMS_START_ROW_INDEX + 3 + i + 1, column=5 + j
                    )
                    fill = cell.fill
                    rgb_tuple = None
                    if fill and fill.fgColor is not None:
                        fg = fill.fgColor
                        if hasattr(fg, "rgb") and fg.rgb is not None:
                            rgb = fg.rgb  # e.g., 'FF00FF00'
                            if len(rgb) == 8:  # ARGB
                                rgb_tuple = tuple(
                                    int(rgb[k : k + 2], 16) for k in (2, 4, 6)
                                )
                            elif len(rgb) == 6:  # RGB
                                rgb_tuple = tuple(
                                    int(rgb[k : k + 2], 16) for k in (0, 2, 4)
                                )
                        elif hasattr(fg, "theme") or hasattr(fg, "indexed"):
                            # Handle theme/indexed colors if needed
                            pass
                    logger.debug(
                        f"Cell ({HEADFORMS_START_ROW_INDEX + 3 + i + 1}, {5 + j}): RGB: {rgb_tuple}"
                    )
                    # If rgb_tuple is available, try to map it back to a VruPredictionColor using VRU_PREDICTION_COLOR_MAP
                    if rgb_tuple is not None:
                        rgb_normalized = tuple(x / 255 for x in rgb_tuple)
                        # Find the closest color in VRU_PREDICTION_COLOR_MAP
                        for color_enum, rgb_val in VRU_PREDICTION_COLOR_MAP.items():
                            if all(
                                abs(a - b) < 1e-3
                                for a, b in zip(rgb_normalized, rgb_val)
                            ):
                                enum_val = color_enum
                                break
                        else:
                            enum_val = VruPredictionColor.GREY
                    else:
                        enum_val = VruPredictionColor.GREY

                    logger.debug(f"Mapped RGB {rgb_tuple}  to enum_val '{enum_val}'")

                    headforms_matrix[i][j] = enum_val
            self.vru_test_points_all = [
                VruTestPoint(
                    row=18 - i,
                    col=10 - j,
                    color=headforms_matrix[i][j],
                )
                for i in range(len(headforms_matrix))
                for j in range(len(headforms_matrix[0]))
            ]
        else:
            self.vru_test_points_all = []

    def compute_vru_bodyregion_score(self):
        """
        Compute and set headform and legform scores for the VRU test data.
        Updates self.headform_scores and self.legform_scores.
        Returns the legform_final_scores dict.
        """
        # Use instance data
        headform_test_points = self.headform_test_points
        vru_head_impact_loadcases = self.headform_loadcases
        vru_legform_loadcases = self.legform_loadcases

        logger.info("headform_test_points:")
        for point in headform_test_points:
            logger.info(f"  {point}")

        logger.info("vru_head_impact_loadcases:")
        for lc in vru_head_impact_loadcases:
            logger.info(f"  {lc}")

        logger.info("vru_legform_loadcases:")
        for lc in vru_legform_loadcases:
            logger.info(f"  {lc}")

        # Compute headform region scores
        headform_region_scores = {}
        for region in ["Cyclist", "Adult", "Child"]:
            score = compute_vru_score(self.vru_test_points_all, region)
            headform_region_scores[region] = score

        pretty_print_loadcases(vru_head_impact_loadcases)
        pretty_print_loadcases(vru_legform_loadcases)

        # Compute blue points and a_pillar for each region
        for region in ["Cyclist", "Adult", "Child"]:
            region_score = headform_region_scores[region]
            region_score.compute_blue_points(vru_head_impact_loadcases)
            region_score.compute_a_pillar(vru_head_impact_loadcases)

        # Log scores
        logger.info(f"VRU Cyclist Score: {headform_region_scores['Cyclist']}")
        logger.info(f"VRU Adult Score: {headform_region_scores['Adult']}")
        logger.info(f"VRU Child Score: {headform_region_scores['Child']}")

        # Store in self.headform_scores
        self.headform_scores = headform_region_scores

        vru_factors = get_vru_factors(vru_head_impact_loadcases)
        logger.info(f"VRU Factors: {vru_factors}")

        vru_max_points_sum = (
            headform_region_scores["Cyclist"].max_points
            + headform_region_scores["Adult"].max_points
            + headform_region_scores["Child"].max_points
        )

        # Set bodyregion scores in loadcases
        for load_case in vru_head_impact_loadcases:
            for seat in load_case.seats:
                dummy = seat.dummy
                for body_region in dummy.body_region_list:
                    if (
                        load_case.name == "Headform"
                        and seat.name == "Driver"
                        and dummy.name == "Adult Headform"
                        and body_region.name == "Cyclist"
                    ):
                        vru_score = headform_region_scores["Cyclist"]
                        bodyregion_score = (
                            vru_score.predicted_score * vru_factors["correction_factor"]
                            + vru_score.blue_points
                            + vru_score.a_pillar
                        ) / vru_score.max_points
                        bodyregion_score = min(bodyregion_score * 100.0, 100.0)
                        body_region.set_bodyregion_score(bodyregion_score)
                        body_region.set_max_score(
                            vru_score.max_points / vru_max_points_sum * 10.0
                        )
                    if (
                        load_case.name == "Headform"
                        and seat.name == "Driver"
                        and dummy.name == "Adult Headform"
                        and body_region.name == "Adult"
                    ):
                        vru_score = headform_region_scores["Adult"]
                        bodyregion_score = (
                            vru_score.predicted_score * vru_factors["correction_factor"]
                            + vru_score.blue_points
                            + vru_score.a_pillar
                        ) / vru_score.max_points
                        bodyregion_score = min(bodyregion_score * 100.0, 100.0)
                        body_region.set_bodyregion_score(bodyregion_score)
                        body_region.set_max_score(
                            vru_score.max_points / vru_max_points_sum * 10.0
                        )
                    if (
                        load_case.name == "Headform"
                        and seat.name == "Driver"
                        and dummy.name == "Child Headform"
                        and body_region.name == "Child"
                    ):
                        vru_score = headform_region_scores["Child"]
                        bodyregion_score = (
                            vru_score.predicted_score * vru_factors["correction_factor"]
                            + vru_score.blue_points
                            + vru_score.a_pillar
                        ) / vru_score.max_points
                        bodyregion_score = min(bodyregion_score * 100.0, 100.0)
                        body_region.set_bodyregion_score(bodyregion_score)
                        body_region.set_max_score(
                            vru_score.max_points / vru_max_points_sum * 10.0
                        )

        # Compute the sum of minimum criteria scores and count for each VRU legform body region
        legform_body_regions = ["Pelvis", "Femur", "Knee & Tibia"]
        legform_min_score_sum = {br: 0.0 for br in legform_body_regions}
        legform_counts = {br: 0 for br in legform_body_regions}
        pelvis_score = 0.0
        for load_case in vru_legform_loadcases:
            for seat in load_case.seats:
                dummy = seat.dummy
                # For Knee & Tibia, collect all criteria from both regions
                knee_tibia_scores = []
                for body_region in dummy.body_region_list:
                    br_name = body_region.name
                    if br_name == "Knee" or br_name == "Tibia":
                        criteria_scores = [
                            c.get_score()
                            for c in body_region._criteria
                            if c.get_score() is not None
                        ]
                        knee_tibia_scores.extend(criteria_scores)
                        for c in body_region._criteria:
                            logger.debug(
                                f"criteria score for {br_name}: {c.get_score()}, test point: {getattr(c, 'test_point', None)}"
                            )
                    elif br_name in legform_body_regions:
                        criteria_scores = [
                            c.get_score()
                            for c in body_region._criteria
                            if c.get_score() is not None
                        ]
                        for c in body_region._criteria:
                            logger.debug(
                                f"criteria score for {br_name}: {c.get_score()}, test point: {getattr(c, 'test_point', None)}"
                            )
                    if br_name == "Pelvis":
                        pelvis_score += sum(criteria_scores)
                        logger.debug(
                            f"Pelvis score: {pelvis_score}, after adding test point: {getattr(c, 'test_point', None)}"
                        )
                        legform_counts[br_name] += len(criteria_scores)
                    elif br_name == "Femur":
                        min_score = min(criteria_scores)
                        logger.debug(
                            f"Minimum score for {br_name}: {min_score}, test point: {getattr(c, 'test_point', None)}"
                        )
                        legform_min_score_sum[br_name] += min_score
                        legform_counts[br_name] += 1
                # After collecting, process Knee & Tibia as one region
                if knee_tibia_scores:
                    min_score = min(knee_tibia_scores)
                    logger.debug(f"Minimum score for Knee & Tibia: {min_score}")
                    legform_min_score_sum["Knee & Tibia"] += min_score
                    legform_counts["Knee & Tibia"] += 1
        logger.debug("legform_min_score_sum: %s", legform_min_score_sum)
        logger.debug("legform_counts: %s", legform_counts)
        # Calculate the final values: sum divided by 100 and by the count for each body region
        legform_final_scores = {}
        for br in legform_body_regions:
            count = legform_counts[br]

            if count > 0:
                if br == "Pelvis":
                    legform_final_scores[br] = pelvis_score / 100.0 / count * 100.0
                else:
                    legform_final_scores[br] = (
                        legform_min_score_sum[br] / 100.0 / count * 100.0
                    )
            else:
                legform_final_scores[br] = 0.0
        logger.debug("legform_final_scores: %s", legform_final_scores)

        # Store in self.legform_scores
        self.legform_scores = legform_final_scores


def compute_vru_score(vru_test_points, body_region):
    region_cells = [
        point for point in vru_test_points if point.body_region == body_region
    ]
    logger.info(f"region_cells for {body_region}: {region_cells}")
    region_color_counts = Counter(point.color for point in region_cells)

    region_score = VruScore(name=body_region)
    region_score.predicted_score = sum(
        region_color_counts.get(color, 0) * weight
        for color, weight in VruScore.COLOR_WEIGHTS.items()
    )
    # Calculate max_points using vru_test_points_all for the region

    count_valid = sum(
        p.color
        not in (
            VruPredictionColor.GREY,
            VruPredictionColor.GREEN_40,
            VruPredictionColor.GREEN_30,
        )
        for p in region_cells
    )
    count_green_40 = sum(p.color == VruPredictionColor.GREEN_40 for p in region_cells)
    count_green_30 = sum(p.color == VruPredictionColor.GREEN_30 for p in region_cells)
    logger.info(
        f"Max points for {body_region}: valid={count_valid}, green_40={count_green_40}, green_30={count_green_30}"
    )
    region_score.max_points = count_valid + count_green_40 * 3 + count_green_30 * 2
    logger.info(f"{body_region} score: {region_score}")
    return region_score


def get_vru_factors(loadcases):
    # Compute weighted VRU prediction score
    color_weights = {"green": 1.0, "yellow": 0.75, "orange": 0.5, "brown": 0.25}
    color_counts = {"green": 0, "yellow": 0, "orange": 0, "brown": 0}

    # Sum of criteria.score where prediction is not blue
    score_sum = 0.0

    for load_case in loadcases:
        for seat in load_case.seats:
            dummy = seat.dummy
            for body_region in dummy.body_region_list:
                for criteria in body_region._criteria:
                    logger.debug(
                        f"[CP - VRU Prediction] Processing criteria: {criteria} in {body_region}"
                    )
                    prediction = criteria.prediction.lower()
                    if prediction in color_counts:
                        color_counts[prediction] += 1
                    if prediction != "blue":
                        score_sum += criteria.score

    predicted_score_verification = sum(
        color_counts[color] * color_weights[color] for color in color_counts
    )
    # Divide the total score sum by 100
    tested_score_verification = score_sum / 100.0
    if predicted_score_verification == 0:
        vru_correction_factor = 0
    else:
        vru_correction_factor = tested_score_verification / predicted_score_verification
    vru_correction_factor = np.clip(vru_correction_factor, 0.85, 1.15)

    return {
        "predicted_score_verification": predicted_score_verification,
        "tested_score_verification": tested_score_verification,
        "correction_factor": vru_correction_factor,
    }


def frequency_proportional_sample(data, N, seed=None):
    """
    Sample N (row, col, color) tuples from data, using color frequency for proportional sampling.
    Keeps (row, col) in the result.
    """
    if seed is not None:
        random.seed(seed)

    if N >= len(data):
        return data.copy()
    # Count color frequencies
    color_counts = Counter([color for _, _, color in data])
    total = sum(color_counts.values())

    # Compute ideal proportions
    proportions = {color: count / total for color, count in color_counts.items()}
    logger.info(f"proportions: {proportions}")

    # Initial rounded down count
    raw_counts = {}
    for color, p in proportions.items():
        count = int(np.floor(p * N))
        raw_counts[color] = count
    logger.debug(f"raw_counts pre remaining distribution: {raw_counts}")
    # Distribute remaining samples
    remaining = N - sum(raw_counts.values())
    residuals = {
        color: (proportions[color] * N - raw_counts[color]) for color in color_counts
    }
    for color in sorted(residuals, key=residuals.get, reverse=True)[:remaining]:
        raw_counts[color] += 1
    logger.debug(f"raw_counts post remaining distribution: {raw_counts}")

    # Sample actual items, keeping (row, col, color)
    sampled = []
    for color, count in raw_counts.items():
        choices = [x for x in data if x[2] == color]
        sampled += random.sample(choices, min(len(choices), count))

    return sampled


def process_headform_test(vru_prediction_df, vru_params):
    """
    Process the VRU predictions DataFrame to extract headforms  matrices,
    compute color percentages, and randomly select samples based on color distribution.

    Args:
        vru_prediction_df (pd.DataFrame): DataFrame containing VRU predictions.

    Returns:
        None
    """

    # Ensure the DataFrame is not empty
    if vru_prediction_df.empty:
        logger.error("The input DataFrame is empty.")
        return
    logger.info(f"vru_params: {vru_params}")

    # Read number of verification tests for both param codes
    mask_head = (vru_params["param_code"] == "CP - VRU Head Impact") & (
        vru_params["Input parameter"].str.contains(
            "Number of verification tests", na=False
        )
    )
    num_verification_tests_head = (
        int(vru_params.loc[mask_head, "Value"].values[0])
        if not vru_params.loc[mask_head].empty
        else None
    )
    logger.info(
        f"Number of verification tests for headform: {num_verification_tests_head}"
    )

    headforms_matrix = None

    # Headforms matrix: from HEADFORMS_START_ROW_INDEX to HEADFORMS_END_ROW_INDEX - 1
    headforms_matrix = vru_prediction_df.iloc[
        HEADFORMS_START_ROW_INDEX:HEADFORMS_END_ROW_INDEX, :
    ].reset_index(drop=True)

    headforms_matrix = headforms_matrix.iloc[2:, 4:].astype(str).values.tolist()
    # Convert all values in headforms_matrix to VruPredictionColor enum
    for i in range(len(headforms_matrix)):
        for j in range(len(headforms_matrix[0])):
            color_str = headforms_matrix[i][j].lower()
            enum_val = next(
                (k for k in VruPredictionColor if k.value.lower() == color_str),
                VruPredictionColor.GREY,
            )
            headforms_matrix[i][j] = enum_val

    for idx, row in enumerate(headforms_matrix):
        logger.info("%d: %s", idx, row)

    # Compute the percentage of each color occurrence in headforms_matrix and print it
    # Use all color values, including 'd red', 'green-40', 'green-30', 'green-20'
    filtered_colors = [
        (i, j, color)
        for i, row in enumerate(headforms_matrix)
        for j, color in enumerate(row)
        if color
        not in (
            VruPredictionColor.GREY,
            VruPredictionColor.BLUE,
            VruPredictionColor.GREEN_40,
            VruPredictionColor.GREEN_30,
            VruPredictionColor.GREEN_20,
            VruPredictionColor.D_RED,
        )
    ]

    selected_row_col_pairs = frequency_proportional_sample(
        filtered_colors, num_verification_tests_head, seed=None
    )

    logger.info(
        f"Randomly selected {num_verification_tests_head} (row, col) pairs (excluding grey/blue): {selected_row_col_pairs}"
    )

    all_cells = [
        (row, col, headforms_matrix[row][col])
        for row in range(len(headforms_matrix))
        for col in range(len(headforms_matrix[0]))
    ]
    # Add blue points to the selected_row_col_pairs
    for row, col, color in all_cells:
        if color == VruPredictionColor.BLUE:
            selected_row_col_pairs.append((row, col, color))

    vru_test_points_all = []
    for row, col, color in all_cells:
        vru_test_point = VruTestPoint(
            row=18 - row,
            col=10 - col,
            color=color,
        )
        vru_test_points_all.append(vru_test_point)

    # Use selected_row_col_pairs to select test points
    headform_test_points = []
    for row, col, color in selected_row_col_pairs:
        # Directly create a new VruTestPoint without searching
        vtp = VruTestPoint(
            row=18 - row,
            col=10 - col,
            color=color,
        )
        vtp.loadcase_name = "Headform"
        headform_test_points.append(vtp)

    a_pillar_test_points = []
    for row, col, color in all_cells:
        if color in (
            VruPredictionColor.GREEN_40,
            VruPredictionColor.GREEN_30,
            VruPredictionColor.GREEN_20,
        ):
            vtp = VruTestPoint(
                row=18 - row,
                col=10 - col,
                color=color,
            )
            vtp.loadcase_name = "Headform Apillar"
            a_pillar_test_points.append(vtp)
    logger.info("A-Pillar test points created: %s", a_pillar_test_points)

    # Combine headform and a-pillar test points
    test_points = headform_test_points + a_pillar_test_points

    return test_points, vru_test_points_all


def select_blue_pattern(row_idx, matrix, num_verification_tests_leg=None):
    row = matrix[row_idx]
    row_no_grey = [color for color in row if color != VruPredictionColor.GREY]
    logger.info(f"Row without grey: {row_no_grey}")
    all_blue = all(color == VruPredictionColor.BLUE for color in row_no_grey)
    logger.info(f"All row is blue: {all_blue}")
    if all_blue and len(row_no_grey) > 1:
        blue_indices = [
            j for j, color in enumerate(row) if color == VruPredictionColor.BLUE
        ]
        start_blue = blue_indices[0]
        end_blue = blue_indices[-1]
        valid_cols = [
            col
            for col in range(start_blue, end_blue + 1)
            if row[col] != VruPredictionColor.GREY
        ]
        coin = random.randint(0, 1)
        logger.info(f"Coin flip result: {coin}")
        selected_cols = [col for idx, col in enumerate(valid_cols) if (idx % 2 == coin)]
        return [(row_idx, col, matrix[1][col]) for col in selected_cols]
    else:
        # Prepare filtered colors for the row (excluding grey/blue/green-40/green-30/green-20/d red)
        filtered_colors_leg = [
            (row_idx, j, color)
            for j, color in enumerate(row)
            if color
            not in (
                VruPredictionColor.GREY,
                VruPredictionColor.BLUE,
                VruPredictionColor.GREEN_40,
                VruPredictionColor.GREEN_30,
                VruPredictionColor.GREEN_20,
                VruPredictionColor.D_RED,
            )
        ]
        if num_verification_tests_leg is not None:
            selected = frequency_proportional_sample(
                filtered_colors_leg, num_verification_tests_leg, seed=None
            )
        else:
            selected = filtered_colors_leg
        # Also add blue points in this row
        for j, color in enumerate(row):
            if color == VruPredictionColor.BLUE:
                selected.append((row_idx, j, color))
        return selected


def process_legform_test(vru_prediction_df, vru_params):
    """
    Process the VRU predictions DataFrame to extract legform matrices,
    compute color percentages, and randomly select samples based on color distribution.

    Args:
        vru_prediction_df (pd.DataFrame): DataFrame containing VRU predictions.

    Returns:
        None
    """

    # Ensure the DataFrame is not empty
    if vru_prediction_df.empty:
        logger.error("The input DataFrame is empty.")
        return
    logger.info(f"vru_params: {vru_params}")

    # Get number of verification tests for Pelvis and Leg separately
    mask_pelvis = (vru_params["param_code"] == "CP - VRU Pelvis Impact") & (
        vru_params["Input parameter"].str.contains(
            "Number of verification tests", na=False
        )
    )
    num_verification_tests_pelvis = (
        int(vru_params.loc[mask_pelvis, "Value"].values[0])
        if not vru_params.loc[mask_pelvis].empty
        else None
    )

    mask_leg = (vru_params["param_code"] == "CP - VRU Leg Impact") & (
        vru_params["Input parameter"].str.contains(
            "Number of verification tests", na=False
        )
    )
    num_verification_tests_leg = (
        int(vru_params.loc[mask_leg, "Value"].values[0])
        if not vru_params.loc[mask_leg].empty
        else None
    )
    logger.info(
        f"Number of verification tests for pelvis: {num_verification_tests_pelvis}, leg: {num_verification_tests_leg}"
    )

    legform_matrix = None

    # Legforms matrix: from LEGFORMS_START_ROW_INDEX to LEGFORMS_END_ROW_INDEX - 1
    legform_matrix = vru_prediction_df.iloc[
        LEGFORMS_START_ROW_INDEX:LEGFORMS_END_ROW_INDEX, :
    ].reset_index(drop=True)

    legform_matrix = legform_matrix.iloc[2:, 4:].astype(str).values.tolist()
    # Convert all values in legforms_string_matrix to VruPredictionColor enum
    for i in range(len(legform_matrix)):
        for j in range(len(legform_matrix[0])):
            color_str = legform_matrix[i][j].lower()
            enum_val = next(
                (k for k in VruPredictionColor if k.value.lower() == color_str),
                VruPredictionColor.GREY,
            )
            legform_matrix[i][j] = enum_val

    for idx, row in enumerate(legform_matrix):
        logger.info("%d: %s", idx, row)

    selected_row_pelvis = select_blue_pattern(
        0,
        legform_matrix,
        num_verification_tests_leg=num_verification_tests_pelvis,
    )

    # Check if all second row is blue
    # Remove GREY from legform_matrix[1] before checking if all are BLUE
    # Use select_blue_pattern for both all-blue and not-all-blue cases
    selected_row_leg = select_blue_pattern(
        1,
        legform_matrix,
        num_verification_tests_leg=num_verification_tests_leg,
    )
    # Combine pelvis and leg selections, and for each selected col in row 1 (leg), also select the same col in row 2
    selected_row_col_pairs = selected_row_pelvis + selected_row_leg

    # For each (row=1, col, color) in selected_row_leg, add (row=2, col, color_at_row2)
    for row, col, _ in selected_row_leg:
        color_at_row2 = legform_matrix[2][col]
        selected_row_col_pairs.append((2, col, color_at_row2))

    logger.info(
        f"Randomly selected {num_verification_tests_leg} (row, col) pairs (excluding grey/blue): {selected_row_col_pairs}"
    )

    legform_test_points = []
    for row, col, color in selected_row_col_pairs:
        # Directly create a new LegformTestPoint without searching
        vtp = LegformTestPoint(
            row=row,
            col=10 - col,
            color=color,
        )
        if row == 0:
            vtp.loadcase_name = "Upper Leg"
        elif row >= 1:
            vtp.loadcase_name = "Lower Leg"

        legform_test_points.append(vtp)

    return legform_test_points


def process_headform_vru_loadcases(vru_test_points):
    vru_head_impact_loadcases = []

    vru_points_data = []
    for point in vru_test_points:
        point_loadcase_name = point.loadcase_name
        seat_name = "Driver"
        point_body_region = point.body_region
        if point_body_region == "Cyclist":
            dummy_name = "Adult " + point_loadcase_name.split()[0]
        else:
            dummy_name = point_body_region + " " + point_loadcase_name.split()[0]
        logger.debug(
            f"I need to create: loadcase_name={point_loadcase_name}, seat_name={seat_name}, "
            f"dummy.name={dummy_name}, point.body_region={point_body_region}, "
        )
        vru_points_data.append(
            {
                "loadcase": point_loadcase_name,
                "seat": seat_name,
                "dummy": dummy_name,
                "body_region": point_body_region,
                "OEM.Prediction": (
                    getattr(point, "color", None).title()
                    if getattr(point, "color", None)
                    else None
                ),
                "Test point": f"{getattr(point, 'row', '')},{getattr(point, 'col', '')}",
            }
        )
    vru_points_df = pd.DataFrame(vru_points_data)
    vru_points_df = vru_points_df.sort_values(
        by=["loadcase", "dummy", "body_region"]
    ).reset_index(drop=True)

    # Split vru_points_df based on 'loadcase' column
    vru_points_dfs_by_loadcase = {
        loadcase: group.reset_index(drop=True)
        for loadcase, group in vru_points_df.groupby("loadcase")
    }

    for loadcase_name, vru_points_df in vru_points_dfs_by_loadcase.items():
        logger.debug(f"Processing loadcase: {loadcase_name}")
        adult_body_regions = []
        child_body_regions = []
        headform_seats = []
        body_region_dict = {}
        for _, row in vru_points_df.iterrows():

            body_region_name = row["body_region"]
            oem_prediction = row["OEM.Prediction"]
            test_point = row["Test point"]

            if body_region_name not in body_region_dict:
                body_region = BodyRegion(name=body_region_name)
                body_region_dict[body_region_name] = body_region
            else:
                body_region = body_region_dict[body_region_name]

            if oem_prediction.lower() in ["green-20"]:
                hpl = 1000.0
                lpl = 1000.0
            elif oem_prediction.lower() in ["green-40", "green-30"]:
                hpl = 1700.0
                lpl = 1700.0
            else:
                hpl = 650.0
                lpl = 1700.0
            criteria = Criteria(name="HIC15", hpl=hpl, lpl=lpl)
            criteria.criteria_type = CriteriaType.CRITERIA
            criteria.set_prediction(oem_prediction.lower() if oem_prediction else None)
            criteria.set_value(0.0)
            # Set the score based on color weights if available
            score = VruScore.COLOR_WEIGHTS.get(criteria.color.lower(), 0.0) * 100
            criteria.score = score
            criteria.test_point = test_point
            # Add criteria to the body region
            body_region._criteria.append(criteria)

        logger.debug(f"body_region_dict: {body_region_dict}")

        adult_headform_seat = None
        if "Adult" in body_region_dict:
            adult_body_regions.append(body_region_dict["Adult"])
        if "Cyclist" in body_region_dict:
            adult_body_regions.append(body_region_dict["Cyclist"])

        if adult_body_regions:
            adult_headform_dummy = Dummy(
                name="Adult Headform", body_region_list=adult_body_regions
            )
            adult_headform_seat = Seat(name="Driver", dummy=adult_headform_dummy)

        child_headform_seat = None
        if "Child" in body_region_dict:
            child_body_regions.append(body_region_dict["Child"])

        if child_body_regions:
            child_headform_dummy = Dummy(
                name="Child Headform", body_region_list=child_body_regions
            )
            child_headform_seat = Seat(name="Driver", dummy=child_headform_dummy)

        # Always create one seat "Driver" with dummy "Adult Headform" (Adult + Cyclist) and one with "Child Headform" (Child)
        headform_seats = []
        if adult_headform_seat is not None:
            headform_seats.append(adult_headform_seat)
        if child_headform_seat is not None:
            headform_seats.append(child_headform_seat)

        headform_loadcase = LoadCase(name=loadcase_name, seats=headform_seats)

        vru_head_impact_loadcases.append(headform_loadcase)

    return vru_head_impact_loadcases


def process_legform_criteria(criteria, test_point, oem_prediction):
    criteria.criteria_type = CriteriaType.CRITERIA
    criteria.set_value(0.0)
    # Set the score based on color weights if available
    if criteria.value < criteria.hpl:
        score = 100.0
    elif criteria.value >= criteria.lpl:
        score = 0.0
    else:
        score = (
            1 - (criteria.value - criteria.hpl) / (criteria.lpl - criteria.hpl)
        ) * 100.0
    criteria.score = score
    criteria.test_point = test_point
    criteria.set_prediction(oem_prediction.lower() if oem_prediction else None)


def process_legform_vru_loadcases(vru_test_points):
    vru_legform_loadcases = []
    # Group test points by loadcase
    loadcase_points = {}
    for point in vru_test_points:
        loadcase_points.setdefault(point.loadcase_name, []).append(point)

    upper_legform_criteria = []

    for loadcase_name, points in loadcase_points.items():
        seat_name = "Driver"
        if loadcase_name == "Upper Leg":
            dummy_name = "Upper legform"
            body_region_names = ["Pelvis"]
        elif loadcase_name == "Lower Leg":
            dummy_name = "aPLI"
            body_region_names = ["Femur", "Knee", "Tibia"]
        else:
            continue  # skip unknown loadcase

        seats = []
        for point in points:
            # Prepare body regions for this test point
            body_region_dict = {
                name: BodyRegion(name=name) for name in body_region_names
            }

            oem_prediction = (
                getattr(point, "color", None).title()
                if getattr(point, "color", None)
                else None
            )
            test_point = f"{getattr(point, 'row', '')},{getattr(point, 'col', '')}"

            # Assign criteria to each body region as per Euro NCAP protocol
            if "Pelvis" in body_region_dict:
                criteria = Criteria(name="Sum of forces", hpl=5.00, lpl=6.00)
                process_legform_criteria(criteria, test_point, oem_prediction)
                upper_legform_criteria.append(criteria)
            if "Femur" in body_region_dict:
                for f in ["F1", "F2", "F3"]:
                    criteria = Criteria(
                        name=f"Bending moment, {f}", hpl=390.00, lpl=440.00
                    )
                    process_legform_criteria(criteria, test_point, oem_prediction)
                    body_region_dict["Femur"]._criteria.append(criteria)
            if "Knee" in body_region_dict:
                criteria = Criteria(name="MCL elongation", hpl=27.00, lpl=32.00)
                process_legform_criteria(criteria, test_point, oem_prediction)
                body_region_dict["Knee"]._criteria.append(criteria)
            if "Tibia" in body_region_dict:
                for t in ["T1", "T2", "T3", "T4"]:
                    criteria = Criteria(
                        name=f"Bending moment, {t}", hpl=275.00, lpl=320.00
                    )
                    process_legform_criteria(criteria, test_point, oem_prediction)
                    body_region_dict["Tibia"]._criteria.append(criteria)

            if loadcase_name == "Lower Leg":
                # For Lower Leg: 1 seat, 1 dummy, 3 body regions (Femur, Knee, Tibia) with all criteria
                body_regions = [
                    body_region_dict[name]
                    for name in ["Femur", "Knee", "Tibia"]
                    if name in body_region_dict
                ]
                if body_regions:
                    dummy = Dummy(name=dummy_name, body_region_list=body_regions)
                    seat = Seat(name=seat_name, dummy=dummy)
                    seats.append(seat)

        # Log body_region_dict in order
        for name in body_region_names:
            if name in body_region_dict:
                logger.debug(f"body_region_dict[{name}]: {body_region_dict[name]}")
                for criteria in body_region_dict[name]._criteria:
                    logger.debug(f"    Criteria: {criteria}")

        if loadcase_name == "Upper Leg":
            # For Upper Leg: 1 seat, 1 dummy, 1 body region (Pelvis) with all criteria
            # Create the Pelvis body region and assign all upper_legform_criteria to it
            pelvis_body_region = BodyRegion(name="Pelvis")
            pelvis_body_region._criteria = upper_legform_criteria
            body_regions = [pelvis_body_region]
            dummy = Dummy(name=dummy_name, body_region_list=body_regions)
            seat = Seat(name=seat_name, dummy=dummy)
            seats.append(seat)

        legform_loadcase = LoadCase(name=loadcase_name, seats=seats)
        vru_legform_loadcases.append(legform_loadcase)

    return vru_legform_loadcases
