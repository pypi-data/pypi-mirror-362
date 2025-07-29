from xtquant import xtdata
import pandas as pd
from loguru import logger


# 获取股票实时行情数据
def get_qmt_real_time_quotes(symbol_list):
    try:
        res = xtdata.get_full_tick(symbol_list)
        records = []
        for symbol, stock_data in res.items():
            record = stock_data.copy()  # 创建字典副本避免修改原始数据
            record['symbol'] = symbol  # 添加股票代码列
            records.append(record)  # 添加到列表
        # 一次性转换为DataFrame
        real_time_quotes_df = pd.DataFrame(records)
        return real_time_quotes_df
    except BaseException as e:
        logger.error("获取实时行情出现异常:{}", e)


if __name__ == '__main__':
    while True:
        symbol_list_test = ['600051.SH', '605090.SH', '600025.SH', '601222.SH', '688031.SH', '603335.SH', '688045.SH',
                            '603341.SH', '600967.SH', '603237.SH', '688528.SH', '688133.SH', '603658.SH', '600865.SH']
        df = get_qmt_real_time_quotes(symbol_list_test)
        logger.info('test')
