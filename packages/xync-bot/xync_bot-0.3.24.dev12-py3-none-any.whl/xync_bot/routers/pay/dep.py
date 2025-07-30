import logging
from asyncio import gather
from enum import IntEnum

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup
from pyrogram.types import CallbackQuery
from tortoise.functions import Min
from x_auth.enums import Role
from x_model.func import ArrayAgg
from xync_schema import models


class Report(StatesGroup):
    text = State()


class CredState(StatesGroup):
    detail = State()
    name = State()


class PaymentState(StatesGroup):
    amount = State()
    timer = State()
    timer_active = State()


class ActionType(IntEnum):
    """Цель (назначение) платежа (target)"""

    sent = 1  # Отправил
    received = 2  # Получил
    not_received = 3  # Не получил


class PayStep(IntEnum):
    """Цель (назначение) платежа (target)"""

    t_type = 1  # Выбор типа
    t_cur = 2  # Выбор валюты
    t_coin = 3  # Выбор монеты
    t_pm = 4  # Выбор платежки
    t_ex = 5  # Выбор биржи
    t_cred_dtl = 6  # Ввод номера карты
    t_cred_name = 7  # Ввод имени
    # t_addr = 8 # todo: позже добавим: Выбор/ввод крипто кошелька
    t_amount = 9  # Ввод суммы
    """ Источник платежа (source) """
    s_type = 10  # Выбор типа
    s_cur = 11  # Выбор типа
    s_pm = 12  # Выбор типа
    s_coin = 13  # Выбор типа
    s_ex = 14  # Выбор типа
    ppo = 15  # Выбор возможности разбивки платежа
    urgency = 16  # Выбор срочности получения платежа
    pending_send = 17  # Ожидание отправки (если мы платим фиатом)
    pending_confirm = 18  # Ожидание пока на той стороне подтвердят получение нашего фиата (если мы платим фиатом)
    pending_receive = 19  # Ожидание поступления (если мы получаем фиат)


flags = {
    "RUB": "🇷🇺",
    "THB": "🇹🇭",
    "IDR": "🇮🇩",
    "TRY": "🇹🇷",
    "GEL": "🇬🇪",
    "VND": "🇻🇳",
    "AED": "🇦🇪",
    "AMD": "🇦🇲",
    "AZN": "🇦🇿",
    "CNY": "🇨🇳",
    "EUR": "🇪🇺",
    "HKD": "🇭🇰",
    "INR": "🇮🇳",
    "PHP": "🇵🇭",
    "USD": "🇺🇸",
}


class SingleStore(type):
    _store = None

    async def __call__(cls):
        if not cls._store:
            cls._store = super(SingleStore, cls).__call__()
            cls._store.coins = {k: v for k, v in await models.Coin.all().order_by("ticker").values_list("id", "ticker")}
            curs = {c.id: c for c in await models.Cur.filter(ticker__in=flags.keys()).order_by("ticker")}
            cls._store.curs = curs
            cls._store.exs = {k: v for k, v in await models.Ex.all().values_list("id", "name")}
            cls._store.pmcurs = {
                k: v
                for k, v in await models.Pmex.filter(pm__pmcurs__cur_id__in=cls._store.curs.keys())
                .annotate(sname=Min("name"))
                .group_by("pm__pmcurs__id")
                .values_list("pm__pmcurs__id", "sname")
            }
            cls._store.coinexs = {
                c.id: [ex.ex_id for ex in c.coinexs] for c in await models.Coin.all().prefetch_related("coinexs")
            }
            cls._store.curpms = {
                cur_id: ids
                for cur_id, ids in await models.Pmcur.filter(cur_id__in=curs.keys())
                .annotate(ids=ArrayAgg("id"))
                .group_by("cur_id")
                .values_list("cur_id", "ids")
            }
            cls._store.curpms = {
                cur_id: ids
                for cur_id, ids in await models.Pmcur.filter(cur_id__in=curs.keys())
                .annotate(ids=ArrayAgg("id"))
                .group_by("cur_id")
                .values_list("cur_id", "ids")
            }

        return cls._store


class Store:
    class Global(metaclass=SingleStore):
        coins: dict[int, str]  # id:ticker
        curs: dict[int, models.Cur]  # id:Cur
        exs: dict[int, str]  # id:name
        coinexs: dict[int, list[int]]  # id:[ex_ids]
        pmcurs: dict[int, str]  # pmcur_id:name
        curpms: dict[int, list[int]]  # id:[pmcur_ids]

    class Permanent:
        msg_id: int = None
        user: models.User = None
        actors: dict[int, int] = None  # key=ex_id
        creds: dict[int, models.Cred] = None  # key=cred_id
        cur_creds: dict[int, list[int]] = None  # pmcur_id:[cred_ids]

    class Current:
        is_target: bool = True
        is_fiat: bool = None
        msg_to_del: Message = None

    class Payment:
        t_cur_id: int = None
        s_cur_id: int = None
        t_coin_id: int = None
        s_coin_id: int = None
        t_pmcur_id: int = None
        s_pmcur_id: int = None
        t_ex_id: int = None
        s_ex_id: int = None
        amount: int | float = None
        ppo: int = 1
        addr_id: int = None
        cred_dtl: str = None
        cred_id: int = None
        urg: int = 5
        pr_id: int = None

    glob: Global
    perm: Permanent = Permanent()
    pay: Payment = Payment()
    curr: Current = Current()


