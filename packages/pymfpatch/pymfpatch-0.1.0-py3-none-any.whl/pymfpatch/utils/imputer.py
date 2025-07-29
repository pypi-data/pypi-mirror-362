import torch
import numpy as np
import pandas as pd
from . import neuralnetwork as ntw
from torch import nn
from tqdm import tqdm
from pandas.api import types as pdt
from torch.utils.data import  DataLoader, Subset
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from .prepfile import DataLoaderEPW, TimeFeatures, WindTransformer, SignedDerivatives
from ..io.parser_utils import merge_header_on_ground_temperatures, format_epw_fields


GRU_VARS = [
    'Dry Bulb Temperature', 'Dew Point Temperature', 'Relative Humidity',
    'Horizontal Infrared Radiation Intensity', 'Atmospheric Station Pressure',
    'wind_dir_sin', 'wind_dir_cos', 'u_wind', 'v_wind', 'Wind Speed',
    'Total Sky Cover', 'Opaque Sky Cover', 'Precipitable Water',
    'Aerosol Optical Depth', 'Snow Depth', 'Global Horizontal Radiation',
]

XGB_VARS = [
    'Direct Normal Radiation',
    'Diffuse Horizontal Radiation', 'Zenith Luminance', 'Visibility',
    'Ceiling Height', 'Albedo', 'Liquid Precipitation Depth'
]

ORDERED_COLS = [
    'Year', 'Month', 'Day', 'Hour', 'Minute',
    'season', 'season_sin', 'season_cos',
    'doy', 'doy_sin', 'doy_cos',
    'hod', 'hod_sin', 'hod_cos',
    'Dry Bulb Temperature', 'Dew Point Temperature', 'Relative Humidity',
    'Atmospheric Station Pressure', 'Global Horizontal Radiation',
    'Wind Speed', 'u_wind', 'v_wind', 'Total Sky Cover', 'Opaque Sky Cover',
    'Ceiling Height', 'Snow Depth', 'Liquid Precipitation Depth',
    'wind_dir_sin', 'wind_dir_cos'
]

THRESHOLDS = {
    'Total Sky Cover': 0,
    'Opaque Sky Cover': 0,
    'Ceiling Height': 0,
    'Total Sky Cover': 0,
    'Opaque Sky Cover': 0,
    'Snow Depth': 0.1,
    'Relative Humidity': 0,
    'Global Horizontal Radiation': 0,
    'Liquid Precipitation Depth': 0.1,
}

