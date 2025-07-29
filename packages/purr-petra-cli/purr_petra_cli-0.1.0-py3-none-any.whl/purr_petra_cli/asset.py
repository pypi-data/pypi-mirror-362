import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import pyodbc
from purr_petra_cli.util import (
    chunk_ids,
    create_selectors,
    get_id_list,
    get_column_info,
    get_recipe,
    make_repo_id,
    make_where_clause,
    timestamp_filename,
)
from purr_petra_cli.dbisam import make_conn_params
from purr_petra_cli.post_process import post_process
from purr_petra_cli.xformer import PURR_WHERE, formatters, transform_dataframe_to_json


######################
import psutil
from concurrent.futures import ThreadPoolExecutor


# Function to estimate number of threads based on available memory (in MB)
def estimate_thread_count(memory_per_thread_mb=500):
    mem = psutil.virtual_memory()
    available_mb = mem.available / (1024 * 1024)  # Convert bytes to MB
    max_threads = int(available_mb // memory_per_thread_mb)
    return max(1, max_threads)  # At least 1 thread


@dataclass
class AssetConfig:
    asset: str
    proj: str
    uwis_list: Optional[List[str]]

    def out_file(self):
        return timestamp_filename(self.proj, self.asset)

    @property
    def repo_id(self):
        return make_repo_id(self.proj)

    @property
    def recipe(self):
        return get_recipe(self.asset)

    @property
    def conn(self):
        return make_conn_params(self.proj)

    @property
    def xforms(self):
        return self.recipe.get("xforms", {})

    @property
    def prefixes(self):
        return self.recipe.get("prefixes", {})

    @property
    def selectors(self):
        where = make_where_clause(self.uwis_list)

        id_sql = self.recipe["identifier"].replace(PURR_WHERE, where)
        chunk_size = self.recipe["chunk_size"] if "chunk_size" in self.recipe else 1000

        ids = get_id_list(self.conn, id_sql)

        chunked_ids = chunk_ids(ids, chunk_size)

        selectors = create_selectors(
            chunked_ids=chunked_ids,
            identifier_keys=self.recipe["identifier_keys"],
            selector=self.recipe["selector"],
        )

        return selectors

    @property
    def post_processor(self):
        if proc_name := self.recipe.get("post_process"):
            return post_process[proc_name]


def compose_and_write_docs(
    cfg: AssetConfig, select: str, out_file: str
) -> tuple[str, int]:
    all_columns = set()

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("[")  # Start of JSON array
        docs_written = 0

        with pyodbc.connect(**cfg.conn) as con:
            cursor = con.cursor()
            cursor.execute(select)
            column_names, column_types = get_column_info(cursor)
            df = pd.DataFrame(
                [tuple(row) for row in cursor.fetchall()], columns=column_names
            )

            all_columns.update(df.columns)

            for col in df.columns:
                col_type = str(df.dtypes[col])
                xform = cfg.xforms.get(col, col_type)
                formatter = formatters.get(xform, lambda x: x)
                df[col] = df[col].apply(formatter)

            df = df.replace({np.nan: None})

            if cfg.post_processor:
                df = cfg.post_processor(df)

            json_data: List[Dict[str, Any]] = transform_dataframe_to_json(
                df, cfg.prefixes
            )

            for json_obj in json_data:
                json_obj["proj"] = cfg.proj
                json_obj["repo_id"] = cfg.repo_id
                json_str = json.dumps(json_obj, default=str)
                f.write(json_str + ",")
                docs_written += 1

        if docs_written > 0:
            f.seek(f.tell() - 1, 0)  # Remove the last comma
        f.write("]")  # End JSON array

    return out_file, docs_written


######################
def run_in_parallel(cfg, output_dir: str):
    num_threads = estimate_thread_count()
    out_files = []

    def task(select):
        out_file = str(Path(output_dir, cfg.out_file()).with_suffix(".json"))
        result = compose_and_write_docs(cfg, select, out_file)
        out_files.append(out_file)
        return result

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(task, cfg.selectors))

    return results


######################


def select_assets(proj: str, asset: str, uwis_list: List[str] | None, output_dir: str):
    cfg = AssetConfig(asset=asset, proj=proj, uwis_list=uwis_list)
    # for x in cfg.selectors:
    #     print(x)

    # return
    x = run_in_parallel(cfg, output_dir)
    print("xxxxxxxxxxxxxxxx")
    print(x)
    print("xxxxxxxxxxxxxxxx")
