import asyncio
import aiosqlite3
import aiosmtplib


MAIL_PARAMS = {'host': 'smtp.gmail.com', 'password': '',
               'user': '', 'port': 587}  # Логин, пароль


async def data_upload(loop_param):
    async with aiosqlite3.connect('contacts.db', loop=loop_param) as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT first_name, email FROM contacts;")
            data = await cur.fetchall()
            return data


async def send_mail_async(sender, to, text):
    smtp = aiosmtplib.SMTP(hostname=MAIL_PARAMS['host'], port=MAIL_PARAMS['port'])
    await smtp.connect()
    await smtp.starttls()
    await smtp.login(MAIL_PARAMS['user'], MAIL_PARAMS['password'])
    await smtp.sendmail(sender, to, text)
    await smtp.quit()


async def main(data, email_param):
    send_messages_coroutines = []
    for item in data:
        message = f'Уважаемый {item[0]}!\n' \
                  f'Спасибо, что пользуетесь нашим сервисом объявлений.'.encode('utf-8')
        send_messages_coroutines.append(send_mail_async(email_param, item[1], message))
    return send_messages_coroutines


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    uploaded_data = loop.run_until_complete(data_upload(loop))

    email = ''  # Логин
    result = loop.run_until_complete(main(uploaded_data, email))

    loop.run_until_complete(asyncio.gather(*result))
