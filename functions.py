# Imports

import numpy as np
import pandas as pd
import yahoo_fin.stock_info as si

# Function to gather data from Yahoo


def get_data(ticker):
    '''
    Gathers the required financial data on the
    given parameter ticker (str)
    '''
    
    financials = si.get_financials(ticker, yearly=True, quarterly=False)
    
    # returns pandas dataframe
    
    return financials

# Function to determine revenue growth(default to 3-yr average if no user input) #


def get_revenue_growth(financials):
    '''
    Takes growth assumptions from user or uses 3-year historical avg if no input
    '''
    
    user_input = input("Would you like to input your own growth assumptions? (Y/N): ")
    
    if user_input == 'Y':
        
        revenue_growth1 = float(input("Enter growth assumption for first forecast year(decimal): "))
        revenue_growth2 = float(input("Enter growth assumption for second forecast year(decimal): "))
        revenue_growth3 = float(input("Enter growth assumption for third forecast year(decimal): "))
        revenue_growth4 = float(input("Enter growth assumption for fourth forecast year(decimal): "))
        revenue_growth5 = float(input("Enter growth assumption for fifth forecast year(decimal): "))
        
        revenue_growth = [revenue_growth1, revenue_growth2, revenue_growth3, revenue_growth4, revenue_growth5]
    
    elif user_input == 'N':
        
        revenue_growth1 = (financials['yearly_income_statement'].loc['totalRevenue'][0] - financials['yearly_income_statement'].loc['totalRevenue'][1]) / financials['yearly_income_statement'].loc['totalRevenue'][1]
        revenue_growth2 = (financials['yearly_income_statement'].loc['totalRevenue'][1] - financials['yearly_income_statement'].loc['totalRevenue'][2]) / financials['yearly_income_statement'].loc['totalRevenue'][2] 
        revenue_growth3 = (financials['yearly_income_statement'].loc['totalRevenue'][2] - financials['yearly_income_statement'].loc['totalRevenue'][3]) / financials['yearly_income_statement'].loc['totalRevenue'][3]
        
        average_growth = (revenue_growth1 + revenue_growth2 + revenue_growth3) / 3
        revenue_growth = [average_growth]
        
    else:
        print("You did not enter a correct answer.")
        user_input = input("Would you like to input your own growth assumptions? (Y/N): ")
        
    return revenue_growth

# Function to forecast financial statements 5-years 


