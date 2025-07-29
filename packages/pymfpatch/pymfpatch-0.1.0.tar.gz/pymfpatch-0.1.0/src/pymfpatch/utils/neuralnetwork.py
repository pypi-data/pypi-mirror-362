import torch
import numpy as np
import pandas as pd
from torch import nn
from xgboost import XGBRegressor
from torch.utils.data import Dataset


XGB_PARAMS = {
    'n_estimators': 5000,
    'learning_rate': 0.3,
    'max_depth': 10,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'n_jobs': 8,
    'verbosity': 0,
    'early_stopping_rounds': 1,
    'lambda':1
}

GRU_PARAMS = {
    'seq_len': 24,
    'batch_size': 512,
    'epochs': 200,
    'hidden': 256,
    'dropout': 0.3,
    'lr': 2e-3,
    'weight_decay': 1e-3,
    'device': 'cuda' if torch.cuda.is_available() else 'cpu',
    'split_validation': 0.2,
    'seed': 42,
    'early_stopping_patience': 3,
    'early_stopping_delta': 1e-4,
}


class EarlyStopping:
    """Utility for early stopping based on validation loss."""
    def __init__(self, patience=GRU_PARAMS['early_stopping_patience'], delta=GRU_PARAMS['early_stopping_delta']):
        self.patience = patience
        self.delta = delta
        self.best_loss = np.inf
        self.counter = 0
        self.should_stop = False

    def __call__(self, val_loss):
        if val_loss + self.delta < self.best_loss:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
                

class WeatherSequenceDataset(Dataset):
    """PyTorch dataset for sequence data."""
    def __init__(self, X_df: pd.DataFrame, y_df: pd.DataFrame, seq_len: int):
        self.X = X_df.values.astype(np.float32)
        self.y = y_df.values.astype(np.float32)
        idx = np.where(~np.isnan(self.y).any(axis=1))[0]
        self.indices = idx[idx>=seq_len-1]
        self.seq_len = seq_len
    def __len__(self): return len(self.indices)
    def __getitem__(self, i):
        end = self.indices[i]
        seq = self.X[end-self.seq_len+1:end+1]
        return torch.from_numpy(seq), torch.from_numpy(self.y[end])
    
class GRUImputer(nn.Module):
    """GRU model for imputation."""
    def __init__(self, in_dim, out_dim, hidden=GRU_PARAMS['hidden'], dropout=GRU_PARAMS['dropout']):
        super().__init__()
        # layer 1
        self.gru1 = nn.GRU(
            input_size=in_dim,
            hidden_size=hidden,
            num_layers=1,
            batch_first=True
        )
        self.drop1 = nn.Dropout(dropout)

        # layer 2
        self.gru2 = nn.GRU(
            input_size=hidden,
            hidden_size=hidden,
            num_layers=1,
            batch_first=True,
            bidirectional=True
        )
        self.drop2 = nn.Dropout(dropout)

        # layer 3
        self.gru3 = nn.GRU(
            input_size=2*hidden,
            hidden_size=hidden,
            num_layers=1,
            batch_first=True
        )
        self.drop3 = nn.Dropout(dropout)

        # final regression head
        self.fc = nn.Linear(hidden, out_dim)

    def forward(self, x):
        """
        x: (batch, seq_len, in_dim)
        returns: (batch, out_dim)
        """
        # GRU 1
        out, _ = self.gru1(x)
        out = self.drop1(out)

        # GRU 2
        out, _ = self.gru2(out)
        out = self.drop2(out)

        # GRU 3 (no return_sequences ? well take last timestep)
        out, _ = self.gru3(out)
        out = self.drop3(out)

        # grab final timestep
        last = out[:, -1, :]               # shape (batch, 128)
        return self.fc(last)               # shape (batch, out_dim)

class XGBImputer:
    def __init__(self, params = XGB_PARAMS, seed=42):
        # params is expected to include 'verbosity' if you want it
        # force MAE logging
        params.update({'eval_metric': 'mae'})
        self.params = params
        self.seed = seed

    def fit(self, X, Y):
        self.models = {}
        for var in Y.columns:
            y = Y[var]
            mask = ~y.isna()
            X_tr, y_tr = X.loc[mask], y.loc[mask]
            eval_set = [(X_tr, y_tr)]

            # read verbosity from your params dict (default to 0)
            verbosity = self.params.get('verbosity', 0)

            # build the regressor, passing all params (including verbosity)
            model = XGBRegressor(
                objective='reg:squarederror',
                random_state=self.seed,
                **self.params
            )

            # fit with the same verbosity controlling per-iteration logs
            model.fit(
                X_tr, y_tr,
                eval_set=eval_set,
                verbose=verbosity
            )

            # summarize final MAE
            last_mae = model.evals_result()['validation_0']['mae'][-1]
            print(f"? {var} final train MAE = {last_mae:.4f}")

            self.models[var] = model
            
            
    def predict(self, X):
        out = {var: m.predict(X) for var, m in self.models.items()}
        return pd.DataFrame(out, index=X.index)