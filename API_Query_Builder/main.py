# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:27:01 2024

@author: me384
"""
from base import BF




def get_summary(filters: str = None, **kwargs):
    """
    Aggregate financial and structure data, subtotaled by year

    Arguments
    ---------
    filters: str, default None, optional
        Filter for the bank search

    Keyword Arguments
    -----------------
    fields: str, default ALL FIELDS, optional
        Comma delimited list of fields to search
    sort_by: str, default OFFICES, optional
        Field name by which to sort returned data
    sort_order: str, default ASC, optional
        Indicator if ascending (ASC) or descending (DESC)
    limit: int, default 10,000, optional
        Number of records to return.  Maximum is 10,000
    offset: int, default 0, optional
        Offset of page to return
    format: str, default json, optional
        Format of the data to return
    friendly_fields: bool, default False, optional
        Return friendly field names
    """
    return BF()._get_data("summary", filters, **kwargs)

def get_financials(filters: str = None, **kwargs):
    """
    Aggregate financial and structure data, subtotaled by year

    Arguments
    ---------
    filters: str, default None, optional
        Filter for the bank search

    Keyword Arguments
    -----------------
    fields: str, default ALL FIELDS, optional
        Comma delimited list of fields to search
    sort_by: str, default OFFICES, optional
        Field name by which to sort returned data
    sort_order: str, default ASC, optional
        Indicator if ascending (ASC) or descending (DESC)
    limit: int, default 10,000, optional
        Number of records to return.  Maximum is 10,000
    offset: int, default 0, optional
        Offset of page to return
    format: str, default json, optional
        Format of the data to return
    friendly_fields: bool, default False, optional
        Return friendly field names
    """
    return BF()._get_data("financials", filters, **kwargs)

