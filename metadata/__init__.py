# -*- coding: utf-8 -*-
"""
Created on Sun May  5 18:36:41 2024

@author: me384
"""

from .summary import summary_dict
from .financials import financials_dict



# The FDIC API has 5 separate datasets below

# The summary dictionary provides aggregate numbers and can be used to aggregate institution data over time

meta_dict = {
    #'failures': failure_dict,
    #'history': history_dict,
    #'institutions': institution_dict,
    #'locations': location_dict,
    'summary': summary_dict,
    'financials': financials_dict
}