def forecast_statements(financials, revenue_growth):
    '''
    Applies the 3yr forecasted growth onto IS, BS
    '''
    
    # Determining the % of revenue for each item
        # Gathers only the most currently year data and current year revenue
    only_current_year_is = financials['yearly_income_statement'].iloc[0:, 0]
    only_current_year_bs = financials['yearly_balance_sheet'].iloc[0:, 0]
    only_current_year_cf = financials['yearly_cash_flow'].iloc[0:, 0]
    current_year_revenue = only_current_year_is['totalRevenue']
        # Creating dictionary to hold % of revenue
    percent_of_sales_is_dict = {}
    percent_of_sales_bs_dict = {}
        
        # # INCOME STATEMENT ##
        
        # looping through current year data to gather % of revenue for income statement
    for line, value in only_current_year_is.items():
        if line != 'totalRevenue':
            if  value != None:
                percent_of_sales_is_dict[line] = value / current_year_revenue
            else:
                percent_of_sales_is_dict[line] = value
    
        # Creating forecast dictionary for year 1 income statement
    forecast_dict_y1_is = {}
    forecast_dict_y1_is['totalRevenue'] = only_current_year_is['totalRevenue'] * (1 + revenue_growth[0])
    
    for line, value in only_current_year_is.items():
        if line != 'totalRevenue':
            if value != None:
                forecast_dict_y1_is[line] = forecast_dict_y1_is['totalRevenue'] * percent_of_sales_is_dict[line]
            else:
                forecast_dict_y1_is[line] = value
            
        # Creating forecast dictionary for year 2 income statement   
    forecast_dict_y2_is = {}
    
    if len(revenue_growth) > 1:
        forecast_dict_y2_is['totalRevenue'] = forecast_dict_y1_is['totalRevenue'] * (1 + revenue_growth[1])
    else:
        forecast_dict_y2_is['totalRevenue'] = forecast_dict_y1_is['totalRevenue'] * (1 + revenue_growth[0])
    
    for line, value in only_current_year_is.items():
        if line != 'totalRevenue':
            if value != None:
                forecast_dict_y2_is[line] = forecast_dict_y2_is['totalRevenue'] * percent_of_sales_is_dict[line]
            else:
                forecast_dict_y2_is[line] = value

        # Creating forecast dictionary for year 3 income statement   
    forecast_dict_y3_is = {}
    
    if len(revenue_growth) > 1:
        forecast_dict_y3_is['totalRevenue'] = forecast_dict_y2_is['totalRevenue'] * (1 + revenue_growth[2])
    else:
        forecast_dict_y3_is['totalRevenue'] = forecast_dict_y2_is['totalRevenue'] * (1 + revenue_growth[0])
    
    for line, value in only_current_year_is.items():
        if line != 'totalRevenue':
            if value != None:
                forecast_dict_y3_is[line] = forecast_dict_y3_is['totalRevenue'] * percent_of_sales_is_dict[line]
            else:
                forecast_dict_y3_is[line] = value
    
        # Creating forecast dictionary for year 4 income statement   
    forecast_dict_y4_is = {}
    
    if len(revenue_growth) > 1:
        forecast_dict_y4_is['totalRevenue'] = forecast_dict_y3_is['totalRevenue'] * (1 + revenue_growth[3])
    else:
        forecast_dict_y4_is['totalRevenue'] = forecast_dict_y3_is['totalRevenue'] * (1 + revenue_growth[0])
    
    for line, value in only_current_year_is.items():
        if line != 'totalRevenue':
            if value != None:
                forecast_dict_y4_is[line] = forecast_dict_y4_is['totalRevenue'] * percent_of_sales_is_dict[line]
            else:
                forecast_dict_y4_is[line] = value
    
        # Creating forecast dictionary for year 5 income statement   
    forecast_dict_y5_is = {}
    
    if len(revenue_growth) > 1:
        forecast_dict_y5_is['totalRevenue'] = forecast_dict_y4_is['totalRevenue'] * (1 + revenue_growth[4])
    else:
        forecast_dict_y5_is['totalRevenue'] = forecast_dict_y4_is['totalRevenue'] * (1 + revenue_growth[0])
    
    for line, value in only_current_year_is.items():
        if line != 'totalRevenue':
            if value != None:
                forecast_dict_y5_is[line] = forecast_dict_y5_is['totalRevenue'] * percent_of_sales_is_dict[line]
            else:
                forecast_dict_y5_is[line] = value
    
        # # BALANCE SHEET ## 
    
        # Determining % of revenue for each balance sheet item
    for line, value in only_current_year_bs.items():
        if  value != None:
            percent_of_sales_bs_dict[line] = value / current_year_revenue
        else:
            percent_of_sales_bs_dict[line] = value
    
        # Creating forecast dict for year 1 balance sheet
    forecast_dict_y1_bs = {}
    
    for line, value in only_current_year_bs.items():
        if value != None:
            forecast_dict_y1_bs[line] = forecast_dict_y1_is['totalRevenue'] * percent_of_sales_bs_dict[line]
        else:
            forecast_dict_y1_bs[line] = value
    
        # Creating forecast dict for year 2 balance sheet
    forecast_dict_y2_bs = {}
    
    for line, value in only_current_year_bs.items():
        if value != None:
            forecast_dict_y2_bs[line] = forecast_dict_y2_is['totalRevenue'] * percent_of_sales_bs_dict[line]
        else:
            forecast_dict_y2_bs[line] = value
    
        # Creating forecast dict for year 3 balance sheet
    forecast_dict_y3_bs = {}
    
    for line, value in only_current_year_bs.items():
        if value != None:
            forecast_dict_y3_bs[line] = forecast_dict_y3_is['totalRevenue'] * percent_of_sales_bs_dict[line]
        else:
            forecast_dict_y3_bs[line] = value
    
        # Creating forecast dict for year 4 balance sheet
    forecast_dict_y4_bs = {}
    
    for line, value in only_current_year_bs.items():
        if value != None:
            forecast_dict_y4_bs[line] = forecast_dict_y4_is['totalRevenue'] * percent_of_sales_bs_dict[line]
        else:
            forecast_dict_y4_bs[line] = value
    
        # Creating forecast dict for year 5 balance sheet
    forecast_dict_y5_bs = {}
    
    for line, value in only_current_year_bs.items():
        if value != None:
            forecast_dict_y5_bs[line] = forecast_dict_y5_is['totalRevenue'] * percent_of_sales_bs_dict[line]
        else:
            forecast_dict_y5_bs[line] = value
    
        # # DEPRECIATION ##
    
    percent_of_rev_depr = only_current_year_cf.loc['depreciation'] / only_current_year_is.loc['totalRevenue']
    
    forecast_depr = {}
    forecast_depr['Current Year'] = only_current_year_cf.loc['depreciation']
    forecast_depr['Forecast Year 1'] = forecast_dict_y1_is['totalRevenue'] * percent_of_rev_depr
    forecast_depr['Forecast Year 2'] = forecast_dict_y2_is['totalRevenue'] * percent_of_rev_depr
    forecast_depr['Forecast Year 3'] = forecast_dict_y3_is['totalRevenue'] * percent_of_rev_depr
    forecast_depr['Forecast Year 4'] = forecast_dict_y4_is['totalRevenue'] * percent_of_rev_depr
    forecast_depr['Forecast Year 5'] = forecast_dict_y5_is['totalRevenue'] * percent_of_rev_depr
    
        # Creating dataframe consisting of all income statement forecast results
    forecast_dataframe_income = pd.DataFrame({'Forecast Year 1': forecast_dict_y1_is, 'Forecast Year 2': forecast_dict_y2_is, 'Forecast Year 3': forecast_dict_y3_is, 'Forecast Year 4': forecast_dict_y4_is, 'Forecast Year 5': forecast_dict_y5_is})
    
        # Creating dataframe consisting of all balance sheet forecast results
    forecast_dataframe_balance = pd.DataFrame({'Forecast Year 1': forecast_dict_y1_bs, 'Forecast Year 2': forecast_dict_y2_bs, 'Forecast Year 3': forecast_dict_y3_bs, 'Forecast Year 4': forecast_dict_y4_bs, 'Forecast Year 5': forecast_dict_y5_bs})
    
    return only_current_year_is, only_current_year_bs, only_current_year_cf, forecast_dataframe_income, forecast_dataframe_balance, forecast_depr

