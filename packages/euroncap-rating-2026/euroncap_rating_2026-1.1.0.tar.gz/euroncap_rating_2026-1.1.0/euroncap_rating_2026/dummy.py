# Copyright 2025, Euro NCAP IVZW
# Created by IVEX NV (https://ivex.ai)
#
# Licensed under the Apache License 2.0.
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from euroncap_rating_2026.body_region import BodyRegion
from euroncap_rating_2026.criteria import Criteria
from euroncap_rating_2026.measurement import Measurement
import pandas as pd
import logging
import numpy as np

logger = logging.getLogger(__name__)


class Dummy(BaseModel):
    """
    Represents a dummy used in vehicle crash tests.

    Attributes:
        name (str): The name of the dummy.
        body_region_list (List[BodyRegion]): A list of body regions in the dummy.
        max_score (Optional[float]): The maximum score for the dummy.
        score (Optional[float]): The score for the dummy.
        capping (Optional[bool]): Indicates if capping is applied to the dummy.
    """

    name: str = Field(
        "HIII-50",
        pattern="^(HIII-50|HIII-05|HIII-95|THOR-50|Q6|Q10|WorldSID-50|Q6-Side|Q10-Side|BioRID-50|HRMD|Adult Headform|Child Headform|aPLI|Upper legform|WorldSID-50-Farside)$",
    )
    body_region_list: List[BodyRegion] = []
    measurement_list: List[Measurement] = []
    max_score: Optional[float] = None
    score: Optional[float] = None
    capping: Optional[bool] = None

    @field_validator("score", mode="before")
    @classmethod
    def ensure_five_decimal_places(cls, v):
        """
        Ensures the score value has three decimal places.

        Args:
            v (float): The score value.

        Returns:
            float: The rounded score value.
        """
        if v is None:
            return v  # Allow None values
        if isinstance(v, (int, float, np.int64)):
            return round(float(v), 5)  # Ensure 5 decimal places
        raise ValueError("Value must be a float or int")

    def get_max_score(self) -> Optional[float]:
        """
        Retrieves the maximum score.

        Returns:
            Optional[float]: The maximum score.
        """
        return self.max_score

    def set_max_score(self, value: Optional[float]):
        """
        Sets the maximum score.

        Args:
            value (Optional[float]): The maximum score.
        """
        if value is None:
            self.max_score = None
            return
        self.max_score = round(value, 4)

    def compute_capping(self) -> None:
        """
        Computes the capping status based on the criteria of the body regions.
        """
        self.capping = any(
            criteria.capping
            for body_region in self.body_region_list
            for criteria in body_region._criteria
        )

    def get_capping(self) -> Optional[bool]:
        """
        Retrieves the capping status.

        Returns:
            Optional[bool]: The capping status.
        """
        return self.capping

    def compute_score(self) -> Optional[float]:
        """
        Computes the score for the dummy based on the scores of the body regions.
        """
        scores = [
            body_region.get_score()
            for body_region in self.body_region_list
            if body_region.get_score() is not None
        ]
        if not scores:
            return None
        logger.debug(f"Body region scores: {scores}")
        total_score = sum(scores)
        if self.capping:
            total_score = 0.0
        self.score = round(total_score, 4)

    def get_score(self) -> Optional[float]:
        """
        Retrieves the score for the dummy.

        Returns:
            Optional[float]: The score for the dummy.
        """
        return self.score

    def set_score(self, value: Optional[float]):
        """
        Sets the score for the dummy.

        Args:
            value (Optional[float]): The score for the dummy.
        """
        if value is None:
            self.score = None
            return
        self.score = round(value, 4)

    def get_body_region(self, body_region_name: str) -> BodyRegion:
        """
        Retrieves a body region by its name.

        Args:
            body_region_name (str): The name of the body region.

        Returns:
            BodyRegion: The body region object.

        Raises:
            ValueError: If the body region is not found.
        """
        for body_region in self.body_region_list:
            if body_region.name == body_region_name:
                return body_region
        raise ValueError(
            f"Body region '{body_region_name}' not found in dummy '{self.name}'"
        )

    @staticmethod
    def get_dummy_from_row(dummy_name, df, row_index):
        """
         This function processes a DataFrame row by row to construct a Dummy object
        based on the provided model description. It validates the input data, extracts
        criteria for each body region, and resolves dependencies between criteria.
            dummy_name (str): The name of the dummy to be created.
            df (pd.DataFrame): The DataFrame containing the data for the dummy.
            row_index (int): The starting index of the row in the DataFrame.
            Dummy: The created Dummy object containing body regions and criteria.
            int: The updated row index after processing the rows for the dummy.
        Raises:
            ValueError: If the dummy name is not found in the model description.
            ValueError: If there are not enough rows in the DataFrame to load all criteria
                for the dummy.
        Notes:
            - The function handles special cases for specific dummy names (e.g., "Q6", "Q10",
              "Q6-Side", "Q10-Side", "WorldSID-50") to adjust criteria dependencies and values.
            - For dummies like "Q6" and "Q10", specific criteria such as "Ares-3ms" and "Ares"
              are handled differently for the "Head" body region.
            - For "WorldSID-50", additional adjustments are made for criteria like "Ares",
              "HIC15", and "Ares-3ms".
        Example:
            dummy, updated_row_index = get_dummy_from_row(
                dummy_name="Q10",
                df=dataframe,
                row_index=0,
        """

        logger.debug(f"Loading dummy: {dummy_name}")

        body_region_list = []
        body_region_measurement_dict = {}

        num_rows_to_inspect = 0
        body_region_criteria_map = {}
        body_region_test_points_map = {}
        for i in range(row_index, len(df)):
            if not pd.isna(df.iloc[i]["Dummy"]) and i != row_index:
                break

            num_rows_to_inspect += 1
            if not pd.isna(df.iloc[i]["Body Region"]):
                current_body_region = df.iloc[i]["Body Region"]
                if "Test Point" in df.columns and not pd.isna(df.iloc[i]["Test Point"]):
                    current_body_region = (
                        f"{current_body_region}_{df.iloc[i]['Test Point']}"
                    )
                    body_region_test_points_map[current_body_region] = df.iloc[i][
                        "Body Region"
                    ]
                if current_body_region not in body_region_criteria_map:
                    body_region_criteria_map[current_body_region] = []
            if not pd.isna(df.iloc[i]["Criteria"]):
                if current_body_region is None:
                    logger.error(
                        f"Error: Criteria '{df.iloc[i]['Criteria']}' found without a corresponding body region at row {i}"
                    )
                    continue
                body_region_criteria_map[current_body_region].append(
                    df.iloc[i]["Criteria"]
                )

        logger.debug(f"Number of rows to inspect: {num_rows_to_inspect}")
        logger.debug(f"Body regions map: {body_region_criteria_map}")
        start_row_index = row_index
        start_row = df.iloc[start_row_index]

        if (
            pd.isna(start_row["Dummy"])
            or pd.isna(start_row["Body Region"])
            or pd.isna(start_row["Criteria"])
        ):
            logger.error(
                f"Error: Indicated row {row_index} is not a valid row to start loading dummy {dummy_name}"
            )
            return None

        head_ares3ms_value = None
        head_hic15_value = None

        current_body_region = None
        for body_region_name, body_region_criteria in body_region_criteria_map.items():
            if body_region_name in body_region_test_points_map:
                body_region_name = body_region_test_points_map[body_region_name]
                logger.debug(
                    f"Body region '{body_region_name}' has test point, using base name: {body_region_name}"
                )
            logger.debug(f"  Loading body region: {body_region_name}")
            body_region_measurement_dict[body_region_name] = []
            criteria_list = []
            for criteria_name in body_region_criteria:
                if criteria_name != df.iloc[row_index]["Criteria"]:
                    error_message = f"Error: At row {row_index} the criteria '{df.iloc[row_index]['Criteria']}' is not the expected '{criteria_name}'"
                    logger.error(error_message)
                    raise ValueError(error_message)

                logger.debug(
                    f"    Loading criteria: {criteria_name} at index {row_index}"
                )
                row = df.iloc[row_index]
                logger.debug("Row index: %s", row_index)
                is_capping = False
                is_measurement = False

                # If LPL and HPL are both NaN, check if it's a measurement:
                # - If Capping is present and not NaN, it's a capping criteria
                # - If Capping is present and NaN, it's a measurement
                # - If Capping is not present, it's a measurement
                if pd.isna(row["LPL"]) and pd.isna(row["HPL"]):
                    if "Capping" in row:
                        if not pd.isna(row["Capping"]):
                            is_capping = True
                        else:
                            is_measurement = True
                    else:
                        is_measurement = True

                if criteria_name == "Farside excursion":
                    row_index += 1
                    continue
                if is_measurement:
                    logger.debug(
                        f"Measurement {criteria_name} detected at row {row_index}"
                    )
                    measurement_values = []
                    if criteria_name in [
                        "Knee load - Variable, left",
                        "Knee load - Variable, right",
                    ]:
                        measurement_values.extend(
                            [
                                (
                                    df.iloc[row_index - 1]["Value"]
                                    if not pd.isna(df.iloc[row_index - 1]["Value"])
                                    else 0.0
                                ),
                                (
                                    df.iloc[row_index - 2]["Value"]
                                    if not pd.isna(df.iloc[row_index - 2]["Value"])
                                    else 0.0
                                ),
                            ]
                        )
                    else:
                        measurement_values.append(
                            row["Value"] if not pd.isna(row["Value"]) else 0.0
                        )

                    measurement = Measurement(
                        name=criteria_name, values=measurement_values
                    )
                    body_region_measurement_dict[body_region_name].append(measurement)
                    row_index += 1
                    continue

                criteria = Criteria.get_criteria_from_row(row)

                if body_region_name == "Head" and criteria.name == "Ares-3ms":
                    head_ares3ms_value = criteria.value

                if body_region_name == "Head" and criteria.name == "HIC15":
                    head_hic15_value = criteria.value

                criteria_list.append(criteria)
                row_index += 1

            body_region_obj = BodyRegion(name=body_region_name)
            logger.debug(
                f"Measurement list for body region '{body_region_name}': {body_region_measurement_dict[body_region_name]}"
            )
            for measurement in body_region_measurement_dict[body_region_name]:
                logger.debug(
                    f"Measurement '{measurement.name}' modifier: {getattr(measurement, 'modifier', None)}"
                )
            body_region_obj.set_measurement_list(
                body_region_measurement_dict[body_region_name]
            )
            body_region_obj.set_criteria_list(criteria_list)
            body_region_list.append(body_region_obj)

        if row_index != start_row_index + num_rows_to_inspect:
            error_message = f"Error: Mismatch in row index calculation. Expected {start_row_index + num_rows_to_inspect}, but got {row_index}."
            logger.error(error_message)
            raise ValueError(error_message)

        if dummy_name in ["Q6", "Q10", "Q6-Side", "Q10-Side"]:
            for body_region in body_region_list:
                if body_region.name == "Head":
                    for criteria in body_region._criteria:
                        # For this dummies, Head Ares-3ms does not depend on Ares
                        if criteria.name == "Ares-3ms":
                            criteria.set_value(head_ares3ms_value)
                            criteria.depends_on = None
                        # For this dummies, Head Ares has always None score
                        if criteria.name == "Ares":
                            criteria.score = None
                # For this dummies, Neck My,extension depends on Head Ares
                elif body_region.name == "Neck":
                    for criteria in body_region._criteria:
                        if criteria.name == "My,extension":
                            head_ares_criteria = next(
                                (
                                    c
                                    for br in body_region_list
                                    if br.name == "Head"
                                    for c in br._criteria
                                    if c.name == "Ares"
                                ),
                                None,
                            )
                            if head_ares_criteria.value < head_ares_criteria.lpl:
                                criteria.score = None
                            else:
                                criteria.set_value(criteria.value)

                            criteria.depends_on = "Ares"

        if dummy_name == "WorldSID-50":
            for body_region in body_region_list:
                if body_region.name == "Head":
                    for criteria in body_region._criteria:
                        if criteria.name == "Ares":
                            criteria.score = None
                            if criteria.capping_value:
                                if criteria.value >= criteria.capping_value:
                                    criteria.capping = True
                                else:
                                    criteria.capping = False
                        elif criteria.name == "HIC15":
                            criteria.depends_on = None
                            criteria.set_value(head_hic15_value)
                        elif criteria.name == "Ares-3ms":
                            criteria.depends_on = None
                            criteria.set_value(head_ares3ms_value)

        return (
            Dummy(name=dummy_name, body_region_list=body_region_list),
            row_index,
        )

    def __repr__(self):
        return f"Dummy('{self.name}', {self.body_region_list})"
