# `pyqmt` 库函数使用示例

本文档提供了 `pyqmt` 库中各个函数的详细使用示例，包括功能、参数、返回值和调用示例。

## `导入库`

### 调用示例

```python
# 假设 qmt 实例已创建
from pyqmt import pyqmt 
```


## `__init__`

### 调用示例

```python
# 假设 qmt 实例已创建
qmt = pyqmt(path="D:\\国金QMT交易端模拟\\userdata_mini", acc='39972702')
qmt._connect()
```


## `query_stock_asset`

### 功能
查询股票账户的资产信息，包括总资产、可用资金等。

### 参数说明
无。

### 返回内容
DataFrame: 包含资产信息的 Pandas DataFrame。

### 调用示例

```python
# 假设 qmt 实例已连接
asset_info = qmt.query_stock_asset()
print("股票资产信息:\n", asset_info)
```

## `get_available_fund`

### 功能
获取股票账户的可用资金。

### 参数说明
无。

### 返回内容
float: 可用资金金额。

### 调用示例

```python
# 假设 qmt 实例已连接
available_fund = qmt.get_available_fund()
print(f"可用资金: {available_fund}")
```

## `get_available_pos`

### 功能
获取指定股票代码的可用持仓数量。

### 参数说明
- symbol (str): 股票代码，例如 '600000.SH'。

### 返回内容
int: 可用持仓数量。

### 调用示例

```python
# 假设 qmt 实例已连接
symbol = '600000.SH'
available_pos = qmt.get_available_pos(symbol)
print(f"{symbol} 可用持仓: {available_pos}")
```

## `query_stock_orders`

### 功能
查询股票账户的委托订单信息。

### 参数说明
- query_all (bool, optional): 是否查询所有历史订单，默认为 False (只查询当日订单)。

### 返回内容
DataFrame: 包含委托订单信息的 Pandas DataFrame。

### 调用示例

```python
# 假设 qmt 实例已连接
# 查询当日委托
daily_orders = qmt.query_stock_orders()
print("当日委托订单:\n", daily_orders)

# 查询所有历史委托
# all_orders = qmt.query_stock_orders(query_all=True)
# print("所有历史委托订单:\n", all_orders)
```

## `query_stock_trades`

### 功能
查询股票账户的成交信息。

### 参数说明
无。

### 返回内容
DataFrame: 包含成交信息的 Pandas DataFrame。

### 调用示例

```python
# 假设 qmt 实例已连接
trades = qmt.query_stock_trades()
print("股票成交信息:\n", trades)
```

## `query_stock_positions`

### 功能
查询股票账户的持仓信息。

### 参数说明
无。

### 返回内容
DataFrame: 包含持仓信息的 Pandas DataFrame。

### 调用示例

```python
# 假设 qmt 实例已连接
positions = qmt.query_stock_positions()
print("股票持仓信息:\n", positions)
```

## `_get_board`

### 功能
根据股票代码获取其所属的板块信息（例如：沪市A股、深市A股）。这是一个内部辅助函数。

### 参数说明
- symbol (str): 股票代码。

### 返回内容
str: 股票所属的板块字符串。

### 调用示例

```python
# 这是一个内部函数，通常不直接调用。示例仅作说明。
# board = qmt._get_board('600000.SH')
# print(f"600000.SH 所属板块: {board}")
```

## `_check_price_cage`

### 功能
检查委托价格是否在股票的涨跌停限制范围内。这是一个内部辅助函数。

### 参数说明
- symbol (str): 股票代码。
- price (float): 委托价格。

### 返回内容
bool: 如果价格在涨跌停范围内则返回 True，否则返回 False。

### 调用示例

```python
# 这是一个内部函数，通常不直接调用。示例仅作说明。
# is_valid = qmt._check_price_cage('600000.SH', 10.50)
# print(f"价格 10.50 是否在涨跌停范围内: {is_valid}")
```

## `_calculate_commission`

### 功能
计算交易佣金。这是一个内部辅助函数。

