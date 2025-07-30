import logging
import pandas as pd
from typing import Dict


logging.basicConfig(
    level=logging.INFO,             
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[logging.StreamHandler()] 
)


class DictionaryParser:
    """
    Class Responsible for parsing through 
    """

    @staticmethod
    def parse_multiple(result_dict:dict) -> Dict[str, pd.DataFrame] | None:
        """
        Quick parser to convert multiple comapny dict to data_frame
        """
        try:
            return {
                key:DictionaryParser.parse_single(result_dict=company_dict)
                for key, company_dict in result_dict.items()
                if "AI" in key
            }
        
        except Exception as e:
            logging.error(f"ERROR DictionaryParser -> (parse_multiple): {e}")
            return None

    @staticmethod
    def parse_single(result_dict:dict) -> pd.DataFrame | None:
        """
        Quick parser to convert parse single company output to dataframe
        """
        if not isinstance(result_dict, dict):
            logging.error(f"Key does not exist")
            return None
        
        results = result_dict.get("results", None)
        if results is None:
            logging.error("result_dict has no key 'results'")
            return None
        
        try:
            final_result = [
                {
                    "alpha_code":row.get("alpha_code", None),
                    "calculation_date":row.get("calculation_date", None),
                    **row.get("ratio_values", {})
                }
                for row in results if isinstance(row, dict)
            ]
            
            data_df = pd.DataFrame(final_result)
            return data_df
        
        except Exception as e:
            logging.error(f"ERROR DictionaryParser -> (parse_single): {e}")
            return None
    