async def fill_creds(person_id: int) -> tuple[dict[int, models.Cred], dict[int, list[int]]]:
    cq = models.Cred.filter(person_id=person_id)
    creds = {c.id: c for c in await cq}
    cur_creds = {
        pci: ids
        for pci, ids in await cq.annotate(ids=ArrayAgg("id")).group_by("pmcur_id").values_list("pmcur_id", "ids")
    }
    return creds, cur_creds


async def fill_actors(person_id: int) -> dict[int, int]:
    ex_actors = {
        # todo: check len(ids) == 1
        exi: ids[0]
        for exi, ids in await models.Actor.filter(person_id=person_id)
        .annotate(ids=ArrayAgg("id"))
        .group_by("ex_id")
        .values_list("ex_id", "ids")
    }
    return ex_actors


async def edit(msg: Message, txt: str, rm: InlineKeyboardMarkup):
    await gather(msg.edit_text(txt), msg.edit_reply_markup(reply_markup=rm))


async def ans(cbq: CallbackQuery, txt: str = None):
    await cbq.answer(txt, cache_time=0)


async def dlt(msg: Message):
    await msg.delete()


async def edt(msg: Message, txt: str, rm: InlineKeyboardMarkup):
    if msg.message_id == msg.bot.store.perm.msg_id:
        await msg.edit_text(txt, reply_markup=rm)
    else:  # окно вызвано в ответ на текст, а не кнопку
        try:
            await msg.bot.edit_message_text(
                txt, chat_id=msg.chat.id, message_id=msg.bot.store.perm.msg_id, reply_markup=rm
            )
        except TelegramBadRequest as e:
            print(msg.bot.store.perm.msg_id, e)


async def xync_have_coin_amount(store: Store) -> bool:
    assets = await models.Asset.filter(
        addr__coin_id=store.pay.t_coin_id, addr__ex_id=store.pay.t_ex_id, addr__actor__user__role__in=Role.ADMIN
    )
    return store.pay.amount <= sum(a.free for a in assets)


async def client_have_coin_amount(store: Store) -> bool:
    assets = await models.Asset.filter(addr__coin_id=store.pay.t_coin_id, addr__actor_id__in=store.perm.actors.values())
    return store.pay.amount <= sum(a.free for a in assets)


async def need_ppo(store: Store):
    cur_id = getattr(store.pay, ("t" if store.curr.is_target else "s") + "_cur_id")
    usd_amount = store.pay.amount * store.glob.curs[cur_id].rate
    if usd_amount < 50:
        return 0
    elif usd_amount > 100:
        return 2
    else:
        return 1


async def client_target_repr(store: Store) -> tuple[models.Addr | models.Cred, str]:
    if store.pay.t_ex_id:
        addr_to = (
            await models.Addr.filter(
                actor__ex_id=store.pay.t_ex_id, coin_id=store.pay.t_coin_id, actor__user=store.perm.user
            )
            .prefetch_related("actor")
            .first()
        )
        ex, coin = store.glob.exs[store.pay.s_ex_id], store.glob.coins[store.pay.s_coin_id]
        if not addr_to:
            logging.error(f"No {coin} addr in {ex} for user: {store.perm.user.username_id}")
        return addr_to, f"{coin} на {ex} по id: `{addr_to.actor.exid}`"
    # иначе: реквизиты для фиата
    cur, pm = store.glob.curs[store.pay.t_cur_id], store.glob.pmcurs[store.pay.t_pmcur_id]
    cred = store.perm.creds[store.pay.cred_id]
    return cred, f"{cur.ticker} на {pm} по номеру: {cred.repr()}"


async def get_merch_target(store: Store) -> tuple[models.Addr | models.Cred, str]:
    if store.pay.s_ex_id:
        addr_in = (
            await models.Addr.filter(
                actor__ex_id=store.pay.s_ex_id, coin_id=store.pay.s_coin_id, actor__user__role__gte=Role.ADMIN
            )
            .prefetch_related("actor")
            .first()
        )
        ex, coin = store.glob.exs[store.pay.s_ex_id], store.glob.coins[store.pay.s_coin_id]
        if not addr_in:
            logging.error(f"No {coin} addr in {ex}")
        return addr_in, f"{coin} на {ex} по id: `{addr_in.actor.exid}`"
    # иначе: реквизиты для фиатной оплаты
    s_pmcur = await models.Pmcur.get(id=store.pay.s_pmcur_id).prefetch_related("pm__grp")
    cred = await models.Cred.filter(
        **({"pmcur__pm__grp": s_pmcur.pm.grp} if s_pmcur.pm.grp else {"pmcur_id": store.pay.s_pmcur_id}),
        person__user__role__gte=Role.ADMIN,
    ).first()  # todo: order by fiat.target-fiat.amount
    cur, pm = store.glob.curs[store.pay.s_cur_id], store.glob.pmcurs[store.pay.s_pmcur_id]
    if not cred:
        logging.error(f"No {cur.ticker} cred for {pm}")
    return cred, f"{cur.ticker} на {pm} по номеру: {cred.repr()}"


def fmt_sec(sec: int):
    days = sec // (24 * 3600)
    sec %= 24 * 3600
    hours = sec // 3600
    sec %= 3600
    minutes = sec // 60
    sec %= 60

    if days > 0:
        return f"{days}д {hours:02d}:{minutes:02d}:{sec:02d}"
    elif hours > 0:
        return f"{hours:02d}:{minutes:02d}:{sec:02d}"
    else:
        return f"{minutes:02d}:{sec:02d}"
