import time
from tigeropen.common.consts import (Language,  # 语言
                                     Market,  # 市场
                                     BarPeriod,  # k线周期
                                     QuoteRight, SecurityType)  # 复权类型
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.trade.trade_client import TradeClient


def get_client_config(sandbox=False):
    # 开发者信息获取
    client_config = TigerOpenClientConfig(sandbox_debug=sandbox)
    client_config.private_key = read_private_key('./data/private.key')
    client_config.tiger_id = '20151498'
    client_config.account = '5565661'
    client_config.language = Language.zh_CN  # 可选，不填默认为英语'
    return client_config


client_config = get_client_config()
quote_client = QuoteClient(client_config)
trade_client = TradeClient(client_config)

all_symbols = quote_client.get_symbols(market=Market.US)
print(all_symbols)

print(all_symbols)
print(len(all_symbols))

# 市场所有股票分为60只一组
batch = [all_symbols[i:i + 60] for i in range(0, len(all_symbols), 60)]
print(len(batch))
print(batch)

result = []

for i in range(len(batch)):
    for item in batch[i]:

        try:
            contract = trade_client.get_contract(item, sec_type=SecurityType.STK)
            if contract.shortable == None:
                result.append(item)
        except:
            print('skip ' + item)

    print('result length = ' + str(len(result)))
    print('batch ' + str(i) + '/' + str(len(batch)))
    time.sleep(61)


def text_save(filename, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename, 'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存成功")


text_save('not_shortable_list.txt', result)