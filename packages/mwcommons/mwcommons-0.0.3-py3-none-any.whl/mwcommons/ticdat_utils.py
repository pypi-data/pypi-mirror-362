import math
import os
import warnings
from typing import Any

import numpy as np
import pandas as pd
from ticdat import PanDatFactory, TicDatFactory

from mwcommons.exceptions import InputDataError


# region Set ticdat parameters
def set_input_parameter(schema, dat, name: str, value: Any):
    assert isinstance(schema, PanDatFactory)
    assert isinstance(dat, schema.PanDat)
    assert isinstance(name, str)

    if name not in schema.parameters:
        raise ValueError(f"Parameter {repr(name)} not found in schema.")

    params_df: pd.DataFrame = dat.parameters.copy()
    _dat = schema.copy_pan_dat(dat)

    if name in params_df["Name"].values:
        print(f"Overwriting parameter {repr(name)} with new value {repr(value)}")
        params_df.loc[params_df["Name"] == name, "Value"] = value
    else:
        print(f"Adding new parameter {repr(name)} with value {repr(value)}")
        new_row = pd.DataFrame({"Name": [name], "Value": [value]})
        params_df = pd.concat([params_df, new_row], ignore_index=True, axis=0)

    _dat.parameters = params_df

    return _dat


def set_multiple_input_parameters(schema, dat, parameters: dict[str, Any]):
    _dat = schema.copy_pan_dat(dat)

    for param_name, param_value in parameters.items():
        _dat = set_input_parameter(schema, _dat, param_name, param_value)

    return _dat


# endregion


# region Read/write/check data
def read_data(input_data_loc: str, schema: PanDatFactory):
    """
    Reads data from file(s) and populates an instance of the corresponding schema.

    Note: reading from .xls requires 'xlrd' package; reading from .xlsx requires 'openpyxl'.

    Parameters
    ----------
    input_data_loc: str
        Path-like string to the input data. It can be a directory containing CSV files, a xls/xlsx file, or a json
        file.
    schema: PanDatFactory
        An instance of the PanDatFactory class of ticdat.

    Returns
    -------
    dat
        A schema.PanDat object populated with the data available in input_data_loc.
    
    Raises
    ------
    TypeError
        If input_data_loc is not a string, or if schema is not a PanDatFactory instance.
    ValueError
        If input_data_loc is not a directory nor a file.
    NotADirectoryError
        If input_data_loc is neither a .xlsx, .xls, or .json file, nor a directory.
    """
    if not isinstance(input_data_loc, str):
        raise TypeError(f"input_data_loc should be a string, not {type(input_data_loc)}")
    if not isinstance(schema, PanDatFactory):
        raise TypeError(f"schema should be a PanDatFactory, not {type(schema)}")
    if not os.path.exists(input_data_loc):
        raise ValueError(f"input_data_loc is not a directory nor a file: '{input_data_loc}'")
    
    if input_data_loc.endswith((".xlsx", ".xls")):
        dat = schema.xls.create_pan_dat(input_data_loc)
    elif input_data_loc.endswith(".json"):
        dat = schema.json.create_pan_dat(input_data_loc)
    else:
        # in this case, input_data_loc must be a directory, read from csv files
        if not os.path.isdir(input_data_loc):
            raise NotADirectoryError(
                f"input_data_loc should be a directory, if not .xlsx, .xls, or .json: {input_data_loc}"
            )
        dat = schema.csv.create_pan_dat(input_data_loc)

    return dat


