"""
nyz_dynamic_design_builder.exporter

This module provides a utility to export Django queryset data to a pandas DataFrame.
It supports handling of ForeignKey, ManyToMany, and date fields, including custom
field mappings through `special_fk_values` and `special_m2m_fields`.
"""

import pandas as pd
from django.db.models import ForeignKey, ManyToManyField
from django.db.models.fields import DateField, DateTimeField


__all__ = [
    "export_data",
    "search_fk_value",
    "get_special_fk_fields",
    "get_special_m2m_fields",
    "get_m2m_fields"
]



def search_fk_value(obj, field, search_fk_list,previous_data_value=None,current_data_value=None):
    for search_field in search_fk_list:
        try:
            value = getattr(obj, field)
            value = getattr(value, search_field, None)
            if isinstance(field, (DateField, DateTimeField)):
                value = value.strftime("%Y-%m-%d %H:%M:%S") if value else ""
            if value:
                if previous_data_value and current_data_value and isinstance(value, str) and previous_data_value in value:
                    value = current_data_value
                return value

        except AttributeError:
            return ""
    return ""


def get_special_m2m_fields(m2m_obj, sub_fields, search_fk_list=None,previous_data_value=None,current_data_value=None):
    rows = {}
    if not m2m_obj:
        return ""

    for sub_field in sub_fields:
        try:
            value = getattr(m2m_obj, sub_field, "")
            if isinstance(value, ForeignKey):
                value = search_fk_value(m2m_obj, sub_field, search_fk_list,previous_data_value,current_data_value)
            if callable(value):
                value = value()
            verbose_name = m2m_obj._meta.get_field(sub_field).verbose_name
        except Exception:
            verbose_name = sub_field
            value = getattr(m2m_obj, sub_field, "")
        key = f"{verbose_name}"
        rows[key] = value
    return rows


def get_m2m_fields(field_name, m2m_values, search_fk_list, ignore_m2m_fields=None, special_m2m_fields=None, current_field=None,previous_data_value=None,current_data_value=None):
    m2m_rows = {}
    for index, m2m_value in enumerate(m2m_values, start=1):
        for field in m2m_value._meta.fields:
            if special_m2m_fields and current_field in special_m2m_fields:
                special_dict = get_special_m2m_fields(m2m_value, special_m2m_fields[current_field], search_fk_list,previous_data_value,current_data_value)
                m2m_rows.update(special_dict)
                continue
            if ignore_m2m_fields and field.name in ignore_m2m_fields:
                continue
            verbose = field.verbose_name
            value = getattr(m2m_value, field.name)
            if isinstance(field, (DateField, DateTimeField)):
                value = value.strftime("%Y-%m-%d %H:%M:%S") if value else ""
            if isinstance(field, ForeignKey):
                value = search_fk_value(m2m_value, field.name, search_fk_list,previous_data_value,current_data_value)
            col_name = f"{field_name} {index} - {verbose}"
            m2m_rows[col_name] = value
    return m2m_rows


def get_special_fk_fields(obj, field_name, sub_fields, search_fk_list=None,previous_data_value=None,current_data_value=None):
    rows = {}
    fk_obj = getattr(obj, field_name, None)
    if not fk_obj:
        return ""

    for sub_field in sub_fields:
        try:
            value = getattr(fk_obj, sub_field, "")
            if isinstance(value, ForeignKey):
                value = search_fk_value(fk_obj, sub_field, search_fk_list,previous_data_value,current_data_value)
            if callable(value):
                value = value()
            verbose_name = fk_obj._meta.get_field(sub_field).verbose_name
        except Exception:
            verbose_name = sub_field
            value = getattr(fk_obj, sub_field, "")
        key = f"{verbose_name}"
        rows[key] = value
    return rows


def export_data(field_list=None, query=None, search_fk_list=None, ignore_m2m_fields=None,
                special_fk_values=None, special_m2m_fields=None,previous_data_value=None,current_data_value=None):
    """
    Export a Django queryset to a pandas DataFrame with intelligent handling of
    ForeignKey, ManyToMany, and date fields.

    Parameters:
    - field_list (list): List of field names to export.
    - query (QuerySet): Django queryset to process.
    - search_fk_list (list): FK attributes to try (e.g., ['name', 'title']).
    - ignore_m2m_fields (list): M2M field names to ignore.
    - special_fk_values (dict): FK field to list of subfields to extract.
    - special_m2m_fields (dict): M2M field to list of subfields to extract.

    Returns:
    - pd.DataFrame: Exported data as DataFrame.
    """
    queryset = query
    model = queryset.model
    data = []

    for index, obj in enumerate(queryset, start=1):
        row = {}
        for field in field_list:
            try:
                field_obj = model._meta.get_field(field)
                verbose_name = field_obj.verbose_name
                if getattr(field_obj, "choices", None): # for choices field *
                    display_method = getattr(obj, f"get_{field}_display", None)
                    if callable(display_method):
                        row[verbose_name] = display_method()
                        continue
                value = getattr(obj, field)

                if isinstance(field_obj, (DateField, DateTimeField)):
                    value = value.strftime("%Y-%m-%d" if isinstance(field_obj, DateField) else "%Y-%m-%d %H:%M:%S") if value else ""




                if isinstance(field_obj, ForeignKey):
                    if special_fk_values and field in special_fk_values:
                        sub_fields = special_fk_values[field]
                        special_dict = get_special_fk_fields(obj, field, sub_fields, search_fk_list,previous_data_value,current_data_value)
                        row.update(special_dict)
                        continue
                    else:
                        value = search_fk_value(obj, field, search_fk_list,previous_data_value, current_data_value)
                        row[verbose_name] = value

                elif isinstance(field_obj, ManyToManyField):
                    m2m_values = value.all()
                    m2m_dict = get_m2m_fields(verbose_name, m2m_values, search_fk_list, ignore_m2m_fields,
                                              special_m2m_fields, field,previous_data_value, current_data_value)
                    row.update(m2m_dict)

                else:
                    row[verbose_name] = value
            except Exception:
                row[field] = ""

        data.append(row)

    return pd.DataFrame(data)
