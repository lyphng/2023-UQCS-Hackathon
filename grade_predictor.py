from typing import Iterable

import numpy as np
import pandas as pd
from sklearn import preprocessing, linear_model


class GradePredictor:
    """
    Predicts the user's grades for a UQ course based on the user's past grades
    and SECAT data.
    """
    def __init__(
        self,
        secat_data_path: str,
        base_grade_prediction_weighting: float = 1/100,
    ):
        """
        Loads the SECAT data and makes the base grade predictions for every
        course using only the SECAT data.

        :param secat_data_path: the file path to the SECAT JSON file
        :param base_grade_prediction_weighting: the weighting (importance) given
            to the predictions made using only the SECAT data
        """
        self._full_course_data = pd.read_json(secat_data_path, lines=True)
        self.model = linear_model.LinearRegression()

        self._use_base_grade_predictions = base_grade_prediction_weighting != 0
        if base_grade_prediction_weighting:
            self._user_grade_prediction_weighting = (
                1 / base_grade_prediction_weighting
            )
            self.base_grade_predictions = self._get_base_grade_predictions()

        prefixes = self._full_course_data["course"].str[:4]
        self._prefix_encoder = preprocessing.LabelEncoder().fit(prefixes)
        self._full_course_data["prefix"] = (
            self._prefix_encoder.transform(prefixes)
        )
        self._full_course_data["level"] = (
            self._full_course_data["course"].str[4]
        )

    def fit(
        self, user_courses: Iterable[str], user_grades: Iterable[float]
    ) -> None:
        """
        Fits the predictor with the user's past courses and their corresponding
        grades.

        :param user_courses: the user's past courses
        :param user_grades: the grades corresponding to each course in
            user_courses
        """
        if self._use_base_grade_predictions:
            user_grades = np.repeat(
                user_grades,
                int(
                    self._user_grade_prediction_weighting
                    * len(self._full_course_data)
                ),
            )
            user_courses = np.repeat(
                user_courses,
                int(
                    self._user_grade_prediction_weighting
                    * len(self._full_course_data)
                ),
            )
            userless_grades = self.base_grade_predictions["grade"].values
            userless_courses = self.base_grade_predictions["course"]

            grades = np.concatenate([user_grades, userless_grades])
            courses = np.concatenate([user_courses, userless_courses])
        else:
            grades = np.array(user_grades)
            courses = np.array(user_courses)

        features = self._get_course_features(courses)
        self.model.fit(features, grades)

    def predict(self, new_courses: Iterable[str]) -> list[float]:
        """
        Predicts the grades for the given new courses
        :param new_courses: the new courses to predict the grades for
        :return: the predicted grades for the courses in new_courses
        """
        features = self._get_course_features(np.array(new_courses))
        predictions = self.model.predict(features)
        return predictions

    def _get_base_grade_predictions(self) -> pd.DataFrame:
        courses = self._full_course_data["course"]
        grade_preds = (
            self._full_course_data["Q2"]
            / self._full_course_data["Q2"].quantile(0.9)
            * 7
        )
        return pd.DataFrame({"course": courses, "grade": grade_preds})

    def _get_course_features(self, courses: np.ndarray) -> np.ndarray:
        courses = pd.Series(courses, name="course")
        course_data = pd.merge(courses, self._full_course_data, on="course")
        features = course_data.drop("course", axis="columns").values
        return features


if __name__ == "__main__":
    predictor = GradePredictor(
        "course_data_clean.json", base_grade_prediction_weighting=1/100
    )
    predictor.fit(
        ["CSSE1001", "CSSE2002", "MATH1051", "MATH1052"], [7, 7, 5, 5]
    )
    new_courses = ["CSSE2010", "CSSE2310", "MATH1061", "MATH2401"]
    grade_predictions = predictor.predict(new_courses)

    for course, grade in zip(new_courses, grade_predictions):
        print(course, round(grade, 2))
