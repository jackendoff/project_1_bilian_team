import requests
import random

def get_coin_depth(coin_name, level):
    '''
    获取订单簿数据
    :param coin_name:币对名称（str）
    :param level:订单深度，有（str）'L20','L150','full'
    :return:返回订单深度字典
    {
  "status":0,
  "data":{
    "type": "depth.L20.ethbtc",
    "ts": 1523619211000,
    "seq": 120,
    "bids": [0.000100000, 1.000000000, 0.000010000, 1.000000000],奇数是价格
    "asks": [1.000000000, 1.000000000]
  }
}
    '''
    # url = 'https://api.fcoin.com/v2/public/server-time'
    url = 'https://api.fcoin.com/v2/market/depth/'+level+'/'+coin_name
    data = requests.get(url)
    result = data.content.decode()
    result_dict = eval(result)
    return result_dict


def  transaction_space(depth_dict):
    '''
    获取订单成交空间
    :param depth_dict:订单簿列表
    :return:trans_space_price:返回成交空间 (float)
    '''
    max_buy_price = depth_dict['data']['bids'][0]
    max_buy_amount = depth_dict['data']['bids'][1]

    min_asks_price = depth_dict['data']['asks'][0]
    min_asks_amount = depth_dict['data']['asks'][1]

    trans_space_price = min_asks_price - max_buy_price
    # trans_space_amount = min_asks_amount - max_buy_amount
    return trans_space_price


def order_random(depth_dict):
    '''
    成交空间内随机下单价格
    :param result_dict: 订单簿数据（dict）
    :return: 返回生成的随机挂单价格（）
    '''
    max_buy_price = depth_dict['data']['bids'][0]
    min_asks_price = depth_dict['data']['asks'][0]
    order_price = random.uniform(max_buy_price, min_asks_price)
    print(max_buy_price, min_asks_price)
    return order_price


def judge_trans_space(me_space, trans_space_price):
    '''
    判断成交空间过小，且则吃小压单，（大压单提示）
    :param me_space: 自定义成交空间大小（）
    :param trans_space_price:
    :return:
    '''
    pass


if __name__ == '__main__':
    coin_name = 'dageth'
    level = ['L20', 'L150', 'full']

    # 获取dag/eth订单簿
    data_dict = get_coin_depth(coin_name, level[2])
    # print(data_dict,type(data_dict))
    # 获取成交价格空间
    trans_space_price = transaction_space(data_dict)
    print(trans_space_price,type(trans_space_price))
    # 获取随机下单价格
    order_price = order_random(data_dict)
    print(order_price)