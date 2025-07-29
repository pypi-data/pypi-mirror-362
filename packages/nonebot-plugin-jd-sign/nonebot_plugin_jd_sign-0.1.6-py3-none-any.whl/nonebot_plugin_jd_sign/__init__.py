# plugins/jd_sign/__init__.py
from nonebot import require

require("nonebot_plugin_apscheduler")

from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from nonebot_plugin_apscheduler import scheduler
from .sign_jd import signBeanAct
from .data_store import get_all_autosign_users
import asyncio
import random

# 注册插件元信息
__plugin_meta__ = PluginMetadata(
    name="京东签到插件",
    description="支持京东登录、自动签到、查询京豆的 QQ 机器人插件",
    usage="指令：京东登录、京东签到、查询、自动签到、查看账户",
    homepage = "https://github.com/Darker718/nonebot_plugin_jd_sign",
    type ="application",
    supported_adapters = {"~onebot.v11"}
)

from . import handlers  # 加载指令处理器


# 定时任务：每天 8 点执行
@scheduler.scheduled_job("cron", hour=8, minute=0, id="jd_auto_sign")
async def auto_sign_job():
    users = get_all_autosign_users()
    for uid, info in users.items():
        await asyncio.sleep(random.randint(30, 60))  # 间隔 30~60 秒
        res = await signBeanAct(info["pt_pin"], info["pt_key"])
        print(f"[自动签到] 用户 {info['pt_pin']}：{res['msg']}")
