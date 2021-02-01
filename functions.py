# Imports

import datetime

import numpy as np
import pandas as pd
import yahoo_fin.stock_info as si


def stock_setup(ticker):
    '''
    Gathers ticker information from user and pulls ticker Income Statement, Balance Sheet and Cash Flow Statement from Yahoo Finance
    '''
    
    income_state = si.get_income_statement(ticker, yearly=True)
    balance_sheet = si.get_balance_sheet(ticker, yearly=True)
    cashflow_state = si.get_cash_flow(ticker, yearly=True)

    financials = [income_state, balance_sheet, cashflow_state]  # less returns, 0=income statement, 1=balance sheet, 2=cashflow statement
    
    return financials  # each item is in its own pandas dataframe 


def get_revenue_growth(financials):
    '''
    Takes income statement as a parameter, function will ask user if they want to input their own revenue assumptions for the 5-year forecast, if not, it will use the average growth from present to 2017
    income statement is financials[0]
    '''

    user_input = input("Would you like to enter your own growth assumptions (Y/N): ")
    revenue_growth = []  # each years revenue growth will be an item in the list
    
    if user_input == 'Y':
        i = 1  # max i value will be 6 because we only want 5 years worth of revenue growth
        while i != 6:
            rev_growth = float(input("Please enter growth assumption for year {} (decimal < 1): ".format(i)))
            revenue_growth.append(rev_growth)
            i += 1
    else:
        rev_growth = 0
        for i in range(3): 
            growth_change = (financials[0].loc['totalRevenue'][i] - financials[0].loc['totalRevenue'][i + 1]) / financials[0].loc['totalRevenue'][i + 1]
            rev_growth += growth_change
        rev_growth /= 3  # 2017 to present is 3 full years worth of data because we are doing the percentage change
        revenue_growth.append(rev_growth)
    
    return revenue_growth


