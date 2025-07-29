# Copyright 2025, Euro NCAP IVZW
# Created by IVEX NV (https://ivex.ai)
#
# Licensed under the Apache License 2.0.
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
import pandas as pd
import numpy as np
import logging
from enum import Enum

logger = logging.getLogger(__name__)

# Mapping of colors to their corresponding score values
color_to_value = {
    "green": 100.0,
    "yellow": 80.0,
    "orange": 40.0,
    "brown": 20.0,
    "red": 0.0,
}


class CriteriaType(Enum):
    UNKNOWN = 0
    CRITERIA = 1
    ZERO_SWITCH = 2
    NONE_SWITCH = 3
    DISABLED = 4
    INVERTED_CRITERIA = 5
    COLOR_CRITERIA = 6
    CAPPING_CRITERIA = 7


class Criteria(BaseModel):
    """
    Represents a criteria used in vehicle crash tests.

    Attributes:
        name (str): The name of the criteria.
        hpl (Optional[float]): The high-performance limit.
        lpl (float): The low-performance limit.
        capping (bool): Indicates if capping is applied to the criteria.
        capping_value (Optional[float]): The capping value for the criteria.
        value (float): The value of the criteria.
        score (float): The score of the criteria.
        color (Optional[str]): The color representing the criteria's performance.
        prediction (Optional[str]): The predicted color for the criteria.
        prediction_result (Optional[str]): The result of the prediction.
        depends_on (str): The criteria that this criteria depends on.
    """

    name: str
    hpl: Optional[float] = None
    lpl: Optional[float] = None
    capping: bool = False
    capping_value: Optional[float] = None
    value: float = 0.0
    score: float = 0.0
    color: Optional[str] = Field(None, pattern="^(green|yellow|orange|brown|red)$")
    prediction: Optional[str] = Field(
        None,
        pattern="^(green|yellow|orange|brown|red|blue|green-40|green-30|green-20)$",
    )
    prediction_result: Optional[str] = Field(
        None, pattern="^(Correct|Incorrect|In Tolerance)$"
    )
    depends_on: str = None
    criteria_type: CriteriaType = CriteriaType.UNKNOWN
    test_point: Optional[str] = None

    @field_validator("value", mode="before")
    @classmethod
    def ensure_two_decimal_places(cls, v):
        """
        Ensures the value has two decimal places.

        Args:
            v (float): The value.

        Returns:
            float: The rounded value.
        """
        if isinstance(v, (int, float, np.int64)):
            return round(float(v), 2)  # Ensure 2 decimal places
        raise ValueError("Value must be a float or int")

    @field_validator("capping_value", mode="before")
    @classmethod
    def ensure_two_decimal_places_cap(cls, v):
        """
        Ensures the capping value has two decimal places.

        Args:
            v (float): The capping value.

        Returns:
            float: The rounded capping value.
        """
        if v is None:
            return v  # Allow None values
        if isinstance(v, (int, float, np.int64)):
            return round(float(v), 2)  # Ensure 2 decimal places
        raise ValueError("Value must be a float or int")

    @property
    def interval_step(self):
        """
        Calculates the interval step for the criteria.

        Returns:
            float: The interval step.
        """
        return round((self.lpl - self.hpl) / 3, 2)

    @property
    def green_yellow_threshold(self):
        """
        Calculates the green-yellow threshold for the criteria.

        Returns:
            float: The green-yellow threshold.
        """
        if self.criteria_type == CriteriaType.NONE_SWITCH:
            return None
        else:
            return round(self.hpl, 2)

    @property
    def yellow_orange_threshold(self):
        """
        Calculates the yellow-orange threshold for the criteria.

        Returns:
            float: The yellow-orange threshold.
        """
        if self.criteria_type == CriteriaType.NONE_SWITCH:
            return None
        else:
            return round(self.hpl + (self.lpl - self.hpl) / 3, 2)

    @property
    def orange_brown_threshold(self):
        """
        Calculates the orange-brown threshold for the criteria.

        Returns:
            float: The orange-brown threshold.
        """
        if self.criteria_type == CriteriaType.NONE_SWITCH:
            return None
        else:
            return round(self.hpl + 2 * (self.lpl - self.hpl) / 3, 2)

    @property
    def brown_red_threshold(self):
        """
        Calculates the brown-red threshold for the criteria.

        Returns:
            float: The brown-red threshold.
        """
        if self.criteria_type == CriteriaType.NONE_SWITCH:
            return None
        else:
            return round(self.lpl, 2)

    def set_prediction(self, prediction_color):
        """
        Sets the prediction color for the criteria.

        Args:
            prediction_color (str): The prediction color.
        """
        self.prediction = prediction_color

    def get_value(self):
        """
        Returns the value for the criteria.

        Returns:
            float: The value of the criteria.
        """
        return self.value

    def set_value(self, value):
        """
        Sets the value for the criteria and calculates the color and score.

        Args:
            value (float): The value to set.
        """
        self.value = round(value, 2)
        if self.capping_value:
            if self.value >= self.capping_value:
                self.capping = True
            else:
                self.capping = False
        self.calculate_color_score()

    def get_score(self):
        """
        Returns the score for the criteria.

        Returns:
            float: The score of the criteria.
        """
        return self.score

    def set_capping_value(self, value):
        """
        Sets the capping value for the criteria.

        Args:
            value (float): The capping value to set.
        """
        self.capping_value = round(value, 2)
        if self.capping_value:
            if self.value >= self.capping_value:
                self.capping = True
            else:
                self.capping = False

    def calculate_color_score(self):
        """
        Calculates the color and score for the criteria based on its value and thresholds.
        """
        logger.debug(f"Calculating color and score for value: {self.value}")
        if pd.isna(self.value):
            logger.debug("Value is None, setting color to None and score to 0.0.")
            self.color = None
            self.score = 0.0

            return

        if self.criteria_type == CriteriaType.CAPPING_CRITERIA:
            if self.value is not None and self.capping_value is not None:
                if self.value >= self.capping_value:
                    self.capping = True
                else:
                    self.capping = False
            logger.debug(
                f"[RESULT] Criteria type: {self.criteria_type}, Capping: {self.capping}"
            )
            self.score = None
            return
        if self.criteria_type == CriteriaType.UNKNOWN:
            if self.value is not None and self.capping_value is not None:
                if self.value >= self.capping_value:
                    self.capping = True
                else:
                    self.capping = False
            logger.debug(
                f"[RESULT] Criteria type: {self.criteria_type}, Capping: {self.capping}"
            )
            return

        if self.criteria_type == CriteriaType.NONE_SWITCH:
            if self.value < self.lpl:
                self.score = 100.0
            else:
                self.score = None
            self.color = None
            logger.debug(
                f"[RESULT] Criteria type: {self.criteria_type}, Color: {self.color}, Score: {self.score}"
            )
            return

        if (
            self.criteria_type == CriteriaType.CRITERIA
            or self.criteria_type == CriteriaType.ZERO_SWITCH
        ):
            logger.debug(
                f"Thresholds for {self.name}: "
                f"green_yellow={self.green_yellow_threshold}, "
                f"yellow_orange={self.yellow_orange_threshold}, "
                f"orange_brown={self.orange_brown_threshold}, "
                f"brown_red={self.brown_red_threshold}"
            )
            # Current assumption is that interval are ALWAYS
            # Closed on the left (<=) - Open on the right (<)
            # v1 <= x < v2
            if self.value < self.green_yellow_threshold:
                test_output_color = "green"
            elif self.value < self.yellow_orange_threshold:
                test_output_color = "yellow"
            elif self.value < self.orange_brown_threshold:
                test_output_color = "orange"
            elif self.value < self.brown_red_threshold:
                test_output_color = "brown"
            else:
                test_output_color = "red"

            if self.prediction is not None:
                increase_factor = round(self.interval_step / 4.0, 2)

                if test_output_color == self.prediction:
                    self.prediction_result = "Correct"
                    self.color = self.prediction
                elif (
                    (
                        self.prediction == "green"
                        and self.value
                        < round(self.green_yellow_threshold + increase_factor, 2)
                    )
                    or (
                        self.prediction == "yellow"
                        and round(self.green_yellow_threshold - increase_factor, 2)
                        <= self.value
                        < round(self.yellow_orange_threshold + increase_factor, 2)
                    )
                    or (
                        self.prediction == "orange"
                        and round(self.yellow_orange_threshold - increase_factor, 2)
                        <= self.value
                        < round(self.orange_brown_threshold + increase_factor, 2)
                    )
                    or (
                        self.prediction == "brown"
                        and round(self.orange_brown_threshold - increase_factor, 2)
                        <= self.value
                        < round(self.brown_red_threshold + increase_factor, 2)
                    )
                    or (
                        self.prediction == "red"
                        and self.value
                        >= round(self.brown_red_threshold - increase_factor, 2)
                    )
                ):
                    self.prediction_result = "In Tolerance"
                    self.color = self.prediction
                else:
                    self.prediction_result = "Incorrect"
                    self.color = test_output_color
                logger.debug(
                    f"Prediction: {self.prediction}, "
                    f"Prediction Result: {self.prediction_result}, "
                    f"Test Output Color: {test_output_color}, "
                    f"Final Color: {self.color}"
                )
            else:
                self.color = test_output_color
        elif self.criteria_type == CriteriaType.INVERTED_CRITERIA:
            # For inverted criteria intervals are
            # Open on the left (<) - Closed on the right (<=)
            # v1 < x <= v2
            if self.value > self.green_yellow_threshold:
                test_output_color = "green"
            elif self.value > self.yellow_orange_threshold:
                test_output_color = "yellow"
            elif self.value > self.orange_brown_threshold:
                test_output_color = "orange"
            elif self.value > self.brown_red_threshold:
                test_output_color = "brown"
            else:
                test_output_color = "red"

            if self.prediction is not None:
                increase_factor = round(self.interval_step / 4.0, 2)

                if test_output_color == self.prediction:
                    self.prediction_result = "Correct"
                    self.color = self.prediction
                elif (
                    (
                        self.prediction == "green"
                        and round(self.green_yellow_threshold - increase_factor, 2)
                        <= self.value
                    )
                    or (
                        self.prediction == "yellow"
                        and round(self.green_yellow_threshold + increase_factor, 2)
                        > self.value
                        >= round(self.yellow_orange_threshold - increase_factor, 2)
                    )
                    or (
                        self.prediction == "orange"
                        and round(self.yellow_orange_threshold + increase_factor, 2)
                        > self.value
                        >= round(self.orange_brown_threshold - increase_factor, 2)
                    )
                    or (
                        self.prediction == "brown"
                        and round(self.orange_brown_threshold + increase_factor, 2)
                        > self.value
                        >= round(self.brown_red_threshold - increase_factor, 2)
                    )
                    or (
                        self.prediction == "red"
                        and self.value
                        < round(self.brown_red_threshold + increase_factor, 2)
                    )
                ):
                    self.prediction_result = "In Tolerance"
                    self.color = self.prediction
                else:
                    self.prediction_result = "Incorrect"
                    self.color = test_output_color
                logger.debug(
                    f"Prediction: {self.prediction}, "
                    f"Prediction Result: {self.prediction_result}, "
                    f"Test Output Color: {test_output_color}, "
                    f"Final Color: {self.color}"
                )
            else:
                self.color = test_output_color

        if self.color is not None:
            self.score = color_to_value[self.color]

        if self.capping_value:
            if self.value >= self.capping_value:
                self.capping = True
            else:
                self.capping = False
        logger.debug(
            f"[RESULT] Criteria type: {self.criteria_type}, Color: {self.color}, Score: {self.score}"
        )

    @staticmethod
    def get_criteria_from_row(row, criteria_type=CriteriaType.UNKNOWN):
        """
        Creates a Criteria object from a row of data.

        Args:
            row (pd.Series): The row of data.

        Returns:
            Criteria: The created Criteria object.
        """
        name = row["Criteria"]
        hpl = row["HPL"]
        lpl = row["LPL"]
        value = row["Value"]
        logger.debug(f"Name: {name}, HPL: {hpl}, LPL: {lpl}, Value: {value}")
        prediction = None

        criteria_type = CriteriaType.UNKNOWN
        if not pd.isna(row["LPL"]) and not pd.isna(row["HPL"]):
            if row["HPL"] < row["LPL"]:
                criteria_type = CriteriaType.CRITERIA
            elif row["HPL"] == row["LPL"]:
                criteria_type = CriteriaType.ZERO_SWITCH
            else:
                criteria_type = CriteriaType.INVERTED_CRITERIA
        elif not pd.isna(row["LPL"]) and pd.isna(row["HPL"]):
            criteria_type = CriteriaType.NONE_SWITCH
        elif pd.isna(row["LPL"]) and pd.isna(row["HPL"]):
            criteria_type = CriteriaType.CAPPING_CRITERIA

        logger.debug(f"Criteria Type: {criteria_type}")
        value = round(value, 2)

        if "OEM.Prediction" in row and not pd.isna(row["OEM.Prediction"]):
            prediction = row["OEM.Prediction"].lower()
        capping_value = None
        if "Capping" in row and not pd.isna(row["Capping"]):
            capping_value = round(row["Capping"], 2)
        if pd.isna(hpl):
            hpl = None
        criteria = Criteria(
            name=name,
            hpl=hpl,
            lpl=lpl,
            capping_value=capping_value,
            value=value,
            prediction=prediction,
            criteria_type=criteria_type,
        )
        if "Test Point" in row and not pd.isna(row["Test Point"]):
            criteria.test_point = row["Test Point"]

        criteria.calculate_color_score()
        return criteria


class ColorCriteria(BaseModel):
    name: str
    criteria_type: CriteriaType = CriteriaType.COLOR_CRITERIA
    color: Optional[str] = Field(None, pattern="^(green|yellow|orange|brown|red)$")
    countermeasure: bool
    redline_above_125mm: bool

    @property
    def score(self) -> float:
        if self.countermeasure:
            if self.color in ["green", "yellow"]:
                return 100.0
            elif self.color == "orange":
                return 75.0
            elif self.color == "red":
                return 50.0 if not self.redline_above_125mm else 25.0
        else:
            if self.color in ["green", "yellow"]:
                return 100.0
            elif self.color == "orange":
                return 75.0
            else:
                return 0.0
