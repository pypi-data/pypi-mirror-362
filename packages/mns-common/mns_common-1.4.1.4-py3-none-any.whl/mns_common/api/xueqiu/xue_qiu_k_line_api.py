import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import requests
import pandas as pd


# year 年
#  quarter 季度
# month 月度
# week 周
# day 日
def get_xue_qiu_k_line(symbol, period, cookie, end_time, hq):
    url = "https://stock.xueqiu.com/v5/stock/chart/kline.json"

    params = {
        "symbol": symbol,
        "begin": end_time,
        "period": period,
        "type": hq,
        "count": "-120084",
        "indicator": "kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance"
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "origin": "https://xueqiu.com",
        "priority": "u=1, i",
        "referer": "https://xueqiu.com/S/SZ300879?md5__1038=n4%2BxgDniDQeWqxYwq0y%2BbDyG%2BYDtODuD7q%2BqRYID",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "cookie": cookie
    }

    response = requests.get(
        url=url,
        params=params,
        headers=headers
    )

    if response.status_code == 200:
        response_data = response.json()
        df = pd.DataFrame(
            data=response_data['data']['item'],
            columns=response_data['data']['column']
        )

        # 1. 转换为 datetime（自动处理毫秒级时间戳）
        df["beijing_time"] = pd.to_datetime(df["timestamp"], unit="ms")

        # 2. 设置 UTC 时区
        df["beijing_time"] = df["beijing_time"].dt.tz_localize("UTC")

        # 3. 转换为北京时间（UTC+8）
        df["beijing_time"] = df["beijing_time"].dt.tz_convert("Asia/Shanghai")

        # 4. 提取年月日（格式：YYYY-MM-DD）
        df["str_day"] = df["beijing_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
        del df["beijing_time"]

        return df
    else:
        # 直接抛出带有明确信息的异常
        raise ValueError("调用雪球接口失败")


if __name__ == '__main__':
    number = 1
    cookies ='cookiesu=431747207996803; device_id=e7bd664c2ad4091241066c3a2ddbd736; xq_is_login=1; u=9627701445; s=ck12tdw0na; bid=7a2d53b7ab3873ab7ec53349413f0a21_mb9aqxtx; xq_a_token=287767c9ca1fce01ce3022eceec5e0ce14f77840; xqat=287767c9ca1fce01ce3022eceec5e0ce14f77840; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjk2Mjc3MDE0NDUsImlzcyI6InVjIiwiZXhwIjoxNzU0NzkxNTExLCJjdG0iOjE3NTIxOTk1MTE2OTYsImNpZCI6ImQ5ZDBuNEFadXAifQ.lAu_FRmvtIgHoK08PJo-a2RPBXiEd7mYp_Iw6S18CIciREuHnGsGkSRz64ZziGD4HRH3_tu8I24DZ1zFHTujFD2t6MBVVFGdN7JV6mhw0JJos2sgIAr6ykm3KJ9rNqiBeSQ1OGBm-5NC5kV3CJNZJj7YICJLJIjKx7940T1TFa3q5gxdDsg2UaRuWprW7cwLp3wtF7NUZ6Kv-OE9C-VaeNlosIFrs5fv1Egp5C5v4INGEK2WwKrhI7GBqfUvWSXXAw4Y-i1UiDVA2L1P_jJgLxvD-ObwgaB40H9hEXd9GpioObTeL1fVylZUpCBO3U03kMBoWj3IBIalEv4jwMIY7Q; xq_r_token=46ef264c7236f56849c570ed35df3f676411df2e; Hm_lvt_1db88642e346389874251b5a1eded6e3=1752069757,1752199513,1752240695,1752299269; HMACCOUNT=16733F9B51C8BBB0; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1752299406; ssxmod_itna=QqjOAKYIwGkYDQG0bGCYG2DmxewDAo40QDXDUqAQtGgnDFqAPDODCOGKD5=RmIqOOaflxRhxaGi+DtzDBkxoDSxD=7DK4GTmGZxHRet3UY2TO=fmGmQY1sUi9TCoGnlThvi0ce7pxMOLH4dlrCRiBCvrRDmD0aDmKDU=GQfpeDxhPD5xDTDWeDGDD37xGaDmeDeOfpD0RvpISfsIo3D7eDXxGC7GRjDiPD7ZgC5D2v/SAAiDDziBQeo7PtRDi3s+fwg+4KDiyDA3BvD7y3DlcxpkQD0OtSiB3fsdYc=pg6y40OD0FXI4oKniW0baF+8fhiK+eorKQgDNODoD5qx4PBqmBqIx8=GhsAx3R4RGDoYeYG53lmoxDir+/C2T/x0i4MpN/ZoVxib0eOB5KKAIj2ICDbADYnDvcGgAKzBq/QmrSG3QWhD+=/wTKexD; ssxmod_itna2=QqjOAKYIwGkYDQG0bGCYG2DmxewDAo40QDXDUqAQtGgnDFqAPDODCOGKD5=RmIqOOaflxRhxaGi+DtbDG+vjq3Vlx03rNW=rWDlp=bcqab0PF44a5YTk4YCHqE8wxCsmUS5So/mA3QCBr9DZxq8sCGHaPHeCgGFO=iqChTC=mIzkE78s0cFD8IaqA5e2xSIC2vsD381/69xUOpEjbAQhRoQFFBwU=uvA=DUL=wFaYOsd+TwaGH08owPCaS8BYgQTkYxpoq80QiCxHKrs3qeDIDthNu0fpFXeQQyUHF4PByzukFk/P8XtqUQ3wZDyMFq//IBFTgRy/79xinsnmStweMPiUuGeAa7K4ZIxxFX8iCRR58DOmaV8WFIPO9uDUH3dH6DFPSmQzE5vyxnplRBvj4xYqGDYf4qEf4tb8vR4B8OyFq4PpLI5pI34L58FpktuYEfp4PO3as3EnlurQAgBbMQqeje4VDuCkdubsfGRYFpYuQ4a8ndaBH/j5QDLKL7hhmVQW/jPKcLlYB9iqmyLFUeZjb4Sw83qGGeeHBdM7I0Qe4YRzFDp2gCkj+u=MMmi88UkILCKh2xjRmoGmh1esOZfEOGwXue2U1Xr09Yz5kHTEHyFpwPdYyI7M5N0xbY2ynROXRbn+91uGlzPW7B5bv+w2CkqDWqGI9f1MTuMr8PYxob4VohQBhNDe4xse4=i/csV5VoDD'
    while True:
        test_df = get_xue_qiu_k_line('SZ000001', '1m', cookies, '1752385814699', '')
        print(number)
        number = number + 1