def statement_forecasts(financials, revenue_growth):
    '''
    Creates 3 unique dictionaries, one for each of the major financial statements. Function will split financials parameter into respective current
    year data and then apply the appropriate growth rate to forecast each year. Forecasts will be growth forecasted onto each item as a % of revenue
    '''
    
    # breaking the historic data into only the last full year 
    current_year_inc = financials[0].iloc[0:, 0]
    current_year_bal = financials[1].iloc[0:, 0]
    current_year_cashflow = financials[2].iloc[0:, 0]
    current_year_revenue = current_year_inc['totalRevenue']
    
    # creating dictionaries to hold the % of revenue for each line item
    percent_of_rev_inc_dict = {}
    percent_of_rev_bal_dict = {}
    
    for line, value in current_year_inc.items():  # adding all income statement line items as their % of revenue to the dict
        if line != 'totalRevenue':
            if  value != None:
                percent_of_rev_inc_dict[line] = value / current_year_revenue
            else:
                percent_of_rev_inc_dict[line] = value
                
    for line, value in current_year_bal.items():  # adding all balance sheet line items as their % of revenue to the dict
        if  value != None:
            percent_of_rev_bal_dict[line] = value / current_year_revenue
        else:
            percent_of_rev_bal_dict[line] = value

    # creating forecast dict for year 1 income statement and balance sheet and forecasting all line items based off % of revenue
    y1_inc_forecast = {}
    y1_bal_forecast = {}
    y1_inc_forecast['totalRevenue'] = current_year_inc['totalRevenue'] * (1 + revenue_growth[0])
    
    for line, value in current_year_inc.items():
        if line != 'totalRevenue':
            if value != None:
                y1_inc_forecast[line] = y1_inc_forecast['totalRevenue'] * percent_of_rev_inc_dict[line]
            else:
                y1_inc_forecast[line] = value
    
    for line, value in current_year_bal.items():
        if value != None:
            y1_bal_forecast[line] = y1_inc_forecast['totalRevenue'] * percent_of_rev_bal_dict[line]
        else:
            y1_bal_forecast[line] = value
            
    # creating forecast dict for year 2 income statement and balance sheet and forecasting all line items based off % of revenue
    y2_inc_forecast = {}
    y2_bal_forecast = {}
    
    if len(revenue_growth) > 1:
        y2_inc_forecast['totalRevenue'] = y1_inc_forecast['totalRevenue'] * (1 + revenue_growth[1])
    else:
        y2_inc_forecast['totalRevenue'] = y1_inc_forecast['totalRevenue'] * (1 + revenue_growth[0])
    
    for line, value in current_year_inc.items():
        if line != 'totalRevenue':
            if value != None:
                y2_inc_forecast[line] = y2_inc_forecast['totalRevenue'] * percent_of_rev_inc_dict[line]
            else:
                y2_inc_forecast[line] = value
    
    for line, value in current_year_bal.items():
        if value != None:
            y2_bal_forecast[line] = y2_inc_forecast['totalRevenue'] * percent_of_rev_bal_dict[line]
        else:
            y2_bal_forecast[line] = value
            
    # creating forecast dict for year 3 income statement and balance sheet and forecasting all line items based off % of revenue
    y3_inc_forecast = {}
    y3_bal_forecast = {}
    
    if len(revenue_growth) > 1:
        y3_inc_forecast['totalRevenue'] = y2_inc_forecast['totalRevenue'] * (1 + revenue_growth[2])
    else:
        y3_inc_forecast['totalRevenue'] = y2_inc_forecast['totalRevenue'] * (1 + revenue_growth[0])
    
    for line, value in current_year_inc.items():
        if line != 'totalRevenue':
            if value != None:
                y3_inc_forecast[line] = y3_inc_forecast['totalRevenue'] * percent_of_rev_inc_dict[line]
            else:
                y3_inc_forecast[line] = value
    
    for line, value in current_year_bal.items():
        if value != None:
            y3_bal_forecast[line] = y3_inc_forecast['totalRevenue'] * percent_of_rev_bal_dict[line]
        else:
            y3_bal_forecast[line] = value
            
    # creating forecast dict for year 4 income statement and balance sheet and forecasting all line items based off % of revenue
    y4_inc_forecast = {}
    y4_bal_forecast = {}
    
    if len(revenue_growth) > 1:
        y4_inc_forecast['totalRevenue'] = y3_inc_forecast['totalRevenue'] * (1 + revenue_growth[3])
    else:
        y4_inc_forecast['totalRevenue'] = y3_inc_forecast['totalRevenue'] * (1 + revenue_growth[0])
    
    for line, value in current_year_inc.items():
        if line != 'totalRevenue':
            if value != None:
                y4_inc_forecast[line] = y4_inc_forecast['totalRevenue'] * percent_of_rev_inc_dict[line]
            else:
                y4_inc_forecast[line] = value
    
    for line, value in current_year_bal.items():
        if value != None:
            y4_bal_forecast[line] = y4_inc_forecast['totalRevenue'] * percent_of_rev_bal_dict[line]
        else:
            y4_bal_forecast[line] = value
            
    # creating forecast dict for year 5 income statement and balance sheet and forecasting all line items based off % of revenue
    y5_inc_forecast = {}
    y5_bal_forecast = {}
    
    if len(revenue_growth) > 1:
        y5_inc_forecast['totalRevenue'] = y4_inc_forecast['totalRevenue'] * (1 + revenue_growth[4])
    else:
        y5_inc_forecast['totalRevenue'] = y4_inc_forecast['totalRevenue'] * (1 + revenue_growth[0])
    
    for line, value in current_year_inc.items():
        if line != 'totalRevenue':
            if value != None:
                y5_inc_forecast[line] = y5_inc_forecast['totalRevenue'] * percent_of_rev_inc_dict[line]
            else:
                y5_inc_forecast[line] = value
    
    for line, value in current_year_bal.items():
        if value != None:
            y5_bal_forecast[line] = y5_inc_forecast['totalRevenue'] * percent_of_rev_bal_dict[line]
        else:
            y5_bal_forecast[line] = value
            
    # calculating depreciation
    percent_of_rev_depr = current_year_cashflow.loc['depreciation'] / current_year_inc.loc['totalRevenue']
    
    forecast_depr = {}
    forecast_depr['Current Year'] = current_year_cashflow.loc['depreciation']
    forecast_depr['Forecast Year 1'] = y1_inc_forecast['totalRevenue'] * percent_of_rev_depr
    forecast_depr['Forecast Year 2'] = y2_inc_forecast['totalRevenue'] * percent_of_rev_depr
    forecast_depr['Forecast Year 3'] = y3_inc_forecast['totalRevenue'] * percent_of_rev_depr
    forecast_depr['Forecast Year 4'] = y4_inc_forecast['totalRevenue'] * percent_of_rev_depr
    forecast_depr['Forecast Year 5'] = y5_inc_forecast['totalRevenue'] * percent_of_rev_depr

    # Creating dataframe consisting of all income statement forecast results
    forecast_dataframe_income = pd.DataFrame({'Forecast Year 1': y1_inc_forecast, 'Forecast Year 2': y2_inc_forecast, 'Forecast Year 3': y3_inc_forecast, 'Forecast Year 4': y4_inc_forecast, 'Forecast Year 5': y5_inc_forecast})
    
        # Creating dataframe consisting of all balance sheet forecast results
    forecast_dataframe_balance = pd.DataFrame({'Forecast Year 1': y1_bal_forecast, 'Forecast Year 2': y2_bal_forecast, 'Forecast Year 3': y3_bal_forecast, 'Forecast Year 4': y4_bal_forecast, 'Forecast Year 5': y5_bal_forecast})
    
    # forecasting free cash flow (fcf)
    forecast_cashflow = {}  # some companies do not have inventory lines (e.g. banks)
    
    try:  # trying to do the forecast with inventory included
        # year 1
        forecast_cashflow['Forecast Year 1'] = {}
        forecast_cashflow['Forecast Year 1']['netIncome'] = forecast_dataframe_income.loc['netIncome', 'Forecast Year 1']
        forecast_cashflow['Forecast Year 1']['inc_depreciation'] = forecast_depr['Forecast Year 1'] - forecast_depr['Current Year']
        forecast_cashflow['Forecast Year 1']['inc_receivables'] = forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 1'] - current_year_bal.loc['netReceivables']
        if np.isnan(forecast_dataframe_balance.loc['inventory', 'Forecast Year 1']) == False:
                    forecast_cashflow['Forecast Year 1']['inc_inventory'] = forecast_dataframe_balance.loc['inventory', 'Forecast Year 1'] - current_year_bal.loc['inventory']
        forecast_cashflow['Forecast Year 1']['inc_payables'] = forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 1'] - current_year_bal.loc['accountsPayable']
        forecast_cashflow['Forecast Year 1']['cf_operations'] = forecast_cashflow['Forecast Year 1']['netIncome'] + forecast_cashflow['Forecast Year 1']['inc_depreciation'] - forecast_cashflow['Forecast Year 1']['inc_receivables'] - forecast_cashflow['Forecast Year 1']['inc_inventory'] + forecast_cashflow['Forecast Year 1']['inc_payables']
        forecast_cashflow['Forecast Year 1']['CAPEX'] = forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 1'] - current_year_bal.loc['propertyPlantEquipment'] + forecast_depr['Forecast Year 1']
        forecast_cashflow['Forecast Year 1']['Free Cash Flow'] = forecast_cashflow['Forecast Year 1']['cf_operations'] + forecast_cashflow['Forecast Year 1']['CAPEX']
    
        # year 2
        forecast_cashflow['Forecast Year 2'] = {}
        forecast_cashflow['Forecast Year 2']['netIncome'] = forecast_dataframe_income.loc['netIncome', 'Forecast Year 2']
        forecast_cashflow['Forecast Year 2']['inc_depreciation'] = forecast_depr['Forecast Year 2'] - forecast_depr['Forecast Year 1']
        forecast_cashflow['Forecast Year 2']['inc_receivables'] = forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 2'] - forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 1']
        if np.isnan(forecast_dataframe_balance.loc['inventory', 'Forecast Year 1']) == False:
            forecast_cashflow['Forecast Year 2']['inc_inventory'] = forecast_dataframe_balance.loc['inventory', 'Forecast Year 2'] - forecast_dataframe_balance.loc['inventory', 'Forecast Year 1']
        forecast_cashflow['Forecast Year 2']['inc_payables'] = forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 2'] - forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 1']
        forecast_cashflow['Forecast Year 2']['cf_operations'] = forecast_cashflow['Forecast Year 2']['netIncome'] + forecast_cashflow['Forecast Year 2']['inc_depreciation'] - forecast_cashflow['Forecast Year 2']['inc_receivables'] - forecast_cashflow['Forecast Year 2']['inc_inventory'] + forecast_cashflow['Forecast Year 2']['inc_payables']
        forecast_cashflow['Forecast Year 2']['CAPEX'] = forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 2'] - forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 1'] + forecast_depr['Forecast Year 2']
        forecast_cashflow['Forecast Year 2']['Free Cash Flow'] = forecast_cashflow['Forecast Year 2']['cf_operations'] + forecast_cashflow['Forecast Year 2']['CAPEX']
    
        # year 3
        forecast_cashflow['Forecast Year 3'] = {}
        forecast_cashflow['Forecast Year 3']['netIncome'] = forecast_dataframe_income.loc['netIncome', 'Forecast Year 3']
        forecast_cashflow['Forecast Year 3']['inc_depreciation'] = forecast_depr['Forecast Year 3'] - forecast_depr['Forecast Year 2']
        forecast_cashflow['Forecast Year 3']['inc_receivables'] = forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 3'] - forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 2']
        if np.isnan(forecast_dataframe_balance.loc['inventory', 'Forecast Year 1']) == False:
            forecast_cashflow['Forecast Year 3']['inc_inventory'] = forecast_dataframe_balance.loc['inventory', 'Forecast Year 3'] - forecast_dataframe_balance.loc['inventory', 'Forecast Year 2']
        forecast_cashflow['Forecast Year 3']['inc_payables'] = forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 3'] - forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 2']
        forecast_cashflow['Forecast Year 3']['cf_operations'] = forecast_cashflow['Forecast Year 3']['netIncome'] + forecast_cashflow['Forecast Year 3']['inc_depreciation'] - forecast_cashflow['Forecast Year 3']['inc_receivables'] - forecast_cashflow['Forecast Year 3']['inc_inventory'] + forecast_cashflow['Forecast Year 3']['inc_payables']
        forecast_cashflow['Forecast Year 3']['CAPEX'] = forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 3'] - forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 2'] + forecast_depr['Forecast Year 3']
        forecast_cashflow['Forecast Year 3']['Free Cash Flow'] = forecast_cashflow['Forecast Year 3']['cf_operations'] + forecast_cashflow['Forecast Year 3']['CAPEX']
    
        # year 4 
        forecast_cashflow['Forecast Year 4'] = {}
        forecast_cashflow['Forecast Year 4']['netIncome'] = forecast_dataframe_income.loc['netIncome', 'Forecast Year 4']
        forecast_cashflow['Forecast Year 4']['inc_depreciation'] = forecast_depr['Forecast Year 4'] - forecast_depr['Forecast Year 3']
        forecast_cashflow['Forecast Year 4']['inc_receivables'] = forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 4'] - forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 3']
        if np.isnan(forecast_dataframe_balance.loc['inventory', 'Forecast Year 1']) == False:
            forecast_cashflow['Forecast Year 4']['inc_inventory'] = forecast_dataframe_balance.loc['inventory', 'Forecast Year 4'] - forecast_dataframe_balance.loc['inventory', 'Forecast Year 3']
        forecast_cashflow['Forecast Year 4']['inc_payables'] = forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 4'] - forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 3']
        forecast_cashflow['Forecast Year 4']['cf_operations'] = forecast_cashflow['Forecast Year 4']['netIncome'] + forecast_cashflow['Forecast Year 4']['inc_depreciation'] - forecast_cashflow['Forecast Year 4']['inc_receivables'] - forecast_cashflow['Forecast Year 4']['inc_inventory'] + forecast_cashflow['Forecast Year 4']['inc_payables']
        forecast_cashflow['Forecast Year 4']['CAPEX'] = forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 4'] - forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 3'] + forecast_depr['Forecast Year 4']
        forecast_cashflow['Forecast Year 4']['Free Cash Flow'] = forecast_cashflow['Forecast Year 4']['cf_operations'] + forecast_cashflow['Forecast Year 4']['CAPEX']
    
        # year 5 
        forecast_cashflow['Forecast Year 5'] = {}
        forecast_cashflow['Forecast Year 5']['netIncome'] = forecast_dataframe_income.loc['netIncome', 'Forecast Year 5']
        forecast_cashflow['Forecast Year 5']['inc_depreciation'] = forecast_depr['Forecast Year 5'] - forecast_depr['Forecast Year 4']
        forecast_cashflow['Forecast Year 5']['inc_receivables'] = forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 5'] - forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 4']
        if np.isnan(forecast_dataframe_balance.loc['inventory', 'Forecast Year 1']) == False:
            forecast_cashflow['Forecast Year 5']['inc_inventory'] = forecast_dataframe_balance.loc['inventory', 'Forecast Year 5'] - forecast_dataframe_balance.loc['inventory', 'Forecast Year 4']
        forecast_cashflow['Forecast Year 5']['inc_payables'] = forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 5'] - forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 4']
        forecast_cashflow['Forecast Year 5']['cf_operations'] = forecast_cashflow['Forecast Year 5']['netIncome'] + forecast_cashflow['Forecast Year 5']['inc_depreciation'] - forecast_cashflow['Forecast Year 5']['inc_receivables'] - forecast_cashflow['Forecast Year 5']['inc_inventory'] + forecast_cashflow['Forecast Year 5']['inc_payables']
        forecast_cashflow['Forecast Year 5']['CAPEX'] = forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 5'] - forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 4'] + forecast_depr['Forecast Year 5']
        forecast_cashflow['Forecast Year 5']['Free Cash Flow'] = forecast_cashflow['Forecast Year 5']['cf_operations'] + forecast_cashflow['Forecast Year 5']['CAPEX']
    
    except KeyError:  # if inventory was not found it will run this code
        # year 1
        forecast_cashflow['Forecast Year 1'] = {}
        forecast_cashflow['Forecast Year 1']['netIncome'] = forecast_dataframe_income.loc['netIncome', 'Forecast Year 1']
        forecast_cashflow['Forecast Year 1']['inc_depreciation'] = forecast_depr['Forecast Year 1'] - forecast_depr['Current Year']
        forecast_cashflow['Forecast Year 1']['inc_receivables'] = forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 1'] - current_year_bal.loc['netReceivables']
        forecast_cashflow['Forecast Year 1']['inc_payables'] = forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 1'] - current_year_bal.loc['accountsPayable']
        forecast_cashflow['Forecast Year 1']['cf_operations'] = forecast_cashflow['Forecast Year 1']['netIncome'] + forecast_cashflow['Forecast Year 1']['inc_depreciation'] - forecast_cashflow['Forecast Year 1']['inc_receivables'] + forecast_cashflow['Forecast Year 1']['inc_payables']
        forecast_cashflow['Forecast Year 1']['CAPEX'] = forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 1'] - current_year_bal.loc['propertyPlantEquipment'] + forecast_depr['Forecast Year 1']
        forecast_cashflow['Forecast Year 1']['Free Cash Flow'] = forecast_cashflow['Forecast Year 1']['cf_operations'] + forecast_cashflow['Forecast Year 1']['CAPEX']
    
        # year 2
        forecast_cashflow['Forecast Year 2'] = {}
        forecast_cashflow['Forecast Year 2']['netIncome'] = forecast_dataframe_income.loc['netIncome', 'Forecast Year 2']
        forecast_cashflow['Forecast Year 2']['inc_depreciation'] = forecast_depr['Forecast Year 2'] - forecast_depr['Forecast Year 1']
        forecast_cashflow['Forecast Year 2']['inc_receivables'] = forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 2'] - forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 1']
        forecast_cashflow['Forecast Year 2']['inc_payables'] = forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 2'] - forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 1']
        forecast_cashflow['Forecast Year 2']['cf_operations'] = forecast_cashflow['Forecast Year 2']['netIncome'] + forecast_cashflow['Forecast Year 2']['inc_depreciation'] - forecast_cashflow['Forecast Year 2']['inc_receivables'] + forecast_cashflow['Forecast Year 2']['inc_payables']
        forecast_cashflow['Forecast Year 2']['CAPEX'] = forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 2'] - forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 1'] + forecast_depr['Forecast Year 2']
        forecast_cashflow['Forecast Year 2']['Free Cash Flow'] = forecast_cashflow['Forecast Year 2']['cf_operations'] + forecast_cashflow['Forecast Year 2']['CAPEX']
    
        # year 3
        forecast_cashflow['Forecast Year 3'] = {}
        forecast_cashflow['Forecast Year 3']['netIncome'] = forecast_dataframe_income.loc['netIncome', 'Forecast Year 3']
        forecast_cashflow['Forecast Year 3']['inc_depreciation'] = forecast_depr['Forecast Year 3'] - forecast_depr['Forecast Year 2']
        forecast_cashflow['Forecast Year 3']['inc_receivables'] = forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 3'] - forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 2']
        forecast_cashflow['Forecast Year 3']['inc_payables'] = forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 3'] - forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 2']
        forecast_cashflow['Forecast Year 3']['cf_operations'] = forecast_cashflow['Forecast Year 3']['netIncome'] + forecast_cashflow['Forecast Year 3']['inc_depreciation'] - forecast_cashflow['Forecast Year 3']['inc_receivables'] + forecast_cashflow['Forecast Year 3']['inc_payables']
        forecast_cashflow['Forecast Year 3']['CAPEX'] = forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 3'] - forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 2'] + forecast_depr['Forecast Year 3']
        forecast_cashflow['Forecast Year 3']['Free Cash Flow'] = forecast_cashflow['Forecast Year 3']['cf_operations'] + forecast_cashflow['Forecast Year 3']['CAPEX']
    
        # year 4 
        forecast_cashflow['Forecast Year 4'] = {}
        forecast_cashflow['Forecast Year 4']['netIncome'] = forecast_dataframe_income.loc['netIncome', 'Forecast Year 4']
        forecast_cashflow['Forecast Year 4']['inc_depreciation'] = forecast_depr['Forecast Year 4'] - forecast_depr['Forecast Year 3']
        forecast_cashflow['Forecast Year 4']['inc_receivables'] = forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 4'] - forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 3']
        forecast_cashflow['Forecast Year 4']['inc_payables'] = forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 4'] - forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 3']
        forecast_cashflow['Forecast Year 4']['cf_operations'] = forecast_cashflow['Forecast Year 4']['netIncome'] + forecast_cashflow['Forecast Year 4']['inc_depreciation'] - forecast_cashflow['Forecast Year 4']['inc_receivables'] + forecast_cashflow['Forecast Year 4']['inc_payables']
        forecast_cashflow['Forecast Year 4']['CAPEX'] = forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 4'] - forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 3'] + forecast_depr['Forecast Year 4']
        forecast_cashflow['Forecast Year 4']['Free Cash Flow'] = forecast_cashflow['Forecast Year 4']['cf_operations'] + forecast_cashflow['Forecast Year 4']['CAPEX']
    
        # year 5 
        forecast_cashflow['Forecast Year 5'] = {}
        forecast_cashflow['Forecast Year 5']['netIncome'] = forecast_dataframe_income.loc['netIncome', 'Forecast Year 5']
        forecast_cashflow['Forecast Year 5']['inc_depreciation'] = forecast_depr['Forecast Year 5'] - forecast_depr['Forecast Year 4']
        forecast_cashflow['Forecast Year 5']['inc_receivables'] = forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 5'] - forecast_dataframe_balance.loc['netReceivables', 'Forecast Year 4']
        forecast_cashflow['Forecast Year 5']['inc_payables'] = forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 5'] - forecast_dataframe_balance.loc['accountsPayable', 'Forecast Year 4']
        forecast_cashflow['Forecast Year 5']['cf_operations'] = forecast_cashflow['Forecast Year 5']['netIncome'] + forecast_cashflow['Forecast Year 5']['inc_depreciation'] - forecast_cashflow['Forecast Year 5']['inc_receivables'] + forecast_cashflow['Forecast Year 5']['inc_payables']
        forecast_cashflow['Forecast Year 5']['CAPEX'] = forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 5'] - forecast_dataframe_balance.loc['propertyPlantEquipment', 'Forecast Year 4'] + forecast_depr['Forecast Year 5']
        forecast_cashflow['Forecast Year 5']['Free Cash Flow'] = forecast_cashflow['Forecast Year 5']['cf_operations'] + forecast_cashflow['Forecast Year 5']['CAPEX']
    
    forecast_dataframe_cashflow = pd.DataFrame.from_dict(forecast_cashflow, orient='columns')
    pd.options.display.float_format = '{:,.2f}'.format
    
    req_statements = [current_year_inc, current_year_bal, current_year_cashflow, forecast_depr, forecast_dataframe_income, forecast_dataframe_balance, forecast_dataframe_cashflow]
    
    return req_statements