# Function to forecast future cash flow


def get_fcf(current_is, current_bs, forecasted_income, forecasted_balance, forecasted_depr):
    '''
    takes pandas dataframes of income statement and balance sheet as parameters
    '''
    
    # Creating main dict for all forecast years
    cashflow_forecast = {}
    
    # Forecast year 1 cash flow
    cashflow_forecast['Forecast Year 1'] = {}
    cashflow_forecast['Forecast Year 1']['netIncome'] = forecasted_income.loc['netIncome', 'Forecast Year 1']
    cashflow_forecast['Forecast Year 1']['inc_depreciation'] = forecasted_depr['Forecast Year 1'] - forecasted_depr['Current Year']
    cashflow_forecast['Forecast Year 1']['inc_receivables'] = forecasted_balance.loc['netReceivables', 'Forecast Year 1'] - current_bs.loc['netReceivables']
    cashflow_forecast['Forecast Year 1']['inc_inventory'] = forecasted_balance.loc['inventory', 'Forecast Year 1'] - current_bs.loc['inventory']
    cashflow_forecast['Forecast Year 1']['inc_payables'] = forecasted_balance.loc['accountsPayable', 'Forecast Year 1'] - current_bs.loc['accountsPayable']
    cashflow_forecast['Forecast Year 1']['cf_operations'] = cashflow_forecast['Forecast Year 1']['netIncome'] + cashflow_forecast['Forecast Year 1']['inc_depreciation'] - cashflow_forecast['Forecast Year 1']['inc_receivables'] - cashflow_forecast['Forecast Year 1']['inc_inventory'] + cashflow_forecast['Forecast Year 1']['inc_payables']
    cashflow_forecast['Forecast Year 1']['CAPEX'] = forecasted_balance.loc['propertyPlantEquipment', 'Forecast Year 1'] - current_bs.loc['propertyPlantEquipment'] + forecasted_depr['Forecast Year 1']
    cashflow_forecast['Forecast Year 1']['Free Cash Flow'] = cashflow_forecast['Forecast Year 1']['cf_operations'] + cashflow_forecast['Forecast Year 1']['CAPEX']
    
    # Forecast year 2 cash flow 
    cashflow_forecast['Forecast Year 2'] = {}
    cashflow_forecast['Forecast Year 2']['netIncome'] = forecasted_income.loc['netIncome', 'Forecast Year 2']
    cashflow_forecast['Forecast Year 2']['inc_depreciation'] = forecasted_depr['Forecast Year 2'] - forecasted_depr['Forecast Year 1']
    cashflow_forecast['Forecast Year 2']['inc_receivables'] = forecasted_balance.loc['netReceivables', 'Forecast Year 2'] - forecasted_balance.loc['netReceivables', 'Forecast Year 1']
    cashflow_forecast['Forecast Year 2']['inc_inventory'] = forecasted_balance.loc['inventory', 'Forecast Year 2'] - forecasted_balance.loc['inventory', 'Forecast Year 1']
    cashflow_forecast['Forecast Year 2']['inc_payables'] = forecasted_balance.loc['accountsPayable', 'Forecast Year 2'] - forecasted_balance.loc['accountsPayable', 'Forecast Year 1']
    cashflow_forecast['Forecast Year 2']['cf_operations'] = cashflow_forecast['Forecast Year 2']['netIncome'] + cashflow_forecast['Forecast Year 2']['inc_depreciation'] - cashflow_forecast['Forecast Year 2']['inc_receivables'] - cashflow_forecast['Forecast Year 2']['inc_inventory'] + cashflow_forecast['Forecast Year 2']['inc_payables']
    cashflow_forecast['Forecast Year 2']['CAPEX'] = forecasted_balance.loc['propertyPlantEquipment', 'Forecast Year 2'] - forecasted_balance.loc['propertyPlantEquipment', 'Forecast Year 1'] + forecasted_depr['Forecast Year 2']
    cashflow_forecast['Forecast Year 2']['Free Cash Flow'] = cashflow_forecast['Forecast Year 2']['cf_operations'] + cashflow_forecast['Forecast Year 2']['CAPEX']
    
    # Forecast year 3 cash flow 
    cashflow_forecast['Forecast Year 3'] = {}
    cashflow_forecast['Forecast Year 3']['netIncome'] = forecasted_income.loc['netIncome', 'Forecast Year 3']
    cashflow_forecast['Forecast Year 3']['inc_depreciation'] = forecasted_depr['Forecast Year 3'] - forecasted_depr['Forecast Year 2']
    cashflow_forecast['Forecast Year 3']['inc_receivables'] = forecasted_balance.loc['netReceivables', 'Forecast Year 3'] - forecasted_balance.loc['netReceivables', 'Forecast Year 2']
    cashflow_forecast['Forecast Year 3']['inc_inventory'] = forecasted_balance.loc['inventory', 'Forecast Year 3'] - forecasted_balance.loc['inventory', 'Forecast Year 2']
    cashflow_forecast['Forecast Year 3']['inc_payables'] = forecasted_balance.loc['accountsPayable', 'Forecast Year 3'] - forecasted_balance.loc['accountsPayable', 'Forecast Year 2']
    cashflow_forecast['Forecast Year 3']['cf_operations'] = cashflow_forecast['Forecast Year 3']['netIncome'] + cashflow_forecast['Forecast Year 3']['inc_depreciation'] - cashflow_forecast['Forecast Year 3']['inc_receivables'] - cashflow_forecast['Forecast Year 3']['inc_inventory'] + cashflow_forecast['Forecast Year 3']['inc_payables']
    cashflow_forecast['Forecast Year 3']['CAPEX'] = forecasted_balance.loc['propertyPlantEquipment', 'Forecast Year 3'] - forecasted_balance.loc['propertyPlantEquipment', 'Forecast Year 2'] + forecasted_depr['Forecast Year 3']
    cashflow_forecast['Forecast Year 3']['Free Cash Flow'] = cashflow_forecast['Forecast Year 3']['cf_operations'] + cashflow_forecast['Forecast Year 3']['CAPEX']
    
    # Forecast year 4 cash flow 
    cashflow_forecast['Forecast Year 4'] = {}
    cashflow_forecast['Forecast Year 4']['netIncome'] = forecasted_income.loc['netIncome', 'Forecast Year 4']
    cashflow_forecast['Forecast Year 4']['inc_depreciation'] = forecasted_depr['Forecast Year 4'] - forecasted_depr['Forecast Year 3']
    cashflow_forecast['Forecast Year 4']['inc_receivables'] = forecasted_balance.loc['netReceivables', 'Forecast Year 4'] - forecasted_balance.loc['netReceivables', 'Forecast Year 3']
    cashflow_forecast['Forecast Year 4']['inc_inventory'] = forecasted_balance.loc['inventory', 'Forecast Year 4'] - forecasted_balance.loc['inventory', 'Forecast Year 3']
    cashflow_forecast['Forecast Year 4']['inc_payables'] = forecasted_balance.loc['accountsPayable', 'Forecast Year 4'] - forecasted_balance.loc['accountsPayable', 'Forecast Year 3']
    cashflow_forecast['Forecast Year 4']['cf_operations'] = cashflow_forecast['Forecast Year 4']['netIncome'] + cashflow_forecast['Forecast Year 4']['inc_depreciation'] - cashflow_forecast['Forecast Year 4']['inc_receivables'] - cashflow_forecast['Forecast Year 4']['inc_inventory'] + cashflow_forecast['Forecast Year 4']['inc_payables']
    cashflow_forecast['Forecast Year 4']['CAPEX'] = forecasted_balance.loc['propertyPlantEquipment', 'Forecast Year 4'] - forecasted_balance.loc['propertyPlantEquipment', 'Forecast Year 3'] + forecasted_depr['Forecast Year 4']
    cashflow_forecast['Forecast Year 4']['Free Cash Flow'] = cashflow_forecast['Forecast Year 4']['cf_operations'] + cashflow_forecast['Forecast Year 4']['CAPEX']
    
    # Forecast year 5 cash flow 
    cashflow_forecast['Forecast Year 5'] = {}
    cashflow_forecast['Forecast Year 5']['netIncome'] = forecasted_income.loc['netIncome', 'Forecast Year 5']
    cashflow_forecast['Forecast Year 5']['inc_depreciation'] = forecasted_depr['Forecast Year 5'] - forecasted_depr['Forecast Year 4']
    cashflow_forecast['Forecast Year 5']['inc_receivables'] = forecasted_balance.loc['netReceivables', 'Forecast Year 5'] - forecasted_balance.loc['netReceivables', 'Forecast Year 4']
    cashflow_forecast['Forecast Year 5']['inc_inventory'] = forecasted_balance.loc['inventory', 'Forecast Year 5'] - forecasted_balance.loc['inventory', 'Forecast Year 4']
    cashflow_forecast['Forecast Year 5']['inc_payables'] = forecasted_balance.loc['accountsPayable', 'Forecast Year 5'] - forecasted_balance.loc['accountsPayable', 'Forecast Year 4']
    cashflow_forecast['Forecast Year 5']['cf_operations'] = cashflow_forecast['Forecast Year 5']['netIncome'] + cashflow_forecast['Forecast Year 5']['inc_depreciation'] - cashflow_forecast['Forecast Year 5']['inc_receivables'] - cashflow_forecast['Forecast Year 5']['inc_inventory'] + cashflow_forecast['Forecast Year 5']['inc_payables']
    cashflow_forecast['Forecast Year 5']['CAPEX'] = forecasted_balance.loc['propertyPlantEquipment', 'Forecast Year 5'] - forecasted_balance.loc['propertyPlantEquipment', 'Forecast Year 4'] + forecasted_depr['Forecast Year 5']
    cashflow_forecast['Forecast Year 5']['Free Cash Flow'] = cashflow_forecast['Forecast Year 5']['cf_operations'] + cashflow_forecast['Forecast Year 5']['CAPEX']
    
    return cashflow_forecast
