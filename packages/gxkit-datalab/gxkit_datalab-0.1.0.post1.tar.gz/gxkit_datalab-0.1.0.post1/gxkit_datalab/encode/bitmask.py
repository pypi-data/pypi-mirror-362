"""
datalab.encode.bitmask
 - encode_bitmask bitmask编码工具
 - decode_bitmask bitmask解码工具
Version 0.1.0
"""
import re
from typing import Dict, List, Optional, Union, Sequence, Any, Mapping, Literal
from collections import defaultdict

import numpy as np
import pandas as pd

from gxkit_datalab.utils.check import check_columns


def encode_bitmask(flags: Union[Dict[str, pd.Series], pd.DataFrame], columns: List[str],
                   col_mask: str = "bitmask", prefix: Optional[str] = "bm") -> pd.DataFrame:
    """bitmask 单规则编码器"""
    if columns is None:
        raise ValueError("columns cannot be None")

    if isinstance(flags, dict):
        if not flags:
            raise ValueError("flags cannot be empty")
        index = next(iter(flags.values())).index
        flags = pd.DataFrame(flags, index=index)
    elif isinstance(flags, pd.DataFrame):
        if flags.empty:
            raise ValueError("flags DataFrame cannot be empty")
    else:
        raise TypeError("flags must be a dict or DataFrame")
    check_columns(list(flags.columns), columns)

    index = flags.index
    n_groups = (len(columns) + 63) // 64
    single_group = n_groups == 1

    bool_df = pd.DataFrame({
        col: flags.get(col, pd.Series(False, index=index)) for col in columns}, index=index).astype(np.uint8)

    bitmask_col = f"{prefix}_{col_mask}" if prefix else col_mask
    masks = {}
    # 向量编码
    for g in range(n_groups):
        sub = bool_df.iloc[:, g * 64: (g + 1) * 64]
        if sub.empty:
            continue
        weights = (1 << np.arange(sub.shape[1], dtype=np.uint64))
        col_name = bitmask_col if single_group else f"{bitmask_col}_{g}"
        masks[col_name] = (sub.values.astype(np.uint64) * weights).sum(axis=1, dtype=np.uint64)

    df_bm = pd.DataFrame(masks, index=index)
    return df_bm


def decode_bitmask(bitmask_df: pd.DataFrame, columns: Optional[Sequence[str]],
                   col_mask: Optional[str] = None, prefix: Optional[str] = None,
                   as_flags: bool = False) -> Union[pd.DataFrame, Dict[str, pd.Series]]:
    """bitmask 单规则解码器"""
    groups: Dict[str, List[str]] = defaultdict(list)
    for col in bitmask_df.columns:
        base = re.sub(r"_(\d+)$", "", col)
        groups[base].append(col)

    if col_mask is None:
        if len(groups) != 1:
            raise ValueError("bitmask_df has multi mask, please use [decode_multi_bitmask].")
        _, mask_cols = next(iter(groups.items()))
    else:
        bitmask_col = f"{prefix}_{col_mask}" if prefix else col_mask
        if bitmask_col not in groups:
            raise ValueError(f"Can not match mask in '{bitmask_col}', fund : {list(groups.keys())}")
        mask_cols = groups[bitmask_col]
    mask_cols = sorted(
        mask_cols, key=lambda x: int(re.search(r"_(\d+)$", x).group(1)) if re.search(r"_(\d+)$", x) else 0)

    if columns is None:
        raise ValueError("columns cannot be None")

    columns = list(columns)
    n_groups = (len(columns) + 63) // 64
    if len(mask_cols) != n_groups:
        raise ValueError(f"Need {n_groups} group, fund : {len(mask_cols)}")

    decoded_frames = []
    for group, bm_col in enumerate(mask_cols):
        series = bitmask_df[bm_col].astype(np.uint64).to_numpy()
        sub_columns = columns[group * 64: (group + 1) * 64]
        width = len(sub_columns)
        if width == 0:
            continue
        bits = ((series[:, None] >> np.arange(width, dtype=np.uint64)) & 1).astype(bool)
        decoded_frames.append(pd.DataFrame(bits, columns=sub_columns, index=bitmask_df.index))

    df = pd.concat(decoded_frames, axis=1) if decoded_frames else pd.DataFrame(index=bitmask_df.index)
    if as_flags:
        return {col: df[col] for col in df.columns}
    return df


