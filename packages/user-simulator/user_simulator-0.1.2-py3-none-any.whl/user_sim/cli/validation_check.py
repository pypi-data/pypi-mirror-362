import os
import csv
import json
import time
import pandas as pd
import yaml
from user_sim.utils.show_logs import *
import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from src.user_sim.core.role_structure import RoleData
from src.user_sim.utils.utilities import read_yaml


logger = logging.getLogger('Info Logger')


@dataclass
class ValidationIssue:
    field: str
    error: str
    error_type: str
    location: str

class ProfileValidation:

    def __init__(self, profile, export_path):
        self.profile = profile
        self.timestamp = int(time.time())
        self.export_path = export_path + f"/run_{self.timestamp}"
        self.profile_errors = []
        self.error_number = 0
        self.conversation_number = 0
        self.combinations_dict = {}

    def export_matrix_to_csv(self, matrix_combination=False):
        df = pd.DataFrame()
        combinations = 0

        for combinations_dict in self.combinations_dict:
            name = "_".join(combinations_dict.get('name', []))
            matrix = combinations_dict.get('matrix', [])
            func_type = combinations_dict.get("type", '')
            combinations = combinations_dict.get('combinations', 0)

            if matrix_combination:
              if df.empty:
                  df = pd.DataFrame(matrix, columns=combinations_dict.get('name'))
              else:
                  df_new = pd.DataFrame(matrix, columns=combinations_dict.get('name'))
                  df = pd.concat([df, df_new], axis=1)
                  combinations = len(df)

            else:
                filename = f"{name}_{func_type}_{combinations}_{self.timestamp}.csv"
                path = f"{self.export_path}/combination_matrices"
                filepath = f"{path}/{filename}"
                if not os.path.exists(path):
                    os.makedirs(path)
                try:
                    df = pd.DataFrame(matrix, columns=combinations_dict.get('name'))
                    df.to_csv(filepath, index=False)
                except Exception as e:
                    logger.error(f"Couldn't export matrix dataframe: {e}")
                logger.info(f"Combinations file saved as: {filepath}")

        if matrix_combination:
            filename = f"full_matrix_{combinations}_{self.timestamp}.csv"
            path = f"{self.export_path}/combination_matrices"
            filepath = f"{path}/{filename}"
            if not os.path.exists(path):
                os.makedirs(path)
            try:
                df.to_csv(filepath, index=False)
            except Exception as e:
                logger.error(f"Couldn't export matrix dataframe: {e}")
            logger.info(f"Combinations file saved as: {filepath}")

    def collect_errors(self, e, prefix="", message=None):
        e_msg = f"{message}: {str(e)}" if message else str(e)
        self.profile_errors.append(
            {"field": 'unknown',
             "error": e_msg,
             "type": type(e).__name__,
             "location": prefix}
            # ValidationIssue(
            #     field='unknown',
            #     error=e_msg,
            #     error_type=type(e).__name__,
            #     location=prefix
            # )
        )

    def validate(self):
        try:
            profile = read_yaml(self.profile)
            user_profile = RoleData(profile, validation=True)
            self.profile_errors, self.error_number = user_profile.get_errors()
            self.conversation_number = user_profile.conversation_number
            self.combinations_dict = user_profile.combinations_dict
        except Exception as e:
            self.collect_errors(e, "YAML_file", message="Invalid YAML syntax")

    def show_report(self, matrix_combination=False):
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
            logger.info(f"Validation report directory created at {self.export_path}")

        error_result = {
            "errors": self.profile_errors,
            "total_errors": self.error_number
        }

        json_result = json.dumps(error_result, indent=4, ensure_ascii=False)
        filepath = f"{self.export_path}/errors_{self.timestamp}.json"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_result)

        for c_dict in self.combinations_dict:
            self.export_matrix_to_csv(matrix_combination)


def main():
    parser = ArgumentParser(description='Conversation generator for a chatbot')
    parser.add_argument('--profile', default='.',
                        help='Directory where the profile is located.')
    parser.add_argument("--export", default='.',
                        help="Directory where the report will be exported")
    parser.add_argument('--verbose', action='store_true', help='Shows debug prints')
    parser.add_argument('--combined_matrix', action='store_true', help='Shows debug prints')
    args = parser.parse_args()

    logger = create_logger(args.verbose, 'Info Logger')
    logger.info('Logs enabled!')

    validation = ProfileValidation(args.profile, args.export)
    validation.validate()
    validation.show_report(args.combined_matrix)


if __name__ == "__main__":
    main()