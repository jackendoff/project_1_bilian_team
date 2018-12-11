import requests
import random


class CoinData(object):
    '''
    获取订单簿数据，成交空间内双向成交
    '''

    def __init__(self, coin_name, level=None, depth_dict=None, me_space=None, min_order=None, trans_space_price=None):
        '''

        :param coin_name: 币对名字（str）
        :param level: 深度标签（str）
        :param depth_dict: 盘口深度（dict）
        :param me_space: 自定义成交空间（float）
        :param min_order: 自定义小单数量（float）
        :param trans_space_price: 真实成交空间（float）
        '''
        self.coin_name = coin_name
        self.order_price = None

        if level is None:
            self.level = 'full'
        else:
            self.level = level
        if depth_dict is None:
            self.depth_dict = {}
        else:
            self.depth_dict = depth_dict
        if me_space is None:
            self.me_space = 1
        else:
            self.me_space = me_space
        if min_order is None:
            self.min_order = 1
        else:
            self.min_order = min_order
        if trans_space_price is None:
            self.trans_space_price = 1
        else:
            self.trans_space_price = trans_space_price

    def get_coin_depth(self):
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
        url = 'https://api.fcoin.com/v2/market/depth/'+self.level+'/'+self.coin_name
        data = requests.get(url)
        result = data.content.decode()
        result_dict = eval(result)
        self.depth_dict = result_dict
        # print('depth_dict深度字典',self.depth_dict)
        return result_dict

    def get_price_amount(self,depth_dict=None):

        '''
        通过depth_dict 获取，bids_price_list,bids_amount_list,asks_price_list,asks_amount_list
        将深度字典拆包，返回bids_list_all，asks_list_all
        :return:
        '''
        if depth_dict is not None:
            self.depth_dict = depth_dict
        bids_price_list = []
        bids_amount_list = []
        asks_price_list = []
        asks_amount_list = []
        try:
            bids_list = self.depth_dict['data']['bids']
            asks_list = self.depth_dict['data']['asks']
            n= 1
            for data in bids_list:
                if n%2 != 0:
                    bids_price_list.append(data)
                else:
                    bids_amount_list.append(data)
                n += 1
            n = 1
            for data in asks_list:
                if n%2 != 0:
                    asks_price_list.append(data)
                else:
                    asks_amount_list.append(data)
                n += 1

            bids_list_all = [bids_price_list,bids_amount_list]
            asks_list_all = [asks_price_list,asks_amount_list]
            return bids_list_all, asks_list_all

        except:
            print('depth_dice数据未获取到,可能是空字典')

    def transaction_space(self,depth_dict=None):
        '''
        获取订单成交空间
        :param depth_dict:订单簿列表
        :return:trans_space_price:返回成交空间 (float)
        '''
        if self.depth_dict is None:
            print('depth_dict is None')
        if depth_dict is not None:
            self.depth_dict = depth_dict
        max_buy_price = self.depth_dict['data']['bids'][0]
        max_buy_amount = self.depth_dict['data']['bids'][1]

        min_asks_price = self.depth_dict['data']['asks'][0]
        min_asks_amount = self.depth_dict['data']['asks'][1]

        trans_space_price = min_asks_price - max_buy_price
        # trans_space_amount = min_asks_amount - max_buy_amount
        self.trans_space_price = trans_space_price
        # print('trans_space_price订单空间',self.trans_space_price)
        return trans_space_price

    def order_random(self,depth_dict=None):
        '''
        成交空间内随机下单价格
        :param result_dict: 订单簿数据（dict）
        :return: 返回生成的随机挂单价格（）
        '''
        if depth_dict is not None:
            self.depth_dict = depth_dict
        max_buy_price = self.depth_dict['data']['bids'][0]
        min_asks_price = self.depth_dict['data']['asks'][0]
        order_price = random.uniform(max_buy_price, min_asks_price)
        # print(max_buy_price, min_asks_price)
        self.order_price = order_price
        # print('order_price随机下单价格',self.order_price)
        return order_price

    def judge_trans_space(self, me_space=None, min_order=None):
        '''
        判断成交空间过小，则吃小压单，（大压单提示）
        :param me_space: 自定义成交空间大小（int）
        :param min_order: 自定义小单数量（int）
        :param depth_dict: 深度数据（dict）
        :param trans_space_price:
        :return:
        '''
        # 当成交空间过小，判断压单数量（min_asks_amount,max_buy_amount）
        if me_space is not None:
            self.me_space = me_space
        if min_order is not None:
            self.min_order = min_order
        # i = 0
        print('self.depth_dict',self.depth_dict)
        while self.trans_space_price < self.me_space:
            if self.depth_dict['data']['bids'][1] < self.min_order:
                print('eating bids')
                depth_dict = self.get_coin_depth()
                self.trans_space_price = self.transaction_space(depth_dict)
                continue
                pass
                # 吃单
            if self.depth_dict['data']['asks'][1] < self.min_order:
                print('eating')
                depth_dict = self.get_coin_depth()
                self.trans_space_price = self.transaction_space(depth_dict)
                pass
                # 吃单
            depth_dict = self.get_coin_depth()
            self.trans_space_price = self.transaction_space(depth_dict)

        pass


if __name__ == '__main__':
    coin_name = 'dageth'
    level = ['L20', 'L150', 'full']

    coin = CoinData(coin_name,level[0])
    dara1 = coin.get_coin_depth()

    price_list, amount_list = coin.get_price_amount()
    # depth_list = coin.get_price_amount()

    print('text_返回',price_list,type(price_list),'\n',amount_list,type(amount_list))


    dara1 = coin.get_coin_depth()
    dara2 = coin.transaction_space()
    dara3 = coin.order_random()
    print(dara1, dara2, dara3)
    coin.judge_trans_space(me_space=1, min_order=200000)

