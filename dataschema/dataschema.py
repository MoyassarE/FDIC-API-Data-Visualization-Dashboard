# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 18:36:21 2024

@author: me384
"""


import pandas as pd
import numpy as np
import plotly.express as px


################################################
#Datasets
################################################

import os




ProjectLocation = "Online"
#ProjectLocation = "Personal Computer"

def getProjectPath():
    currentfilepath = os.path.abspath(__file__)
    ProjectName = "bankfindAPI"
    ProjectPath = currentfilepath.split(ProjectName) # The project path is the first item after splitting the string
    
    return ProjectPath[0] 

def getInputPopulation():
    
    if ProjectLocation == "Personal Computer":
        ProjectPath = getProjectPath()
        FileMapping = 'bankfindAPI\\input\\banklist.xlsx' # Insert path of the file in the project
        FileLocation = ProjectPath + FileMapping
        
        sheetname = "banklist"
        
        SourceListOfBanks = pd.read_excel(FileLocation, sheet_name = sheetname, skiprows = None)    
    
    elif ProjectLocation == "Online":
        input_data_url = 'https://raw.githubusercontent.com/MoyassarE/FDIC-API-Data-Visualization-Dashboard/main/dataschema/dataschema.csv'
        SourceListOfBanks = pd.read_csv(input_data_url)
        
    return SourceListOfBanks

def getDataSchema():
    if ProjectLocation == "Personal Computer":
        ProjectPath = getProjectPath()
        FileMapping = 'bankfindAPI\\dataschema\\Selected Financial Data.xlsx' # Insert path of the file in the project
        FileLocation = ProjectPath + FileMapping    
        
        sheetname = "Selected Data"
        
        DataSchema = pd.read_excel(FileLocation, sheet_name = sheetname, skiprows = None) 
    
    elif ProjectLocation == "Online":
        dataschema_url = 'https://raw.githubusercontent.com/MoyassarE/FDIC-API-Data-Visualization-Dashboard/main/dataschema/dataschema.csv'
        DataSchema = pd.read_csv(dataschema_url)
    
    
    return DataSchema

def getOutputAPIData():
    if ProjectLocation == "Personal Computer":
        ProjectPath = getProjectPath()
        FileMapping = 'bankfindAPI\\output\\FDIC API Pulled Data.csv' # Insert path of the file in the project
        FileLocation = ProjectPath + FileMapping
    
        # when you index a column is is no longer in the dataset, but it is used to look up values
        BankFinancialData = pd.read_csv(FileLocation)
    
    elif ProjectLocation == "Online":
        output_data_url = 'https://raw.githubusercontent.com/MoyassarE/FDIC-API-Data-Visualization-Dashboard/main/output/FDIC%20API%20Pulled%20Data.csv'
        BankFinancialData = pd.read_csv(output_data_url)

    return BankFinancialData       

def update_Data_Schema():
    # After updates are made to the excel sheet file 
    # This method will save the data schema data into a csv file
    # So that after it is pushed to the github library
    # This data can be pullled using a github URL 
    # Allowing this code to be run in online server
    # as opposed to on a personal computer
    
    
    selected_data = getDataSchema()
    ProjectPath = getProjectPath()
    FileMapping = 'bankfindAPI\\dataschema\\' 
    CSV_Name = 'dataschema.csv'
    Full_Path = ProjectPath + FileMapping + CSV_Name
    selected_data.to_csv(Full_Path)
    


################################################
#Functions used by the API class to pull from the API
# There are 3 main user inputs when pulling from the API:
#    - The List of Banks
#    - The date
#    - The data points 
################################################

def getAllQueryColumns():
    #######################################
    # Create a string containing all the columns you would like to pull from the API
    ####################################### 
  
    SelectDataTable = getDataSchema()
    
    # Pull in the relevent codes
    CodeNames = pd.Series(SelectDataTable["Code"])
    
    # Skip any blank lines
    CodeNames = CodeNames[CodeNames.notnull()]
    
    # Combine all the columns names to request the data from the API
    FilterConcatenation = ','.join(CodeNames)
    
    return FilterConcatenation



def getListOfDefaultedBanks():
    #######################################
    # Pull a list of bank ids
    ####################################### 
       
    # when you index a column is is no longer in the dataset, but it is used to look up values
    DefaultedBankTable = getInputPopulation()
    
    # Within the column names there are trailing spaces. 
    # Remove trailing spaces
    DefaultedBankTable.columns = [c.strip() for c in DefaultedBankTable.columns]
    
    
    # Get List of Failed Banks by certification number
    DefaultedBankIDsList = DefaultedBankTable["Cert"].tolist() 
    
    return DefaultedBankIDsList


def getListOfClosingDatesForDefaultedBanks():
    #######################################
    # Pull a the dates associated with the banks
    ####################################### 
    
    # when you index a column is is no longer in the dataset, but it is used to look up values
    DefaultedBankTable = getInputPopulation()
    
    # Within the column names there are trailing spaces. 
    # Remove trailing spaces
    DefaultedBankTable.columns = [c.strip() for c in DefaultedBankTable.columns]
    

    # Get List of the dates each bank failed
    DefaultedBankClosingDateList = DefaultedBankTable["Closing Date"].tolist() 
    
    return DefaultedBankClosingDateList





################################################
#Data Analysis/Visualization of Pulled Data
################################################



def getCategoryMetaData():
    #######################################
    # First make a flat dictionary of all possible categories as well as the column number it belongs to
    #######################################
    
    TotalLevels = 3

    SelectDataTable = getDataSchema()
    
    # First make a flat dictionary of all possible categories as well as the column number it belongs to
    CategoryMetaData = []
    for level in range(TotalLevels, 0, -1):
        CategoryValues = pd.Series(SelectDataTable[f'Level {level} Category'].unique()).tolist()
        for category in CategoryValues:
            if isinstance(category, str):
                if level == 1:
                    ParentValue = ""
                else:
                    filteredTable = SelectDataTable[SelectDataTable[f'Level {level} Category'] == category]
                    ParentValue = pd.Series(filteredTable[f'Level {level-1} Category'].unique()).tolist()
                    ParentValue = ParentValue[0]
                newRow = np.array([category, level, ParentValue])
                CategoryMetaData.append(newRow)
    CategoryMetaData = np.array(CategoryMetaData)
    return CategoryMetaData      



def getDictionaryOfChildLevelItems(ParentCategory):
    
    ######################################
    # For a given category, get all childen categories and all line items that make up the children
    # If there is no children, provide a breakdown of all line items as children
    # Example OUTPUT:  The parent is Assets. A dictionary of the children would
    #{'Cash': ['CHBAL'], 
    #'Securities': ['SCUST', SCABS', 'SCSFP', 'SCODOT'], 
    #'Loans': ['LNRECONS',, 'LNOTCI'],
    #'Other Assets': ['BKPREM', 'ORE', 'INTAN', 'AOA']}
    #
    #This function is used as input to create graphs that breakdown the sum of children data
    ######################################
    
    ChildValuesDictionary = {}
    
    SelectDataTable = getDataSchema() 
    
    # Filter the table based on the category provided
    CategoryMetaData = getCategoryMetaData()  # Get data on all categories
    ParentMetaData = CategoryMetaData[(CategoryMetaData[:,0]==ParentCategory)] # Filter for provided category
    ParentCategoryLevel = ParentMetaData[0][1]  # Get the level of the column name
    ParentLevelColumnName = f'Level {ParentCategoryLevel} Category' 
    filteredTable = SelectDataTable[SelectDataTable[ParentLevelColumnName] == ParentCategory] # Filter the table

       
    # Get a list of children (i.e. rows in which the category is the parent)
    ChildrenMetaData = CategoryMetaData[(CategoryMetaData[:,2]==ParentCategory)]
    
    if len(ChildrenMetaData)==0:
        CategoryHasChildren = False
    else:
        CategoryHasChildren = True
        

    
    if CategoryHasChildren:
        childCategoryLevel = str(int(ParentCategoryLevel) + 1)
        ChildLevelColumnName = f'Level {childCategoryLevel} Category'
        ChildValues = ChildrenMetaData[:,0]
    else:
        ChildLevelColumnName = 'Description'
        ChildValues = pd.Series(filteredTable[ChildLevelColumnName].unique()).tolist()
        
        
    
    #For the selected children column, make a sum for all individual children    
    for childCategory in ChildValues:
        ChildLevelFilteredTable = filteredTable[filteredTable[ChildLevelColumnName] == childCategory]
        CodeNamesFiltered = pd.Series(ChildLevelFilteredTable["Code"])
        ChildValuesDictionary[childCategory] = CodeNamesFiltered.tolist()

    return ChildValuesDictionary


def getGraphOfChildLevelItems(ParentCategory):
    
    #################################
    # This function takes any category  and provide a breakdown graph of its children
    #################################
    
    # when you index a column is is no longer in the dataset, but it is used to look up values
    DefaultedBankTable = getOutputAPIData()
    
    ChildsDictionary = getDictionaryOfChildLevelItems(ParentCategory)
    
    ChildColumnNames = list(ChildsDictionary.keys())
    
    
    
    # Make new columns for the sums of the childs
    for categoryName,listOfUnderlyingColumns in ChildsDictionary.items():
        DefaultedBankTable[categoryName] = DefaultedBankTable[listOfUnderlyingColumns].sum(axis=1)
    
    
    # Make a total column which represents the sum of the parent
    DefaultedBankTable[ParentCategory]= DefaultedBankTable[ChildColumnNames].sum(axis=1)
    
    TopN = 50
    
    # Sort by total sum at a parent level
    DefaultedBankTable.sort_values(by=ParentCategory, ascending=True, inplace=True)
    DefaultedBankTable.insert(0, 'RankBySize', range(1, 1 + len(DefaultedBankTable)))
    
    DefaultedBankTable = DefaultedBankTable.tail(TopN)

    # How to use pip in CMD line: https://stackoverflow.com/questions/45954528/pip-is-configured-with-locations-that-require-tls-ssl-however-the-ssl-module-in
    # How to set PATH: https://stackoverflow.com/questions/9546324/adding-a-directory-to-the-path-environment-variable-in-windows
    
    
    InvertedTable = DefaultedBankTable[['RankBySize']+['NAME']+ChildColumnNames].melt(['RankBySize','NAME'], var_name='Asset Type', value_name='Amount (in thousands)')
    
    
    
    fig = px.area(InvertedTable, x="RankBySize", y="Amount (in thousands)", color="Asset Type", text='NAME')
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    #fig.show()
    
    return fig

def getTreeMapGraphOfAllCategories():
    
    CategoryMetaData = getCategoryMetaData()    

    names=CategoryMetaData[:,0]
    parents=CategoryMetaData[:,2]
    
    treefig = px.treemap(names=names, parents=parents)
    
    return treefig

ProjectLocation = "Personal Computer"
input_data = getInputPopulation()

ProjectPath = getProjectPath()
FileMapping = 'bankfindAPI\\input\\banklist.csv' # Insert path of the file in the project
FileLocation = ProjectPath + FileMapping

input_data.to_csv(FileLocation)
