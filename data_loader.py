import os
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

import pandas as pd


class CSVDataLoader(ABC):
    @abstractmethod
    def _read_metadata(self, metadata_path: str) -> Tuple[List[str], Dict]:
        pass

    @abstractmethod
    def read_table(self, table_name: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_table_names(self) -> List[str]:
        pass
    
    @abstractmethod
    def get_queries(self) -> Dict[str, List[str]]:
        pass


class SpiderCSVDataLoader(CSVDataLoader):
    def __init__(self, dataset_dir: str, metadata_path: str):
        self.dataset_dir = dataset_dir        
        self.table_names, self.queries = self._read_metadata(metadata_path)
    
    def _read_metadata(self, metadata_path: str) -> Tuple[List[str], Dict]:
        table_names = []
        queries = {}

        metadata_df = pd.read_csv(metadata_path)

        for _, row in metadata_df.iterrows():
            db_name = row["db name"]
            t1_name, c1_name = row["t1 name"], row["c1 name"]
            t2_name, c2_name = row["t2 name"], row["c2 name"]
            subj_name = row["subject name"]

            # Skip ID column that does not have subject column
            if subj_name == "-": 
                continue

            t1_path = os.path.join(db_name, t1_name)
            if t1_path not in table_names:
                table_names.append(t1_path)
            
            t2_path = os.path.join(db_name, t2_name)
            if t2_path not in table_names:
                table_names.append(t2_path)

            query_id = t1_path + "!" + subj_name
            answer = t2_path + "!" + subj_name
            if query_id in queries:
                queries[query_id].append(answer)
            else:
                queries[query_id] = [answer]

        return table_names, queries
    
    def read_table(self, table_name: str, drop_nan=True, **kwargs) -> pd.DataFrame:
        table_path = os.path.join(self.dataset_dir, f"{table_name}.csv")
        table = pd.read_csv(
            table_path, on_bad_lines="skip", lineterminator="\n", **kwargs)
        
        if drop_nan:
            table.dropna(axis=1, how="all", inplace=True)
            table.dropna(axis=0, how="any", inplace=True)

        return table

    def get_table_names(self) -> List[str]:
        return self.table_names
    
    def get_queries(self) -> Dict[str, List[str]]:
        return self.queries


if __name__ == "__main__":
    """
    Test Spider dataloader
    """
    dataset_dir = "/data/spider_artifact/tables"
    metadata_path = "/data/spider_artifact/dev_metadata.csv"
    dataloader = SpiderCSVDataLoader(dataset_dir, metadata_path)