### 参数说明
- symbol (str): 股票代码。
- price (float): 成交价格。
- volume (int): 成交数量。
- trade_type (str): 交易类型 ('buy' 或 'sell')。

### 返回内容
float: 计算出的佣金金额。

### 调用示例

```python
# 这是一个内部函数，通常不直接调用。示例仅作说明。
# commission = qmt._calculate_commission('600000.SH', 10.0, 100, 'buy')
# print(f"计算佣金: {commission}")
```

## `get_last_price`

### 功能
获取指定股票的最新价格。

### 参数说明
- symbol (str): 股票代码。

### 返回内容
float: 股票的最新价格。

### 调用示例

```python
# 假设 qmt 实例已连接
symbol = '600000.SH'
last_price = qmt.get_last_price(symbol)
print(f"{symbol} 最新价格: {last_price}")
```

## `_get_security_rule`

### 功能
获取指定股票的交易规则，包括最小交易单位、价格精度等。这是一个内部辅助函数。

### 参数说明
- symbol (str): 股票代码。

### 返回内容
dict: 包含交易规则的字典。

### 调用示例

```python
# 这是一个内部函数，通常不直接调用。示例仅作说明。
# rule = qmt._get_security_rule('600000.SH')
# print(f"600000.SH 交易规则: {rule}")
```

## `_adjust_volume`

### 功能
根据交易规则调整交易数量，使其符合最小交易单位。这是一个内部辅助函数。

### 参数说明
- symbol (str): 股票代码。
- volume (int): 原始交易数量。

### 返回内容
int: 调整后的交易数量。

### 调用示例

```python
# 这是一个内部函数，通常不直接调用。示例仅作说明。
# adjusted_volume = qmt._adjust_volume('600000.SH', 123)
# print(f"调整后的数量: {adjusted_volume}")
```

## `buy`

### 功能
买入指定股票。

### 参数说明
- symbol (str): 股票代码。
- volume (int): 买入数量。
- price (float, optional): 买入价格。如果为 None，则为市价委托。
- strategy_name (str, optional): 策略名称，默认为空字符串。
- order_remark (str, optional): 订单备注，默认为空字符串。

### 返回内容
int: 委托订单ID (大于0表示成功，小于等于0表示失败)。

### 调用示例

```python
# 假设 qmt 实例已连接
# 市价买入 600000.SH 100股
order_id_market_buy = qmt.buy('600000.SH', 100)
print(f"市价买入委托ID: {order_id_market_buy}")

# 限价买入 600000.SH 100股，价格 10.50
# order_id_limit_buy = qmt.buy('600000.SH', 100, price=10.50)
# print(f"限价买入委托ID: {order_id_limit_buy}")
```

## `sell`

### 功能
卖出指定股票。

### 参数说明
- symbol (str): 股票代码。
- volume (int): 卖出数量。
- price (float, optional): 卖出价格。如果为 None，则为市价委托。
- strategy_name (str, optional): 策略名称，默认为空字符串。
- order_remark (str, optional): 订单备注，默认为空字符串。

### 返回内容
int: 委托订单ID (大于0表示成功，小于等于0表示失败)。

### 调用示例

```python
# 假设 qmt 实例已连接
# 市价卖出 600000.SH 100股
order_id_market_sell = qmt.sell('600000.SH', 100)
print(f"市价卖出委托ID: {order_id_market_sell}")

# 限价卖出 600000.SH 100股，价格 10.50
# order_id_limit_sell = qmt.sell('600000.SH', 100, price=10.50)
# print(f"限价卖出委托ID: {order_id_limit_sell}")
```

## `cancel_order`

### 功能
撤销指定订单。

### 参数说明
- order_id (int): 要撤销的订单ID。

### 返回内容
int: 撤销操作的结果码 (0 表示成功，非0表示失败)。

### 调用示例

```python
# 假设 qmt 实例已连接，并且有一个待撤销的订单ID
# order_id_to_cancel = 123456789
# result = qmt.cancel_order(order_id_to_cancel)
# print(f"撤销订单 {order_id_to_cancel} 结果: {result}")
```

