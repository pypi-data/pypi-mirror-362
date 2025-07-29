import json
import tempfile
from enum import Enum
from pathlib import Path
from typing import List, Optional, cast
import typer
from purr_petra_cli.setup import prepare
from purr_petra_cli.proj import validate_proj_dir
from purr_petra_cli.util import parse_uwis, ensure_dir
from purr_petra_cli.asset import select_assets


app = typer.Typer()


class Asset(str, Enum):
    core = "core"
    dst = "dst"
    formation = "formation"
    ip = "ip"
    perforation = "perforation"
    production = "production"
    raster_log = "raster_log"
    survey = "survey"
    vector_log = "vector_log"
    well = "well"
    zone = "zone"


asset_members_str = ", ".join([member.value for member in Asset])


@app.command()
def collect(
    proj: str = typer.Option(
        ...,
        help="Path to project directory, It's probably a UNC path",
        callback=validate_proj_dir,
        show_envvar=False,
    ),
    asset: Asset = typer.Option(
        Asset.well, help=f"The asset (choose from: {asset_members_str})"
    ),
    uwis: Optional[str] = typer.Option(
        None,
        help="Full or partial UWI list. Separate UWIs with spaces or commas. "
        + "Use * or % as wildcards. This is a single arg, so wrap it in quotes."
        + '  Example: --uwis "05010001102000 350112* 350110*"  '
        + "omitting the --uwis arg selects everything--BEWARE!",
        callback=parse_uwis,
    ),
    output_dir: str = typer.Option(
        Path(tempfile.gettempdir()),
        help="Define an output directory store exported json data. "
        + "Enclose paths with spaces in quotes."
        + "(Defaults to System TEMP).",
        callback=ensure_dir,
    ),
):
    # asset = asset.value # to get a real string from the Enum causes type error

    uwis_list = cast(Optional[List[str]], uwis)

    print("proj=", proj)
    print("asset=", asset.value)
    print("uwis=", uwis)
    print("uwis_list=", uwis_list)
    print("output_dir=", output_dir)

    # epsg = get_storage_epsg(proj)

    res = select_assets(
        proj=proj,
        asset=asset.value,
        uwis_list=uwis_list,
        output_dir=output_dir,
    )
    print(json.dumps(res, indent=4))
    # print(res)


@app.command()
def setup():
    """
    Register the Elevate Software dbodbc.dll to enable querying Petra databases.

    RUN THIS COMMAND IN A CONSOLE AS ADMINISTRATOR. It writes to the registry.
    This command requires no additional options or configuration.
    """
    prepare()


if __name__ == "__main__":
    app()


# C:\Users\bryan\dev\purr_petra_cli>uv pip install -e .
# C:\Users\bryan\dev\purr_petra_cli>uv run purr-petra-cli collect --proj IAMaproj --asset dst
# INTERSTATE has 05009052460000,
# --uwis "1234*,050090524*" should return
#   [3074, 3075, 3076, 3077, 3078, 3079, 3080, 3081, 3082, 3083]

# uv run purr-petra-cli collect --asset well --proj C:\dev_data\petra\projects\INTERSTATE
# stack: 35087204750001