def mask_bitmask(df: pd.DataFrame, columns: Sequence[str],
                 flags: Optional[Union[Dict[str, pd.Series], pd.DataFrame]] = None,
                 bitmask_df: Optional[pd.DataFrame] = None,
                 col_mask: Optional[str] = None,
                 prefix: Optional[str] = "bm", value=np.nan) -> pd.DataFrame:
    """单规则 bitmask 掩码"""
    df = df.copy()

    # 已传入 flags
    if flags is not None:
        if isinstance(flags, dict):
            flags = pd.DataFrame(flags)
        for col in flags.columns:
            if col in df.columns:
                df.loc[flags[col], col] = value
        return df

    # 通过 bitmask_df 解码
    if bitmask_df is not None:
        flags = decode_bitmask(bitmask_df, columns=columns, col_mask=col_mask, prefix=prefix, as_flags=True)
        return mask_bitmask(df, columns=columns, flags=flags, value=value)

    raise ValueError("flags or (bitmask_df + columns) must be provided.")


def decode_multi_bitmask(multi_bitmask_df: pd.DataFrame, columns: Sequence[str],
                         col_masks: Optional[Sequence[str]] = None, prefix: Optional[str] = "bm",
                         as_flags: bool = False) -> Dict[str, Union[pd.DataFrame, Dict[str, pd.Series]]]:
    """bitmask 多规则解码器"""

    results = {}
    groups: Dict[str, List[str]] = defaultdict(list)

    for col in multi_bitmask_df.columns:
        base = re.sub(r"_(\d+)$", "", col)
        groups[base].append(col)

    colmask_to_base = {}
    for base in groups:
        if prefix and base.startswith(prefix + "_"):
            col_mask = base[len(prefix) + 1:]
        else:
            col_mask = base
        colmask_to_base[col_mask] = base

    selected_masks = col_masks or list(colmask_to_base.keys())

    for col_mask in selected_masks:
        if col_mask not in colmask_to_base:
            raise ValueError(f"col_mask '{col_mask}' not found in bitmask columns: {list(colmask_to_base.keys())}")
        results[col_mask] = decode_bitmask(bitmask_df=multi_bitmask_df, columns=columns,
                                           col_mask=col_mask, prefix=prefix, as_flags=as_flags)

    return results


def mask_multi_bitmask(df: pd.DataFrame,
                       columns: Optional[Sequence[str]] = None,
                       flags: Optional[Dict[str, Union[pd.Series, pd.DataFrame]]] = None,
                       bitmask_df: Optional[pd.DataFrame] = None,
                       col_masks: Optional[Sequence[str]] = None,
                       prefix: Optional[str] = "bm",
                       value=np.nan) -> pd.DataFrame:
    """多规则 bitmask 掩码"""
    df = df.copy()

    if flags is not None:
        if not isinstance(flags, dict):
            raise TypeError("flags must be a dict returned by decode_multi_bitmask")
        for col, flag in flags.items():
            if isinstance(flag, pd.Series):
                if col in df.columns:
                    df.loc[flag, col] = value
            elif isinstance(flag, pd.DataFrame):
                for subcol in flag.columns:
                    if subcol in df.columns:
                        df.loc[flag[subcol], subcol] = value
            else:
                raise TypeError(f"Invalid flag type for {col}: {type(flag)}")
        return df

    # 通过 bitmask_df 解码
    if bitmask_df is not None and columns is not None:
        flags = decode_multi_bitmask(bitmask_df, columns=columns, col_masks=col_masks, prefix=prefix, as_flags=False)
        return mask_multi_bitmask(df, flags=flags, value=value)

    raise ValueError("Either flags or (bitmask_df + columns) must be provided.")