## `is_trading_time`

### 功能
判断当前时间是否在A股交易时间内（包括集合竞价和连续竞价）。

### 参数说明
无。

### 返回内容
bool: 如果是交易时间则返回 True，否则返回 False。

### 调用示例

```python
# 假设 qmt 实例已连接
is_trade_time = qmt.is_trading_time()
print(f"当前是否为交易时间: {is_trade_time}")
```

## `check_symbol_is_limit_down`

### 功能
检查指定股票是否涨停、跌停或正常。

### 参数说明
- symbol (str): 股票代码。

### 返回内容
str: '涨停'、'跌停' 或 '正常'。

### 调用示例

```python
# 假设 qmt 实例已连接
symbol = '600000.SH'
status = qmt.check_symbol_is_limit_down(symbol)
print(f"{symbol} 涨跌停状态: {status}")
```

## `cancel_all_orders`

### 功能
撤销当前账户所有未成交或部分成交的订单。

### 参数说明
无。

### 返回内容
bool: 如果所有订单都成功处理则返回 True，否则返回 False。

### 调用示例

```python
# 假设 qmt 实例已连接
# result = qmt.cancel_all_orders()
# print(f"撤销所有订单结果: {result}")
```

## `cancel_buy_orders`

### 功能
撤销所有买入委托订单。

### 参数说明
无。

### 返回内容
无。

### 调用示例

```python
# 假设 qmt 实例已连接
# qmt.cancel_buy_orders()
# print("所有买入订单撤销操作完成。")
```

## `cancel_sell_orders`

### 功能
撤销所有卖出委托订单。

### 参数说明
无。

### 返回内容
无。

### 调用示例

```python
# 假设 qmt 实例已连接
# qmt.cancel_sell_orders()
# print("所有卖出订单撤销操作完成。")
```

## `cancel_symbol_orders`

### 功能
撤销指定股票代码的所有未成交或部分成交的订单。

### 参数说明
- symbol (str): 股票代码。

### 返回内容
无。

### 调用示例

```python
# 假设 qmt 实例已连接
# symbol_to_cancel = '600000.SH'
# qmt.cancel_symbol_orders(symbol_to_cancel)
# print(f"股票 {symbol_to_cancel} 的所有订单撤销操作完成。")
```

## `all_sell`

### 功能
卖出所有持仓股票。

### 参数说明
无。

### 返回内容
无。

### 调用示例

```python
# 假设 qmt 实例已连接
# qmt.all_sell()
# print("所有持仓股票卖出操作完成。")
```

## `makeup_order`

### 功能
监控委托状态，定期检查委托列表，并在达到等待间隔后撤销未完全成交的订单并进行补单操作。

### 参数说明
- wait_interval (int, optional): 等待间隔，单位秒，默认为 60 秒。

### 返回内容
bool: 如果所有补单操作都成功处理则返回 True，否则返回 False。

### 调用示例

```python
# 假设 qmt 实例已连接
# result = qmt.makeup_order(wait_interval=30)
# print(f"补单任务执行结果: {result}")
```

## `get_upl`

### 功能
获取指定股票的涨停价。

### 参数说明
- symbol (str): 股票代码。

### 返回内容
float: 股票的涨停价，如果获取失败则返回 0.0。

### 调用示例

```python
# 假设 qmt 实例已连接
symbol = '600000.SH'
upl = qmt.get_upl(symbol)
print(f"{symbol} 涨停价: {upl}")
```

## `get_dnl`

### 功能
获取指定股票的跌停价。

### 参数说明
- symbol (str): 股票代码。

### 返回内容
float: 股票的跌停价，如果获取失败则返回 0.0。

### 调用示例

```python
# 假设 qmt 实例已连接
symbol = '600000.SH'
dnl = qmt.get_dnl(symbol)
print(f"{symbol} 跌停价: {dnl}")
```

