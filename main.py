from functions_new import stock_setup, get_revenue_growth, statement_forecasts, get_wacc


def main():
    
    # gathering ticker from user
    ticker = input("Please enter the ticker symbol exactly how it is on Yahoo Finance: ")
    
    # initiating data scrape
    data = stock_setup(ticker)

    # determining growth rate
    growth = get_revenue_growth(data)
    
    # gathering required forecast data
    required_statements = statement_forecasts(data, growth)

    # determining wacc and related stats, determines intrinsic value
    wacc_stats = get_wacc(required_statements, ticker)
    
    # outputting for user view
    
    print("""
------------------------------------------------------   
DISCOUNTED CASH FLOW MODEL RESULTS FOR {0}            
------------------------------------------------------
                                                      
                                                      
IMPORTANT ASSUMPTIONS                                 
------------------------------------------------------
""".format(ticker))
    i = 1
    for val in growth:
        if len(growth) == 1:
            print("Growth Rate All Years:               {0:.2%}".format(val))
        else:
            print("Growth Rate Year {0}:                  {1:.2%}".format(i, val))
            i += 1

    print("""                                                      
Risk-Free Rate Used:                 {0:.2%}          
Expected Market Return:              {1:.2%}          
Expected Cost of Debt:               {2:.2%}          
Perpetual Growth Rate Assumption:    {3:.2%}          
Tax Rate Used:                       {4:.2%}          
Weighted Average Cost of Capital:    {5:.2%}          
                                                      
                                                      
MARKET VALUES                                         
------------------------------------------------------           
                                                      
Market Value Per Share:             ${6:,.2f}         
Market Capitalization:              ${7:,.2f}         
Enterprise Value:                   ${8:,.2f}         
                                                      
Intrinsic Value Per Share:          ${9:,.2f}
------------------------------------------------------
""".format(wacc_stats[0], wacc_stats[1], wacc_stats[2], wacc_stats[3], wacc_stats[4], wacc_stats[5], wacc_stats[6], wacc_stats[8], wacc_stats[9], wacc_stats[7]))


main()
