from asyncio import gather
from datetime import datetime

import PGram
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from xync_bot.routers.pay.dep import fill_creds, fill_actors, dlt, ans, Store
from xync_schema import models

from xync_bot.routers.pay import cd, dep, window

pay = Router()


@pay.message(Command("pay"))
async def h_start(msg: Message):
    """Step 1: Select target type"""
    store: Store = msg.bot.store
    store.curr.is_target = True
    await gather(window.type_select(msg), dlt(msg))
    store.perm.user = await models.User.get(username_id=msg.from_user.id)
    store.perm.creds, store.perm.cur_creds = await fill_creds(store.perm.user.person_id)


@pay.callback_query(cd.MoneyType.filter(F.is_fiat))
async def h_got_fiat_type(query: CallbackQuery, bot: PGram):
    """Step 2f: Select cur"""
    bot.store.curr.is_fiat = True
    await gather(window.cur_select(query.message), ans(query, "Понял, фиат"))


@pay.callback_query(cd.MoneyType.filter(F.is_fiat.__eq__(0)))
async def h_got_crypto_type(query: CallbackQuery, bot: PGram):
    """Step 2c: Select coin"""
    bot.store.curr.is_fiat = False
    bot.store.perm.actors, *_ = await gather(
        fill_actors(bot.store.perm.user.person_id), window.coin_select(query.message), ans(query, "Понял, крипта")
    )


@pay.callback_query(cd.Coin.filter())
async def h_got_coin(query: CallbackQuery, callback_data: cd.Coin, bot: PGram):
    """Step 3c: Select target ex"""
    setattr(bot.store.pay, ("t" if bot.store.curr.is_target else "s") + "_coin_id", callback_data.id)
    await gather(window.ex_select(query.message), ans(query, "Эта монета есть на следующих биржах"))


@pay.callback_query(cd.Cur.filter())
async def h_got_cur(query: CallbackQuery, callback_data: cd.Cur, bot: PGram):
    """Step 3f: Select target pm"""
    setattr(bot.store.pay, ("t" if bot.store.curr.is_target else "s") + "_cur_id", callback_data.id)
    await gather(window.pm(query.message), ans(query, "Вот платежные системы доступные для этой валюты"))


@pay.callback_query(cd.Pm.filter(F.is_target))
async def h_got_target_pm(query: CallbackQuery, callback_data: cd.Pm, state: FSMContext):
    """Step 4f: Fill target cred.detail"""
    query.message.bot.store.pay.t_pmcur_id = callback_data.pmcur_id
    await gather(
        window.fill_cred_dtl(query.message),
        ans(query, "Теперь нужны реквизиты"),
        state.set_state(dep.CredState.detail),
    )


@pay.callback_query(cd.Cred.filter())
async def h_got_cred(query: CallbackQuery, callback_data: cd.Cred, state: FSMContext):
    query.message.bot.store.pay.cred_id = callback_data.id
    await gather(
        window.amount(query.message), ans(query, "Теперь нужна сумма"), state.set_state(dep.PaymentState.amount)
    )


@pay.message(dep.CredState.detail)
async def h_got_cred_dtl(msg: Message, state: FSMContext):
    """Step 4.1f: Fill target cred.name"""
    msg.bot.store.pay.cred_dtl = msg.text
    await gather(window.fill_cred_name(msg), dlt(msg), state.set_state(dep.CredState.name))


@pay.message(dep.CredState.name)
async def h_got_cred_name(msg: Message, state: FSMContext):
    """Step 5f: Save target cred"""
    store: Store = msg.bot.store
    cred, _ = await models.Cred.update_or_create(
        {"name": msg.text},
        detail=store.pay.cred_dtl,
        person_id=store.perm.user.person_id,
        pmcur_id=store.pay.t_pmcur_id,
    )
    store.pay.cred_id = cred.id
    store.perm.creds[cred.id] = cred
    await gather(window.amount(msg), dlt(msg), state.set_state(dep.PaymentState.amount))


@pay.callback_query(cd.Ex.filter())
async def h_got_ex(query: CallbackQuery, callback_data: cd.Ex, state: FSMContext):
    """Step 4c: Save target"""
    store: Store = query.message.bot.store
    ist = store.curr.is_target
    setattr(store.pay, ("t" if ist else "s") + "_ex_id", callback_data.id)
    if ist:
        await window.amount(query.message)
        actor_id = store.perm.actors[store.pay.t_ex_id]
        addr = await models.Addr.get(coin_id=store.pay.t_coin_id, actor_id=actor_id)
        store.pay.addr_id = addr.id
    else:
        await window.set_ppo(query.message)
    await ans(query, f"Биржа {store.glob.exs[callback_data.id]} выбрана")
    await state.set_state(dep.PaymentState.amount)


@pay.message(dep.PaymentState.amount)
async def h_got_amount(msg: Message, state: FSMContext):
    """Step 6: Save target amount"""
    store: Store = msg.bot.store
    if not msg.text.isnumeric():
        store.curr.msg_to_del = await msg.answer("Пожалуйста, введите корректное число")
        return
    if store.curr.msg_to_del:
        await store.curr.msg_to_del.delete()
    store.pay.amount = float(msg.text)
    """Step 7: Select source type"""
    store.curr.is_target = False
    await gather((window.type_select if store.curr.is_fiat else window.cur_select)(msg), dlt(msg), state.clear())


