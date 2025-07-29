from typing import Optional, List
import importlib
import hashlib
import time

from purr_petra_cli.xformer import PURR_WHERE
from pathlib import Path
import pyodbc
from typing import Any, Dict, Union, Literal, Tuple, TypeAlias
from purr_petra_cli.dbisam import db_exec


def parse_uwis(uwis: Optional[str]) -> List[str] | None:
    """Parse POSTed uwi string into a suitable SQLAnywhere SIMILAR TO clause.
    Split by commas or spaces, replace '*' with '%', joined to '|'

    Example:
        0505* pilot %0001 -> '0505%|pilot|%0001'

    Args:
        uwis (Optional[str]): incoming request string

    Returns:
        List[str]: A list of UWI strings if present
    """
    if uwis is None:
        return uwis

    try:
        split = [
            item
            for item in uwis.strip().replace(",", " ").replace('"', "").split()
            if item
        ]
        parsed = [item.replace("*", "%").replace("'", "''") for item in split]
        # logger.debug(f"parse_uwi returns: {parsed}")
        return parsed
    except AttributeError as ae:
        print(ae)
        # logger.error(f"'uwis' must be a string, not {type(uwis)}")
        return []
    except Exception as e:  # pylint: disable=broad-except
        # logger.error(f"Unexpected error occurred: {str(e)}")
        print(e)
        return []


def get_recipe(asset: str) -> Dict[str, Any]:
    module_path = f"purr_petra_cli.recipes.{asset}"
    try:
        recipe_module = importlib.import_module(module_path)
        return getattr(recipe_module, "recipe")

    except ModuleNotFoundError as mnfe:
        print(f"Error: failed to find recipe at: {module_path}")
        raise mnfe

    except AttributeError as ae:
        print(f"Error: No recipe in module: '{module_path}'")
        raise ae


def make_repo_id(proj: str) -> str:
    fp = Path(proj)
    prefix = fp.name.upper()[:3]
    if len(fp.name) < 3:
        prefix = prefix.ljust(3, "_")
    suffix = hashlib.md5(str(fp).lower().encode()).hexdigest()[:6]
    return f"{prefix}_{suffix}"


def timestamp_filename(proj: str, asset: str) -> str:
    repo_id = make_repo_id(proj)

    return f"{repo_id}_{int(time.time_ns())}_{asset}".lower()


def ensure_dir(dir: str) -> str:
    Path(dir).mkdir(parents=True, exist_ok=True)
    return str(dir)


def make_where_clause(uwi_list: List[str] | None):
    """Construct the UWI-centric part of a WHERE clause containing UWIs. The
    WHERE clause will start: "WHERE 1=1 " to which we append:
    "AND u_uwi LIKE '0123%' OR u_uwi LIKE '4567'"

    Args:
        uwi_list (List[str]): List of UWI strings with optional wildcard chars
    """
    # ASSUMES u.uwi WILL ALWAYS BE THE UWI FILTER
    col = "u.uwi"
    clause = "WHERE 1=1"
    if uwi_list:
        uwis = [f"{col} LIKE '{uwi}'" for uwi in uwi_list]
        clause += " AND " + " OR ".join(uwis)

    return clause


def make_id_in_clauses(identifier_keys: List[str], ids: List[Union[str, int]]) -> str:
    """Generate a SQL WHERE clause for filtering by IDs"""
    clause = "WHERE 1=1 "
    if len(identifier_keys) == 1 and str(ids[0]).replace("'", "").isdigit():
        no_quotes = ",".join(str(i).replace("'", "") for i in ids)
        clause += f"AND {identifier_keys[0]} IN ({no_quotes})"
    else:
        idc = " || '-' || ".join(f"CAST({i} AS VARCHAR(10))" for i in identifier_keys)
        ids_str = ",".join(str(i) for i in ids)
        clause += f"AND {idc} IN ({ids_str})"
    return clause


def create_selectors(
    chunked_ids: List[List[Union[str, int]]], identifier_keys: List[str], selector: str
) -> List[str]:
    """Create a list of SQL selectors based on recipe and chunked ids"""
    selectors = []
    for ids in chunked_ids:
        in_clause = make_id_in_clauses(identifier_keys, ids)
        select_sql = selector.replace(PURR_WHERE, in_clause)
        selectors.append(select_sql)
    return selectors


ColTypes: TypeAlias = Union[
    Literal["string", "int64", "float64", "bool", "datetime64[ns]", "object"], str
]


def map_col_type(sql_type):
    """
    Map SQL data types to pandas data types.
    """
    type_map = {
        int: "int64",
        str: "string",
        float: "float64",
        bool: "bool",
        type(None): "object",
        "datetime64[ns]": "datetime64[ns]",
    }
    return type_map.get(sql_type, "object")


def get_column_info(cursor: pyodbc.Cursor) -> Tuple[List[str], Dict[str, str]]:
    """Return column names, types from pyodbc/SQLAnywhere"""
    cursor_desc = cursor.description
    column_names = [col[0] for col in cursor_desc]
    column_types = {col[0]: map_col_type(col[1]) for col in cursor_desc}
    return column_names, column_types


def get_id_list(conn, id_sql):
    """
    Executes and asset recipe's identifier SQL and returns ids.
    :return: Results will be either be a single "keylist"
    [{keylist: ["1-62", "1-82", "2-83", "2-84"]}]
    or a list of key ids
    [{key: "1-62"}, {key: "1-82"}, {key: "2-83"}, {key: "2-84"}]
    Force int() or str(); the typical case is a list of int
    """

    def int_or_string(obj):
        try:
            return int(obj)
        except ValueError:
            return f"'{str(obj).strip()}'"

    res = db_exec(conn, id_sql)

    if isinstance(res, Exception):
        print(res)
        return []

    ids = []

    if not res:
        print("no ids found")
    elif "keylist" in res[0] and res[0]["keylist"] is not None:
        ids = res[0]["keylist"].split(",")
    elif "key" in res[0] and res[0]["key"] is not None:
        ids = [k["key"] for k in res]
    else:
        print("key or keylist missing; cannot make id list")

    # use a Set here to avoid having to use costly DISTINCT in SQL
    uniq_keys = {int_or_string(i) for i in ids}
    return list(uniq_keys)


def chunk_ids(ids, chunk):
    """
    [621, 826, 831, 834, 835, 838, 846, 847, 848]
    ...with chunk=4...
    [[621, 826, 831, 834], [835, 838, 846, 847], [848]]

    ["1-62", "1-82", "2-83", "2-83", "2-83", "2-83", "2-84", "3-84", "4-84"]
    ...with chunk=4...
    [
        ['1-62', '1-82'],
        ['2-83', '2-83', '2-83', '2-83', '2-84'],
        ['3-84', '4-84']
    ]
    Note how the group of 2's is kept together, even if it exceeds chunk=4

    :param ids: This is usually a list of wsn ints: [11, 22, 33, 44] but may
        also be "compound" str : ['1-11', '1-22', '1-33', '2-22', '2-44'].
    :param chunk: The preferred batch size to process in a single query
    :return: List of id lists
    """

    if len(ids) == 0:
        return []

    id_groups = {}

    for item in ids:
        left = str(item).split("-", maxsplit=1)[0]
        if left not in id_groups:
            id_groups[left] = []
        id_groups[left].append(item)

    result = []
    current_subarray = []

    for group in id_groups.values():
        if len(current_subarray) + len(group) <= chunk:
            current_subarray.extend(group)
        else:
            result.append(current_subarray)
            current_subarray = group[:]

    if current_subarray:
        result.append(current_subarray)

    return result
