"""
datalab.utils.normalize 数据/字符标准化工具包
 - norm_rule 用于规则检测的规则转换工具
Version 0.1.0
"""
from typing import Iterable, Tuple, List
import re


def norm_rule(rule_str: str, columns: Iterable[str]) -> Tuple[str, List[str]]:
    """转换rule为pandas能识别的形式"""

    if not isinstance(rule_str, str) or not rule_str.strip():
        raise ValueError("rule must be a non-empty string")

    normalized = rule_str.strip()
    # col is not null
    normalized = re.sub(r"\b([A-Za-z_][A-Za-z0-9_]*)\s+is\s+not\s+null\b", r"\1.notna()", normalized,
                        flags=re.IGNORECASE)
    # col is null
    normalized = re.sub(r"\b([A-Za-z_][A-Za-z0-9_]*)\s+is\s+null\b", r"\1.isna()", normalized, flags=re.IGNORECASE)

    # col not in
    normalized = re.sub(r"\b([A-Za-z_][A-Za-z0-9_]*)\s+not\s+in\s*\(([^()]*)\)",
                        lambda m: f"~{m.group(1)}.isin([{m.group(2)}])", normalized, flags=re.IGNORECASE)
    # col in
    normalized = re.sub(r"\b([A-Za-z_][A-Za-z0-9_]*)\s+in\s*\(([^()]*)\)",
                        lambda m: f"{m.group(1)}.isin([{m.group(2)}])", normalized, flags=re.IGNORECASE)

    # 检测columns
    tokens = set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", normalized))

    keywords = {"and", "or", "not", "in", "True", "False", "None", "isna", "notna", "isin"}

    used_cols = []
    col_set = set(columns)
    for token in tokens:
        if token in keywords:
            continue
        if token not in col_set:
            raise ValueError(f"Column '{token}' not found in columns")
        used_cols.append(token)

    return normalized, used_cols
