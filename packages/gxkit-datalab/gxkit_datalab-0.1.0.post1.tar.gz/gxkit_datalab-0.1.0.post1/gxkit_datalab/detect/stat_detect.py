from typing import Optional, List, Union, Sequence

import numpy as np
import pandas as pd
from statistics import NormalDist

from gxkit_datalab.utils.convert import convert_columns
from gxkit_datalab.encode.bitmask import encode_bitmask


def zscore_det(df: pd.DataFrame, threshold: float = 3.0,
               columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
               bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
               merge: bool = True, col_mask: str = "zscore", bm_prefix: str = "bm") -> pd.DataFrame:
    """全局 Z-score 检测"""
    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)

    flags = {}
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce")
        mean = series.mean(skipna=True)
        std = series.std(skipna=True)
        if std == 0 or np.isnan(std):
            mask = pd.Series(False, index=df.index)
        else:
            mask = (series - mean).abs() > threshold * std
        flags[col] = mask.fillna(False)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def mad_det(df: pd.DataFrame, threshold: float = 3.5,
            columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
            bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
            merge: bool = True, col_mask: str = "mad", bm_prefix: str = "bm") -> pd.DataFrame:
    """MAD 检测"""
    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)

    flags = {}
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce")
        median = series.median(skipna=True)
        mad = (series - median).abs().median(skipna=True)
        if mad == 0 or np.isnan(mad):
            mask = pd.Series(False, index=df.index)
        else:
            mask = (series - median).abs() > threshold * mad * 1.4826
        flags[col] = mask.fillna(False)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def iqr_det(df: pd.DataFrame, factor: float = 1.5,
            columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
            bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
            merge: bool = True, col_mask: str = "iqr", bm_prefix: str = "bm") -> pd.DataFrame:
    """基于四分位的检测"""
    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)

    flags = {}
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce")
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0 or np.isnan(iqr):
            mask = pd.Series(False, index=df.index)
        else:
            lower = q1 - factor * iqr
            upper = q3 + factor * iqr
            mask = (series < lower) | (series > upper)
        flags[col] = mask.fillna(False)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def rolling_zscore_det(df: pd.DataFrame, window: int = 10, threshold: float = 3.0,
                       columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                       bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                       merge: bool = True, col_mask: str = "roll_zscore", bm_prefix: str = "bm") -> pd.DataFrame:
    """滑窗 Z-score 检测"""
    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)

    flags = {}
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce")
        rolling_mean = series.rolling(window, min_periods=1).mean()
        rolling_std = series.rolling(window, min_periods=1).std()
        mask = (series - rolling_mean).abs() > threshold * rolling_std
        flags[col] = mask.fillna(False)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def rolling_mad_det(df: pd.DataFrame, window: int = 10, threshold: float = 3.5,
                    columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                    bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                    merge: bool = True, col_mask: str = "roll_mad", bm_prefix: str = "bm") -> pd.DataFrame:
    """滑窗 MAD 检测"""
    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)

    flags = {}
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce")
        rolling_median = series.rolling(window, min_periods=1).median()
        mad = (series - rolling_median).abs().rolling(window, min_periods=1).median()
        mask = (series - rolling_median).abs() > threshold * mad * 1.4826
        flags[col] = mask.fillna(False)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def rolling_iqr_det(df: pd.DataFrame, window: int = 10, factor: float = 1.5,
                    columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                    bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                    merge: bool = True, col_mask: str = "roll_iqr", bm_prefix: str = "bm") -> pd.DataFrame:
    """滑窗四分位数检测"""
    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)

    flags = {}
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce")
        q1 = series.rolling(window, min_periods=1).quantile(0.25)
        q3 = series.rolling(window, min_periods=1).quantile(0.75)
        iqr = q3 - q1
        lower = q1 - factor * iqr
        upper = q3 + factor * iqr
        mask = (series < lower) | (series > upper)
        flags[col] = mask.fillna(False)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def trend_shift_det(df: pd.DataFrame, short_window: int = 5, long_window: int = 20, threshold: float = 2.0,
                    columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                    bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                    merge: bool = True, col_mask: str = "trend", bm_prefix: str = "bm") -> pd.DataFrame:
    """检测时间序列中局部均值漂移异常"""
    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)

    flags = {}
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce")
        short_mean = series.rolling(short_window, min_periods=1).mean()
        long_mean = series.rolling(long_window, min_periods=1).mean()
        std = series.std(skipna=True)
        if std == 0 or np.isnan(std):
            mask = pd.Series(False, index=df.index)
        else:
            mask = (short_mean - long_mean).abs() > threshold * std
        flags[col] = mask.fillna(False)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def hampel_filter_det(df: pd.DataFrame, window: int = 7, n_sigma: float = 3.0,
                      columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                      bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                      merge: bool = True, col_mask: str = "hampel", bm_prefix: str = "bm") -> pd.DataFrame:
    """滑窗中位数 ± n×MAD 检测"""
    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)

    flags = {}
    scale = 1.4826
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce")
        rolling_median = series.rolling(window, center=True, min_periods=1).median()
        mad = (series - rolling_median).abs().rolling(window, center=True, min_periods=1).median()
        threshold_val = n_sigma * scale * mad
        mask = (series - rolling_median).abs() > threshold_val
        flags[col] = mask.fillna(False)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def grubbs_det(df: pd.DataFrame, alpha: float = 0.05,
               columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
               bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
               merge: bool = True, col_mask: str = "grubbs", bm_prefix: str = "bm") -> pd.DataFrame:
    """格拉布斯检测"""
    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)

    flags = {}
    norm = NormalDist()
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce")
        valid = series.dropna()
        n = len(valid)
        if n < 3:
            flags[col] = pd.Series(False, index=df.index)
            continue
        mean = valid.mean()
        std = valid.std(ddof=1)
        if std == 0 or np.isnan(std):
            mask = pd.Series(False, index=df.index)
        else:
            t_val = norm.inv_cdf(1 - alpha / (2 * n))
            Gcrit = (n - 1) / np.sqrt(n) * np.sqrt(t_val ** 2 / (n - 2 + t_val ** 2))
            mask = ((series - mean).abs() / std) > Gcrit
        flags[col] = mask.fillna(False)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def esd_test_det(df: pd.DataFrame, max_outliers: int = 5, alpha: float = 0.05,
                 columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                 bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                 merge: bool = True, col_mask: str = "esd", bm_prefix: str = "bm") -> pd.DataFrame:
    """Generalized ESD Test - Grubbs 检验的推广版"""
    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)

    norm = NormalDist()
    flags = {}
    for col in columns:
        series = pd.to_numeric(df[col], errors="coerce")
        s = series.dropna()
        out_idx: List[int] = []
        for i in range(min(max_outliers, len(s))):
            n = len(s)
            if n < 3:
                break
            mean = s.mean()
            std = s.std(ddof=1)
            if std == 0 or np.isnan(std):
                break
            deviations = (s - mean).abs()
            idx = deviations.idxmax()
            Ri = deviations.loc[idx] / std
            t_val = norm.inv_cdf(1 - alpha / (2 * (n - i)))
            lam = (n - i - 1) / np.sqrt(n - i) * np.sqrt(t_val ** 2 / (n - i - 2 + t_val ** 2))
            if Ri > lam:
                out_idx.append(idx)
                s = s.drop(idx)
            else:
                break
        mask = pd.Series(False, index=df.index)
        mask.loc[out_idx] = True
        flags[col] = mask

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df
