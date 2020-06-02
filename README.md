# InsiderTrades Webscraper and Plotting

Summary:
With this script, you can download all insider trade from the SIX Stock exchange. 
In the iPython file, you find how to read in the insider trades for a spefic company and plot its stocks performance against it.
Find below the companies with most insider trades within the last year and 3 examples of the outcome.

## This is how the script is set-up:

### Imports
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```


# Load Insider Trades
```python
insider = pd.read_csv("InsiderTrades_20200531-183230.csv")
```


# Fix date
```python
insider['DATUM'] = pd.to_datetime(insider['DATUM'], format='%d.%m.%Y')
insider = insider.set_index('DATUM')
insider.head()
```

# Show most common companies
```python
insider_most = insider.groupby('EMITTENT').count().reset_index()
insider_most.sort_values('WERT', ascending=False).head(15)
```

|EMITTENT|	WERT|
| ------------- |:-------------:|
|Alpine Select AG	|172|
|nebag ag	|99|
|AEVIS VICTORIA SA	|89|
|Chocoladefabriken Lindt & Sprüngli AG	|61|
|EFG International	|50|
|VZ Holding AG	|44|
|dormakaba Holding AG	|43|
|KTM Industries AG	|42|
|Logitech International S.A.	|42|
|SGS SA	|39|
|Edisun Power Europe AG	|38|
|Roche Holding AG	|37|
|HIAG Immobilien Holding AG	|35|
|Schindler Holding AG	|35|
|Kühne + Nagel International AG	|34|


# Lookup files available
```python
import os
os.listdir("./data/") # returns list
```

# This is the only field, where you have to make modifications
You have to specify, which .csv file corresponds with company you choose to display the insider trades with. 
In our case, there is a .csv file available for Roche (ROG.SW_2020-06-01.csv). We later define the stock name as well (matches entry from the most common companies with insider trades (see above).

# Load Stock Data
```python
stock = pd.read_csv('./data/ROG.SW_2020-06-01.csv')

# Define name of stock (multiple use)
stock_name = 'Roche Holding AG'

#stock.head()
# Fix Date and index
stock['Date'] = pd.to_datetime(stock['Date'], format='%Y-%m-%d')
stock = stock.set_index('Date')
stock.head()
```

# Process data
```python
stock1 = stock["Adj Close"]
stock2 = insider[(insider['EMITTENT'] == stock_name) & (insider['TYP']=='Erwerb')]['WERT']
stock3 = insider[(insider['EMITTENT'] == stock_name) & (insider['TYP']=='Veräusserung')]['WERT']
stock3.head()

merged_df = pd.concat(frames, axis=1)
merged_df.head()
```

# Merge the the dataframes
```python
merged_df['SELLS'] = merged_df['WERT']
merged_df = merged_df.drop(['WERT'], axis=1)

frames2 =  [merged_df, stock3]
merged_df = pd.concat(frames2, axis=1)
merged_df['BUYS'] = merged_df['WERT']
merged_df = merged_df.drop(['WERT'],  axis=1)
merged_df
```

# Plot the result
```python
%matplotlib inline
# Control the default size of figures in this Jupyter notebook
%pylab inline
pylab.rcParams['figure.figsize'] = (15, 9)   # Change the size of plots

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Time window')
ax1.set_ylabel('Stock Price', color=color)
ax1.plot(merged_df['Adj Close'].index, merged_df['Adj Close'], color=color, 
         label=("Stock Price of "+stock_name))
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:green'
ax2.set_ylabel('Insider Trades', color=color)  # we already handled the x-label with ax1
ax2.bar(merged_df['Adj Close'].index, merged_df['BUYS'], color=color, label="Insider Buys")
ax2.tick_params(axis='y', labelcolor=color)

color = 'tab:red'
#ax2.set_ylabel('sin2', color=color)  # we already handled the x-label with ax1
ax2.bar(merged_df['Adj Close'].index, merged_df['SELLS'], color=color, label="Insider Sells")
ax2.tick_params(axis='y', labelcolor=color)
plt.legend()
plt.title(stock_name+" Stock Performance with Insider Trades")
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
```


Fig. 2: Stock performance of KTM Industries vs. Insider Trades
<p align="center">
  <img src="KTM.png" width="100%" title="Broken Container">
</p>


<p>
Fig. 2: Stock performance of KTM vs. Insider Trades
<p align="center">
  <img src="Logitech.png" width="100%" title="Broken Container">
</p>

<p>
Fig. 3: Stock performance of KTM vs. Insider Trades
<p align="center">
  <img src="Roche.png" width="100%" title="Broken Container">
</p>