class WeatherImputer:
    def __init__(
        self,
        epw_reference_path: str,
        epw_station_path: str,
        gru_vars: list = GRU_VARS,
        xgb_vars: list = XGB_VARS,
        gru_params: dict = ntw.GRU_PARAMS,
        xgb_params: dict = ntw.XGB_PARAMS,
        ground_temp_tol:float = 1.5
    ):
        self.ref_path = epw_reference_path
        self.stn_path = epw_station_path
        self.GRU_PARAMS = gru_params
        self.XGB_PARAMS = xgb_params
        self.GRU_VARS = gru_vars
        self.XGB_VARS = xgb_vars
        self.tolerance = ground_temp_tol
        
        self._load_data()
        self._prepare_features()
        
    def _load_data(self):
        self.loader = DataLoaderEPW(self.ref_path, self.stn_path)
        self.loader.drop_all_nan_cols()
        self.ref_df = self.loader.reference
        self.stn_df = self.loader.station
    
        drop_cols = [
            'Data Source and Uncertainty Flags','Global Horizontal Illuminance',
            'Present Weather Observation','Present Weather Codes',
            'Days Since Last Snowfall','Liquid Precipitation Quantity'
        ]
        self.ref_clean = self.ref_df.drop(columns=drop_cols)
        self.stn_clean = self.stn_df.drop(columns=drop_cols)
        
    def _prepare_features(self):
        self.ref_enc = WindTransformer.encode_uv(self.ref_clean)
        self.stn_enc = WindTransformer.encode_uv(self.stn_clean)
        
        
    def _gru_model(self):  
        X_full = TimeFeatures.apply(self.ref_enc)
        Y_full = TimeFeatures.apply(self.stn_enc)
    
        # Prepare for imputation
        X = X_full[[c for c in ORDERED_COLS if c in X_full]]
        nan_cols = Y_full.columns[Y_full.isna().any()]
        X = SignedDerivatives.add(X, list(nan_cols))
        Y_diff = (Y_full[nan_cols] - self.ref_enc[nan_cols]).astype(np.float64)
        
        # imputation
        gru_cols = [c for c in self.GRU_VARS if c in Y_diff]
        if not gru_cols:
            print("No GRU variables to impute, skipping GRU imputation.")
            imputed_gru = pd.DataFrame(index=self.ref_enc.index)
        else:
            SEQ_LEN = self.GRU_PARAMS['seq_len']
            BATCH_SIZE = self.GRU_PARAMS['batch_size']
            X_gru, Y_gru = X.copy(), Y_diff[gru_cols]
            x_s = StandardScaler().fit(X_gru); Xs = pd.DataFrame(x_s.transform(X_gru), index=X_gru.index, columns=X_gru.columns)
            y_s = StandardScaler().fit(Y_gru); Ys = pd.DataFrame(y_s.transform(Y_gru), index=Y_gru.index, columns=Y_gru.columns)
            ds = ntw.WeatherSequenceDataset(Xs, Ys, self.GRU_PARAMS['seq_len'])
        
            positions = list(range(len(ds)))
            train_pos, val_pos = train_test_split(
                positions, test_size=self.GRU_PARAMS['split_validation'], random_state=self.GRU_PARAMS['seed']
            )
            train_loader = DataLoader(Subset(ds, train_pos), batch_size=self.GRU_PARAMS['batch_size'], shuffle=True)
            val_loader   = DataLoader(Subset(ds, val_pos),   batch_size=self.GRU_PARAMS['batch_size'], shuffle=False)    
        
            gru_model = ntw.GRUImputer(
                in_dim=Xs.shape[1], out_dim=Ys.shape[1],
                hidden=self.GRU_PARAMS['hidden'], dropout=self.GRU_PARAMS['dropout']
            ).to(self.GRU_PARAMS['device'])
            
            optimizer = torch.optim.AdamW(gru_model.parameters(), lr=self.GRU_PARAMS['lr'], weight_decay=self.GRU_PARAMS['weight_decay'])
            loss_fn = nn.L1Loss()
            stopper = ntw.EarlyStopping(
                patience=self.GRU_PARAMS['early_stopping_patience'],
                delta=self.GRU_PARAMS['early_stopping_delta']
            )
    
            for epoch in range(1, self.GRU_PARAMS['epochs']+1):
                gru_model.train()
                train_losses = []
                for xb, yb in tqdm(train_loader, desc=f"Epoch {epoch} [train]"):
                    xb, yb = xb.to(self.GRU_PARAMS['device']), yb.to(self.GRU_PARAMS['device'])
                    optimizer.zero_grad()
                    pred = gru_model(xb)
                    loss = loss_fn(pred, yb)
                    loss.backward()
                    optimizer.step()
                    train_losses.append(loss.item())
                avg_train = np.mean(train_losses)
    
                gru_model.eval()
                val_losses = []
                with torch.no_grad():
                    for xb, yb in val_loader:
                        xb, yb = xb.to(self.GRU_PARAMS['device']), yb.to(self.GRU_PARAMS['device'])
                        val_losses.append(loss_fn(gru_model(xb), yb).item())
                avg_val = np.mean(val_losses)
                print(f"Epoch {epoch} - train MAE: {avg_train:.4f}, val MAE: {avg_val:.4f}")
    
                stopper(avg_val)
                if stopper.should_stop:
                    print(f"Early stopping at epoch {epoch}")
                    break
        
            # GRU Inference batch on GPU
            if self.GRU_PARAMS['device'] == 'cuda':
                torch.cuda.empty_cache()  # free whatever you can
                Xn = Xs.values.astype(np.float32)
                indices = np.arange(SEQ_LEN-1, len(Xn))
                batch_size_inf = BATCH_SIZE    # or whatever your GPU can handle
                preds = []
                with torch.no_grad():
                    for i in range(0, len(indices), batch_size_inf):
                        batch_idx = indices[i:i+batch_size_inf]
                        # build a small batch of shape (B, seq_len, features)
                        seqs = [Xn[j-SEQ_LEN+1:j+1] for j in batch_idx]
                        xb = torch.from_numpy(np.stack(seqs)).to(self.GRU_PARAMS['device'])   
                        out = gru_model(xb)                                
                        preds.append(out.cpu().numpy())                   
                    # concatenate all the little batches back into one array
                    pred_scaled = np.vstack(preds)
            else:
                # GRU Inference on CPU
                gru_model.eval()
                with torch.no_grad():
                    arr = []
                    Xn = Xs.values.astype(np.float32)
                    for i in range(SEQ_LEN-1,len(Xn)):
                        arr.append(Xn[i-SEQ_LEN+1:i+1])
                    stacked = torch.from_numpy(np.stack(arr)).to(self.GRU_PARAMS['device'])
                    pred_scaled = gru_model(stacked).cpu().numpy()
        
            diffs = pd.DataFrame(y_s.inverse_transform(pred_scaled), columns=Ys.columns, index=Xs.index[SEQ_LEN-1:])
            full_diff = pd.concat([pd.DataFrame(np.zeros((SEQ_LEN-1,len(Ys.columns))), columns=Ys.columns, index=Xs.index[:SEQ_LEN-1]), diffs])
            imputed_gru = self.ref_enc[gru_cols].add(full_diff.values, axis=0)
            for c in gru_cols:
                dt=self.stn_enc[c].dtype
                if pdt.is_integer_dtype(dt): imputed_gru[c]=imputed_gru[c].round().astype(dt)
                else: imputed_gru[c]=imputed_gru[c].astype(dt)
            imputed_gru = WindTransformer.decode_uv(imputed_gru)
    
        # Merge
        self.result = self.stn_df.copy()
        self.result.update(imputed_gru)
        
    def _xgb_model(self):
        # XGB Imputation
        aligned = self.stn_df.reindex(self.result.index).astype(self.result.dtypes.to_dict(), errors='ignore')
        self.result.update(aligned)
        X2 = TimeFeatures.apply(self.result)[[c for c in ORDERED_COLS if c in self.result]]
        nan2 = self.result[self.XGB_VARS].isna().any()
        X2 = (
            TimeFeatures
              .apply(self.result)[[c for c in ORDERED_COLS if c in self.result]]
              .dropna(axis=1, how='any')
        )
        diff2 = (
        self.result[nan2[nan2].index.tolist()]
          .subtract(self.ref_clean[nan2[nan2].index.tolist()])
          .astype(np.float64)
          .dropna(axis=1, how='all')
          )
        if diff2.columns.empty:
            print("No XGB variables to impute, skipping XGB imputation.")
        else: 
            for var in diff2.columns:
                y_var = diff2[var]
                X_comp = X2.loc[y_var.notna()]; Y_comp = y_var.dropna().to_frame()
                X_part = X2.loc[y_var.isna()]
                sc = StandardScaler().fit(X_comp)
                Xc_s = pd.DataFrame(sc.transform(X_comp), index=X_comp.index, columns=X_comp.columns)
                Xp_s = pd.DataFrame(sc.transform(X_part), index=X_part.index, columns=X_part.columns)
                imp = ntw.XGBImputer(self.XGB_PARAMS)
                imp.fit(Xc_s, Y_comp)
                p = imp.predict(Xp_s)
                if var in THRESHOLDS: p[var]=p[var].mask(p[var]<THRESHOLDS[var],0)
                dt=self.result[var].dtype
                if pdt.is_integer_dtype(dt): p[var]=p[var].round().astype(dt)
                self.result.loc[p.index,var]=p[var]
                
    def _post_process(self):
        # Final adjustments
        for c,t in THRESHOLDS.items(): self.result[c]=self.result[c].mask(self.result[c]<t,0)
        self.result['Data Source and Uncertainty Flags']='*?*?*?*?*?*?*?*?*?*?*?*?*'
        self.result['Global Horizontal Illuminance']=110*self.result['Global Horizontal Radiation']
        self.result['Direct Normal Illuminance']=105*self.result['Direct Normal Radiation']
        self.result['Diffuse Horizontal Illuminance']=119*self.result['Diffuse Horizontal Radiation']
        self.result['Present Weather Observation']=0
        self.result['Present Weather Codes']=999999999
        self.result['Liquid Precipitation Quantity']=1
        # Days since last snowfall
        dt = pd.to_datetime(
            self.result['Year'].astype(str).str.zfill(4)
            + self.result['Month'].astype(str).str.zfill(2)
            + self.result['Day'].astype(str).str.zfill(2)
            + (self.result['Hour']-1).astype(str).str.zfill(2)
            + self.result['Minute'].astype(str).str.zfill(2),
            format='%Y%m%d%H%M'
        )
        mask = self.result['Snow Depth']>0
        last = dt.where(mask).ffill().fillna(dt.iloc[0]-pd.Timedelta(days=1))
        self.result['Days Since Last Snowfall']=(dt-last).dt.days
        self.result.drop(columns=['HoY'], inplace=True)
    
        # Sort from past to present before writing
        self.result.sort_values(
            by=['Year','Month','Day','Hour','Minute'],
            inplace=True
        )
    
        # Merge with a 1.5°C tolerance
        self.new_header_station = merge_header_on_ground_temperatures(self.loader.header_station, self.loader.header_reference, tolerance = self.tolerance)
        self.result = format_epw_fields(self.result)
        
    def process(self):
        print("-------------- start --------------")
        print("... use GRU for temporal prediction")
        self._gru_model()
        print("... use XGB for regression")
        self._xgb_model()
        print("... post-processing")
        self._post_process()
        print("--------------- end ---------------")
        
    def write(self, opath:str = 'imputed_weather.epw'):
        with open(opath, 'w', encoding='utf-8', newline='') as f:
            # write header block as-is
            f.write(self.new_header_station)
            f.write('\n')
            # write data rows without pandas header, avoid extra blank lines
            self.result.to_csv(f, index=False, header=False)
    
        print(f'Imputed weather saved to {opath}')