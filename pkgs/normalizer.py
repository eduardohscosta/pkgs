import locale
import unidecode
import string
import toolz
import pandas as pd
from typing import Union, Any

# set locale parameters (para conversão de encoding Python -> Excel)
# ---------------------------------------------------------------------
locale.setlocale(locale.LC_ALL, 'pt-br.UTF-8')

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# VALUES NORMALIZERS
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

def normalize_letter_type(value: str, letter_case_type: str = 'lower') -> str:
    """
    Apply a letter case type.
  
    Parameters:
    value (str): String to apply letter case type
    letter_case_type (str): Type of letter case to apply
  
    Returns:
    str: String with applied letter case
    """
    return eval(f'value.{letter_case_type}()')

def remove_numbers(value: str) -> str:
    """
    Replace all numbers by empty values.
  
    Parameters:
    value (str): String to replace numbers
  
    Returns:
    str: String with replaced numbers
    """
    return ''.join([i for i in value if not i.isdigit()])

def remove_letters(value: Union[str, int, float]) -> int:
    """Remove all letters from a value.

    Parameters
    ----------
    value : [str, int, float]
        Value to remove the letters.
    
    Return
    ----------
    int
       Integer/Float value.
    """
    letters_list = [str(l) for l in string.ascii_letters]
    return ''.join([i for i in value if i not in letters_list])

# def replace_space_to_underscore(value: str) -> str:
#     """
#     Replace all the spaces to undercore.
  
#     Parameters:
#     value (str): String to replace spaces
  
#     Returns:
#     str: String with replaced spaces
#     """
#     return value.replace(' ', '_')

# def remove_accents(value: str) -> str:
#     """
#     Remove all acents in a string.
  
#     Parameters:
#     value (str): String to remove accents
  
#     Returns:
#     str: String with replaced accents
#     """
#     return replace_space_to_underscore(unidecode.unidecode(value))

def remove_punctuation(value: str) -> str:
    """
    Replace all punctuation/special characters for empty values.
  
    Replace all punctuation/special characters for empty values. If there are any exception, the specific punctuation exeception will be ignored.
  
    Parameters:
    value (str): String to remove punctuation/special
  
    Returns:
    str: String with replaced punctuation/special
    """
    punctuation_list = [str(p) for p in string.punctuation]
    return ''.join([i for i in value if i not in punctuation_list])

# ---------------------------------------------------------------------

normalize_string = toolz.compose_left(
    normalize_letter_type,
    remove_numbers,
    # replace_space_to_underscore,
    # remove_accents,
    remove_punctuation,
)

normalize_number = toolz.compose_left(
    # remove_accents,
    remove_letters
)

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# VALUES NORMALIZERS
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

def normalize_cols_intire_null(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(how='all', axis=1)

def normalize_rows_intire_null(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(how='all', axis=0)

normalize_all_nulls = toolz.compose_left(
    normalize_cols_intire_null,
    normalize_rows_intire_null,
    )

# ---------------------------------------------------------------------

def _check_int_value(value: Any):
    if str(value).endswith('.0'):
        return int(normalize_number(str(value).replace('.0', '')))
    return int(normalize_number(str(value)))

def normalize_int_cols(df: pd.DataFrame):
    return df.applymap(_check_int_value).astype('int64') if df.shape[-1] > 0 else df

def _check_float_value(value: Any):
    if isinstance(value, str) and ',' in str(value):
        return locale.atof(normalize_number(str(value)))
    return float(value)

def normalize_float_cols(df: pd.DataFrame):
    return df.applymap(_check_float_value).astype('float64') if df.shape[-1] > 0 else df

def normalize_float_cols_as_str(df: pd.DataFrame):
    return df.applymap(locale.str).astype('string') if df.shape[-1] > 0 else df

def _strip_str_values(df: pd.DataFrame):
    return df.applymap(lambda x: str(x).strip())

def normalize_str_cols(df: pd.DataFrame, to_upper: bool = False, to_lower: bool = False):
    if df.shape[-1] > 0:
        if not to_upper and not to_lower:
            return _strip_str_values(df)
        elif to_upper and not to_lower:
            return _strip_str_values(df).applymap(str.upper)
        elif not to_upper and to_lower:
            return _strip_str_values(df).applymap(str.lower)
        return _strip_str_values(df)

    return df

def normalize_date_cols(df: pd.DataFrame):
    if df.shape[-1] > 0:
        df.applymap(lambda x: pd.to_datetime(x, format="%d-%m-%y", errors='coerce'))
    return df

def normalize_week(cycle: str, week: str):
    return f"{cycle} {week}"
