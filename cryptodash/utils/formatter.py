import pandas as pd
from typing import Dict, Optional


def format_numeric_dataframe(
    df: pd.DataFrame, column_formats: Optional[Dict[str, str]] = None
):
    '''
    Generic DataFrame formatter:
    - Default: all numeric columns -> comma-separated, 2 decimals
    - Negative numbers -> red
    - column_formats allows per-column format overrides

    Example:
    column_formats = {
        '24h Change (%)': '{:+.2f}%',
        'Market Cap ($)': '${:,.0f}'
    }
    '''
    column_formats = column_formats or {}

    numeric_cols = df.select_dtypes(include='number').columns

    # Default formatting for numeric columns
    format_map = {
        col: column_formats.get(col, '{:,.2f}') for col in numeric_cols
    }

    styler = df.style.format(format_map).map(
        lambda x: 'color: red' if isinstance(x, (int, float)) and x < 0 else '',
        subset=numeric_cols,
    )

    return styler
