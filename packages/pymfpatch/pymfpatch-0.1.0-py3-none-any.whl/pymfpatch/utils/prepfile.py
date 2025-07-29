import pandas as pd
import numpy as np
from ..io.parser_utils import parse_epw_with_nans

def prepare_epw_df(df, df_ref):
    """
    Resample `df` to hourly frequency between the min/max datetimes
    found in `df_ref` (based on Year/Month/Day/Hour/Minute),
    taking the first record in each hour and re-populating the
    original time columns.
    """
    df = df.copy()
    df_ref = df_ref.copy()
    
    # 1) Build true datetime for df_ref and get its span
    df_ref['Hour'] -= 1
    ref_dt = pd.to_datetime(df_ref[['Year','Month','Day','Hour','Minute']])
    min_dt = ref_dt.min().floor('h')
    max_dt = ref_dt.max().ceil ('h')
    
    # 2) Build datetime index on df
    df['Hour'] -= 1
    df['datetime'] = pd.to_datetime(df[['Year','Month','Day','Hour','Minute']])
    df = df.set_index('datetime')
    
    # 3) Resample hourly, taking first observation in each bucket
    df_hourly = df.resample('h').first()
    
    # 4) Reindex to force every hour between min_dt and max_dt
    full_range = pd.date_range(start=min_dt, end=max_dt, freq='h')
    df_hourly = df_hourly.reindex(full_range)
    
    # 5) Re-populate Y/M/D/H/M columns from that new index
    df_hourly['Year']   = df_hourly.index.year
    df_hourly['Month']  = df_hourly.index.month
    df_hourly['Day']    = df_hourly.index.day
    # add back the +1 to match your EPW hour convention
    df_hourly['Hour']   = df_hourly.index.hour + 1
    df_hourly['Minute'] = df_hourly.index.minute
    
    df_hourly['HoY'] = (
        (df_hourly.index.dayofyear - 1) * 24 + df_hourly.index.hour
    )
    
    # 6) Drop the datetime index (optional)
    return df_hourly.reset_index(drop=True)

class DataLoaderEPW:
    """
    Load and align EPW weather files.
    """
    def __init__(self, ref_path: str, stn_path: str):
        self.reference, self.header_reference = parse_epw_with_nans(ref_path)
        self.station, self.header_station = parse_epw_with_nans(stn_path)
        self.station = prepare_epw_df(self.station, self.reference)

    def drop_all_nan_cols(self):
        nan_cols = [c for c in self.station.columns if self.station[c].isna().all()]
        shared = [c for c in nan_cols if c in self.reference.columns]
        self.station.loc[:, shared] = self.reference[shared]

    def clean_frame(self, drop_cols: list) -> pd.DataFrame:
        return self.station.drop(columns=drop_cols).copy()

class TimeFeatures:
    """
    Add cyclical time-based features.
    """
    @staticmethod
    def apply(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        ts = pd.to_datetime({
            'year': df['Year'], 'month': df['Month'], 'day': df['Day'],
            'hour': df['Hour'] - 1
        })
        doy = ts.dt.dayofyear
        hod = ts.dt.hour
        season = ((ts.dt.month % 12) // 3).astype(int)
        df['season'], df['doy'], df['hod'] = season, doy, hod
        df['season_sin'], df['season_cos'] = np.sin(2*np.pi*season/4), np.cos(2*np.pi*season/4)
        df['doy_sin'], df['doy_cos'] = np.sin(2*np.pi*doy/365.25), np.cos(2*np.pi*doy/365.25)
        df['hod_sin'], df['hod_cos'] = np.sin(2*np.pi*hod/24), np.cos(2*np.pi*hod/24)
        return df

class WindTransformer:
    """
    Encode/decode wind direction and u/v components.
    """
    @staticmethod
    def encode_direction(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        rad = np.deg2rad(df['Wind Direction'])
        df['wind_dir_sin'], df['wind_dir_cos'] = np.sin(rad), np.cos(rad)
        df.drop(columns=['Wind Direction'], inplace=True)
        return df

    @staticmethod
    def decode_direction(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        rad = np.arctan2(df['wind_dir_sin'], df['wind_dir_cos'])
        deg = (np.rad2deg(rad) + 360) % 360
        df['Wind Direction'] = deg.round().astype('int64')
        return df.drop(columns=['wind_dir_sin','wind_dir_cos'])

    @staticmethod
    def encode_uv(df: pd.DataFrame, speed='Wind Speed', direction='Wind Direction', drop=True) -> pd.DataFrame:
        df = df.copy()
        theta = np.deg2rad(df[direction].astype(float))
        spd = df[speed].astype(float)
        df['u_wind'], df['v_wind'] = -spd*np.sin(theta), -spd*np.cos(theta)
        if drop: df.drop(columns=[speed,direction], inplace=True)
        return df

    @staticmethod
    def decode_uv(df: pd.DataFrame, u_col='u_wind', v_col='v_wind', drop=True) -> pd.DataFrame:
        df = df.copy()
        u, v = df[u_col].astype(float), df[v_col].astype(float)
        df['Wind Speed'] = np.hypot(u,v)
        deg = (np.rad2deg(np.arctan2(-u,-v)) + 360) % 360
        df['Wind Direction'] = deg.round().astype('int64')
        if drop: df.drop(columns=[u_col,v_col], inplace=True)
        return df

class SignedDerivatives:
    """
    Add signed left/right derivative features.
    """
    @staticmethod
    def add(df: pd.DataFrame, cols: list) -> pd.DataFrame:
        df = df.copy(); df.sort_index(inplace=True)
        for c in cols:
            if c in df.columns:
                left = df[c] - df[c].shift(1)
                right = df[c].shift(-1) - df[c]
                df[f'{c}_ld'] = np.sign(left).fillna(0).astype(np.int8)
                df[f'{c}_rd'] = np.sign(right).fillna(0).astype(np.int8)
        return df