from __future__ import annotations

import os
import re
from datetime import date, datetime, time, timezone
from typing import Any

import pandas as pd
import swisseph as swe

SIGN_NAMES = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

SIGN_LORDS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}

PLANET_ORDER = [
    "Asc",
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    "Rahu",
    "Ketu",
]

PLANET_IDS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Rahu": swe.TRUE_NODE,
    "Ketu": swe.TRUE_NODE,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

COMBUSTION_ORB = {
    "Moon": 12,
    "Mars": 17,
    "Mercury": 13,
    "Venus": 9,
    "Jupiter": 11,
    "Saturn": 15,
    "Neptune": 11,
    "Pluto": 16,
    "Uranus": 16,
}

NAKSHATRA_LORDS = {
    "Ashwini": "Ketu",
    "Bharani": "Venus",
    "Krittika": "Sun",
    "Rohini": "Moon",
    "Mrigashira": "Mars",
    "Ardra": "Rahu",
    "Punarvasu": "Jupiter",
    "Pushya": "Saturn",
    "Ashlesha": "Mercury",
    "Magha": "Ketu",
    "Purva Phalguni": "Venus",
    "Uttara Phalguni": "Sun",
    "Hasta": "Moon",
    "Chitra": "Mars",
    "Swati": "Rahu",
    "Vishakha": "Jupiter",
    "Anuradha": "Saturn",
    "Jyeshtha": "Mercury",
    "Mula": "Ketu",
    "Purva Ashadha": "Venus",
    "Uttara Ashadha": "Sun",
    "Abhijit": "Sun",
    "Shravana": "Moon",
    "Dhanishta": "Mars",
    "Shatabhisha": "Rahu",
    "Purva Bhadrapada": "Jupiter",
    "Uttara Bhadrapada": "Saturn",
    "Revati": "Mercury",
}

NAKSHATRA_RANGES = [
    ("Ashwini", 0.0, 13.3333),
    ("Bharani", 13.3333, 26.6667),
    ("Krittika", 26.6667, 40.0),
    ("Rohini", 40.0, 53.3333),
    ("Mrigashira", 53.3333, 66.6667),
    ("Ardra", 66.6667, 80.0),
    ("Punarvasu", 80.0, 93.3333),
    ("Pushya", 93.3333, 106.6667),
    ("Ashlesha", 106.6667, 120.0),
    ("Magha", 120.0, 133.3333),
    ("Purva Phalguni", 133.3333, 146.6667),
    ("Uttara Phalguni", 146.6667, 160.0),
    ("Hasta", 160.0, 173.3333),
    ("Chitra", 173.3333, 186.6667),
    ("Swati", 186.6667, 200.0),
    ("Vishakha", 200.0, 213.3333),
    ("Anuradha", 213.3333, 226.6667),
    ("Jyeshtha", 226.6667, 240.0),
    ("Mula", 240.0, 253.3333),
    ("Purva Ashadha", 253.3333, 266.6667),
    ("Uttara Ashadha", 266.6667, 276.6667),
    ("Abhijit", 276.6667, 280.8889),
    ("Shravana", 280.8889, 293.3333),
    ("Dhanishta", 293.3333, 306.6667),
    ("Shatabhisha", 306.6667, 320.0),
    ("Purva Bhadrapada", 320.0, 333.3333),
    ("Uttara Bhadrapada", 333.3333, 346.6667),
    ("Revati", 346.6667, 360.0),
]

D9_NAVAMSA_TABLE = [
    [1, 10, 7, 4, 1, 10, 7, 4, 1, 10, 7, 4],
    [2, 11, 8, 5, 2, 11, 8, 5, 2, 11, 8, 5],
    [3, 12, 9, 6, 3, 12, 9, 6, 3, 12, 9, 6],
    [4, 1, 10, 7, 4, 1, 10, 7, 4, 1, 10, 7],
    [5, 2, 11, 8, 5, 2, 11, 8, 5, 2, 11, 8],
    [6, 3, 12, 9, 6, 3, 12, 9, 6, 3, 12, 9],
    [7, 4, 1, 10, 7, 4, 1, 10, 7, 4, 1, 10],
    [8, 5, 2, 11, 8, 5, 2, 11, 8, 5, 2, 11],
    [9, 6, 3, 12, 9, 6, 3, 12, 9, 6, 3, 12],
]

