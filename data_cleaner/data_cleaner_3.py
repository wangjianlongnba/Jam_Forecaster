# coding:utf-8
from pymongo import MongoClient
import time
import json
import requests
import pandas as pd
import numpy as np


class DataCleaner():
    """
    数据清洗器
    """

    def __init__(self):
        """
        初始化
        """
        self.client = MongoClient()
        self.db = self.client.jam_forecaster
        # 全局可用地点集
        self.positions = ['昌化路1223621,3627,3628', '昌化路302-3628,-3627,-3621', '曲阜路112585,2586', '曲阜路191-2586,-2585', '洛川中路285609,5610,5611', '武定路264779,4780,4794,4796,4797', '西藏中路294-444,-443,-441,-440,-439', '武定路206-4797,-4796,-4794,-4780,-4779', '洛川中路208-5611,-5610,-5609', '恒丰路296-205,-207,-208,-209,-210', '恒丰路116210,209,208,207,205', '西藏中路114439,440,441,443,444', '新闸路203-3413,-3405,-3402,-3394,-3393', '新闸路233393,3394,3402,3405,3413', '南昌路214075,4085', '南昌路200-4085,-4075', '大统路273-2224,-4849', '中潭路1153632,3633', '中潭路295-3633,-3632', '海防路263384,3388', '海防路206-3388,-3384', '昌平路253568,4805', '昌平路206-4805,-3568', '福建中路293-4895,-3848,-3847', '天目东路212114,2113', '天目东路200-2113,-2114', '人民大道37420,419', '人民大道218-419,-420', '合肥路162701,2703', '株洲路973927,3930', '株洲路278-3930,-3927', '会文路1274995,4221', '会文路307-4221,-4995', '武胜路154023,4028,4030', '长寿路218-479,-480,-481,-4412,-3346,-483,-484', '天目西路183-1116,-194,-193,-192,-191', '宝山路871718,1714,1713,1711', '河南北路292-910,-909,-4494,-908', '河南北路112908,4494,909,910', '宝山路267-1711,-1713,-1714,-1718', '虬江路202-3940,-3938,-3936,-3935', '柳营路332034,5225,2033,2032,2031', '浙江北路286-3780,-3779,-3778,-3777', '天目中路12196,197,4646,199', '河南中路106903,904,906,2042', '岚皋路1001621,2109,2110,1625', '长寿路38484,483,3346,4412,481,480,479', '浙江北路1083777,3778,3779,3780', '恒通路210-6085,-6084,-6083,-6082', '广中路170-1258,-1257,-3931,-1254', '柳营路213-2031,-2032,-2033,-5225,-2034', '宜昌路209-3638,-3636,-4808', '天目西路3191,192,193,194,1116', '恒通路306082,6083,6084,6085', '虬江路153935,3936,3938,3940', '安远路205-4792,-4580,-4374,-3579', '同心路1364267,4266,3553,3554', '岚皋路279-1625,-2110,-2109,-1621', '海宁路22638,639,640,641,4483,642,643', '延长中路312416,2417,2419']
        # 全局可用时间集
        self.time_points = {}
        # 初始化日期遍历list
        date_list = [(6, d) for d in range(1, 11)]+[(5, 1), (5, 3)]
        # 初始化时分遍历list
        time_list = [(m, s) for m in range(0, 24) for s in range(0, 60)]

        # 全局数据df
        self.df = pd.DataFrame(columns = self.positions)


    def run(self):
        """
        清理器主程序
        """
        # 初始化，全部数据都有，就开始
        i = 0
        begin_flag = 0
        while begin_flag == 0:
            begin_flag = 1
            # 后移一格
            i += 1
            for position in self.positions:
                piece = self.db.traffic_3.find_one({"identity": position, "i": i})
                begin_flag *= (piece!=None)
            print("第{}次排除".format(i))
        print("从第{}次开始".format(i))

        # 开始收集，全部数据都没有，就结束，其余时间补缺
        end_flag = 0
        while end_flag == 0:
            end_flag = 0
            row = []
            for position in self.positions:
                piece = self.db.traffic_3.find_one({"identity": position, "i": i})
                if piece:
                    speed = piece['speed']
                    row.append(speed)
                    # 不会终止
                    end_flag = 0
                else:
                    # 补缺
                    speed = self.df[position][i-1]
                    row.append(speed)
                    print("{}补缺".format(position))
            print("第{}次完成".format(i))
            # 后移一格
            i += 1
            # 添加到全局数据df
            self.df.loc[i] = row

        print("完成清洗，df长度{}".format(len(self.df)))
        print(self.df)

        self.df.to_csv("./data.csv")


if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.run()