def get_wacc(req_statements, ticker):
    ''' 
    Gathers stock info (beta, current price, shares outstanding) and uses forecast dataframes to generate weighted average cost of capital (WACC), and then computes intrinsic value of stock
    '''

    # grabbing required security data to use CAPM, and grabs current price
    ticker_call = si.get_quote_table(ticker)
    ticker_beta = ticker_call['Beta (5Y Monthly)']
    ticker_price = ticker_call['Previous Close']
    ticker_stats = si.get_stats(ticker)
    ticker_shares = ticker_stats.iloc[18].values[-1]
    
    # converting shares outstanding value to full value (unabbreviated)
    if ticker_shares[-1] == 'T':
        temp = float(ticker_shares[:-1])
        ticker_shares = temp * 1000000000000
    elif ticker_shares[-1] == 'B':
        temp = float(ticker_shares[:-1])
        ticker_shares = temp * 1000000000
    elif ticker_shares[-1] == 'M':
        temp = float(ticker_shares[:-1])
        ticker_shares = temp * 1000000
    elif ticker_shares[-1] == 'k':
        temp = float(ticker_shares[:-1])
        ticker_shares = temp * 1000
    
    # User input assumptions required to compute WACC and terminal value
    risk_free = float(input("Enter your risk-free debt assumption(decimal): "))
    exp_mkt_return = float(input("Enter your expected market return assumption(decimal): "))
    exp_kd = float(input("Enter your cost of debt assumption: "))
    perp_growth = float(input("Enter your perpetual growth rate assumption: "))
    
    # Calculating tax rate (if company had less than a 0% tax rate in the most recent year, then it will default to 30%
    tax_rate = req_statements[0]['incomeTaxExpense'] / req_statements[0]['incomeBeforeTax']
    if tax_rate < 0:
        tax_rate = 0.30
    
    # calculating net debt
    debt_values = {}  # row(index) name will be key, value is value
    paydown_values = {}  # items such as short term investments and cash, that will be used to get net debt
    for name, value in req_statements[1].items():
        if name == 'shortLongTermDebt' and np.isnan(req_statements[1]['shortLongTermDebt']) == False:
            debt_values[name] = value
        elif name == 'longTermDebt' and np.isnan(req_statements[1]['longTermDebt']) == False:
            debt_values[name] = value
        elif name == 'cash' and np.isnan(req_statements[1]['cash']) == False:
            paydown_values[name] = value
        elif name == 'shortTermInvestments' and np.isnan(req_statements[1]['shortTermInvestments']) == False:
            paydown_values[name] = value
        
    net_debt = 0  # setting value to 0 so we can iterate through both required dictionaries and add/sub
    total_debt = 0  # total debt consists of only debt items
    for value in debt_values.values():
        net_debt += value
        total_debt += value
        
    for value in paydown_values.values():
        net_debt -= value
       
    # current market value 
    mkt_cap = ticker_call['Market Cap']
    
    # converting market cap to full value (unabbreviated)
    if mkt_cap[-1] == 'T':
        temp = float(mkt_cap[:-1])
        mkt_cap = temp * 1000000000000
    elif mkt_cap[-1] == 'B':
        temp = float(mkt_cap[:-1])
        mkt_cap = temp * 1000000000
    elif mkt_cap[-1] == 'M':
        temp = float(mkt_cap[:-1])
        mkt_cap = temp * 1000000
    elif mkt_cap[-1] == 'k':
        temp = float(mkt_cap[:-1])
        mkt_cap = temp * 1000
    
    mkt_enterprise = mkt_cap + net_debt
    mkt_val_share = ticker_price
    
    # calculating capital structure
    debt_to_cap = total_debt / (total_debt + mkt_cap)
    equity_to_cap = mkt_cap / (total_debt + mkt_cap)
    
    # calculating discount rate (WACC)
    cost_of_equity = risk_free + (ticker_beta * (exp_mkt_return - risk_free))
    cost_of_debt = exp_kd * (1 - tax_rate)
    wacc = (cost_of_debt * debt_to_cap) + (cost_of_equity * equity_to_cap)

    # determining terminal value
    term_value = req_statements[-1].iloc[-1, -1] * (1 + perp_growth) / (wacc - perp_growth)
    
    # determining NPV of FCF
    fcf_list = req_statements[-1].iloc[-1].values.tolist()
    fcf_list.append(term_value)
    net_present_value = np.npv(wacc, fcf_list)
    
    # Calculating Intrinsic Value
    ins_equity_value = net_present_value - net_debt
    ins_val_share = ins_equity_value / ticker_shares

    wacc_stats = [risk_free, exp_mkt_return, exp_kd, perp_growth, tax_rate, wacc, mkt_val_share, ins_val_share, mkt_cap, mkt_enterprise, mkt_val_share, net_debt]
    
    return wacc_stats