NADI_MAP = {
    "Ashwini": "Pawan",
    "Bharani": "Prachanda",
    "Krittika": "Prachanda",
    "Rohini": "Pawan",
    "Mrigashira": "Dahan",
    "Ardra": "Soumya",
    "Punarvasu": "Neera",
    "Pushya": "Jala",
    "Ashlesha": "Amrit",
    "Magha": "Amrit",
    "Purva Phalguni": "Jala",
    "Uttara Phalguni": "Neera",
    "Hasta": "Soumya",
    "Chitra": "Dahan",
    "Swati": "Pawan",
    "Vishakha": "Prachanda",
    "Anuradha": "Prachanda",
    "Jyeshtha": "Pawan",
    "Mula": "Dahan",
    "Purva Ashadha": "Soumya",
    "Uttara Ashadha": "Neera",
    "Shravana": "Amrit",
    "Dhanishta": "Amrit",
    "Shatabhisha": "Jala",
    "Purva Bhadrapada": "Neera",
    "Uttara Bhadrapada": "Soumya",
    "Revati": "Dahan",
}

PUSHKARA_NAVAMSA_MAP = {
    "Aries": [((20, 0), (23, 20), "Libra"), ((26, 40), (30, 0), "Sagittarius")],
    "Taurus": [((6, 40), (10, 0), "Pisces"), ((13, 20), (16, 40), "Taurus")],
    "Gemini": [((16, 40), (20, 0), "Pisces"), ((23, 20), (26, 40), "Taurus")],
    "Cancer": [((0, 0), (3, 20), "Cancer"), ((6, 40), (10, 0), "Virgo")],
    "Leo": [((20, 0), (23, 20), "Libra"), ((26, 40), (30, 0), "Sagittarius")],
    "Virgo": [((6, 40), (10, 0), "Pisces"), ((13, 20), (16, 40), "Taurus")],
    "Libra": [((16, 40), (20, 0), "Pisces"), ((23, 20), (26, 40), "Taurus")],
    "Scorpio": [((0, 0), (3, 20), "Cancer"), ((6, 40), (10, 0), "Virgo")],
    "Sagittarius": [((20, 0), (23, 20), "Libra"), ((26, 40), (30, 0), "Sagittarius")],
    "Capricorn": [((6, 40), (10, 0), "Pisces"), ((13, 20), (16, 40), "Taurus")],
    "Aquarius": [((16, 40), (20, 0), "Pisces"), ((23, 20), (26, 40), "Taurus")],
    "Pisces": [((0, 0), (3, 20), "Cancer"), ((6, 40), (10, 0), "Virgo")],
}


def _deg_to_dms_str(deg: float) -> str:
    d = int(deg)
    m = int((deg - d) * 60)
    s = int(round((deg - d) * 3600 % 60))
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        d += 1
    return f"{d:02d}°{m:02d}'{s:02d}\""


def _dms_to_seconds(dms_str: str) -> int:
    s = re.sub(r"[^\d]", " ", str(dms_str))
    s = re.sub(r"\s+", " ", s).strip()
    parts = s.split()
    while len(parts) < 3:
        parts.append("0")
    d, m, sec = [int(float(x)) for x in parts[:3]]
    return d * 3600 + m * 60 + sec


def _dms_to_deg(dms_str: str) -> float:
    nums = [int(x) for x in re.findall(r"\d+", str(dms_str))]
    d, m, s = (nums + [0, 0])[:3]
    return d + m / 60 + s / 3600


def _lat_to_dms(val: float) -> str:
    sign = "-" if val < 0 else ""
    val = abs(val)
    d = int(val)
    m = int((val - d) * 60)
    s = int(round((val - d) * 3600 % 60))
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        d += 1
    return f"{sign}{d:02d}°{m:02d}'{s:02d}\""


