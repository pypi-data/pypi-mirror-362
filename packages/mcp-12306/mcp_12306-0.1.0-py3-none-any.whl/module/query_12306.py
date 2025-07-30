from datetime import timedelta, datetime, date
import requests
from typing import List, Dict, Any
import os
import json
import logging
import aiohttp
import asyncio
from collections import defaultdict

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s', filename="query_12306.log", filemode="a")

TICKET_QUERY_URL = "https://kyfw.12306.cn/otn/leftTicket/queryU"
INDEX_URL = "https://kyfw.12306.cn"

arrive_map = {
    0: "当日到达",
    1: "次日到达",
    2: "两日到达",
    "default": "多日到达"
}
seat_map = {
    "9": "business_seat",
    "M": "first_class_seat",
    "O": "second_class_seat",
    "D": "premium_first_class_seat",
    "3": "hard_sleep",
    "4": "soft_sleep",
    "1": "hard_seat",
}
english_to_chinese_map = {
    "business_seat": "商务座",
    "first_class_seat": "一等座",
    "second_class_seat": "二等座",
    "premium_first_class_seat": "优选一等座",
    "hard_sleep": "硬卧",
    "soft_sleep": "软卧",
    "hard_seat": "硬座",
    "no_seat": "无座",
}
purpose_codes = {
    "student": "0X00",
    "adult": "ADULT"
}

