# market-break

> a set of utilities for backtesting vectorized trading algorithms, high-frequency trading strategies and investing strategies.

## Installation
_______

````
pip install python-market-break
````

Connect to a live database for real-time data.

```python
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database/2024-06-14.sqlite')
```

Extract The data from the database into a DataFrame.

```python
from cryptocore.market.database import extract_dataframe, table_name

EXCHANGE = "binance"
SYMBOL = "ETH/USDT"

df = extract_dataframe(engine, table_name(exchange=EXCHANGE, symbol=SYMBOL))
df = df.iloc[3500:7000].reset_index()
```


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>exchange</th>
      <th>symbol</th>
      <th>timestamp</th>
      <th>datetime</th>
      <th>received_datetime</th>
      <th>open</th>
      <th>high</th>
      <th>low</th>
      <th>close</th>
      <th>bid</th>
      <th>ask</th>
      <th>bid_volume</th>
      <th>ask_volume</th>
      <th>side</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3500</td>
      <td>binance</td>
      <td>ETH/USDT</td>
      <td>1.718353e+12</td>
      <td>2024-06-14 11:19:38.208</td>
      <td>2024-06-14 08:19:38.156</td>
      <td>3510.78</td>
      <td>3539.83</td>
      <td>3428.0</td>
      <td>3521.99</td>
      <td>3521.98</td>
      <td>3521.99</td>
      <td>59.7590</td>
      <td>21.0623</td>
      <td>buy</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3501</td>
      <td>binance</td>
      <td>ETH/USDT</td>
      <td>1.718353e+12</td>
      <td>2024-06-14 11:19:39.031</td>
      <td>2024-06-14 08:19:39.155</td>
      <td>3510.78</td>
      <td>3539.83</td>
      <td>3428.0</td>
      <td>3521.98</td>
      <td>3521.98</td>
      <td>3521.99</td>
      <td>58.2914</td>
      <td>28.2213</td>
      <td>sell</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3502</td>
      <td>binance</td>
      <td>ETH/USDT</td>
      <td>1.718353e+12</td>
      <td>2024-06-14 11:19:39.857</td>
      <td>2024-06-14 08:19:40.158</td>
      <td>3510.78</td>
      <td>3539.83</td>
      <td>3428.0</td>
      <td>3521.99</td>
      <td>3521.98</td>
      <td>3521.99</td>
      <td>58.2418</td>
      <td>24.8653</td>
      <td>buy</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3503</td>
      <td>binance</td>
      <td>ETH/USDT</td>
      <td>1.718353e+12</td>
      <td>2024-06-14 11:19:40.574</td>
      <td>2024-06-14 08:19:41.179</td>
      <td>3510.78</td>
      <td>3539.83</td>
      <td>3428.0</td>
      <td>3521.99</td>
      <td>3521.98</td>
      <td>3521.99</td>
      <td>63.9093</td>
      <td>24.8653</td>
      <td>buy</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3504</td>
      <td>binance</td>
      <td>ETH/USDT</td>
      <td>1.718353e+12</td>
      <td>2024-06-14 11:19:42.080</td>
      <td>2024-06-14 08:19:42.161</td>
      <td>3510.78</td>
      <td>3539.83</td>
      <td>3428.0</td>
      <td>3521.99</td>
      <td>3521.98</td>
      <td>3521.99</td>
      <td>64.6069</td>
      <td>14.6805</td>
      <td>buy</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>3495</th>
      <td>6995</td>
      <td>binance</td>
      <td>ETH/USDT</td>
      <td>1.718357e+12</td>
      <td>2024-06-14 12:17:55.995</td>
      <td>2024-06-14 09:17:55.971</td>
      <td>3493.19</td>
      <td>3539.83</td>
      <td>3428.0</td>
      <td>3518.19</td>
      <td>3518.19</td>
      <td>3518.20</td>
      <td>125.1496</td>
      <td>5.5759</td>
      <td>sell</td>
    </tr>
    <tr>
      <th>3496</th>
      <td>6996</td>
      <td>binance</td>
      <td>ETH/USDT</td>
      <td>1.718357e+12</td>
      <td>2024-06-14 12:17:56.069</td>
      <td>2024-06-14 09:17:56.976</td>
      <td>3493.19</td>
      <td>3539.83</td>
      <td>3428.0</td>
      <td>3518.20</td>
      <td>3518.19</td>
      <td>3518.20</td>
      <td>125.1496</td>
      <td>5.5728</td>
      <td>buy</td>
    </tr>
    <tr>
      <th>3497</th>
      <td>6997</td>
      <td>binance</td>
      <td>ETH/USDT</td>
      <td>1.718357e+12</td>
      <td>2024-06-14 12:17:57.779</td>
      <td>2024-06-14 09:17:58.075</td>
      <td>3492.59</td>
      <td>3539.83</td>
      <td>3428.0</td>
      <td>3518.20</td>
      <td>3518.19</td>
      <td>3518.20</td>
      <td>121.2325</td>
      <td>7.5728</td>
      <td>buy</td>
    </tr>
    <tr>
      <th>3498</th>
      <td>6998</td>
      <td>binance</td>
      <td>ETH/USDT</td>
      <td>1.718357e+12</td>
      <td>2024-06-14 12:17:58.886</td>
      <td>2024-06-14 09:17:58.973</td>
      <td>3492.59</td>
      <td>3539.83</td>
      <td>3428.0</td>
      <td>3518.20</td>
      <td>3518.19</td>
      <td>3518.20</td>
      <td>83.2826</td>
      <td>7.7234</td>
      <td>buy</td>
    </tr>
    <tr>
      <th>3499</th>
      <td>6999</td>
      <td>binance</td>
      <td>ETH/USDT</td>
      <td>1.718357e+12</td>
      <td>2024-06-14 12:18:00.028</td>
      <td>2024-06-14 09:17:59.973</td>
      <td>3492.60</td>
      <td>3539.83</td>
      <td>3428.0</td>
      <td>3518.20</td>
      <td>3518.19</td>
      <td>3518.20</td>
      <td>75.6586</td>
      <td>9.3705</td>
      <td>buy</td>
    </tr>
  </tbody>
