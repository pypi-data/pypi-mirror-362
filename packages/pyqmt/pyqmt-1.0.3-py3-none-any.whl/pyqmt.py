#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PYQMT - 基于miniQMT进行简化的量化交易库
版本: 1.0.2 | 创建日期: 2025-07-02
版权声明: 本代码受版权保护，未经授权禁止修改、隐藏或分发。
"""
import time
import random
import datetime
import pandas as pd
import logging as log
import datetime
import schedule

# 添加打包的xtquant库到系统路径

try:
    from xtquant import xttrader, xtdata, xtconstant
    from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
    from xtquant.xttype import StockAccount
except ImportError:
    print("警告: 无法导入xtquant模块。请确保已正确配置QMT环境。")
    print("建议: 检查QMT路径是否正确、是否登录了miniQMT、账户是否正确、账户是否具有miniQMT权限、并重启QMT终端后重试。")
    raise
xtdata.enable_hello = False

# 打印作者声明函数 - 不可修改的核心部分
def print_author_declaration():
    """打印不可修改的作者和版权声明"""
    print("\n" + "=" * 80)
    print("QMT_Manager - QMT_XTQUANT交易接口封装库 v1.0.2")
    print("-" * 80)
    print("作者: [量化交易汤姆猫] | 微信: QUANT0808")
    print("欢迎联系我：BUG反馈、功能完善、量化交流")
    print("量化资料库: https://quant0808.netlify.app")
    print("-" * 80)
    print("风险提示: 仅供参考，不构成投资建议，使用风险需自行承担")
    print("=" * 80 + "\n")

# 在模块加载时打印声明
print_author_declaration()

# 配置日志
log.basicConfig(
    level='INFO',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class qmtcb(XtQuantTraderCallback):
    def on_order_error(self, order_id, error_code, error_msg):
        log.error(f"【下单失败】订单 ID: {order_id}, 错误码: {error_code}, 错误信息: {error_msg}")

# 定义管理类
class pyqmt:
    def __init__(self, path: str, acc: str):
        """
        初始化 pyqmt 交易管理类。

        参数:
            path (str): miniQMT 交易终端的安装路径。
            acc (str): 资金账户，用于连接和订阅交易账户。
        """
        self.path = path
        self.acc = acc
        # self.order_file = order_file
        self.委托等待间隔 = 30 #秒
        self.xt_trader = self._connect()
        # 检查连接状态
        if self.xt_trader is None:
            log.error("无法连接到QMT交易终端或订阅账户失败，部分功能将不可用")
            log.info("建议检查以下项目:")
            log.info("1. miniQMT交易端是否已启动")
            log.info("2. 账号是否正确")
            log.info("3. miniqmt路径是否正确")
        else:
            log.info("交易终端连接成功，可以正常使用")

        self.trade_rules = {
            '688': {'name': '科创板', 'min': 200, 'step': 1, 'slippage': 0.01, 'unit': '股'},
            '300': {'name': '创业板', 'min': 100, 'step': 100, 'slippage': 0.01, 'unit': '股'},
            '60': {'name': '沪市主板', 'min': 100, 'step': 100, 'slippage': 0.01, 'unit': '股'},
            '00': {'name': '深市主板', 'min': 100, 'step': 100, 'slippage': 0.01, 'unit': '股'},
            '50': {'name': '沪市ETF', 'min': 100, 'step': 100, 'slippage': 0.001, 'unit': '份'},
            '51': {'name': '沪市ETF', 'min': 100, 'step': 100, 'slippage': 0.001, 'unit': '份'},
            '52': {'name': '沪市ETF', 'min': 100, 'step': 100, 'slippage': 0.001, 'unit': '份'},
            '53': {'name': '沪市ETF', 'min': 100, 'step': 100, 'slippage': 0.001, 'unit': '份'},
            '56': {'name': '沪市ETF', 'min': 100, 'step': 100, 'slippage': 0.001, 'unit': '份'},
            '58': {'name': '沪市ETF', 'min': 100, 'step': 100, 'slippage': 0.001, 'unit': '份'},
            '15': {'name': '深市ETF', 'min': 100, 'step': 100, 'slippage': 0.001, 'unit': '份'},
            '16': {'name': '深市ETF', 'min': 100, 'step': 100, 'slippage': 0.001, 'unit': '份'},
            '11': {'name': '可转债', 'min': 10, 'step': 10, 'slippage': 0.001, 'unit': '张'},
            '12': {'name': '可转债', 'min': 10, 'step': 10, 'slippage': 0.001, 'unit': '张'},
            '4': {'name': '北京股票', 'min': 0, 'step': 100, 'slippage': 0.01, 'unit': '股'},
            '8': {'name': '北京股票', 'min': 0, 'step': 100, 'slippage': 0.01, 'unit': '股'},
            '9': {'name': '北京股票', 'min': 0, 'step': 100, 'slippage': 0.01, 'unit': '股'},
        }
        # self._init_order_table()

    def _connect(self) -> XtQuantTrader:
        """
        安全连接QMT交易终端。

        返回:
            XtQuantTrader: 连接成功的 XtQuantTrader 实例，如果连接失败则返回 None。
        """
        """安全连接QMT交易终端 - 错误容错版"""
        try:
            session_id = random.randint(10000000, 99999999)
            xt_trader = XtQuantTrader(self.path, session_id)
            
            # 注册回调
            callback = qmtcb()
            xt_trader.register_callback(callback)
            
            # 启动交易系统
            xt_trader.start()
            
            # 建立连接
            connect_id = xt_trader.connect()
            if connect_id != 0:
                error_msg = f"miniqmt链接失败，错误码: {connect_id}"
                log.error(error_msg)
                # 改为记录错误但不抛出异常
                return None  # 返回None表示连接失败
            
            log.info('miniqmt连接成功')
            
            # 订阅账户
            acc_id = StockAccount(self.acc)
            sub_res = xt_trader.subscribe(acc_id)
            if sub_res != 0:
                error_msg = f"账户订阅失败，错误码: {sub_res}"
                log.error(error_msg)
                # 返回None表示订阅失败
                return None
            
            log.info('账户订阅成功')
            return xt_trader
            
        except Exception as e:
            log.error(f"连接QMT时发生未预期的错误: {str(e)}")
            return None  # 在异常情况下也返回None



    def query_stock_asset(self):
        """
        查询当前账户的资产信息。

        返回:
            pd.DataFrame: 包含账户资产信息的 DataFrame，如果查询失败则返回 None。
        """
        asset = self.xt_trader.query_stock_asset(StockAccount(self.acc))
        asset_list = []
        asset_dict = {
            '账户类型': asset.account_type,
            '资金账户': asset.account_id,
            '可用资金': asset.cash,
            '冻结金额': asset.frozen_cash,
            '持仓市值': asset.market_value,
            '总资产': asset.total_asset
        }
        asset_list.append(asset_dict)
        asset_df = pd.DataFrame(asset_list)
        asset_df.set_index('资金账户', inplace=True)
        return asset_df

    def get_available_fund(self):
        """
        获取当前账户的可用资金。

        返回:
            float: 可用资金金额，如果查询失败则返回 0。
        """
        asset = self.xt_trader.query_stock_asset(StockAccount(self.acc))
        return asset.cash if asset else 0

    def get_available_pos(self, symbol):
        """
        获取指定股票代码的可用持仓数量。

        参数:
            symbol (str): 股票代码。

        返回:
            int: 可用持仓数量，如果查询失败或无持仓则返回 0。
        """
        pos = self.xt_trader.query_stock_position(StockAccount(self.acc), symbol)
        return pos.can_use_volume if pos else 0

    def query_stock_orders(self):
        """
        查询当前账户的所有委托订单。

        返回:
            pd.DataFrame: 包含委托订单信息的 DataFrame，如果查询失败或无订单则返回 None。
        """
        orders = self.xt_trader.query_stock_orders(StockAccount(self.acc))
        if not orders:
            print("当前没有委托订单。")
            return None
        order_list = []
        for order in orders:
            order_dict = {
                '资金账号': order.account_id,
                '证券代码': order.stock_code,
                '订单编号': order.order_id,
                '柜台合同编号': order.order_sysid,
                '报单时间': order.order_time,
                '委托类型': order.order_type,
                '委托数量': order.order_volume,
                '报价类型': order.price_type,
                '委托价格': order.price,
                '成交数量': order.traded_volume,
                '成交均价': order.traded_price,
                '委托状态': order.order_status,
                '委托状态描述': order.status_msg,
                '策略名称': order.strategy_name,
                '委托备注': order.order_remark,
            }
            order_list.append(order_dict)
        orders_df = pd.DataFrame(order_list)
        return orders_df

    def query_stock_trades(self):
        """
        查询当前账户的所有成交记录。

        返回:
            pd.DataFrame: 包含成交记录信息的 DataFrame，如果查询失败或无记录则返回 None。
        """
        trades = self.xt_trader.query_stock_trades(StockAccount(self.acc))
        if not trades:
            print("当前没有成交记录。")
            return None
        trade_list = []
        for trade in trades:
            trade_dict = {
                '资金账号': trade.account_id,
                '证券代码': trade.stock_code,
                '成交时间': trade.traded_time,
                '成交数量': trade.traded_volume,
                '成交金额': trade.traded_amount,
                '成交均价': trade.traded_price,
                '委托类型': trade.order_type,
                '交易编号': trade.traded_id,
            }
            trade_list.append(trade_dict)
        trades_df = pd.DataFrame(trade_list)
        trades_df['成交时间'] = pd.to_datetime(trades_df['成交时间'], unit='s', utc=True)
        trades_df['成交时间'] = trades_df['成交时间'].dt.tz_convert('Asia/Shanghai')
        trades_df['成交时间'] = trades_df['成交时间'].dt.strftime("%Y-%m-%d %H:%M:%S")
        trades_df['成交时间'] = pd.to_datetime(trades_df['成交时间'])
        trades_df.set_index('资金账号', inplace=True)
        return trades_df

    def query_stock_positions(self):
        """
        查询当前账户的所有持仓信息。

        返回:
            pd.DataFrame: 包含持仓信息的 DataFrame，如果查询失败或无持仓则返回 None。
        """
        positions = self.xt_trader.query_stock_positions(StockAccount(self.acc))
        if not positions:
            print("当前没有持仓信息。")
            return None
        position_list = []
        for position in positions:
            position_dict = {
                '资金账号': position.account_id,
                '证券代码': position.stock_code,
                '持仓数量': position.volume,
                '可用数量': position.can_use_volume,
                '开仓价': position.open_price,
                '市值': position.market_value,
                '冻结数量': position.frozen_volume,
                '在途股份': position.on_road_volume,
                '昨夜拥股': position.yesterday_volume,
                '成本价': position.open_price
            }
            position_list.append(position_dict)
        pos_df = pd.DataFrame(position_list)
        return pos_df

    def _get_board(self, symbol):
        """
        根据股票代码判断所属板块。

        参数:
            symbol (str): 股票代码。

        返回:
            str: 股票所属的板块名称（如 '主板', '创业板', '科创板', '北交所', '其他'）。
        """
        prefix = symbol[:3] if symbol.startswith('688') else symbol[:2]
        rule = self.trade_rules.get(prefix)
        if rule:
            name = rule['name']
            if name in ['沪市主板', '深市主板']:
                return '主板'
            elif name == '创业板':
                return '创业板'
            elif name == '科创板':
                return '科创板'
            elif name == '北京股票':
                return '北交所'
            else:
                return '其他'
        return '其他'

    def _check_price_cage(self, symbol, order_side, order_price=None):
        """
        检查委托价格是否符合价格笼子规则。

        参数:
            symbol (str): 股票代码。
            order_side (str): 委托方向 ('buy' 或 'sell')。
            order_price (float, optional): 委托价格。如果为 None，则跳过价格检查。

        返回:
            bool: 如果价格符合规则或不适用价格笼子检查，则返回 True；否则返回 False。
        """
        if order_price==None:
            print(f"【价格笼子】最新价委托 {symbol} 无需价格检查")
            return True
        
        board = self._get_board(symbol)
        if board == '其他':
            print(f"【价格笼子】{symbol} 不属于价格笼子生效范围，跳过检查。")
            return True
        
        now_time = datetime.datetime.now().time()
        start_time = datetime.time(9, 25)
        end_time = datetime.time(14, 57)
        if not (start_time <= now_time <= end_time):
            print(f"【价格笼子】当前时间 {now_time.strftime('%H:%M:%S')} 不在生效时间 (09:25-14:57) 内，跳过检查。")
            return True
        reference_price = self.get_last_price(symbol)
        if reference_price is None or reference_price <= 0:
            print(f"【价格笼子】{symbol} 参考价无效 ({reference_price})，跳过检查。")
            return True
        if board in ['主板', '创业板']:
            if order_side == 'buy':
                upper_limit = max(reference_price * 1.02, reference_price + 0.1)
                if order_price > upper_limit:
                    print(f"【价格笼子校验失败】{symbol} 买入委托价 {order_price:.2f} 过高。")
                    return False
            elif order_side == 'sell':
                lower_limit = min(reference_price * 0.98, reference_price - 0.1)
                if order_price < lower_limit:
                    print(f"【价格笼子校验失败】{symbol} 卖出委托价 {order_price:.2f} 过低。")
                    return False
        elif board == '北交所':
            if order_side == 'buy':
                upper_limit = max(reference_price * 1.05, reference_price + 0.1)
                if order_price > upper_limit:
                    print(f"【价格笼子校验失败】{symbol} 买入委托价 {order_price:.2f} 过高。")
                    return False
            elif order_side == 'sell':
                lower_limit = min(reference_price * 0.95, reference_price - 0.1)
                if order_price < lower_limit:
                    print(f"【价格笼子校验失败】{symbol} 卖出委托价 {order_price:.2f} 过低。")
                    return False
        elif board == '科创板':
            if order_side == 'buy':
                upper_limit = round(reference_price * 1.02, 2)
                if order_price > upper_limit:
                    print(f"【价格笼子校验失败】{symbol} 买入委托价 {order_price:.2f} 过高。")
                    return False
            elif order_side == 'sell':
                lower_limit = round(reference_price * 0.98, 2)
                if order_price < lower_limit:
                    print(f"【价格笼子校验失败】{symbol} 卖出委托价 {order_price:.2f} 过低。")
                    return False
        print(f"【价格笼子校验通过】{symbol} 委托价 {order_price:.2f} 在允许范围内。")
        return True

    def _calculate_commission(self, symbol, price, volume):
        """
        计算交易佣金。

        参数:
            symbol (str): 股票代码。
            price (float): 成交价格。
            volume (int): 成交数量。

        返回:
            float: 计算出的佣金，最低为5元。
        """
        amount = price * volume
        commission = amount * 0.0002
        return max(commission, 5)

    def get_last_price(self, symbol):
        """
        获取指定股票的最新价格。

        参数:
            symbol (str): 股票代码。

        返回:
            float: 股票的最新价格，如果获取失败则返回 None。
        """
        try:
            data = xtdata.get_full_tick([symbol])
            last_price = data[symbol]['lastPrice']
            return last_price
        except Exception as e:
            print(f"【行情获取失败】{symbol} 错误:{str(e)}")
            return None

    def _get_security_rule(self, symbol):
        """
        根据股票代码获取对应的交易规则。

        参数:
            symbol (str): 股票代码。

        返回:
            dict: 包含股票交易规则的字典，如果未找到则返回默认规则。
        """
        code = symbol.split('.')[0] if '.' in symbol else symbol
        for prefix in self.trade_rules:
            if code.startswith(prefix):
                return self.trade_rules[prefix]
        return {'name': '默认', 'min': 100, 'step': 100, 'slippage': 0.01, 'unit': '股'}

    def _adjust_volume(self, symbol, volume):
        """
        根据交易规则调整委托数量，使其符合最小交易单位和步长。

        参数:
            symbol (str): 股票代码。
            volume (int): 原始委托数量。

        返回:
            int: 调整后的委托数量，如果该品种禁止交易则返回 0。
        """
        rule = self._get_security_rule(symbol)
        if rule['min'] == 0:
            print(f"【交易禁止】{symbol} 北交所品种不支持交易")
            return 0
        adjusted = max(rule['min'], volume) // rule['step'] * rule['step']
        if adjusted != volume:
            print(f"【数量调整】{symbol} {volume}{rule['unit']} -> {adjusted}{rule['unit']}")
        return int(adjusted)

    def buy(self, symbol, volume, price=None, strategy_name='', order_remark=''):
        """
        买入股票。

        参数:
            symbol (str): 股票代码。
            volume (int): 委托数量。
            price (float, optional): 委托价格。如果为 None，则以最新价买入。
            strategy_name (str, optional): 策略名称。
            order_remark (str, optional): 订单备注。
            retry_count (int, optional): 重试次数，目前未使用。

        返回:
            int: 委托订单ID，如果下单失败则返回 -1。
        """
        try:
            # 规则调整委托数量
            adj_volume = self._adjust_volume(symbol, volume)
            if adj_volume <= 0:
                return -1
            if not symbol or adj_volume <= 0:
                print("【参数错误】证券代码或数量无效")
                return -1
            
            # 价格笼子检查
            if not self._check_price_cage(symbol,'buy',price):
                return -1
            
            # 获取规则和行情
            rule = self._get_security_rule(symbol)
            last_price = self.get_last_price(symbol)
            if last_price is None or last_price <= 0:
                print(f"【行情无效】{symbol} 获取最新价失败")
                return -1
            
            # 资金检查
            # 使用参考价格计算所需资金（对于市价单使用含滑点的预估价格）
            reference_price = last_price * (1 + rule['slippage']) if price is None else price
            required_fund = reference_price * adj_volume
            commission = self._calculate_commission(symbol, reference_price, adj_volume)
            available_fund = self.get_available_fund()
            if available_fund < required_fund + commission:
                print(f"【资金不足】可用资金:{available_fund:.2f}元，所需资金:{required_fund+commission:.2f}元(含手续费{commission:.2f}元)")
                return -1
            
            # 正确处理市价/限价委托
            if price is None:
                # 最新价委托
                final_price = 0.0
                price_type = xtconstant.LATEST_PRICE
            else:
                # 限价委托
                final_price = round(float(price), 3)
                price_type = xtconstant.FIX_PRICE
            
            # 计算参考价格（仅限市价委托，用于日志记录）
            if price is None and rule['slippage'] != 0:
                reference_price = round(last_price * (1 + rule['slippage']), 3)
                log.info(f"【最新价买入参考价】{symbol} 计算参考价:{reference_price}")
            else:
                reference_price = final_price
            
            strategy_name = str(strategy_name) if pd.notna(strategy_name) else ''
            order_remark = str(order_remark) if pd.notna(order_remark) else ''
            
            # 尝试下单
            order_id = self.xt_trader.order_stock(
                StockAccount(self.acc), symbol, xtconstant.STOCK_BUY, adj_volume,
                price_type, final_price, strategy_name, order_remark
            )
       
                    
            if order_id > 0:
                # 使用不同日志描述市价/限价
                if price is None:
                    print(f"【最新价买入委托成功】{symbol} 参考价:{reference_price} 数量:{adj_volume}{rule['unit']} 委托编号:{order_id}")
                else:
                    print(f"【限价买入委托成功】{symbol} 价格:{final_price} 数量:{adj_volume}{rule['unit']} 委托编号:{order_id}")
                    
                return order_id
            else:
                print(f"【买入委托失败】{symbol} 错误码:{order_id}")
                return order_id
        except ConnectionError as e:
            print(f"【网络错误】下单时发生网络连接问题: {str(e)}")
            return -1
        except ValueError as e:
            print(f"【参数错误】下单时发生参数错误: {str(e)}")
            return -1
        except AttributeError as e:
            print(f"【API错误】下单时发生属性错误，可能由于 QMT 返回数据异常: {str(e)}")
            return -1
        except Exception as e:
            print(f"【下单异常】买入 {symbol} 时发生未知错误: {str(e)}")
            
    
    def sell(self, symbol, volume, price=None, strategy_name='', order_remark=''):
        """
        卖出股票。

        参数:
            symbol (str): 股票代码。
            volume (int): 委托数量。
            price (float, optional): 委托价格。如果为 None，则以最新价卖出。
            strategy_name (str, optional): 策略名称。
            order_remark (str, optional): 订单备注。
            retry_count (int, optional): 重试次数，目前未使用。

        返回:
            int: 委托订单ID，如果下单失败则返回 -1。
        """
        try:
            # 检查参数有效性
            if volume <= 0 or not symbol:
                print("【参数错误】证券代码或数量无效")
                return -1
                
            # 价格笼子检查
            if not self._check_price_cage(symbol,'sell',price):
                return -1
            
            # 获取规则和行情
            rule = self._get_security_rule(symbol)
            last_price = self.get_last_price(symbol)
            if last_price is None or last_price <= 0:
                print(f"【行情无效】{symbol} 获取最新价失败")
                return -1
            
            # 检查可用持仓
            available_pos = self.get_available_pos(symbol)
            if available_pos <= 0:
                print(f"【卖出失败】 {symbol} 可用股数为0")
                return -1
            
            # 调整委托数量（如果超过可用数量）
            original_volume = volume
            if volume > available_pos:
                volume = available_pos
                print(f"【委托数量调整】{symbol} | 委托数量超过可用数量，已调整为可用数量 | {original_volume} --> {volume}")
            
            # 向下取整（适配交易规则）
            adj_volume = self._adjust_volume(symbol, volume)
            if adj_volume <= 0:
                return -1
            if adj_volume != volume:
                print(f"【数量调整】{symbol} 调整后数量:{adj_volume}{rule['unit']}")
            
            # 修复：正确处理市价/限价委托
            if price is None:
                # 市价委托
                final_price = 0.0
                price_type = xtconstant.LATEST_PRICE
            else:
                # 限价委托
                final_price = round(float(price), 3)
                price_type = xtconstant.FIX_PRICE
            
            # 计算参考价格（仅限市价委托，用于日志记录）
            if price is None and rule['slippage'] != 0:
                reference_price = round(last_price * (1 - rule['slippage']), 3)
                log.info(f"【最新价卖出参考价】{symbol} 计算参考价:{reference_price}")
            else:
                reference_price = final_price
            
            strategy_name = str(strategy_name) if pd.notna(strategy_name) else ''
            order_remark = str(order_remark) if pd.notna(order_remark) else ''
            
            # 尝试下单
            order_id = self.xt_trader.order_stock(
                StockAccount(self.acc), symbol, xtconstant.STOCK_SELL, adj_volume,
                price_type, final_price, strategy_name, order_remark
            )
            
            if order_id > 0:
                # 使用不同日志描述市价/限价
                if price is None:
                    print(f"【最新价卖出委托成功】{symbol} 参考价:{reference_price} 数量:{adj_volume}{rule['unit']} 委托编号:{order_id}")
                else:
                    print(f"【限价卖出委托成功】{symbol} 价格:{final_price} 数量:{adj_volume}{rule['unit']} 委托编号:{order_id}")
                    
                return order_id
            else:
                print(f"【卖出委托失败】{symbol} 错误码:{order_id}")
                return order_id
        except ConnectionError as e:
            print(f"【网络错误】下单时发生网络连接问题: {str(e)}")
            return -1
        except ValueError as e:
            print(f"【参数错误】下单时发生参数错误: {str(e)}")
            return -1
        except AttributeError as e:
            print(f"【API错误】下单时发生属性错误，可能由于 QMT 返回数据异常: {str(e)}")
            return -1
        except Exception as e:
            print(f"【下单异常】卖出 {symbol} 时发生未知错误: {str(e)}")
            return -1
    
    def makeup_order(self, wait_interval=60):
        """
        监控委托状态，定期检查委托列表，并在达到等待间隔后撤销未完全成交的订单并进行补单操作。

        返回:
            bool: 如果所有补单操作都成功处理则返回 True，否则返回 False。
        """
        log.info(f"开始执行补单任务，等待间隔：{wait_interval} 秒...")
        try:
            orders = self.query_stock_orders()
            if orders.empty:
                log.info("没有找到任何委托订单，无需补单。")
                return True

            # 筛选出未成交或部成订单
            pending_orders = orders[orders['委托状态'].isin(['未成交', '部成'])]

            if pending_orders.empty:
                log.info("没有找到未成交或部成订单，无需补单。")
                return True

            for index, order in pending_orders.iterrows():
                try:
                    order_id = order['order_id']
                    symbol = order['stock_code']
                    order_side = '买' if order['order_type'] == xtconstant.STOCK_BUY else '卖'
                    original_price_type = order['price_type']  # 原始价格类型（市价/限价）
                    order_volume = order['order_volume']
                    traded_volume = order['traded_volume']
                    remaining_volume = order_volume - traded_volume
                    strategy_name = order.get('strategy_name', '')
                    order_remark = order.get('order_remark', '')
                    original_price = order['price'] if 'price' in order and original_price_type == xtconstant.FIX_PRICE else None
                    
                    if 'order_time' in order:
                        try:
                            # 直接转换为datetime对象
                            order_time = datetime.datetime.fromtimestamp(order['order_time'])
                        except:
                            log.warning(f"订单 {order_id} 的时间格式无法识别: {order['order_time']}")
                            continue
                    else:
                        log.warning(f"订单 {order_id} 缺少 order_time 字段")
                        continue
                    
                    current_time = datetime.datetime.now()
                    time_diff = (current_time - order_time).total_seconds()

                    if time_diff >= wait_interval:
                        log.info(f"订单 {order_id} ({symbol}) 已等待 {time_diff} 秒，超过 {wait_interval} 秒，准备撤单并补单")
                        
                        # 撤单
                        cancel_result = self.cancel_order(order_id)
                        if cancel_result == 0:
                            log.info(f"撤单请求成功发送 {order_id}")
                            
                            # 给交易所处理撤单的时间（重要）
                            time.sleep(1)
                            
                            if remaining_volume > 0:
                                log.info(f"准备补单 {symbol} {order_side} 数量 {remaining_volume}")
                                
                                # 使用相同的价格策略补单
                                if original_price_type == xtconstant.LATEST_PRICE:
                                    # 市价单
                                    if order_side == '买':
                                        new_order_id = self.buy(symbol, remaining_volume, None, strategy_name, order_remark)
                                    else:
                                        new_order_id = self.sell(symbol, remaining_volume, None, strategy_name, order_remark)
                                else:
                                    # 限价单（使用原始委托价格）
                                    if order_side == '买':
                                        new_order_id = self.buy(symbol, remaining_volume, original_price, strategy_name, order_remark)
                                    else:
                                        new_order_id = self.sell(symbol, remaining_volume, original_price, strategy_name, order_remark)
                                
                                if new_order_id > 0:
                                    log.info(f"补单成功 {symbol} 新订单ID {new_order_id}")
                                else:
                                    log.error(f"补单失败 {symbol}，错误代码：{new_order_id}")
                            else:
                                log.info(f"无需补单 {symbol}，剩余数量为0")
                        else:
                            log.warning(f"撤单失败 {order_id}，错误代码：{cancel_result}")
                    else:
                        log.info(f"订单 {order_id} ({symbol}) 已等待 {time_diff} 秒，未达到补单条件")
                except Exception as inner_e:
                    log.error(f"处理订单 {order_id} 时出错: {str(inner_e)}")
                    continue
                        
            log.info("补单任务执行完成")
            return True
        except Exception as e:
            log.error(f"执行补单任务时发生全局错误: {str(e)}")
            return False
        
    def cancel_order(self, order_id):
        """
        撤销指定订单。

        参数:
            order_id (int): 要撤销的订单ID。

        返回:
            int: 撤销操作的结果码 (0 表示成功，非0表示失败)。
        """
        try:
            result = self.xt_trader.cancel_order_stock(StockAccount(self.acc), order_id)
            if result == 0:
                print(f"【撤单成功】订单 {order_id}")
                self._update_order_in_csv(order_id, {'status': 'canceled'})
            else:
                print(f"【撤单失败】订单 {order_id} 错误码: {result}")
        except Exception as e:
            print(f"【撤单异常】订单 {order_id} 错误: {str(e)}")

        
    def is_trading_time(self):
        """
        判断当前时间是否在A股交易时间内（包括集合竞价和连续竞价）。
        交易时间：周一到周五 9:15-15:00（包括9:15和14:59）
        返回:
            bool: 如果是交易时间则返回 True，否则返回 False。
        """
        # 获取当前时间
        now = datetime.now()
        weekday = now.weekday()  # 0-6，0 为星期一
        hour = now.hour
        minute = now.minute
        
        # 检查是否为周末
        if weekday >= 5:  # 5和6是周六和周日
            log.info('【非交易时间】 现在是周末')
            return False
        
        # 将时间转换为分钟数方便比较
        current_minutes = hour * 60 + minute
        
        # 检查是否在上午交易时段 (9:15-11:30)
        if (9 * 60 + 15) <= current_minutes <= (11 * 60 + 30):
            log.info('【交易时间】 现在是早盘')
            return True
            
        # 检查是否在下午交易时段 (13:00-15:00)
        if (13 * 60 + 0) <= current_minutes <= (15 * 60 + 0):
            log.info('【交易时间】 现在是午盘')
            return True
        
        # 其余时间都是非交易时间
        log.info('【非交易时间】 现在是非交易时间')
        return False
    
    def check_symbol_is_limit_down(self, symbol):
        """
        检查指定股票是否跌停。
        参数:
            symbol (str): 股票代码。

        返回:
            bool: 如果股票跌停则返回 True，否则返回 False。
        """
        try:
            data = xtdata.get_instrument_detail(symbol)
        except Exception as e:
            log.warning('获取标的基础信息失败：{e}')
            return None

        up_stop_price = data['UpStopPrice']
        down_stop_price = data['DownStopPrice']
        try:
            lastprice = xtdata.get_full_tick([symbol])
            lastprice = lastprice[symbol]['lastPrice']
        except Exception as e:
            log.warning('获取最新价失败：{e}')
            return None
        
        if lastprice >= up_stop_price:
            log.info(f'标的{symbol}涨停')
            return '涨停'
        elif lastprice <= down_stop_price:
            log.info(f'标的{symbol}跌停')
            return  '跌停'
        else:
            log.info(f'标的{symbol}未涨停、未跌停')
            return  '正常'

    def cancel_all_orders(self):
        """
        撤销当前账户所有未成交或部分成交的订单。
        返回:
            bool: 如果所有订单都成功处理则返回 True，否则返回 False。
        """
        cancel_orders = self.xt_trader.query_stock_orders(StockAccount(self.acc),True)
        if not cancel_orders:
            print("当前没有委托订单。")
            return False
        order_list = []
        for order in cancel_orders:
            order_dict = {
                '资金账号': order.account_id,
                '证券代码': order.stock_code,
                '订单编号': order.order_id,
                '柜台合同编号': order.order_sysid,
                '报单时间': order.order_time,
                '委托类型': order.order_type,
                '委托数量': order.order_volume,
                '报价类型': order.price_type,
                '委托价格': order.price,
                '成交数量': order.traded_volume,
                '成交均价': order.traded_price,
                '委托状态': order.order_status,
                '委托状态描述': order.status_msg,
                '策略名称': order.strategy_name,
                '委托备注': order.order_remark,
            }
            order_list.append(order_dict)
        orders_df = pd.DataFrame(order_list) #可以撤单的委托

        撤销成功数 = 0
        for index,row in orders_df.iterrows():
            order_id = row['订单编号']
            stock_code = row['证券代码']
            try:
                cancel_res = self.xt_trader.cancel_order_stock(StockAccount(self.acc),order_id)
                if cancel_res == 0:
                    log.info(f"{stock_code} | {order_id} | 撤单成功")
                    撤销成功数 += 1
                else:
                    log.warning(f"{stock_code} | {order_id} | 撤单失败")
            except Exception as e:
                log.warning(f'撤单操作失败，{str(e)}')

        log.info(f"【全部撤单】已成功撤销 {撤销成功数}/{len(orders_df)} 个订单")
        return 撤销成功数>0


    def cancel_buy_orders(self):
        """
        撤销所有买入委托订单。
        """
        log.info("开始撤销所有买入委托订单...")
        try:
            orders = self.query_stock_orders()
            if orders.empty:
                log.info("没有找到任何委托订单，无需撤销。")
                return

            buy_pending_orders = orders[
                (orders['order_status'].isin(['未成交', '部成'])) &
                (orders['order_type'] == '买')
            ]

            if buy_pending_orders.empty:
                log.info("没有找到未成交或部成买入订单，无需撤销。")
                return

            for index, order in buy_pending_orders.iterrows():
                order_id = order['order_id']
                symbol = order['stock_code']
                order_status = order['order_status']
                log.info(f"正在撤销买入订单: ID={order_id}, 股票={symbol}, 状态={order_status}")
                self.cancel_order(order_id)
                time.sleep(0.1)  # 避免请求过于频繁
            log.info("所有买入委托订单撤销操作完成。")
        except Exception as e:
            log.error(f"撤销所有买入委托订单时发生错误: {e}")

    def cancel_sell_orders(self):
        """
        撤销所有卖出委托订单。
        """
        log.info("开始撤销所有卖出委托订单...")
        try:
            orders = self.query_stock_orders()
            if orders.empty:
                log.info("没有找到任何委托订单，无需撤销。")
                return

            sell_pending_orders = orders[
                (orders['order_status'].isin(['未成交', '部成'])) &
                (orders['order_type'] == '卖')
            ]

            if sell_pending_orders.empty:
                log.info("没有找到未成交或部成卖出订单，无需撤销。")
                return

            for index, order in sell_pending_orders.iterrows():
                order_id = order['order_id']
                symbol = order['stock_code']
                order_status = order['order_status']
                log.info(f"正在撤销卖出订单: ID={order_id}, 股票={symbol}, 状态={order_status}")
                self.cancel_order(order_id)
                time.sleep(0.1)  # 避免请求过于频繁
            log.info("所有卖出委托订单撤销操作完成。")
        except Exception as e:
            log.error(f"撤销所有卖出委托订单时发生错误: {e}")

    def cancel_symbol_orders(self, symbol):
        """
        撤销指定股票代码的所有未成交或部分成交的订单。
        参数:
            symbol (str): 股票代码。
        """
        log.info(f"开始撤销股票 {symbol} 的所有委托订单...")
        try:
            orders = self.query_stock_orders()
            if orders.empty:
                log.info("没有找到任何委托订单，无需撤销。")
                return

            symbol_pending_orders = orders[
                (orders['order_status'].isin(['未成交', '部成'])) &
                (orders['stock_code'] == symbol)
            ]

            if symbol_pending_orders.empty:
                log.info(f"没有找到股票 {symbol} 的未成交或部成订单，无需撤销。")
                return

            for index, order in symbol_pending_orders.iterrows():
                order_id = order['order_id']
                order_status = order['order_status']
                log.info(f"正在撤销股票 {symbol} 的订单: ID={order_id}, 状态={order_status}")
                self.cancel_order(order_id)
                time.sleep(0.1)  # 避免请求过于频繁
            log.info(f"股票 {symbol} 的所有委托订单撤销操作完成。")
        except Exception as e:
            log.error(f"撤销股票 {symbol} 的委托订单时发生错误: {e}")

    def all_sell(self):
        """
        卖出所有持仓股票。
        """
        log.info("开始卖出所有持仓股票...")
        try:
            positions = self.query_stock_positions()
            if positions.empty:
                log.info("没有持仓股票，无需卖出。")
                return

            for index, pos in positions.iterrows():
                symbol = pos['证券代码']
                volume = pos['可用数量']
                if volume > 0:
                    log.info(f"正在卖出股票: {symbol}, 数量: {volume}")
                    self.sell(symbol, volume, price=None)  # 使用 price=None 表示市价委托
                    time.sleep(0.1)  # 避免请求过于频繁
                else:
                    log.info(f"股票 {symbol} 可用数量为0，跳过卖出。")
            log.info("所有持仓股票卖出操作完成。")
        except Exception as e:
            log.error(f"卖出所有持仓股票时发生错误: {e}")
    
    # =============================

    
    
    def get_upl(self, symbol):
        """
        获取指定股票的涨停价。

        参数:
            symbol (str): 股票代码。

        返回:
            float: 股票的涨停价，如果获取失败则返回 None。
        """

        try:
            data = xtdata.get_instrument_detail(symbol)
            return data['UpStopPrice']
        except Exception as e:
            log.error(f"获取 {symbol} 涨停价失败: {e}")
            return 0.0

    def get_dnl(self, symbol):
        """
        获取指定股票的跌停价。

        参数:
            symbol (str): 股票代码。

        返回:
            float: 股票的跌停价，如果获取失败则返回 None。
        """
  
        try:
            data = xtdata.get_instrument_detail(symbol)
            return data['DownStopPrice']
        except Exception as e:
            log.error(f"获取 {symbol} 跌停价失败: {e}")
            return 0.0
            

          
    # ================= 元数据保护 =================
    @property
    def print_author_declaration(self):
        """
        此属性用于控制作者声明的打印行为，并禁用用户修改。
        """
    def __str__(self):
        """
        返回对象的字符串表示，用于用户友好的输出。

        返回:
            str: 对象的字符串表示。
        """

        return f"pyqmt(acc='{self.acc}', trade_rules={self.trade_rules})"
    
    def __repr__(self):
        """
        返回对象的官方字符串表示。
        """
        return self.__str__()
    
    def _disable_declaration_modification(self):
        """
        禁用用户修改作者声明。
        """
      
        # 覆盖 print_author_declaration 属性，使其不可修改
        def _set_declaration(instance, value):
            raise AttributeError("Author declaration cannot be modified.")

        self.__class__.print_author_declaration = property(
            lambda self: self._print_author_declaration_impl,
            _set_declaration
        )
       
        