class TrainInfoQuery():
    def __init__(self):
        self.station_name_dict, self.station_code_dict, self.city_station_dict = self.get_station_dict()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        
    @staticmethod
    def filter_train_info(query: dict, result: List[dict[str, Any]]) -> List[dict[str, Any]]:
        """
        根据查询条件，过滤车次信息
        """
        def match_query(query: dict, data: dict[str, Any]) -> bool:
            # 出发站
            if query.get("from_station") and data.get("from_station") != query.get("from_station"):
                return False
            # 到达站
            if query.get("to_station") and data.get("to_station") != query.get("to_station"):
                return False
            # 出发日期
            if query.get("start_date") and data["start_date"] != query.get("start_date"):
                return False
            # 车次
            if query.get("train_no") and data.get("train_no") != query.get("train_no"):
                return False
            # 车辆类型
            train_type = query.get("train_type")
            if train_type:
                train_type_list = train_type.split("|")
                if len(train_type_list) > 0 and data["train_no"][0] not in train_type_list:
                    return False
            # 座位类型：商务座，一等座，二等座，优选一等座，硬卧，软卧，硬座，无座
            # 同时筛选：有票，只看有座（避免无座）
            seat_type = query.get("seat_type")
            has_seat = query.get("avoid_no_seat", False)
            has_ticket = query.get("has_seat", False)
            ticket_remain = 0
            seat_remain = 0
            if seat_type:
                seat_type_list = seat_type.split("|")
                if len(seat_type_list) > 0:
                    for seat_type in seat_type_list:
                        if seat_type in seat_map:
                            remain = data[seat_type].get("remain", 0)
                            if seat_type != "no_seat":
                                seat_remain += remain
                            ticket_remain += remain
            # 筛选有座
            if has_seat and not seat_remain:
                return False
            # 筛选有票
            if has_ticket and not ticket_remain:
                return False
            return True
        return [data for data in result if match_query(query, data)]

    @staticmethod
    def valid_name(name: str) -> str:
        """
        验证车站或城市名称
        """
        if name[-1] == "站":
            name = name[:-1]
        elif name[-1] == "市":
            name = name[:-1]
        if not name:
            raise ValueError(f"Invalid station name: {name}")
        return name

    def get_station_code_by_name(self, name: str) -> str:
        """
        根据车站名称，返回车站代码
        """
        query_name = self.valid_name(name)
        if query_name in self.station_name_dict:
            return self.station_name_dict[query_name]["code"]
        raise ValueError(f"Invalid station name: {name}")

    def get_stations_in_city(self, city: str) -> List[tuple[str, str]]:
        """
        根据城市名，以元组(代码, 名称)形式，返回车站代码和车站名称
        """
        city = self.valid_name(city)
        stations = []
        for k, v in self.city_station_dict.items():
            if k == city:
                stations.append(v)
        return stations
    
    def is_date_can_query(self, query_date: str) -> bool:
        """
        判断日期是否可以查询到车辆信息
        """
        end_date = datetime.strptime(query_date, "%Y-%m-%d") + timedelta(days=13)
        return query_date >= date.today().strftime("%Y-%m-%d") and query_date <= end_date.strftime("%Y-%m-%d")
    
    @staticmethod
    def get_station_dict() -> tuple[Dict[str, Dict[str, str]], Dict[str, Dict[str, str]], Dict[str, List[tuple[str, str]]]]:
        """从本地station.txt读取12306车站名与车站代码的详细信息映射字典"""
        station_file = os.path.join(os.path.dirname(__file__), "station.txt")
        with open(station_file, "r", encoding="utf-8") as f:
            text = f.read()
        # 车站信息以@开头，|||结尾
        import re
        pattern = re.compile(r'@([^@]+?)\|\|\|')
        matches = pattern.findall(text)

        station_name_dict = {}
        station_code_dict = {}
        city_station_dict = defaultdict(list)
        for item in matches:
            parts = item.split('|')
            if len(parts) >= 8:
                station_info = {
                    "short_code": parts[0],
                    "name": parts[1],
                    "code": parts[2],
                    "pinyin": parts[3],
                    "abbr": parts[4],
                    "id1": parts[5],
                    "id2": parts[6],
                    "city": parts[7],
                }
                # 车站代码:Dict[str, str]
                station_name_dict[station_info["name"]] = station_info
                station_code_dict[station_info["code"]] = station_info
                city_station_dict[station_info["city"]].append((station_info["code"], station_info["name"]))
            else:
                print(f"Invalid station info: {item}")
                continue
        
        return station_name_dict, station_code_dict, city_station_dict

    @staticmethod
    def parse_12306_result(result_str: str) -> dict[str, Any]:
        """解析12306网站返回结果"""
        all_data_list = result_str.split("|")
        # 解析座/铺位和价格信息
        parse_price_dict = TrainInfoQuery.parse_price(all_data_list[39])
        # 列车到达信息：当日到达，次日到达，两日到达，... arrive_day: 0:当天，1:次日，2:两日...
        arrive_info, arrive_day = TrainInfoQuery.arrive(start_time=all_data_list[8], duration=all_data_list[10])  
        # 列车出发日期：20250712
        start_date = all_data_list[13]
        # 1. 将字符串转换为 datetime 对象（先按原始格式解析）
        start_date = datetime.strptime(start_date, "%Y%m%d")
        # 2. 计算加上 arrive_day 天后的日期（arrive_day 为整数，如 3 表示加 3 天）
        arrive_date = start_date + timedelta(days=arrive_day)
        # 3. 格式化为 YYYY-MM-DD 字符串
        arrive_date = arrive_date.strftime("%Y-%m-%d")
        start_date = start_date.strftime("%Y-%m-%d")
        trains_dict = {
            "train_no": all_data_list[3],
            "start_time": all_data_list[8],
            "arrive_time": all_data_list[9],
            "duration": all_data_list[10],
            "seat_price": parse_price_dict,
            "arrive_info": arrive_info,
            "start_date": start_date,
            "arrive_date": arrive_date
        }
        return trains_dict

    @staticmethod
    def arrive(start_time: str, duration: str) -> tuple[str, int]:
        """
        解析列车到达信息：当日到达，次日到达，两日到达，...
        """
        minute = int(start_time.split(":")[1]) + int(duration.split(":")[1])
        hour = (minute // 60) + int(start_time.split(":")[0])
        minute = minute % 60
        arrive_day = hour // 24
        arrive_info = arrive_map.get(arrive_day, arrive_map["default"])
        return arrive_info, arrive_day

    def get_station_name_by_code(self, code: str) -> List[tuple[str, str]]:
        """通过城市中文名获取车站代码，如：南京南->NkH"""
        city_station = []
        for k, v in self.city_station_dict.items():
            if k == code:
                city_station.append(v)
        return city_station

    async def query_train_info(self, train_no: str) -> List[Dict[str, Any]]:
        """
        根据车次信息查询车次信息，包括途径站（车站中文名，出发时间，到达时间，历时，停靠时间）信息，不包含价格信息
        """
        try:
            params = {
                "train_no": train_no,
            }
            async with aiohttp.ClientSession() as session:
                resp = await session.get(TICKET_QUERY_URL, params=params, headers=self.headers)
                data = await resp.json()
                print(resp.text)
                # TODO 这里要改成返回途径站信息
                return []
        except Exception as e:
            logging.error(f"query:查询车次信息失败: {e}", exc_info=True)
            return []

    async def query_left_tickets(
        self,
        from_station: str = "NKH",
        to_station: str = "HKN",
        train_date: str = date.today().strftime("%Y-%m-%d"),
        purpose_codes: str = "ADULT",
    ) -> List[Dict[str, Any]]:
        """
        查询余票信息
        :param from_station: 出发站代码
        :param to_station: 到达站代码
        :param train_date: 出发日期，格式YYYY-MM-DD
        :param purpose_codes: 乘客类型，ADULT/0X00（学生票）
        :return: 车次信息列表
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        query_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Referer": "https://kyfw.12306.cn/index/",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
        }
        params = {
            "leftTicketDTO.train_date": train_date,
            "leftTicketDTO.from_station": from_station,
            "leftTicketDTO.to_station": to_station,
            "purpose_codes": purpose_codes
        }
        print(params)
        try:
            session = aiohttp.ClientSession()
            # 先访问主页，获取 Cookie
            async with session.get(INDEX_URL, headers=headers) as resp:
                await resp.text()  # 触发 Cookie 存储
            async with session.get(INDEX_URL, headers=headers) as resp:
                # 再访问查询接口
                resp = await session.get(TICKET_QUERY_URL, params=params, headers=query_headers)
                print("响应状态码:", resp.status)
                data = await resp.json()
        except Exception as e:
            logging.error(f"request:请求查询车票信息失败: {e}", exc_info=True)
            raise Exception("request:请求查询车票信息失败")
        
        result = []
        try:
            for raw in data.get("data", {}).get("result", []):
                processed = TrainInfoQuery.parse_12306_result(raw)
                result.append(processed)
        except Exception as e:
            logging.error(f"parse:解析查询车票信息失败: {e}", exc_info=True)
            raise Exception("parse:解析查询车票信息失败")
        return result

    @staticmethod
    def parse_price(price_str: str) -> dict[str, dict[str, int]]:
        """
        解析12306票价字符串，每10个字符为一组，返回票种、票价、余票量的字典
        例： '9060000000M0319000000O0200000000D0440000000O020003065'
        """
        # 根据列车类型获取座位代号与类型映射
        result = {}
        n = len(price_str) // 10
        for i in range(n):
            seg = price_str[i*10:(i+1)*10]
            if len(seg) < 10:
                continue
            seat_code = seg[0]
            price = int(seg[1:5])
            no_seat = int(seg[5:7]) == 3
            remain = int(seg[7:10])
            seat_type = seat_map.get(seat_code)
            if not seat_type:
                continue
            # 先处理无座（O开头且余票不为0，且不是二等座）
            if (seat_code == "O" or seat_code == '1') and no_seat:
                result["no_seat"] = {"price": price, "remain": remain}
            else:
                result[seat_type] = {"price": price, "remain": remain}
        return result

if __name__ == "__main__":
    station_name_dict, station_code_dict, city_station_dict = TrainInfoQuery.get_station_dict()
    print(station_name_dict)
    # 测试余票查询
    async def main():
        result = await TrainInfoQuery().query_left_tickets("NKH", "HKN", "2025-07-17")
        result = TrainInfoQuery.filter_train_info(query={}, result=result)
        print(result)
    asyncio.run(main())
