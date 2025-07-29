"""
报表模块数据采集
"""

import json

from DrissionPage import Chromium
from requests import post

from ._dict import RequestData
from ._utils import get__date_utc


class Urls:
    goods_profit = 'https://ss.erp321.com/profit-report/goods-profit'


class DataPacketUrls:
    goods_profit = 'https://pf1.erp321.com/WebApi/PF/OrderSku/GetPFSkuList?uvalue=pfcweb_profit-report.goods-profit'


class Report:
    def __init__(self, browser: Chromium):
        self._browser = browser
        self._timeout = 15

    def __generate__combine_date(self, begin_date: str, end_date: str):
        """生成数据包查询所需要的 combine_date 值"""

        if begin_date == end_date:
            combine_begin_date = combine_end_date = get__date_utc(
                date=end_date, replace_with_nowtime=True
            )
        else:
            date_maps = [f'{begin_date} 00:00:00', f'{end_date} 23:59:59']
            combine_begin_date, combine_end_date = [
                get__date_utc(
                    date_map, pattern='%Y-%m-%d %H:%M:%S', replace_with_nowtime=False
                )
                for date_map in date_maps
            ]

        return combine_begin_date, combine_end_date

    def get__goods_profit__detail(
        self,
        shop_id: str,
        goods_ids: list[str],
        begin_date: str,
        end_date: str,
        raw=False,
        timeout: float = None,
    ):
        """
        获取商品利润数据

        Args:
            shop_id: 店铺ID
            goods_ids: 商品ID列表
            begin_date: 开始日期
            end_date: 结束日期
        Returns:
            数据对象: {商品id: {字段: 值, ...}, ...}
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        # 检查当前打开的页面中是否有胜算商品利润页面
        page = None
        for tab in self._browser.get_tabs():
            if Urls.goods_profit in tab.url:
                page = tab
                self._browser.activate_tab(page)
                break

        if page is None:
            page = self._browser.new_tab()
            page.change_mode('d', go=False)
            page.get(Urls.goods_profit)
            page.wait.eles_loaded('t:button@@text()=查 询', timeout=30)

        combine_begin_date, combine_end_date = self.__generate__combine_date(
            begin_date, end_date
        )

        reqdata = (
            RequestData.goods_profit.replace('$combine_begin_date', combine_begin_date)
            .replace('$combine_end_date', combine_end_date)
            .replace('$shop_id', str(shop_id))
            .replace('$goods_ids', json.dumps(goods_ids))
            .replace('$begin_date', begin_date)
            .replace('$end_date', end_date)
        )
        reqdata_json = json.loads(reqdata)
        resp = post(
            DataPacketUrls.goods_profit,
            json=reqdata_json,
            timeout=_timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
                'Content-Type': 'application/json;charset=UTF-8',
                'Cookie': page.cookies().as_str(),
                'Referer': Urls.goods_profit,
            },
        )
        try:
            resp_json: dict = resp.json()
        except Exception as e:
            raise ValueError(f'商品利润数据包格式化出错: {e}') from e

        if 'data' not in resp_json:
            raise ValueError('商品利润数据包中未找到 data 字段')
        data = resp_json['data']

        if raw is True:
            return data

        if not isinstance(data, dict):
            raise ValueError('商品利润数据包中 data 字段非预期 dict 类型')

        if 'fldHeads' not in data:
            raise ValueError('商品利润数据包中未找到 data.fldHeads 字段')
        heads: list[dict] = data['fldHeads']
        if not isinstance(heads, list):
            raise ValueError('商品利润数据包中 data.fldHeads 字段非预期 list 类型')

        if 'dataList' not in data:
            raise ValueError('商品利润数据包中未找到 data.dataList 字段')
        data_list: list[dict] = data['dataList']
        if not isinstance(data_list, list):
            raise ValueError('商品利润数据包中 data.dataList 字段非预期 list 类型')

        titles = {head.get('fld'): head.get('title') for head in heads}
        records = {}
        for item in data_list:
            goods_id = item.get('primaryKey')
            record = {}
            for key, title in titles.items():
                value = item.get(key)
                record[title] = value
            records[goods_id] = record

        return records