def write_data(sln, output_data_loc: str, schema: PanDatFactory) -> None:
    """
    Writes data to the specified location.

    Parameters
    ----------
    sln
        A schema.PanDat object populated with the data to be written to file/files.
    output_data_loc: str
        Path-like string to save the sln to. It can be a directory (to save the data as .csv files), a .xlsx file,
        or a .json file.
    schema: PanDatFactory
        An instance of the PanDatFactory class of ticdat, compatible with sln.
    
    Returns
    -------
    None
    
    Raises
    ------
    TypeError
        If output_data_loc is not a string, or if schema is not a ticdat.PanDatFactory instance.
    NotADirectoryError
        If the parent directory of output_data_loc does not exist.
    """
    if not isinstance(output_data_loc, str):
        raise TypeError(f"output_data_loc should be a string, not {type(output_data_loc)}")
    if not isinstance(schema, PanDatFactory):
        raise TypeError(f"schema should be a PanDatFactory, not {type(schema)}")
    
    parent_dir = os.path.dirname(output_data_loc)
    if not os.path.exists(parent_dir):
        raise NotADirectoryError(f"Parent directory of output_data_loc does not exist: {output_data_loc}")
    
    if output_data_loc.endswith(".xlsx"):
        schema.xls.write_file(sln, output_data_loc)
    elif output_data_loc.endswith(".json"):
        schema.json.write_file_pd(sln, output_data_loc, orient='split')
    else:
        # if path has extension, warn the user that it will be ignored and considered as a directory
        if os.path.splitext(output_data_loc)[1]:
            warnings.warn(
                f"output_data_loc's extension will be ignored and it'll be considered a directory instead: "
                f"{output_data_loc}",
                UserWarning
            )
        
        # we assume that output_data_loc is a directory, write csv files inside it
        schema.csv.write_directory(sln, output_data_loc)

    return None


def print_failures(schema: PanDatFactory | TicDatFactory, failures: dict[str, Any]) -> None:
    """Prints out a sample of the data failure encountered."""
    if isinstance(schema, PanDatFactory):
        for table_name, table in failures.items():
            print(table_name)
            print(table.head().to_string())
    elif isinstance(schema, TicDatFactory):
        for table_name, table in failures.items():
            print(table_name)
            print({key: table[key] for key in list(table)[:5]})
    else:
        raise TypeError(f"bad schema type: {type(schema)}")


def check_data(dat, schema: PanDatFactory | TicDatFactory) -> None:
    """
    Runs data integrity checks and prints out some sample failures to facilitate debugging.

    :param dat: A PanDat or TicDat object.
    :param schema: The schema that `dat` belongs to.
    :return: None
    """
    print("Running data integrity check...")
    if isinstance(schema, TicDatFactory):
        if not schema.good_tic_dat_object(dat):
            raise InputDataError("Not a good TicDat object")
    elif isinstance(schema, PanDatFactory):
        if not schema.good_pan_dat_object(dat):
            raise InputDataError("Not a good PanDat object")
    else:
        raise TypeError(f"bad schema type: {type(schema)}")
    foreign_key_failures = schema.find_foreign_key_failures(dat)
    if foreign_key_failures:
        print_failures(schema, foreign_key_failures)
        raise InputDataError(f"Foreign key failures found in {len(foreign_key_failures)} table(s)/field(s).")
    data_type_failures = schema.find_data_type_failures(dat)
    if data_type_failures:
        print_failures(schema, data_type_failures)
        raise InputDataError(f"Data type failures found in {len(data_type_failures)} table(s)/field(s).")
    data_row_failures = schema.find_data_row_failures(dat)
    if data_row_failures:
        print_failures(schema, data_row_failures)
        raise InputDataError(f"Data row failures found in {len(data_row_failures)} table(s)/field(s).")
    duplicates = schema.find_duplicates(dat)
    if duplicates:
        print_failures(schema, duplicates)
        raise InputDataError(f"Duplicates found in {len(duplicates)} table(s)/field(s).")
    print("Data is good!")


# endregion


