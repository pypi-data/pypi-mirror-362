# nonebot_plugin_jd_sign

🎁 一个基于 [NoneBot2](https://nonebot.dev/) 的京东签到插件，支持 QQ 机器人自动进行京东签到、查询京豆数、自动定时签到等功能。

![License](https://img.shields.io/github/license/Darker718/nonebot_plugin_jd_sign)


---

## ✨ 功能特性

- ✅ 支持京东账号登录（通过 pt_key 和 pt_pin）
- 🧾 支持签到查询（查询京豆数量与连续签到天数）
- 🔁 支持定时自动签到（每天早上 8 点，间隔执行）
- 🔍 支持查看当前登录账户状态
- 🛠️ 每个 QQ 用户单独记录 pt_key/pt_pin，支持自动更新

---

## 📦 安装

### 使用 `nb-cli` 安装（推荐）：

```bash
nb plugin install nonebot_plugin_jd_sign
```

## 🔧 配置项

插件默认不需要额外配置。如需修改执行时间，请自定义 APScheduler 配置。

## 📚 使用说明

### 👉 指令列表：

| 指令     | 功能描述                                                     |
| -------- | ------------------------------------------------------------ |
| 京东登录 | 用户先发送指令然后根据提示输入 `pt_key=xxx;pt_pin=xxx;` 完成登录 |
| 京东签到 | 手动执行京东签到，返回签到结果                               |
| 查询     | 查询累计京豆与连续签到天数                                   |
| 自动签到 | 开启每日自动签到（每天早上 8 点）                            |
| 查看账户 | 查看当前登录账户的 pt_pin、自动签到状态与更新时间            |

## ⏰ 自动签到机制

- 插件依赖 `nonebot_plugin_apscheduler` 实现定时任务
- 每天早上 `08:00` 自动对开启了“自动签到”的用户依次执行签到
- 多个账户之间间隔 `30~60秒` 避免触发风控

------

## 🔧 依赖插件

- [nonebot2](https://github.com/nonebot/nonebot2)
- [nonebot-plugin-alconna](https://github.com/nonebot/plugin-alconna)
- [nonebot-plugin-apscheduler](https://github.com/nonebot/plugin-apscheduler)
- [httpx](https://www.python-httpx.org/)
- [loguru](https://github.com/Delgan/loguru)

------

## 📄 License

MIT © yourname

## 💡 鸣谢

本插件基于京东官方 API 行为模拟，仅用于学习交流，请勿用于非法用途，违反者后果自负。