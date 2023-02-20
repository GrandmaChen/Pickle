import time
import datetime
import pandas as pd
from tigeropen.common.consts import (Language,  # 语言
                                     Market,  # 市场
                                     BarPeriod,  # k线周期
                                     QuoteRight, SecurityType)  # 复权类型
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.trade.trade_client import TradeClient
import matplotlib.pyplot as plt
from tkinter import messagebox
import numpy as np


def get_client_config(sandbox=False):
    # 开发者信息获取
    client_config = TigerOpenClientConfig(sandbox_debug=sandbox)
    client_config.private_key = read_private_key('./data/private.key')
    client_config.tiger_id = '20151498'
    client_config.account = '20211023094922838'
    client_config.language = Language.zh_CN  # 可选，不填默认为英语'
    return client_config


# 调用上方定义的函数生成用户配置ClientConfig对象
client_config = get_client_config()

# 随后传入配置参数对象来初始化TradeClient
trade_client = TradeClient(client_config)

from tigeropen.common.consts import Market, SecurityType, Currency
from tigeropen.common.util.contract_utils import stock_contract

# 下单需要先初始化一个contract对象，contract对象中保存着合约信息，详情请见合约对象。创建contract对象的方法请参考文档 基本操作-交易类-获取合约 部分，示例如下：
# 方法1: 直接本地构造contract对象。 期货 contract 的构造方法请参考文档 基本操作-交易类-获取合约 部分
contract = stock_contract(symbol='TIGR', currency='USD')

# 方法2: 联网方式获取Contract对象，此方法仅针对股票
stock_contract = trade_client.get_contracts(symbol='SPY')[0]

# 以下为目前支持的几种订单类型对象
from tigeropen.common.util.order_utils import (market_order,  # 市价单
                                               limit_order,  # 限价单
                                               stop_order,  # 止损单
                                               stop_limit_order,  # 限价止损单
                                               trail_order,  # 移动止损单
                                               order_leg)  # 附加订单

# 创建订单对象，订单对象中保存了下单所需的账户、目标合约等信息，详情请见订单对象。这里以限价单为例
stock_order = market_order(account=client_config.account,  # 下单账户，可以使用标准、环球、或模拟账户
                           contract=stock_contract,  # 第1步中获取的合约对象
                           action='BUY',
                           quantity=100)

# 提交订单。注意：提交订单前，order对象的id为None, 提交成功后， order对象的id会变为全局订单id
trade_client.place_order(stock_order)

print(stock_order)
