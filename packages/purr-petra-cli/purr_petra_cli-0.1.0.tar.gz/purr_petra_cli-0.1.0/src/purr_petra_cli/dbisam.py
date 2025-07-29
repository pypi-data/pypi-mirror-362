from pathlib import Path
from typing import Any, Dict, List
import pyodbc


DBISAM_DRIVER = "DBISAM 4 ODBC Driver"
DBISAM_FETCH_SIZE = 1000


def db_exec(conn: Dict, sql: str) -> List[Dict[str, Any]] | Exception:
    results = []
    try:
        with pyodbc.connect(**conn) as connection:
            connection.setencoding("CP1252")
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                while True:
                    rows = cursor.fetchmany(DBISAM_FETCH_SIZE)
                    if not rows:
                        break
                    results.extend([dict(zip(columns, row)) for row in rows])
        return results
    except pyodbc.ProgrammingError as pe:
        raise pe
    except Exception as ex:
        raise ex


def db_exec2(conn: Dict, sql: str) -> List[Dict[str, Any]] | Exception:
    """Convenience method for using pyodbc and DBISAM with Petra

    The dreaded "DBISAM Engine Error # 11013. Access denied to table or file"
    error might happen with malware scans or slow networks or bad luck, but
    removing asyncio seems to have mitigated most occurrences.

    Args:
        conn (dict): DBISAM connection parameters.
        sql (str): A single SQL statement to execute on the database.

    Returns:
        List[Dict[str, Any]]: list of dicts representing rows from query result.

    Raises:
        - pyodbc.ProgrammingError: For cases where table(s) might not exist due
        to an unxepected schema.
        - If the databases is older than DBISAM v4 (i.e Petra from about 2017),
        the general Exception will be something like: "not the correct version"
    """

    try:
        # pylint: disable=c-extension-no-member
        with pyodbc.connect(**conn) as connection:
            # I suspect S&P does not modify this per locale, but you should
            # probably verify the dbisam encoding if dealing with non-US data.
            # DBISAM says Locale = "ANSI Standard"
            connection.setencoding("CP1252")

            with connection.cursor() as cursor:
                cursor.execute(sql)

                return [
                    dict(zip([col[0] for col in cursor.description], row))
                    for row in cursor.fetchall()
                ]

    except pyodbc.ProgrammingError as pe:
        # logger.error(pe)
        raise pe
    except Exception as ex:
        # logger.error(ex)
        raise ex


def make_conn_params(proj: str) -> dict:
    """Assemble Petra-centric connection parameters used by pyodbc

    Args:
        repo_path (str): Path to a Petra project base directory.

    Returns:
        dict: dictionary of DBISAM connection parameters.
    """
    params = {"driver": DBISAM_DRIVER, "catalogname": str(Path(proj) / "DB")}
    return params


def make_parms_conn_params(proj: str) -> dict:
    """Assemble Petra-centric connection parameters for PARMS used by pyodbc

    Args:
        repo_path (str): Path to a Petra project base directory.

    Returns:
        dict: dictionary of DBISAM connection parameters.
    """
    params = {"driver": DBISAM_DRIVER, "catalogname": str(Path(proj) / "PARMS")}
    return params