def _build_nak_pada_ranges() -> list[dict[str, Any]]:
    nak_order = [
        "Ashwini",
        "Bharani",
        "Krittika",
        "Rohini",
        "Mrigashira",
        "Ardra",
        "Punarvasu",
        "Pushya",
        "Ashlesha",
        "Magha",
        "Purva Phalguni",
        "Uttara Phalguni",
        "Hasta",
        "Chitra",
        "Swati",
        "Vishakha",
        "Anuradha",
        "Jyeshtha",
        "Mula",
        "Purva Ashadha",
        "Uttara Ashadha",
        "Shravana",
        "Dhanishta",
        "Shatabhisha",
        "Purva Bhadrapada",
        "Uttara Bhadrapada",
        "Revati",
    ]
    nak_len = 13 + 20 / 60.0
    pada_len = nak_len / 4.0

    ranges: list[dict[str, Any]] = []
    deg = 0.0
    for nak in nak_order:
        for pada in (1, 2, 3, 4):
            start = deg
            end = deg + pada_len
            ranges.append(
                {
                    "start": start,
                    "end": end,
                    "nak": nak,
                    "pada": pada,
                    "nak_lord": NAKSHATRA_LORDS.get(nak, "Unknown"),
                }
            )
            deg = end

    abhijit_start = 270 + 6 + 40 / 60.0
    abhijit_end = 270 + 10 + 53 / 60.0 + 20 / 3600.0
    ranges.append(
        {
            "start": abhijit_start,
            "end": abhijit_end,
            "nak": "Abhijit",
            "pada": 1,
            "nak_lord": NAKSHATRA_LORDS["Abhijit"],
        }
    )
    return ranges


NAK_PADA_RANGES = _build_nak_pada_ranges()


def d9_nak_pada_from_abs_long(abs_long_sid_deg: float) -> tuple[str, int, str]:
    d = abs_long_sid_deg % 360.0

    for row in NAK_PADA_RANGES:
        if row["nak"] == "Abhijit" and row["start"] <= d < row["end"]:
            return row["nak"], row["pada"], row["nak_lord"]

    for row in NAK_PADA_RANGES:
        if row["nak"] == "Abhijit":
            continue
        if row["start"] <= d < row["end"]:
            return row["nak"], row["pada"], row["nak_lord"]

    last_regular = [r for r in NAK_PADA_RANGES if r["nak"] != "Abhijit"][-1]
    return last_regular["nak"], last_regular["pada"], last_regular["nak_lord"]