# region Manual data type setting/checking and foreign key relationships
def set_data_types(dat, schema: PanDatFactory):
    """
    Return a copy of the input dat with the data types set according to the schema.

    Remember that ticdat doesn't enforce datatypes, it's meant only to check/validate the input data matches the
    specified types.
    """
    if not isinstance(schema, PanDatFactory):
        raise TypeError(f"schema should be a PanDatFactory object, not {type(schema)}")
    if not schema.good_pan_dat_object(dat):
        raise InputDataError("dat is not a good PanDat object")

    dat_ = schema.copy_pan_dat(pan_dat=dat)

    # get data_types dict from input_schema: {}
    data_types = schema.schema(include_ancillary_info=True)["data_types"]

    # iterate over the data_types to get a dict with the data dtypes for each column, for each DataFrame
    for table_name in data_types.keys():
        table_df = getattr(dat_, table_name)
        table_df = table_df.reset_index(drop=True)
        fields = data_types[table_name].keys()
        for field in fields:
            field_data_type = data_types[table_name][field]._asdict()
            if field_data_type["datetime"]:
                table_df[field] = pd.to_datetime(table_df[field])

            elif field_data_type["strings_allowed"]:
                # if strings_allowed, the field is supposed to be str. However, simply setting astype(str) could
                # silently convert NaN values to 'nan' instead of '' (empty string). Similarly, original integer values
                # may have been understood as float an converted from 10 to 10.0 (if there was NaN values for instance,
                # pandas cast to float), so directly converting to str would lead to '10.0' instead of '10'.
                # We'll handle these cases carefully.
                table_df[field] = _set_series_type_to_str(table_df[field])

            elif field_data_type["number_allowed"]:
                table_df[field] = table_df[field].astype(float)
                if field_data_type["must_be_int"]:
                    int_field = table_df[field].astype(int)
                    # ensure we don't accidently round values in a silent bug
                    matching_values = np.isclose(int_field, table_df[field])
                    if not matching_values.all():
                        raise InputDataError(
                            f"The column {table_name}.{field} must be int, but it contains non-integer values that "
                            f"would be rounded by .astype(int) and therefore the type conversion is not clear. "
                            f"Rounding errors would occur for:\n{table_df.loc[~matching_values].to_string()}"
                        )
                    table_df[field] = int_field

        setattr(dat_, table_name, table_df)

    return dat_


def _set_series_type_to_str(series: pd.Series) -> pd.Series:
    """
    Converts a pandas series to str, converting NaN to '', decimals like '123.0' or 123.0 to '123', and keeping
    everything else unchanged.

    Parameters
    ----------
    series : pandas.series
        Series whose values are to be converted to str. It may contain decimals, so if we simply convert to str
        directly, we'll have strings like '123.0' but what we actually want is '123'.

    Returns
    -------
    pandas.series
        The output series with values converted to str and decimals removed, if any. NaN values are converted to the
        empty string ''. All the other values (non-numeric, not-null) are simply passed to .astype('str').
    """
    # try to convert to numeric first, to get entries that are numeric. Non-numeric entries will be NaN (coerce)
    to_numeric = pd.to_numeric(series, errors="coerce")

    # get indices
    numeric_indices = ~to_numeric.isna()
    nan_indices = series.isna()
    remaining_indices = (~numeric_indices) & (~nan_indices)

    # get entries
    numeric_entries = series.loc[numeric_indices]
    nan_entries = series.loc[nan_indices]
    remaining_entries = series.loc[remaining_indices]

    # convert entries
    # numeric: float -> int (e.g. 123.0 -> 123) -> str
    # NaN entries: simply fill with ''
    # everything else: simply convert to str
    numeric_entries = numeric_entries.astype("float").astype("int").astype("str")
    nan_entries = nan_entries.fillna("")
    remaining_entries = remaining_entries.astype("str")

    # put everything together keeping the original order
    output = pd.concat([numeric_entries, nan_entries, remaining_entries]).sort_index()

    return output


def set_parameters_datatypes(params: dict[str, Any], schema: PanDatFactory) -> dict[str, Any]:
    if not isinstance(params, dict):
        raise TypeError(f"params should be a dictionary, not {type(params)}")
    if not isinstance(schema, PanDatFactory):
        raise TypeError(f"schema should be a PanDatFactory object, not {type(schema)}")

    new_params = {}
    for parameter, value in params.items():
        # get ticdat datatype, that is, a dictionary like {number_allowed: True, strings_allowed: (), ...} as defined
        # in the schema
        ticdat_datatype = schema.parameters[parameter]._asdict()["type_dictionary"]._asdict()

        if is_null(value):
            if ticdat_datatype["nullable"]:
                new_params[parameter] = None
            else:
                raise ValueError(
                    f"Parameter {parameter} is not nullable (according to schema), but its value is null: {value}"
                )

        else:
            if ticdat_datatype["datetime"]:
                new_params[parameter] = pd.to_datetime(value)

            elif ticdat_datatype["strings_allowed"]:
                new_params[parameter] = str(value)

            elif ticdat_datatype["number_allowed"]:
                numeric_value = float(value)
                if ticdat_datatype["must_be_int"]:
                    int_value = round(numeric_value)
                    # ensure we don't accidently round value in a silent bug
                    if not math.isclose(int_value, numeric_value):
                        raise InputDataError(
                            f"The parameter '{parameter}' must be int, but rounding it would lead to a relevant "
                            f"rounding error, and therefore the type conversion is not clear. Value: {numeric_value}"
                        )
                    new_params[parameter] = int_value
                else:
                    new_params[parameter] = numeric_value

    return new_params