</table>
<p>3500 rows × 15 columns</p>
</div>


Import column names to handle the data.

```python
from market_break.labels import BID, ASK, DATETIME, ENTRY, EXIT, TYPE, LONG
```

Import a class of backtesting functions.

```python
from market_break.backtest import Trades
```

Generate trades record, both short and long as a DataFrame, from definition of up-trends and down-trends.

```python
trades = Trades.generate(
    up=df[ASK] > df[ASK].shift(1),
    down=df[BID] < df[BID].shift(1),
    adjust=True
)
```

Process the results of the generated trades.

```python
FEE = 0.001

returns = Trades.returns(trades, bid=df[BID], ask=df[ASK], fee=FEE)
```

Imports a class of Plotting trading results.

```python
from market_break.backtest import Plot
```

Plot a histogram of the trades returns.

```python
Plot.returns_histogram(returns, bins=35)
```



![png](media/output_8_0.png)


Plot a graph of the trades returns.

```python
Plot.returns_signals(returns, index=df[DATETIME].iloc)
```



![png](media/output_9_0.png)


Plot pie graphs of the winning and losing trades and their profits and losses.

```python
Plot.returns_pie(returns)
```



![png](media/output_10_0.png)


Plot the signals for long and short entries and exits, with the bid-ask spread.
Also plotting The balance, profits and losses.

```python
long_trades = trades[trades[TYPE] == LONG]

Plot.price_signals(
    bid=df[BID], ask=df[ASK], index=df[DATETIME].iloc,
    long=long_trades[ENTRY], short=long_trades[EXIT]
)
Plot.returns_balance(returns, index=df[DATETIME].iloc)
```



![png](media/output_11_0.png)





![png](media/output_11_1.png)


Import a class for generating a report from the results.

```python
from market_break.backtest import Report
```

Generating and displaying the results with the report.

```python
report = Report.generate(
    index=df[DATETIME], returns=returns, 
    long=trades[EXIT].values, short=trades[EXIT].values
)

print(Report.repr(report))
```

    [Index]
    start                   2024-06-14 11:19:38.20
    end                     2024-06-14 12:18:00.02
    total duration              0 days 00:58:21.82
    min. tick duration                  0:00:00.06
    max. tick duration                  0:00:01.90
    avg. tick duration                  0:00:01.00
    ticks                                     3500
    
    [Trades]
    long trades                                125
    short trades                               125
    min. TUW                                   0:0
    max. TUW                                   0:0
    avg. TUW                                   0:0
    
    [Gains]
    [%] min. gain                           0.0003
    [%] max. gain                           0.1482
    [%] avg. gain                           0.0291
    [%] total gains                         2.4411
    winning trades                              84
    
    [Losses]
    [%] min. loss                          -0.0003
    [%] max. loss                           -0.017
    [%] avg. loss                          -0.0063
    [%] total losses                       -0.2383
    losing trades                               38
    
    [Performance]
    PnL factor                              10.245
    avg. profit factor                      1.0002
    [%] win rate                              67.2
    [%] total profit                        2.2029
    