def get_nakshatra_fixed(abs_long_sid_deg: float) -> tuple[str, int, str]:
    d = abs_long_sid_deg % 360
    for name, start, end in NAKSHATRA_RANGES:
        if start <= d < end:
            lord = NAKSHATRA_LORDS.get(name, "Unknown")
            span = end - start
            pada_size = span / 4.0
            pada = int((d - start) // pada_size) + 1
            return name, pada, lord
    return "Revati", 4, NAKSHATRA_LORDS["Revati"]


def get_nakshatra_from_deg_27(deg: float) -> str:
    nakshatras = [
        "Ashwini",
        "Bharani",
        "Krittika",
        "Rohini",
        "Mrigashira",
        "Ardra",
        "Punarvasu",
        "Pushya",
        "Ashlesha",
        "Magha",
        "Purva Phalguni",
        "Uttara Phalguni",
        "Hasta",
        "Chitra",
        "Swati",
        "Vishakha",
        "Anuradha",
        "Jyeshtha",
        "Mula",
        "Purva Ashadha",
        "Uttara Ashadha",
        "Shravana",
        "Dhanishta",
        "Shatabhisha",
        "Purva Bhadrapada",
        "Uttara Bhadrapada",
        "Revati",
    ]
    return nakshatras[int((deg % 360) // (360 / 27))]


def get_navamsa_sign_table(sign_num: int, deg_in_sign: float) -> tuple[str, int]:
    pada = int(deg_in_sign // (10 / 3))
    pada = min(pada, 8)
    d9_sign_num = D9_NAVAMSA_TABLE[pada][sign_num - 1]
    return SIGN_NAMES[d9_sign_num - 1], d9_sign_num


def _sign_type(sign_num: int) -> str:
    if sign_num in [1, 4, 7, 10]:
        return "Movable"
    if sign_num in [2, 5, 8, 11]:
        return "Fixed"
    return "Dual"


def _dms_to_pada_for_vargottama(dms_str: str) -> int:
    deg = _dms_to_deg(dms_str)
    return int(deg // (30 / 9)) + 1


def _is_pushkara_navamsa(row: pd.Series) -> str:
    sign = row["Sign"]
    deg = _dms_to_deg(row["Degree"])
    d9_sign = row["D9 Sign Name"]

    for start, end, target_d9 in PUSHKARA_NAVAMSA_MAP.get(sign, []):
        start_deg = start[0] + start[1] / 60
        end_deg = end[0] + end[1] / 60
        if start_deg <= deg < end_deg and d9_sign == target_d9:
            return "Yes"
    return "No"


class KpMappingService:
    def __init__(self, kp_mapping_path: str, ephe_path: str):
        self.kp_mapping_path = kp_mapping_path
        self.ephe_path = ephe_path

        swe.set_ephe_path(self.ephe_path)
        self.kp_df, self.kp_cols = self._load_kp_mapping(self.kp_mapping_path)

    @staticmethod
    def _load_kp_mapping(path: str) -> tuple[pd.DataFrame, dict[str, str]]:
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"KP mapping file not found: {path}. Place kp_mapping_all.xlsx in the project root "
                "or set KP_MAPPING_FILE env var."
            )

        df = pd.read_excel(path)
        df.columns = [str(col).strip() for col in df.columns]

        def pick_col(predicate: Any, label: str) -> str:
            for col in df.columns:
                if predicate(col.lower()):
                    return col
            raise ValueError(f"Unable to detect '{label}' column in KP mapping file")

        sign_col = "Sign" if "Sign" in df.columns else pick_col(lambda c: "sign" in c and "lord" not in c, "Sign")
        from_col = pick_col(lambda c: "from" in c, "From")
        to_col = pick_col(lambda c: "to" in c, "To")
        sub_lord_col = pick_col(lambda c: "sub lord" in c and "sub sub lord" not in c, "Sub Lord")
        sub_sub_lord_col = pick_col(lambda c: "sub sub lord" in c, "Sub Sub Lord")
        sign_lord_col = pick_col(lambda c: "sign" in c and "lord" in c, "Sign Lord")

        df["_sign"] = df[sign_col].astype(str).str.strip().str.lower()
        df["_from_sec"] = df[from_col].apply(_dms_to_seconds)
        df["_to_sec"] = df[to_col].apply(_dms_to_seconds)

        cols = {
            "sign_lord": sign_lord_col,
            "sub_lord": sub_lord_col,
            "sub_sub_lord": sub_sub_lord_col,
        }
        return df, cols

    def _lookup_kp(self, sign_name: str, sec: int) -> pd.Series | None:
        kp_sub = self.kp_df[self.kp_df["_sign"] == sign_name.lower()]
        if kp_sub.empty:
            return None

        row = kp_sub[(kp_sub["_from_sec"] <= sec) & (sec < kp_sub["_to_sec"])]
        if row.empty:
            return kp_sub.iloc[-1]
        return row.iloc[0]

    @staticmethod
    def _compute_planet_metrics(name: str, jd: float, asc_deg: float) -> dict[str, Any] | None:
        sid_flag = swe.FLG_SIDEREAL | swe.FLG_SWIEPH

        if name == "Asc":
            deg = asc_deg
            speed_deg = speed_arcmin = dist = decl = 0.0
            lat_val = 0.0
            position = "D"
        else:
            if name == "Ketu":
                rahu_sid = swe.calc_ut(jd, swe.TRUE_NODE, sid_flag)[0][0]
                deg = (rahu_sid + 180) % 360
            elif name == "Rahu":
                deg = swe.calc_ut(jd, swe.TRUE_NODE, sid_flag)[0][0] % 360
            else:
                deg = swe.calc_ut(jd, PLANET_IDS[name], sid_flag)[0][0] % 360

            if name == "Ketu":
                calc = swe.calc_ut(jd, swe.TRUE_NODE)[0]
                speed_deg = -calc[3]
                speed_arcmin = speed_deg * 60
                dist = calc[2]
                decl = -swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)[0][1]
            elif name == "Rahu":
                calc = swe.calc_ut(jd, swe.TRUE_NODE)[0]
                speed_deg = calc[3]
                speed_arcmin = speed_deg * 60
                dist = calc[2]
                decl = swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)[0][1]
            else:
                calc = swe.calc_ut(jd, PLANET_IDS[name])[0]
                speed_deg = calc[3]
                speed_arcmin = speed_deg * 60
                dist = calc[2]
                decl = swe.calc_ut(jd, PLANET_IDS[name], swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)[0][1]

            lat_val = 0.0 if name in ["Rahu", "Ketu"] else swe.calc_ut(jd, PLANET_IDS[name], sid_flag)[0][1]

            if name in ["Rahu", "Ketu"]:
                position = "R" if speed_deg < 0 else "D"
            else:
                is_retro = speed_deg < 0
                planet_trop = swe.calc_ut(jd, PLANET_IDS[name])[0][0] % 360
                sun_trop = swe.calc_ut(jd, swe.SUN)[0][0] % 360
                sep = abs((planet_trop - sun_trop) % 360)
                if sep > 180:
                    sep = 360 - sep
                is_combust = name in COMBUSTION_ORB and sep <= COMBUSTION_ORB[name]
                if is_retro and is_combust:
                    position = "RC"
                elif is_retro:
                    position = "R"
                elif is_combust:
                    position = "C"
                else:
                    position = "D"

        return {
            "deg": deg % 360,
            "speed_deg": speed_deg,
            "speed_arcmin": speed_arcmin,
            "distance": dist,
            "declination": decl,
            "latitude": lat_val,
            "position": position,
        }

    def generate(
        self,
        *,
        local_date: date,
        local_time: time,
        latitude: float,
        longitude: float,
        timezone_offset: float,
        ayanamsa: str,
        planets: list[str],
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        sid_map = {
            "Lahiri": swe.SIDM_LAHIRI,
            "Krishnamurti": swe.SIDM_KRISHNAMURTI,
            "Raman": swe.SIDM_RAMAN,
        }
        if ayanamsa not in sid_map:
            raise ValueError(f"Unsupported ayanamsa: {ayanamsa}")

        swe.set_ephe_path(self.ephe_path)
        swe.set_sid_mode(sid_map[ayanamsa])

        local_dt = datetime.combine(local_date, local_time)
        local_hours = local_dt.hour + local_dt.minute / 60 + local_dt.second / 3600
        jd = swe.julday(local_dt.year, local_dt.month, local_dt.day, local_hours) - timezone_offset / 24.0

        _, ascmc = swe.houses_ex(jd, latitude, longitude, b"A", swe.FLG_SIDEREAL)
        asc_deg = ascmc[0] % 360

        rows: list[dict[str, Any]] = []
        planet_set = set(planets)

        for name in PLANET_ORDER:
            if name not in planet_set:
                continue

            metrics = self._compute_planet_metrics(name, jd, asc_deg)
            if metrics is None:
                continue

            deg = metrics["deg"]
            sign_num = int(deg // 30) + 1
            sign_name = SIGN_NAMES[sign_num - 1]
            deg_in_sign = deg % 30
            dms = _deg_to_dms_str(deg_in_sign)
            sec = _dms_to_seconds(dms)

            kp_row = self._lookup_kp(sign_name, sec)
            sign_lord = kp_row[self.kp_cols["sign_lord"]] if kp_row is not None else None
            sub_lord = kp_row[self.kp_cols["sub_lord"]] if kp_row is not None else None
            sub_sub_lord = kp_row[self.kp_cols["sub_sub_lord"]] if kp_row is not None else None

            nakshatra, pada, nak_lord = get_nakshatra_fixed(deg)

            d9_sign_name, d9_sign_num = get_navamsa_sign_table(sign_num, deg_in_sign)
            navamsa_size = 30 / 9
            deg_in_d9 = (deg_in_sign % navamsa_size) * 9
            d9_long_deg = (d9_sign_num - 1) * 30 + deg_in_d9
            d9_nakshatra, d9_pada, d9_nak_lord = d9_nak_pada_from_abs_long(d9_long_deg)

            rows.append(
                {
                    "Planet": name,
                    "Sign": sign_name,
                    "Degree": dms,
                    "Sign Lord": sign_lord,
                    "Nakshatra": nakshatra,
                    "D9 Nakshatra": d9_nakshatra,
                    "Pada": int(pada),
                    "D9 Pada": int(d9_pada),
                    "NakshLord": nak_lord,
                    "D9 Naksh Lord": d9_nak_lord,
                    "Sublord": sub_lord,
                    "SubSubLord": sub_sub_lord,
                    "Position": metrics["position"],
                    "Sign Num": sign_num,
                    "D9 Sign Num": d9_sign_num,
                    "D9 Sign Name": d9_sign_name,
                    "D1 Longitudinal Degree": deg,
                    "D9 Longitudinal Degree": d9_long_deg,
                    "Speed (deg/day)": metrics["speed_deg"],
                    "Speed (arcmin/day)": metrics["speed_arcmin"],
                    "Distance": metrics["distance"],
                    "Declination": metrics["declination"],
                    "Latitude": _lat_to_dms(metrics["latitude"]),
                }
            )

        df = pd.DataFrame(rows)
        if df.empty:
            meta = {
                "date": local_date.isoformat(),
                "time": local_time.isoformat(),
                "latitude": latitude,
                "longitude": longitude,
                "timezone_offset": timezone_offset,
                "ayanamsa": ayanamsa,
                "rows": 0,
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            }
            return meta, []

        def is_vargottama(row: pd.Series) -> str:
            if int(row["Sign Num"]) != int(row["D9 Sign Num"]):
                return "No"
            sign_type = _sign_type(int(row["Sign Num"]))
            pada_num = _dms_to_pada_for_vargottama(row["Degree"])
            if sign_type == "Movable" and pada_num == 1:
                return "Yes"
            if sign_type == "Fixed" and pada_num == 5:
                return "Yes"
            if sign_type == "Dual" and pada_num == 9:
                return "Yes"
            return "No"

        df["Vargottama"] = df.apply(is_vargottama, axis=1)
        df["Nadi (D1)"] = df["Nakshatra"].map(NADI_MAP)
        df["D9 Nakshatra"] = df["D9 Longitudinal Degree"].apply(get_nakshatra_from_deg_27)
        df["Nadi (D9)"] = df["D9 Nakshatra"].map(NADI_MAP)
        df["Pushkara Navamsha"] = df.apply(_is_pushkara_navamsa, axis=1)

        float_cols = [
            "D1 Longitudinal Degree",
            "D9 Longitudinal Degree",
            "Speed (deg/day)",
            "Speed (arcmin/day)",
            "Distance",
            "Declination",
        ]
        for col in float_cols:
            if col in df.columns:
                df[col] = df[col].astype(float).round(6)

        column_order = [
            "Planet",
            "Sign",
            "Degree",
            "Sign Lord",
            "Nakshatra",
            "D9 Nakshatra",
            "Pada",
            "D9 Pada",
            "NakshLord",
            "D9 Naksh Lord",
            "Sublord",
            "SubSubLord",
            "Position",
            "Sign Num",
            "D9 Sign Num",
            "D9 Sign Name",
            "Vargottama",
            "Nadi (D1)",
            "Nadi (D9)",
            "Pushkara Navamsha",
            "D1 Longitudinal Degree",
            "D9 Longitudinal Degree",
            "Speed (deg/day)",
            "Speed (arcmin/day)",
            "Distance",
            "Declination",
            "Latitude",
        ]
        df = df[[c for c in column_order if c in df.columns]]

        records = df.where(pd.notna(df), None).to_dict(orient="records")

        meta = {
            "date": local_date.isoformat(),
            "time": local_time.isoformat(),
            "latitude": latitude,
            "longitude": longitude,
            "timezone_offset": timezone_offset,
            "ayanamsa": ayanamsa,
            "rows": len(records),
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        return meta, records

