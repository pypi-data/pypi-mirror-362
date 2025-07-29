import pandas as pd
import numpy as np


def parse_epw(filepath):
    """
    Reads an EPW file by automatically detecting where the data starts.
    It looks for the first line where the first four comma-separated fields
    can be converted to integers (year, month, day, hour). Everything before
    that is treated as "header metadata" (not column names) and returned as
    one multi-line string.

    Returns:
        df (pd.DataFrame): the numeric data block (no header row interpreted)
        header (str or None): all lines before data-start joined by '\n', 
                              or None if none exist
    """
    start_line = None
    header_lines = []

    # 1) Scan file until we find the first numeric data row.
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            parts = line.rstrip('\n').split(',')
            if len(parts) >= 4:
                try:
                    month = int(parts[1])
                    day = int(parts[2])
                    hour = int(parts[3])
                    if 1 <= month <= 12 and 1 <= day <= 31 and (0 <= hour <= 23 or 1 <= hour <= 24):
                        start_line = i
                        break
                except ValueError:
                    # Not a numeric data linetreat as header metadata
                    header_lines.append(line.rstrip('\n'))
                    continue
            else:
                # Fewer than 4 fields => definitely header metadata
                header_lines.append(line.rstrip('\n'))

    if start_line is None:
        raise ValueError("Could not determine where the data starts in the EPW file.")

    # 2) If there were any lines before the data block, join them into one string.
    if header_lines:
        header = "\n".join(header_lines)
    else:
        header = None

    # 3) Read the numeric data block into a DataFrame (header=None).
    #    skiprows=start_line ensures we start exactly at the first numeric line.
    df = pd.read_csv(filepath, skiprows=start_line, header=None)

    return df, header

# 2) the full list of EPW column names (35 total):
EPW_COLUMNS = [
    "Year","Month","Day","Hour","Minute","Data Source and Uncertainty Flags",
    "Dry Bulb Temperature","Dew Point Temperature","Relative Humidity",
    "Atmospheric Station Pressure","Extraterrestrial Horizontal Radiation",
    "Extraterrestrial Direct Normal Radiation",
    "Horizontal Infrared Radiation Intensity","Global Horizontal Radiation",
    "Direct Normal Radiation","Diffuse Horizontal Radiation",
    "Global Horizontal Illuminance","Direct Normal Illuminance",
    "Diffuse Horizontal Illuminance","Zenith Luminance",
    "Wind Direction","Wind Speed","Total Sky Cover","Opaque Sky Cover",
    "Visibility","Ceiling Height","Present Weather Observation",
    "Present Weather Codes","Precipitable Water","Aerosol Optical Depth",
    "Snow Depth","Days Since Last Snowfall","Albedo",
    "Liquid Precipitation Depth","Liquid Precipitation Quantity"
]

EPW_SPECS = {
    'Dry Bulb Temperature':             {'missing':   99.9,    'min':   -70,  'max':    70,  'precision': 1},  # (°C)
    'Dew Point Temperature':            {'missing':   99.9,    'min':   -70,  'max':    70,  'precision': 1},  # (°C)
    'Relative Humidity':                {'missing':  999.0,    'min':     0,  'max':   110,  'precision': 0},  # (%)
    'Atmospheric Station Pressure':     {'missing': 999999,    'min': 31000,  'max':120000,  'precision': 0},  # (Pa)
    'Extraterrestrial Horizontal Radiation':      {'missing':  9999,    'min':     0,  'precision': 0},  # (Wh/m²)
    'Extraterrestrial Direct Normal Radiation':   {'missing':  9999,    'min':     0,  'precision': 0},  # (Wh/m²)
    'Horizontal Infrared Radiation Intensity':    {'missing':  9999,    'min':     0,  'precision': 0},  # (Wh/m²)
    'Global Horizontal Radiation':                {'missing':  9999,    'min':     0,  'precision': 0},  # (Wh/m²)
    'Direct Normal Radiation':                    {'missing':  9999,    'min':     0,  'precision': 0},  # (Wh/m²)
    'Diffuse Horizontal Radiation':               {'missing':  9999,    'min':     0,  'precision': 0},  # (Wh/m²)
    'Global Horizontal Illuminance':              {'missing': 999999,    'min':     0,  'precision': 0},  # (lux)
    'Direct Normal Illuminance':                  {'missing': 999999,    'min':     0,  'precision': 0},  # (lux)
    'Diffuse Horizontal Illuminance':             {'missing': 999999,    'min':     0,  'precision': 0},  # (lux)
    'Zenith Luminance':                           {'missing':   9999,    'min':     0,  'precision': 0},  # (Cd/m²)
    'Wind Direction':                             {'missing':    999,    'min':     0,  'max':  360,  'precision': 0},  # (degrees)
    'Wind Speed':                                 {'missing':    999,    'min':     0,  'max':   40,  'precision': 1},  # (m/s)
    'Total Sky Cover':                            {'missing':     99,    'min':     0,  'max':   10,  'precision': 0},  # (oktas)
    'Opaque Sky Cover':                           {'missing':     99,    'min':     0,  'max':   10,  'precision': 0},  # (oktas)
    'Visibility':                                 {'missing':   9999,                           'precision': 0},  # (km)
    'Ceiling Height':                             {'missing':  99999,                           'precision': 0},  # (m)
    'Precipitable Water':                         {'missing':    999,                           'precision': 1},  # (mm)
    'Aerosol Optical Depth':                      {'missing':    0.999,                         'precision': 3},  # (unitless)
    'Snow Depth':                                 {'missing':    999,                           'precision': 1},  # (cm)
    'Days Since Last Snowfall':                   {'missing':     99,                           'precision': 0},  # (days)
    'Albedo':                                     {'missing':    999,                           'precision': 2},  # (unitless)
    'Liquid Precipitation Depth':                 {'missing':    999,                           'precision': 1},  # (mm)
    'Liquid Precipitation Quantity':              {'missing':     99,                           'precision': 0},  # (hours)
}

