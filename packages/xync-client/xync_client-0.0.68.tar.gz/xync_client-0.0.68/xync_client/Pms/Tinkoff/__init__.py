import asyncio
import os
import time

from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError, Error

from xync_client.loader import TORM
from x_model import init_db
from xync_schema import models


async def _input(page, code):
    for i in range(len(code)):
        await page.keyboard.press(code[i])


async def send_cred(page, cred, amount, payment):
    if len(cred) < 15:
        # Переходим на сбп и вводим данные получателя
        await page.locator(
            '[data-qa-type="desktop-ib-pay-buttons"] [data-qa-type="atomPanel pay-card-0"]',
            has_text="Перевести по телефону",
        ).click()
        await page.locator('[data-qa-type="recipient-input.value.placeholder"]').click()
        await page.wait_for_timeout(300)
        await page.locator('[data-qa-type="recipient-input.value.input"]').fill(cred)
        await page.locator('[data-qa-type="amount-from.placeholder"]').click()
        await page.locator('[data-qa-type="amount-from.input"]').fill(amount)
        await page.wait_for_timeout(300)
        await page.locator('[data-qa-type="bank-plate-other-bank click-area"]').click()
        await page.locator('[data-qa-type*="inputAutocomplete.value.input"]').click()
        await page.locator('[data-qa-type*="inputAutocomplete.value.input"]').fill(payment)
        await page.wait_for_timeout(300)
        await page.locator('[data-qa-type="banks-popup-list"]').click()
        await page.locator('[data-qa-type="transfer-button"]').click()
    else:
        #карта
        await page.goto("https://www.tbank.ru/mybank/payments/transfer-card-to-card/?internal_source=homePayments_transferList_category")
        time.sleep(2)
        await page.click(".abKlprGZ6")
        await _input(page, cred)
        await page.click(".bbuFarxsk.cbuFarxsk")
        await _input(page, amount)
        await page.locator('button[data-qa-type="submit-button"][type="submit"]').click()

def recursion_payments(amount: int, transactions: list):
    tran = transactions.pop(0)
    normalized_tran = tran.replace("−", "-").replace(",", ".")
    if 0 > int(float(normalized_tran)) != amount:
        return recursion_payments(amount, transactions)
    return int(float(tran.replace("−", "-").replace(",", ".")))

async def check_payment(page, amount):
    try:
        await page.goto("https://www.tbank.ru/events/feed")
    except Error:
        await page.wait_for_timeout(1000)
        await page.goto("https://www.tbank.ru/events/feed")

    await page.wait_for_timeout(2000)
    await page.locator('[data-qa-type = "timeline-operations-list"]:last-child').scroll_into_view_if_needed()

    transactions = await page.locator(
        '[data-qa-type="timeline-operations-list"] [data-qa-type="operation-money"]'
    ).all_text_contents()

    result = recursion_payments(amount, transactions)

    if result == amount:
        print("Платеж", result, "получен")
    else:
        print("Ничегошеньки нет")

    await page.wait_for_timeout(3000)
    return result

async def main():
    async with async_playwright() as p:
        _ = await init_db(TORM, True)
        agent = await models.PmAgent.filter(pm__norm="t", auth__isnull=False).first()
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=agent.state, record_video_dir="videos")
        page = await context.new_page()
        await page.goto("https://www.tbank.ru/mybank/")
        await page.wait_for_timeout(1000)
        try:
            await page.wait_for_url("https://www.tbank.ru/mybank/", timeout=3000)
        except TimeoutError:
            # Новый пользователь
            if await page.locator('[automation-id="form-title"]', has_text="Вход в Т‑Банк").is_visible():
                await page.wait_for_timeout(200)
                await page.locator('[automation-id="phone-input"]').fill(agent.auth.get("number"))
                await page.locator('[automation-id="button-submit"] svg').click()
                await page.locator('[automation-id="otp-input"]').fill(input("Введите код: "))
                time.sleep(3)
                await page.locator('[automation-id="cancel-button"]', has_text="Не сейчас").click(delay=500)
                time.sleep(5)
                cookies = await page.context.storage_state()
                agent.state = cookies
                await agent.save()
                await page.wait_for_timeout(200)

        time.sleep(2)
        # await send_cred(page, "2202206275295967", "1", "Сбербанк")
        await check_payment(page, 100)
        # await page.video.path()
        # # BufferedInputFile(pth, 'tbank')
        # # await bot.send_video('mixartemev')
        # ...
        time.sleep(100)
        await context.close()
        await browser.close()



asyncio.run(main())
