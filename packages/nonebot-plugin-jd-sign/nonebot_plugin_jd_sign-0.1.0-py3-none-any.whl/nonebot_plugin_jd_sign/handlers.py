# plugins/jd_sign/handlers.py
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import ArgPlainText
from .data_store import (
    update_user, get_user,
    set_autosign, get_all_autosign_users
)
from .sign_jd import signBeanAct, findBeanSceneNew
import re

login = on_command("京东登录", aliases={"jd登录"}, priority=5, block=True)
sign = on_command("京东签到", aliases={"jd签到"}, priority=5, block=True)
query = on_command("查询", aliases={"京东查询", "jd查询"}, priority=5, block=True)
autosign_cmd = on_command("自动签到", priority=5, block=True)
check = on_command("查看账户", aliases={"京东账户", "账户"}, priority=5, block=True)


# 登录步骤1：提示输入 cookie
@login.handle()
async def _(event: MessageEvent):
    await login.send("请输入你的 pt_key 和 pt_pin，如下格式：\npt_key=xxx;pt_pin=xxx;")


# 登录步骤2：接收并存储 cookie
@login.got("cookie")
async def _(event: MessageEvent, cookie: str = ArgPlainText("cookie")):
    match = re.search(r"pt_key=([^;]+);.*pt_pin=([^;]+);?", cookie)
    if not match:
        await login.finish("格式错误！请重新发送：pt_key=xxx;pt_pin=xxx;")
    pt_key, pt_pin = match.group(1), match.group(2)
    update_user(str(event.user_id), pt_key, pt_pin)
    await login.finish(f"用户 {pt_pin} 登录成功！")


# 签到
@sign.handle()
async def _(event: MessageEvent):
    user = get_user(str(event.user_id))
    if not user:
        await sign.finish("你还没有登录，请先发送“京东登录”")
    res = await signBeanAct(user["pt_pin"], user["pt_key"])
    await sign.finish(res["msg"])


# 查询
@query.handle()
async def _(event: MessageEvent):
    user = get_user(str(event.user_id))
    if not user:
        await query.finish("你还没有登录，请先发送“京东登录”")
    res = await findBeanSceneNew(user["pt_pin"], user["pt_key"])
    await query.finish(res["msg"])


# 自动签到
@autosign_cmd.handle()
async def _(event: MessageEvent):
    uid = str(event.user_id)
    user = get_user(uid)
    if not user:
        await autosign_cmd.finish("你还没有登录，请先发送“京东登录”")
    set_autosign(uid, True)
    await autosign_cmd.finish("自动签到功能已开启，每天早上 8 点将自动签到~")


@check.handle()
async def _(event: MessageEvent):
    user = get_user(str(event.user_id))
    if not user:
        await check.finish("你还没有登录，请先发送“京东登录”")
    pt_pin = user.get("pt_pin", "未知")
    auto = "开启" if user.get("autosign") else "关闭"
    last = user.get("last_update", "未知")
    msg = f"""🧾 当前账户信息：
pt_pin: {pt_pin}
自动签到: {auto}
最后更新时间: {last}"""
    await check.finish(msg)