def parse_epw_with_nans(filepath):
    # read raw
    df, header = parse_epw(filepath)

    # assign the 35 EPW column names
    if len(df.columns) != len(EPW_COLUMNS):
        raise ValueError(
            f"Expected {len(EPW_COLUMNS)} columns in EPW data, "
            f"found {len(df.columns)}"
        )
    df.columns = EPW_COLUMNS

    # for each spec, coerce, mask, cast, and assign in one step
    for col, spec in EPW_SPECS.items():
        if col not in df.columns:
            continue

        missing_val = spec['missing']
        precision   = spec['precision']

        # 1) parse to numeric, coerce errors ? NaN
        series = pd.to_numeric(df[col], errors="coerce")

        # 2) mask the sentinel missing value ? pandas pd.NA
        series = series.mask(series == missing_val, pd.NA)

        # 3) cast to integer extension if precision==0, else leave as float
        if precision == 0:
            df[col] = series.astype("Int64")    # nullable integer dtype
        else:
            df[col] = series                    # float dtype with NaNs

    return df, header

def format_epw_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans a weather DataFrame according to EnergyPlus field specifications:
      - Replaces NaNs with the specified missing value codes.
      - Enforces minimum and maximum thresholds where defined.
      - Rounds each field to the configured precision.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the weather fields as columns (full descriptive names).
    
    Returns
    -------
    pd.DataFrame
        A cleaned, rounded copy of the original DataFrame.
    """
    
    df_clean = df.copy()

    for col, specs in EPW_SPECS.items():
        miss = specs['missing']
        # 1) Turn sentinel ? NaN so it wont get clipped
        series = df_clean[col].replace(miss, np.nan)
    
        # 2) Clip to [min, max] (only applies to non-NaN)
        if 'min' in specs:
            series = series.clip(lower=specs['min'])
        if 'max' in specs:
            series = series.clip(upper=specs['max'])
    
        # 3) Round & cast
        prec = specs['precision']
        series = series.round(prec)
        if prec == 0:
            # will upcast ints with NaN to float, so we cast back to Int64
            series = series.astype("Int64")
        else:
            series = series.astype('float64')
            pass
    
        # 4) Fill NaNs back to your missing-value sentinel
        df_clean.loc[:,col] = series.fillna(miss)
    
    return df_clean

def merge_header_on_ground_temperatures(header_station: str,
                              header_reference: str,
                              tolerance: float = 1.5) -> str:
    """
    In the 'GROUND TEMPERATURES' line of header_station, fill any
    blank/'nan' with the corresponding value from header_reference.
    If the absolute difference between station and reference exceeds
    `tolerance`, take the smaller of the two.
    Returns the modified header_station string.
    """
    # Split into lines
    station_lines = header_station.strip().splitlines()
    ref_lines     = header_reference.strip().splitlines()

    # Locate the GROUND TEMPERATURES line
    def find_gt_line(lines):
        for idx, line in enumerate(lines):
            if line.startswith("GROUND TEMPERATURES"):
                return idx, line
        raise ValueError("No GROUND TEMPERATURES line found.")

    s_idx, s_line = find_gt_line(station_lines)
    _,     r_line = find_gt_line(ref_lines)

    # Split CSV fields
    s_parts = s_line.split(",")
    r_parts = r_line.split(",")

    # First 5 columns stay the same; remaining are the 12 monthly temps
    prefix  = s_parts[:5]
    s_temps = s_parts[5:]
    r_temps = r_parts[5:]

    # Merge according to the rules
    merged = []
    for s, r in zip(s_temps, r_temps):
        s_str = s.strip().lower()
        # Rule 1: blank or 'nan' ? take reference
        if not s_str or s_str == "nan":
            merged.append(r)
            continue

        # Parse to floats
        s_val = float(s)
        r_val = float(r)

        # Rule 2: if difference > tolerance, take the smaller
        if abs(s_val - r_val) > tolerance:
            merged.append(str(min(s_val, r_val)))
        else:
            # Otherwise keep station
            merged.append(s)

    # Rebuild the GROUND TEMPERATURES line
    new_gt_line = ",".join(prefix + merged)
    station_lines[s_idx] = new_gt_line

    # Return the updated header as one string
    return "\n".join(station_lines)