@pay.callback_query(cd.Pm.filter(F.is_target.__eq__(0)))
async def h_got_source_pm(query: CallbackQuery, callback_data: cd.Pm):
    store: Store = query.message.bot.store
    store.pay.s_pmcur_id = callback_data.pmcur_id
    await gather(
        window.set_ppo(query.message),
        ans(query, store.glob.pmcurs[callback_data.pmcur_id]),
    )


@pay.callback_query(cd.Ppo.filter())
async def h_got_ppo(query: CallbackQuery, callback_data: cd.Ppo):
    query.message.bot.store.pay.ppo = callback_data.num
    await gather(window.set_urgency(query.message), ans(query, str(callback_data.num)))


@pay.callback_query(cd.Time.filter())
async def h_got_urgency(query: CallbackQuery, callback_data: cd.Time):
    query.message.bot.store.pay.urg = callback_data.minutes
    await window.create_payreq(query.message)
    await ans(query, f"Ok {callback_data.minutes} min.")


# ACTIONS
@pay.callback_query(cd.Action.filter(F.act.__eq__(cd.ActionType.received)))
async def payment_confirmed(query: CallbackQuery, state: FSMContext):
    await ans(query, None)
    payed_at = datetime.now()
    await state.update_data(timer_active=False, payed_at_formatted=payed_at)
    data = await state.get_data()
    if data.get("pay_req_id"):
        pay_req = await models.PayReq.get(id=data["pay_req_id"])
        pay_req.payed_at = payed_at
        await pay_req.save()
    await state.clear()
    await window.success(query.message)


@pay.callback_query(cd.Action.filter(F.act.__eq__(cd.ActionType.not_received)))
async def no_payment(query: CallbackQuery, state: FSMContext):
    await ans(query, None)
    await state.update_data(timer_active=False)
    await query.message.edit_text("Платеж не получен!")
    await query.message.answer("укажите детали платежа")
    await state.clear()
    await state.set_state(dep.Report.text)


@pay.message(dep.Report.text)
async def payment_not_specified(msg: Message, state: FSMContext):
    await state.update_data(text=msg.text)
    data = await state.get_data()
    complaint_text = (
        f"Жалоба на неполученный платеж:\n"
        f"Пользователь: @{msg.from_user.username or msg.from_user.id}\n"
        f"Детали платежа: {data["text"]}\n"
        f"Время: {msg.date.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    await msg.bot.send_message(chat_id="xyncpay", text=complaint_text)


# NAVIGATION
@pay.callback_query(cd.PayNav.filter(F.to.in_([cd.PayStep.t_type, cd.PayStep.s_type])))
async def handle_home(query: CallbackQuery, state: FSMContext):
    await gather(window.type_select(query.message), state.clear(), ans(query, "Создаем платеж заново"))


@pay.callback_query(cd.PayNav.filter(F.to.in_([cd.PayStep.t_coin, cd.PayStep.s_coin])))
async def to_coin_select(query: CallbackQuery, state: FSMContext):
    await ans(query, None)
    is_target = await state.get_value("is_target")
    pref = "t" if is_target else "s"
    await state.update_data({pref + "_ex_id": None, pref + "_coin_id": None})
    await window.coin_select(query.message)


@pay.callback_query(cd.PayNav.filter(F.to.in_([cd.PayStep.t_cur, cd.PayStep.s_cur])))
async def to_cur_select(query: CallbackQuery, state: FSMContext):
    await ans(query, None)
    is_target = await state.get_value("is_target")
    pref = "t" if is_target else "s"
    await state.update_data({pref + "_pmcur_id": None, pref + "_cur_id": None})
    await window.cur_select(query.message)


@pay.callback_query(cd.PayNav.filter(F.to.in_([cd.PayStep.t_pm, cd.PayStep.s_pm])))
async def to_pm_select(query: CallbackQuery, state: FSMContext):
    await ans(query, None)
    await window.pm(query.message)


@pay.callback_query(cd.PayNav.filter(F.to.__eq__(cd.PayStep.t_cred_dtl)))
async def back_to_cred_detail(query: CallbackQuery, state: FSMContext):
    await ans(query, None)
    await state.update_data(detail=None)
    await window.fill_cred_dtl(query.message)


@pay.callback_query(cd.PayNav.filter(F.to.__eq__(cd.PayStep.t_cred_name)))
async def back_to_cred_name(query: CallbackQuery, state: FSMContext):
    await ans(query, None)
    await state.update_data(name=None)
    await window.fill_cred_name(query.message)


@pay.callback_query(cd.PayNav.filter(F.to.in_([cd.PayStep.t_ex, cd.PayStep.s_ex])))
async def back_to_ex_select(query: CallbackQuery, state: FSMContext):
    await ans(query, None)
    await state.update_data({("t" if await state.get_value("is_target") else "s") + "ex_id": None})
    await window.ex_select(query.message)


@pay.callback_query(cd.PayNav.filter(F.to.__eq__(cd.PayStep.t_amount)))
async def back_to_amount(query: CallbackQuery, state: FSMContext):
    await ans(query, None)
    await state.update_data(amount=None)
    await window.amount(query.message)
    await state.set_state(dep.PaymentState.amount)


@pay.callback_query(cd.PayNav.filter(F.to.in_([cd.PayStep.t_pm])))
async def back_to_payment(query: CallbackQuery, state: FSMContext):
    await ans(query, None)
    await state.update_data(payment=None)
    await window.pm(query.message)
