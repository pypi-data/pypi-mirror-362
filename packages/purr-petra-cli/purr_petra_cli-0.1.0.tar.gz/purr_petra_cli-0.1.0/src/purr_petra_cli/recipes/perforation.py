"""Petra perforation"""

from purr_petra_cli.xformer import PURR_WHERE

"""
Petra's concept of perfs is less 'overwrought' than geographix. The sensible
thing is to consider common dates to signify a single completion event. The
completion may even be indicated by the API number's last 4 digits:
0001, 0002, 0003 signify recompletions
maybe in 11th position like 0100 if it's a horizontal well"
"""


identifier_keys = ["w.wsn", "p.recid"]
id_form = " || '-' || ".join([f"CAST({i} AS VARCHAR(10))" for i in identifier_keys])

selector = f"""
    SELECT
        w.wsn          AS w_wsn,
        w.uwi          AS w_uwi,

        u.wsn          AS u_wsn,
        u.uwi          AS u_uwi,
        u.label        AS u_label,
        u.sortname     AS u_sortname,
        u.flags        AS u_flags,        

        p.recid        AS p_recid,
        p.wsn          AS p_wsn,
        p.flags        AS p_flags,
        p.date         AS p_date,
        p.enddate      AS p_enddate,
        p.top          AS p_top,
        p.base         AS p_base,
        p.diameter     AS p_diameter,
        p.numshots     AS p_numshots,
        p.method       AS p_method,
        p.comptype     AS p_comptype,
        p.perftype     AS p_perftype,
        p.remark       AS p_remark,
        p.fmname       AS p_fmname,
        p.chgdate      AS p_chgdate,
        p.source       AS p_source

    FROM well w
    LEFT JOIN uwi u ON u.wsn = w.wsn
    JOIN perfs p ON p.wsn = w.wsn
    {PURR_WHERE}
    """

identifier = f"""
    SELECT
        LIST({id_form}) AS keylist
    FROM well w
    LEFT JOIN uwi u ON u.wsn = w.wsn
    JOIN perfs p ON p.wsn = w.wsn
    {PURR_WHERE}
    """

recipe = {
    "selector": selector,
    "identifier": identifier,
    "prefixes": {
        "w_": "well",
        "u_": "uwi",
        "p_": "perfs",
    },
    "identifier_keys": identifier_keys,
    "xforms": {
        "w_chgdate": "excel_date",
        "p_date": "excel_date",
        "p_enddate": "excel_date",
        "p_remark": "memo_to_string",
        "p_chgdate": "excel_date",
    },
    "post_process": "perforation_agg",
    "chunk_size": 1000,
}
