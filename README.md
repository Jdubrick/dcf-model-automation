# dcf-model-automation

# Overview
The purpose of this project was to attempt to combine my financial knowledge with my programming knowledge. I wanted to see if I could automate the creation of a DCF model
(discounted cash flow), and along the way I was teaching myself how to use pandas and Numpy.

# Libaries
Pandas, NumPy, Yahoo_Fin 

# Description
The user will enter a ticker symbol exactly as it shows on Yahoo Finance. The program will then ask the user if they would like to input their revenue growth assumptions for the next 5 years (if user entry is no, it will use the previous 3-year growth average). The program then pulls all financial data from Yahoo Finance and forecasts the 3-statements for 5 years, all line items are being forecasted based off of a percentage of revenue. Program then asks the user for their assumptions on the following:

1. Risk-free Rate
2. Expected Market Return
3. Expected Cost of Debt
4. Perpetual Growth Rate

Most of these metrics will be used to calculate the companies cost of equity by using the Capital Asset Pricing Model (CAPM). It will then use the following to compute the Weighted-Average-Cost-of-Capital (WACC) based off the companies D/E ratio. The exit is being determined by the perpetual growth method. 
