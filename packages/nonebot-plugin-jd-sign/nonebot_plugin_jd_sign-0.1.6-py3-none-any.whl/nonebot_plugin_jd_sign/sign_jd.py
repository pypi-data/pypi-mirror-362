import asyncio
from httpx import AsyncClient
from loguru import logger


# 签到
async def signBeanAct(pt_pin: str, pt_key: str):
    logger.info(f"开始京东签到任务：{pt_pin}")
    result = {"code": 400, "msg": f"{pt_pin} 签到失败"}

    meta = {
        "method": "POST",
        "url": "https://api.m.jd.com/client.action",
        "data": {
            'functionId': 'signBeanAct',
            'body': '{}',
            'appid': 'signed_wh5_ihub',
            'client': 'android',
            'clientVersion': '15.1.55',
        },
        "headers": {
            "User-Agent": "jdapp",
            "Referer": "https://pro.m.jd.com",
        },
        "cookies": {
            "pt_key": pt_key,
            "pt_pin": pt_pin
        }
    }

    try:
        async with AsyncClient(headers=meta["headers"], cookies=meta["cookies"], timeout=15) as client:
            res = await client.post(meta["url"], data=meta["data"])
            if res.status_code == 200:
                json_data = res.json()
                if json_data.get("errorMessage"):
                    logger.warning(f"{pt_pin} 签到失败，pt_key 可能已过期")
                    result["msg"] = f"{pt_pin} 登录失效"
                else:
                    status = json_data.get("data", {}).get("status")
                    beanUserType = json_data.get("data", {}).get("beanUserType")
                    continuousDays = json_data.get("data", {}).get("continuousDays")
                    if status == "1":
                        if beanUserType == 2:
                            count = json_data.get("data", {}).get("newUserAward", {}).get("awardList")[0].get(
                                "beanCount")
                            result.update({"code": 200,
                                           "msg": f"{pt_pin} 签到成功，获得京豆：{count or '无'}，连续签到天数：{continuousDays or '无'}"})
                        elif beanUserType == 1:
                            count = json_data.get("data", {}).get("dailyAward", {}).get("beanAward").get(
                                "beanCount")
                            result.update({"code": 200,
                                           "msg": f"{pt_pin} 签到成功，获得京豆：{count or '无'}，连续签到天数：{continuousDays or '无'}"})
                    else:
                        result.update({"code": 200, "msg": f"{pt_pin} 今天已签到"})
            else:
                result["msg"] = f"{pt_pin} 请求失败"
    except Exception as e:
        logger.error(f"{pt_pin} 签到异常: {e}")
        result["msg"] = f"{pt_pin} 签到异常"

    logger.info(result["msg"])
    return result


# 查询
async def findBeanSceneNew(pt_pin: str, pt_key: str):
    # logger.info(f"开始京东签到任务：{pt_pin}")
    result = {"code": 400, "msg": f"{pt_pin} 签到失败"}

    meta = {
        "method": "POST",
        "url": "https://api.m.jd.com/client.action",
        "data": {
            'functionId': 'findBeanSceneNew',
            'body': '{}',
            'appid': 'signed_wh5_ihub',
            'client': 'android',
            'clientVersion': '15.1.55',
        },
        "headers": {
            "User-Agent": "jdapp",
            "Referer": "https://pro.m.jd.com",
        },
        "cookies": {
            "pt_key": pt_key,
            "pt_pin": pt_pin
        }
    }

    try:
        async with AsyncClient(headers=meta["headers"], cookies=meta["cookies"], timeout=15) as client:
            res = await client.post(meta["url"], data=meta["data"])
            if res.status_code == 200:
                json_data = res.json()
                if json_data.get("errorMessage"):
                    logger.warning(f"{pt_pin} 查询失败，pt_key 可能已过期")
                    result["msg"] = f"{pt_pin} 登录失效"
                else:
                    status = json_data.get("data", {}).get("status")
                    count = json_data.get("data", {}).get("totalUserBean", {})
                    days = json_data.get("data", {}).get("continuousDays", {})
                    result.update(
                        {"code": 200, "msg": f"{pt_pin} 查询成功，累计京豆：{count or '无'}，连续签到天数：{days or '无'}"})
            else:
                result["msg"] = f"{pt_pin} 请求失败"
    except Exception as e:
        logger.error(f"{pt_pin} 查询异常: {e}")
        result["msg"] = f"{pt_pin} 查询异常"

    logger.info(result["msg"])
    return result

