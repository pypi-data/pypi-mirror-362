from typing import Dict, Tuple, Optional, List, Union, Sequence

import pandas as pd

from gxkit_datalab.exception import DetectError
from gxkit_datalab.utils.convert import convert_columns
from gxkit_datalab.utils.normalize import norm_rule
from gxkit_datalab.encode.bitmask import encode_bitmask


def rule_det(df: pd.DataFrame, columns: Optional[Union[str, Sequence[str], pd.Index]], rule: str,
             bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
             merge: bool = True, col_mask: str = "rule", bm_prefix: str = "bm") -> pd.DataFrame:
    """pandas规则检测: 输入类query规则进行检测"""
    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)
    flags = {}
    rule_expr, _ = norm_rule(rule, bm_columns)
    try:
        mask = df.eval(rule_expr, engine="python")
        mask = mask.fillna(False).astype(bool)
        for col in columns:
            flags[col] = mask
    except Exception as e:
        raise DetectError("datalab.detect.rule_det", f"Invalid rule: {rule_expr} | {e}") from e
    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def rules_det(df: pd.DataFrame, rules: Dict[str, Tuple[Union[str, Sequence[str], pd.Index], str]],
              bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
              merge: bool = True, col_mask: str = "rule", bm_prefix: str = "bm") -> pd.DataFrame:
    """pandas规则检测: 输入多个规则进行检测"""
    bm_columns = convert_columns(df, bm_columns)
    bitmask_df_list: List[pd.DataFrame] = []
    for rule_name, rule in rules.items():
        flags = {}
        rule_cols, rule_str = rule
        rule_cols = convert_columns(df, rule_cols)
        rule_expr, _ = norm_rule(rule_str, bm_columns)
        try:
            mask = df.eval(rule_expr, engine="python")
            mask = mask.fillna(False).astype(bool)
            for col in rule_cols:
                flags[col] = mask
        except Exception as e:
            raise DetectError("datalab.detect.rule_det", f"Invalid rule: {rule_expr} | {e}") from e
        bm_df = encode_bitmask(flags, columns=bm_columns,
                               col_mask=f"{col_mask}_{rule_name}", prefix=bm_prefix)
        bitmask_df_list.append(bm_df)

    if len(bitmask_df_list) == 0:
        raise DetectError("datalab.detect.rule_det", "rules cannot be empty")

    bitmask_df = pd.concat(bitmask_df_list, axis=1)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def threshold_det(df: pd.DataFrame, limits: Dict[str, Tuple[float, float]],
                  bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
                  merge: bool = True, col_mask: str = "threshold", bm_prefix: str = "bm") -> pd.DataFrame:
    """阈值检测函数: 根据上下限对 df 的多个列进行异常检测"""
    bm_columns = convert_columns(df, bm_columns)

    # 初始化 bool 掩码
    flags = {}
    for col, bounds in limits.items():
        low, high = bounds
        flags[col] = (df[col] < low) | (df[col] > high)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def flatline_det(df: pd.DataFrame, columns: Optional[Union[str, Sequence[str], pd.Index]] = None, window: int = 4,
                 bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None, drop_special: bool = True,
                 merge: bool = True, col_mask: str = "flatline", bm_prefix: str = "bm") -> pd.DataFrame:
    """平稳波动检测: 连续window个值完全相同即视为异常"""
    if window <= 1:
        raise ValueError("window must be greater than 1")

    columns = convert_columns(df, columns)
    bm_columns = convert_columns(df, bm_columns)

    flags = {}
    for col in columns:
        series = df[col]
        group = series.ne(series.shift()).cumsum()
        size = group.groupby(group).transform("size")
        first_val = series.groupby(group).transform("first")
        mask = size >= window
        if drop_special:
            mask &= ~(first_val.isna() | (first_val == 0))
        flags[col] = mask.fillna(False)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df


def jump_det(df: pd.DataFrame, columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
             factor: float = 5.0, bm_columns: Optional[Union[str, Sequence[str], pd.Index]] = None,
             merge: bool = True, col_mask: str = "jump", bm_prefix: str = "bm") -> pd.DataFrame:
    """跳变检测: 当差分超过多倍标准差时判定为异常"""
    columns = convert_columns(df, columns) 
    bm_columns = convert_columns(df, bm_columns)

    flags = {}
    for col in columns:
        series = df[col]
        diff = series.diff().abs()
        threshold = diff.std(skipna=True) * factor
        mask = diff > threshold
        flags[col] = mask.fillna(False)

    bitmask_df = encode_bitmask(flags, columns=bm_columns, col_mask=col_mask, prefix=bm_prefix)
    return pd.concat([df, bitmask_df], axis=1) if merge else bitmask_df