def is_null(value) -> bool:
    """
    Check if 'value' is None, NaN, empty string, or empty collections.

    The reason to create this function instead of simply relying on the built-in bool() is because
    1.  bool(float('nan')) returns True, suggesting it's not null, but we want it to be null;
    2.  bool(0) returns False, suggesting it's null, but we want it to be not null.

    Parameters
    ----------
    value : Any
        Value to be checked.

    Returns
    -------
    bool
        True if the value is None, NaN, empty string, or empty collections, False otherwise.

    Examples:
    >>> is_null(None)
    True
    >>> is_null(float('nan'))
    True
    >>> is_null(np.nan)
    True
    >>> is_null("")
    True
    >>> is_null([])
    True
    >>> is_null({})
    True
    >>> is_null(set())
    True
    >>> is_null(0)
    False
    >>> is_null("non-empty")
    False
    >>> is_null("nan")
    False
    >>> is_null([1, 2, 3])
    False
    >>> is_null([np.nan])
    False
    """
    if isinstance(value, (int, float)):
        return np.isnan(value)

    return not bool(value)


def check_foreign_key(
    dat,
    native_table: dict[str, Any],
    foreign_table: dict[str, Any],
    reverse: bool = False,
) -> None:
    """
    Ensure a foreign key relation from native_table to foreign_table structures.

    This is similar to ticdat's foreign keys. The advantage of this function is that it allows for filtering the
    tables before checking the foreign key relation, if desired. For example, it's useful when there's a master
    customers table with a type column, and another table with a customer's field supposed to have only some specific
    customers' types, the standard ticdat's foreign key relation would not be enough to check this.

    Parameters
    ----------
    dat
        A PanDat object that holds the native and foreign tables as attributes.
    native_table, foreign_table : dict[str, Any]
        A dictionary with mandatory keys 'name, 'fields', 'entry', and optional keys 'subset', 'filters'.
        Their VALUES' datatypes are as follows:
            'name': str
                The name of the native/foreign table.
            'fields': str or list[str]
                Field (or list of fields) in the native/foreign table to be checked against a foreign/native table's
                field (or list of fields). If a list, the foreign_table/native_table's corresponding value must be a
                list as well, with the same length.
            'entry': str
                The name of the entry in the native/foreign table to be reported in the error message. For example,
                the frontend name of the column(s) in 'fields' to be reported to the user in case of a foreign key
                failure.
            'subset': dict[str, Union[list, dict, tuple, set]] or None, default=None
                A dictionary whose keys are fields of the native/foreign table, and values are either, sets, lists,
                tuples, or dictionaries. It'll be used to filter the native/foreign table by where the field is in
                the iterable before checking the inclusion. Set it to None if no filter is supposed to be applied.
                If 'subset' is missing in the keys, the function behaves the same as its value was None.
            'filters' : callable or None, default=None
                A function that takes as argument the native/foreign table and returns a boolean series (not a
                dataframe! indicating the rows to preserve before checking the inclusion. Set it to None if no filter
                is supposed to be applied.
    reverse : bool, default=False
        Whether to check the reverse inclusion as well, i.e., equality. Defaults to False, that is, only the
        unidirectional inclusion from the native table to the foreign table is checked. Set it to True to check the
        equality.

    Examples
    --------
    In the example below, assume "dat" is a ticdat.PanDatFactory.PanDat object that contains 'land_shipments' and
    'edges' tables. When filtering the foreign table, the example illustrates two equivalent options by using
    "subset" and "filters" keys; the former is usually shorter and more handy, whereas the latter is more flexible.

    native_table = {
        'name': 'land_shipments',  # native table, attribute of "dat"
        'fields': ['Origin ID', 'Destination ID'],  # columns of dat.land_shipments
        'entry': '(Origin ID, Destination ID) pairs',  # how to call the given fields in the error message
    }
    foreign_table = {
        'name': 'edges',  # foreign table, attribute of "dat"
        'fields': ['Origin Node ID', 'Destination Node ID'],  # columns of dat.edges
        'entry': '(Origin Node ID, Destination Node ID) pairs', # how to call the given fields in the error message
        'subset': {'Edge Type': {'Land'}}  # filter the edges table by 'Edge Type' in {'Land'}
        'filters: lambda df: df['Edge Type'] == 'Land'  # filter the edges table by where 'Edge Type' == 'Land'
    }
    check_foreign_key(dat, native_table, foreign_table)

    Raises
    ------
    TypeError
        If the values in each dictionary don't match the expected datatypes specified above.
    ValueError
        If one of the mandatory keys 'name', 'fields', and 'entry' is not present in the dictionaries native_table
        and/or foreign_table. If 'fields' don't refer to actual column(s) of the corresponding table. If 'subset' is
        given but its keys don't refer to actual columns of the table.
    AttributeError
        If 'name' doesn't refer to an actual table, attribute of dat. If 'fields' is not a str or a list of str.
        If 'subset' is given but is not a dictionary like {str: Union[list, dict, tuple, set]}.

    InputDataError
        If the foreign key relation from the native table to the foreign table fails, that is, the field(s) in the
        native table (possibly filtered) contains some value(s) not present in the foreign table's field(s) (possibly
        filtered). If reverse is True, then this exception is raised in case the equality fails (instead of the
        unidirectional inclusion).
    """
    # ensure mandatory dictionaries' keys are present
    mandatory_keys = ["name", "field", "entry"]
    missing_keys = []  # list of tuples (dictionary, missing_key) to report
    for dictionary, dict_name in [
        (native_table, "native_table"),
        (foreign_table, "foreign_table"),
    ]:
        # get missing mandatory keys in the argument dictionaries
        for key in mandatory_keys:
            if key not in dictionary:
                missing_keys.append((dict_name, key))

    if missing_keys:
        raise ValueError(
            f"{mandatory_keys} are mandatory keys for the dictionaries native_table and foreign_table. The following "
            f"are pairs of (dictionary, missing_key):\n{missing_keys}"
        )

    # ensure consistency between the given arguments
    for dictionary, dict_name in [
        (native_table, "native_table"),
        (foreign_table, "foreign_table"),
    ]:
        # ensure 'name' is a str
        if not isinstance(dictionary["name"], str):
            raise TypeError(
                f"{dict_name}['name'] must be a str, got {type(dictionary['name'])} instead: {dictionary['name']}"
            )

        # ensure tables' names are indeed attributes of dat
        table_name = dictionary["name"]
        if not hasattr(dat, table_name):
            raise AttributeError(
                f"{dict_name}['name'] should be an attribute of 'dat', i.e., an input table, got '{table_name}' "
                f"instead."
            )
        table_df = getattr(dat, table_name)

        # ensure fields are str or list[str] and are indeed columns of their corresponding tables
        fields = dictionary["field"]
        if not isinstance(fields, (str, list)):
            raise TypeError(
                f"{dict_name}['field'] must be either a str or a list, got {type(fields)} instead: {fields}"
            )
        if isinstance(fields, list) and not all(isinstance(field, str) for field in fields):
            raise TypeError(f"When {dict_name}['field'] is a list, its elements must be strings, got {fields}")
        if isinstance(fields, str):
            # overwrite the str with a singleton list back in the original dictionary
            dictionary["field"] = [fields]
            fields = [fields]
        for field in fields:
            if field not in table_df.columns:
                raise ValueError(
                    f"'{field}' (from {dict_name}['fields']) is not a column of '{table_name}' table. Available "
                    f"columns are: {list(table_df.columns)}"
                )

        # ensure 'entry' is a str
        if not isinstance(dictionary["entry"], str):
            raise TypeError(
                f"{dict_name}['entry'] must be a str, got {type(dictionary['entry'])} instead: {dictionary['entry']}"
            )

        # ensure subset is a dictionary of str: list | dict | tuple | set, if passed, whose keys are indeed
        # columns of the table
        subset = dictionary.get("subset", None)
        if subset is not None:
            if not isinstance(subset, dict):
                raise TypeError(f"{dict_name}['subset'] must be a dictionary, got {type(subset)} instead: {subset}")
            for field in subset:
                if field not in table_df.columns:
                    raise ValueError(
                        f"'{field}' key (from {dict_name}['subset']) is not a column of '{table_name}' table. "
                        f"Available columns are: {list(table_df.columns)}"
                    )
                if not isinstance(subset[field], (dict, list, set, tuple)):
                    raise TypeError(
                        f"{dict_name}['subset'][{field}] must be a dict, list, set or tuple, got "
                        f"{type(subset[field])} instead: {subset[field]}"
                    )

        # ensure 'filters' is a callable, if passed
        filters = dictionary.get("filters", None)
        if (filters is not None) and (not callable(filters)):
            raise TypeError(f"{dict_name}['filters'] must be a callable, got {type(filters)} instead: {filters}")

    native_table_df = getattr(dat, native_table["name"])
    foreign_table_df = getattr(dat, foreign_table["name"])

    # create standard function to filter each table before comparing
    def _filter_df(df: pd.DataFrame, table_dict: dict) -> pd.DataFrame:
        _df = df.copy()
        # if table_dict sets a subset to filter its dataframe, filter it by each condition.
        # This is equivalent to _df[_df['field1'].isin(subset1) & _df['field2'].isin(subset2) & ...]
        for column, subset in table_dict.get("subset", {}).items():
            _df = _df[_df[column].isin(subset)]
        # if table_dict sets a filter function, apply it
        filter_function = table_dict.get("filters")
        if filter_function is not None:
            _df = _df[filter_function(_df)]
        return _df

    # create standard function to get the entries for each table, as a set, to compare
    def _get_entries_to_compare(table_dict: dict, table_df: pd.DataFrame) -> set:
        df = table_df.copy()
        df = _filter_df(df, table_dict)
        # return the entries as a set of tuples whose length is the number of fields
        return set(df[table_dict["field"]].apply(tuple, axis=1))

    # get sets of values to compare
    native_table_entries: set = _get_entries_to_compare(native_table, native_table_df)
    foreign_table_entries: set = _get_entries_to_compare(foreign_table, foreign_table_df)

    # create function to standardize the error message
    def _error_message(native_table: dict, foreign_table: dict, df_to_report: pd.DataFrame) -> str:
        base_text = f"The following {native_table['entry']} show up in {native_table['name']}[{native_table['field']}],"

        if "subset" in native_table:
            base_text += f" where {native_table['name']} satisfies"
            for field, subset in native_table["subset"].items():
                base_text += f" {field} is in {subset},"

        base_text += f" but they don't appear in {foreign_table['name']}[{foreign_table['field']}]"

        if "subset" in foreign_table:
            base_text += f" where {foreign_table['name']} satisfies"
            for field, subset in foreign_table["subset"].items():
                base_text += f" {field} is in {subset}, "

        return base_text.rstrip(", ") + f":\n{df_to_report.to_string(index=False)}"

    # compare inclusion of values from the native table into the foreign ones
    missing_entries = native_table_entries.difference(foreign_table_entries)
    if missing_entries:
        # there are entries in the native table that are not in the foreign table
        df_to_report = native_table_df[
            native_table_df[native_table["field"]].apply(tuple, axis=1).isin(missing_entries)
        ]
        df_to_report = _filter_df(df_to_report, native_table)
        raise InputDataError(_error_message(native_table, foreign_table, df_to_report))

    # check reverse inclusion (i.e. equality) if requested
    if reverse:
        missing_entries_reverse = foreign_table_entries.difference(native_table_entries)
        if missing_entries_reverse:
            # there are entries in the foreign table that are not in the native table
            df_to_report = foreign_table_df[
                foreign_table_df[foreign_table["field"]].apply(tuple, axis=1).isin(missing_entries_reverse)
            ]
            df_to_report = _filter_df(df_to_report, foreign_table)
            raise InputDataError(_error_message(foreign_table, native_table, df_to_report))


# endregion


if __name__ == "__main__":
    import doctest

    doctest.testmod()
