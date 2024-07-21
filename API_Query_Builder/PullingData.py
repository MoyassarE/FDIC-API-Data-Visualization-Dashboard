# -*- coding: utf-8 -*-
"""
Created on Mon May 20 14:20:34 2024

@author: me384
"""
from main import get_summary, get_financials
import pandas as pd
from dateutil.relativedelta import relativedelta
from dataschema.dataschema import getAllQueryColumns, getListOfDefaultedBanks, getListOfClosingDatesForDefaultedBanks, getProjectPath



def Pull_Data_For_All_Institutions():
    

    ####################
    # Pull all data for each failed bank from the date that they closed
    # 3 inputs:
    #   - Bankid (cert #)
    #   - Date of the pull (cert #)
    #   - Data to query (cert #)
    ####################


    # Get List of Failed Banks by certification number
    DefaultedBankIDsList = getListOfDefaultedBanks()
    
    # Get List of the dates each bank failed
    DefaultedBankClosingDateList = getListOfClosingDatesForDefaultedBanks()
    
    # Get a string containing all the columns you would like to pull from the API    
    FilterConcatenation = getAllQueryColumns()


    ####################
    # Loop through list of banks and pull from FDIC API
    ####################
    
    df = pd.DataFrame()
    for x in range(len(DefaultedBankIDsList)):
        ClosingDateMinus6to9months = DefaultedBankClosingDateList[x] + relativedelta(months = -9) + pd.offsets.QuarterEnd()
        query_filters=f'CERT:{DefaultedBankIDsList[x]} AND REPDTE:{ClosingDateMinus6to9months.strftime("%Y%m%d")}'
        query_fields= FilterConcatenation
        
        
        tempdf = get_financials(
        filters=query_filters,
        fields=query_fields,
        output='pandas')
    if x == 0:
        df = tempdf
    else:
        df=pd.concat([df, tempdf])

    ####################
    # Output complete data to output folder
    ####################
    
    ProjectPath = getProjectPath()
    OutputMapping = 'bankfindAPI\\output\\FDIC API Pulled Data.xlsx' # Insert path of the file in the project
    OutputLocation = ProjectPath + OutputMapping      
    df.to_csv(OutputLocation,'query1')


#Pull_Data_For_All_Institutions()



