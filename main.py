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


# 涨跌幅计算方法为(现价 - 前价) / 前价
def change_rate(symbol):
    return (symbol.latest_price - symbol.high) / symbol.high


# 检查每一只股票的最后一个最高点的时间是否早于最后一个最低点
def filter(pre_filtered, pre_filtered_symbols):
    # 获取数据
    result = quote_client.get_timeline(pre_filtered_symbols, include_hour_trading=True, begin_time=-1, lang=None)

    filtered = []
    for symbol in pre_filtered_symbols:
        # 从结果中筛选出单只股票的结果
        details = result[result.symbol == symbol]

        time_min = details[details.price == details.price.min()].values[-1][1]
        time_max = details[details.price == details.price.max()].values[-1][1]

        if time_max < time_min:
            for each in pre_filtered:
                if each[0] == symbol:
                    filtered.append(each)

    return filtered


client_config = get_client_config()
quote_client = QuoteClient(client_config)
trade_client = TradeClient(client_config)

all_symbols = quote_client.get_symbols(market=Market.US)
print(all_symbols)
#
# filtered_list = []
#
# # 筛选股票
# # for each in all_symbols:
# #     if not each.endswith('.WS') and not each.endswith('W') and not '.' in each:
# #         filtered_list.append(each)
#
# print(all_symbols)
# print(len(all_symbols))
#
# # 市场所有股票分为50只一组
# batch = [all_symbols[i:i + 50] for i in range(0, len(all_symbols), 50)]
# print(len(batch))
#
# result_symbols = []
#
# # 把全市场50*227只股票分为两组，一组50*113，另一组50*114
# batch1 = batch[:len(batch) // 2]
# batch2 = batch[len(batch) // 2:]
# print(len(batch1))
# print(len(batch2))
#
# # 跌幅
# changerate = -0.35
#
#
# def date_format(millisecond):
#     time = datetime.datetime.fromtimestamp(millisecond / 1e3)
#     return time
#
#
# def draw_MACD(df):
#     plt.figure(figsize=(12.2, 4.5))
#     plt.plot(df.index, df['MACD'], label='MACD', color='red')
#     plt.plot(df.index, df['Signal Line'], label='Signal Line', color='blue')
#     plt.xticks(rotation=45)
#     plt.legend(loc='upper left')
#     plt.show()
#
#
# def calculate_MACD(df, column_name):
#     ShortEMA = df[column_name].ewm(span=12, adjust=False).mean()
#     LongEMA = df[column_name].ewm(span=26, adjust=False).mean()
#     MACD = ShortEMA - LongEMA
#     signal = MACD.ewm(span=9, adjust=False).mean()
#     df['MACD'] = MACD
#     df['Signal Line'] = signal
#     return df
#
#
# df = quote_client.get_timeline(['AAPL'], include_hour_trading=False, begin_time=-1, lang=None)
#
# '''
# Date = df.time.apply(lambda x: date_format(x))
# df['date'] = Date
# df.set_index(pd.DatetimeIndex(df['date'].values))
#
# k_3_mins = pd.DataFrame(df.groupby(np.arange(len(df)) // 3)['price'].agg(['min']))
# # df_max.to_csv('3-min.csv')
# df_min = calculate_MACD(k_3_mins, 'min')
#
# print(k_3_mins)
# print('-------------------------------')
# draw_MACD(k_3_mins)
# '''
# # # 画k线图
# # plt.figure(figsize=(15, 8))
# # plt.plot(df_max['price'], label='price')
# # plt.xticks(rotation=45)
# # plt.title('Close Price History')
# # plt.xlabel('date')
# # plt.ylabel('Price USD ($)')
# # plt.show()
#
# '''
# # 画k线图
# plt.figure(figsize=(15, 8))
# plt.plot(df['price'], label='price')
# plt.xticks(rotation=45)
# plt.title('Close Price History')
# plt.xlabel('date')
# plt.ylabel('Price USD ($)')
# plt.show()
#
# '''
#
# '''
# # 计算MACD
# ShortEMA = df.price.ewm(span=12, adjust=False).mean()
# LongEMA = df.price.ewm(span=26, adjust=False).mean()
# MACD = ShortEMA - LongEMA
# signal = MACD.ewm(span=9, adjust=False).mean()
#
# # 画MACD
# plt.figure(figsize=(12.2, 4.5))
# plt.plot(df.index, MACD, label='AAPL MACD', color='red')
# plt.plot(df.index, signal, label='Signal Line', color='blue')
# plt.xticks(rotation=45)
# plt.legend(loc='upper left')
# plt.show()
#
# '''
#
# # 一分钟可以请求
# # 获取并筛选batch1中最高点到现价跌幅超过x的股票
# # for i in range(len(batch1)):
# #     print(i)
# #     result1 = quote_client.get_timeline(batch1[i], include_hour_trading=True, begin_time=-1, lang=None)
# #     print(result1)
# #     result1.to_csv('.\\test\\' + str(i) + '.csv')
# # for index, symbol in result1.iterrows():
# #     if symbol.high != 0 and symbol.latest_price != 0 and change_rate(symbol) < changerate:
# #         new = [symbol.symbol, change_rate(symbol)]
# #         if not result_symbols.__contains__(symbol.symbol):
# #             result_symbols.append(symbol.symbol)
# #             messagebox.showinfo('目标出现！', new[0] + str(new[1]))
# #             print(new)
# for i in range(len(batch2)):
#     print(i)
#     result1 = quote_client.get_timeline(batch2[i], include_hour_trading=True, begin_time=-1, lang=None)
#     print(result1)
#     result1.to_csv('.\\test2\\' + str(i) + '.csv')
# # time.sleep(61)
# # 获取并筛选batch2中最高点到现价跌幅超过x的股票
# # for i in range(len(batch2)):
# #     result2 = quote_client.get_stock_briefs(batch2[i], lang=None)
# #     for index, symbol in result2.iterrows():
# #         if symbol.high != 0 and symbol.latest_price != 0 and change_rate(symbol) < changerate:
# #             new = [symbol.symbol, change_rate(symbol)]
# #             if not result_symbols.__contains__(symbol.symbol):
# #                 result_symbols.append(symbol.symbol)
# #                 messagebox.showinfo('目标出现！', new[0] + str(new[1]))
# #                 print(new)
#
# # time.sleep(61)
