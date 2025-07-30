<div align="left">
    <h1>SkyManagerAPI <img src="https://sun9-87.userapi.com/s/v1/if2/V2hDbOtYk5zwTO8A-Fe9oQcDkr_SWTwL3T0I96qmrXlKEklSNjXMx7gBT-oRf6Coh51kOK9ZFMdGXSJWBcOywrmW.jpg?quality=95&as=32x19,48x28,72x42,108x63,160x94,240x141,360x211,480x281,540x317,640x375,720x422,771x452&from=bu&cs=771x0" width=45 height=25></h1>
    <p align="left" >
        <a href="https://pypi.org/project/skymanagerapi/">
            <img src="https://img.shields.io/pypi/v/skymanagerapi?style=flat-square" alt="PyPI">
        </a>
        <a href="https://pypi.org/project/skymanagerapi/">
            <img src="https://img.shields.io/pypi/dm/skymanagerapi?style=flat-square" alt="PyPI">
        </a>
    </p>
</div>


## Использование

With ``skymanagerapi`` you can use <a href="https://api.skymanager.top/redoc">SkyManagerAPI</a> together with Telegram<br/>
Documentation: https://api.skymanager.top/redoc

## Установка

```bash
pip install skymanager
```

## Требования

 - ``Python 3.8+``
 - ``aiohttp``

## Возможности

 - ``Asynchronous``
 - ``Exception handling``


## Пример обязательной подписки, показов методом */check*

```python
from skymanagerapi import SkyManager

from aiogram import types


skym = SkyManager(skym_token) # skym_token api-ключ сервиса SkyManager

async def message_handler(message: types.Message):
    # Применяйте везде, где требуется проверка
    if not await skym.check(
            user_id=message.from_user.id,
            language_code=message.from_user.language_code,
            is_premium=message.from_user.is_premium): 
        return

async def callback_handler(call: types.CallbackQuery):
    # Применяйте везде, где требуется проверка
    if not await skym.check(
            user_id=call.from_user.id,
            language_code=call.from_user.language_code,
            is_premium=call.from_user.is_premium):
        return
```

### Использование пользовательского сообщения

```python
# Опционально, для метода check. Можно настроить также в @SkyManagerBot
message_custom = {
    "text": "🤖 Чтобы пользоваться чат-ботом, сначала выполните задания",
    "row_width": 2,                         # кнопок в одной в строке
    "buttons": [                            # [0] - bot, [1] - channel, [2] - url, [3] - boost
        {"title": "▶️ Запустить бота"},     # bot
        {"title": "➕ Подписаться"},        # channel
        {"title": "🌐 Открыть"},            # external / url
    ]
}
await skym.check(user_id, language_code=language_code, message=message)
```

## Пример интеграции без токена бота методами /get_tasks, /check_tasks

```python
# Получение задач для пользователя /get_tasks
@dp.message(Command(commands=["start"]))
async def message_handler(message: types.Message):
    data = await skym.get_tasks(
        user_id=message.from_user.id,
        language_code=message.from_user.language_code,  # used only for new pinning
        is_premium=message.from_user.is_premium,
        limit=5) # количество слотов
    if data.get("result"):  
        # ВАЖНО! Необходимо добавить в код бота функцию отправки сообщения op_message(). Пример ниже.
        await op_message(bot, message.chat.id, data["result"], data["bundle_id"])
        return

...

# Получение статуса выполнения задач
@dp.callback_query(lambda c: c.data and c.data.startswith("sky_fp:"))
async def check_subscription(call: types.CallbackQuery):
    bundle_id = call.data.split(":", 1)[1]
    done = await skym.check_tasks(call.from_user.id, bundle_id)

    if done:
        await call.message.delete()
        await call.message.answer("Подписка подтверждена ✅")
    else:
        await call.answer("Вы ещё не подписались.", show_alert=True)


# Пример функции op_message().
async def op_message(bot, chat_id: int, tasks: list[dict], bundle_id: str, template: dict | None = None) -> None:
    if not tasks:
        return
    tpl        = template or {}
    text       = tpl.get("text", "👋 Для продолжения подпишитесь и нажмите «✅ Проверить».")
    row_width  = int(tpl.get("row_width", 2)) or 2

    t_bot      = tpl.get("button_bot",     "Запустить")
    t_channel  = tpl.get("button_channel", "Подписаться")
    t_url      = tpl.get("button_url",     "Перейти")
    t_boost    = tpl.get("button_boost",   "Голосовать")
    t_confirm  = tpl.get("button_fp",      "✅ Проверить")

    title_map = {"bot": t_bot, "channel": t_channel, "external": t_url, "boost": t_boost}

    rows, row = [], []
    for idx, t in enumerate(tasks, start=1):
        rtype = t.get("rtype", "external")
        row.append(
            types.InlineKeyboardButton(
                text=f"{idx} {title_map.get(rtype, t_url)}",
                url=t["url"],
            )
        )
        if len(row) == row_width:
            rows.append(row); row = []
    if row: rows.append(row)

    # 👉 bundle_id упаковываем в callback_data
    rows.append([
        types.InlineKeyboardButton(
            text=t_confirm,
            callback_data=f"sky_fp:{bundle_id}"
        )
    ])
    kb = types.InlineKeyboardMarkup(inline_keyboard=rows)
    await bot.send_message(chat_id, text, reply_markup=kb, parse_mode="HTML")

```


Developed by Mits (c) 2024-2025
