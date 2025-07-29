import numpy as np
import pandas as pd
from typing import Callable, Optional
from dataclasses import dataclass, field
from sklearn.base import BaseEstimator, TransformerMixin


def _log1p_safe(x: pd.Series | np.ndarray) -> pd.Series:
    """float-safe log1p."""
    return np.log1p(x.astype(float))


def _expm1_safe(x: pd.Series | np.ndarray) -> pd.Series:
    """float-safe expm1 (обратная log1p)."""
    return np.expm1(x.astype(float))


@dataclass
class RobustLogScaler(BaseEstimator, TransformerMixin):
    """
    Робастная медианная стандартизация на растущем окне:

      z_i = 0.6745 · (f(x_i) − median_{≤i}) / MAD_{≤i}

    Parameters
    ----------
    feature_col: str, default="tte"
        Имя столбца для нормализации.
    out_col: str | None, default = None
        Имя столбца для сохранения результата.
    transform_func: Callable[[pd.Series], pd.Series],
                    default = _log1p_safe
        Функция
    keep_params: bool = True
        Флаг сохранения значений `med` и `MAD`.

    Notes
    -----
    MAD (Median Absolute Deviation) медиана от вектора
    значений абсолютных отклонений медианы предыдущих значений f(x_i).

    Examples
    --------
    >>> df = pd.DataFrame({"tte": [1, 2, 4]})
    >>> scaler = RobustLogScaler(
    ...    feature_col="tte", out_col="tte_z", keep_params=False)
    >>> df_z = scaler.fit_transform(df)
    >>> print(df_z.to_string(index=False))
     tte    tte_z
       1 -0.67450
       2  0.00000
       4  0.84977
    >>> scaler.inverse_transform(df_z["tte_z"])
    array([1., 2., 4.])
    """

    feature_col: str = "target"
    out_col: Optional[str] = None

    transform_func: Callable[[pd.Series | np.ndarray], pd.Series] = _log1p_safe
    inverse_func: Callable[[pd.Series | np.ndarray], pd.Series] = _expm1_safe

    eps: Optional[float] = None
    strategy_if_const: str = "eps"  # {"eps", "nan"}

    lookback: Optional[int] = None  # None -> expanding от начала

    keep_params: bool = True
    const_flag_col: Optional[str] = None

    _median_series_: Optional[np.ndarray] = field(
        init=False, repr=False, default=None)
    _mad_series_: Optional[np.ndarray] = field(
        init=False, repr=False, default=None)

    def _compute_eps(self, med: pd.Series | np.ndarray | float):
        """eps = max(0.05 |median|, 1e-6) или заданный self.eps."""
        if self.eps is not None:
            return self.eps

        if isinstance(med, pd.Series):
            eps = med.abs() * 0.05
            eps.replace(0, 1e-6, inplace=True)
            return eps

        med_arr = np.asarray(med, dtype=float)
        eps_val = 0.05 * np.abs(med_arr)
        eps_val = np.where(eps_val == 0, 1e-6, eps_val)
        return eps_val if isinstance(med, np.ndarray) else float(eps_val)

    def fit(self, X: pd.DataFrame, y=None):
        if self.feature_col not in X.columns:
            raise ValueError(
                f"RobustLogScaler: нет колонки '{self.feature_col}'")
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if self.feature_col not in X.columns:
            raise ValueError(
                f"RobustLogScaler: '{self.feature_col}' отсутствует")
        if self.strategy_if_const not in {"eps", "nan"}:
            raise ValueError("strategy_if_const ∈ {'eps','nan'}")

        df = X.copy()
        x_t = self.transform_func(df[self.feature_col])

        if self.lookback:
            med = x_t.rolling(self.lookback, min_periods=1).median()
            mad = (x_t - med).abs().rolling(self.lookback, min_periods=1) \
                .median()
        else:
            med = x_t.expanding(min_periods=1).median()
            mad = (x_t - med).abs().expanding(min_periods=1).median()

        # MAD == 0
        eps_val = self._compute_eps(med)
        mad_adj = mad.where(mad != 0, eps_val)
        if self.strategy_if_const == "nan":
            mad_adj = mad_adj.where(mad != 0, np.nan)

        with np.errstate(divide="ignore", invalid="ignore"):
            z = 0.6745 * (x_t - med) / mad_adj

        dst = self.out_col or self.feature_col
        df[dst] = z

        if self.keep_params:
            df[f"{dst}_median"] = med
            df[f"{dst}_mad"] = mad
        if self.const_flag_col:
            df[self.const_flag_col] = mad.eq(0)

        # сохраняем для inverse
        self._median_series_ = med.values
        self._mad_series_ = mad.values
        return df

    def inverse_transform(self, z: np.ndarray | pd.Series) -> np.ndarray:
        if self._median_series_ is None or self._mad_series_ is None:
            raise RuntimeError(
                "inverse_transform: сначала вызовите transform()")

        z_arr = np.asarray(z, dtype=float)
        if z_arr.shape[0] != len(self._median_series_):
            raise ValueError(
                "inverse_transform: длина z не совпадает со статистиками")

        med = self._median_series_
        mad = np.where(self._mad_series_ == 0,
                       self._compute_eps(med),
                       self._mad_series_)

        raw = z_arr * mad / 0.6745 + med
        return self.inverse_func(raw)
