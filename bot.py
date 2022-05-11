from telethon import TelegramClient, events, sync, Button
from telethon.tl.types import UserStatusEmpty, UserStatusOffline, UserStatusOnline, UserStatusRecently, UserStatusLastWeek, UserStatusLastMonth
from time import sleep

USER_NAME = ""
BOT_TOKEN = ""
APP_ID = ""
API_HASH = ""

client = TelegramClient(USER_NAME, APP_ID, API_HASH)

client.connect()
client.start()
bot = TelegramClient('bot', APP_ID, API_HASH).start(bot_token=BOT_TOKEN)

contacts = {}
IS_RUNNING = False


@bot.on(events.NewMessage(pattern='^/stop$'))
async def stop(event):
    global IS_RUNNING

    if not IS_RUNNING:
        return await event.respond('Monitoring is already stopped')

    IS_RUNNING = False
    return await event.respond('Monitoring has been stopped')


@bot.on(events.NewMessage(pattern='^/start$'))
async def start(event):
    global IS_RUNNING

    if IS_RUNNING:
        return await event.respond('Monitoring is already started')

    if(len(contacts) < 1):
        try:
            # idContact = 1528080160
            idContact = 1996192868
            cInfo = await client.get_entity(idContact)
            contacts[idContact] = {"name": "b", "status": UserStatusEmpty}
        except:
            return await event.respond('1528080160 not added')

    IS_RUNNING = True
    await bot.send_message(event.chat, 'starting...', buttons=[
        [
            Button.text('/start'),
            Button.text('/stop'),
            Button.text('/list'),
        ],
        [
            Button.text('/'),
            Button.text('/'),
            Button.text('/')
        ],
        [
            Button.text('/'),
            Button.text('/'),
            Button.text('/')
        ],
        [
            Button.text('/'),
            Button.text('/'),
            Button.text('/')
        ]
    ])

    await event.respond(f'Monitoring has been started')

    while IS_RUNNING and len(contacts) > 0:
        for idContact in contacts:
            try:
                cInfo = await client.get_entity(idContact)
            except:
                await event.respond(f'{idContact} is not your contact')
                del contacts[idContact]
                continue
            if contacts[idContact]["status"] != cInfo.status:
                responseTxt = ""
                if isinstance(cInfo.status, UserStatusOnline):
                    responseTxt = f'{contacts[idContact]["name"]} is online'
                elif isinstance(cInfo.status, UserStatusOffline):
                    responseTxt = f'{contacts[idContact]["name"]} is offline'
                elif isinstance(cInfo.status, UserStatusRecently):
                    responseTxt = f'{contacts[idContact]["name"]} is online recently'
                elif isinstance(cInfo.status, UserStatusLastWeek):
                    responseTxt = f'{contacts[idContact]["name"]} is online last week'
                elif isinstance(cInfo.status, UserStatusLastMonth):
                    responseTxt = f'{contacts[idContact]["name"]} is online last month'
                else:
                    responseTxt = f'{contacts[idContact]["name"]} not has status'

                await event.respond(responseTxt)
                contacts[idContact]["status"] = cInfo.status
        sleep(0.5)

    if len(contacts) == 0:
        await event.respond('sin contactos')

    IS_RUNNING = False
    return


@bot.on(events.NewMessage(pattern='^/add'))
async def add(event):

    message = event.message
    person_info = message.message.split()
    if len(person_info) < 1:
        return await event.respond(f'Phonenumber is required')
    if int(person_info[1]) == 0:
        return await event.respond(f'Phonenumber is incorrect')
    if len(person_info) < 2:
        return await event.respond(f'Name is required')

    id = int(person_info[1])
    name = person_info[2]

    try:
        _ = await client.get_entity(id)
    except:
        return await event.respond(f'{name} is not your contact')

    contacts[id] = {"name": name, "status": UserStatusEmpty}

    return await event.respond(f'{str(contacts[id])} has been added')


@bot.on(events.NewMessage(pattern='^/rm'))
async def remove(event):
    message = event.message
    person_info = message.message.split()
    id = int(person_info[1])
    name = person_info[2]

    await event.respond(f'User {str(contacts[id])}, has been deleted')
    del contacts[id]


@bot.on(events.NewMessage(pattern='/list'))
async def list(event):
    response = 'List is empty'
    if(len(contacts)):
        response = 'User list: \n'+'\n'.join([str(x) for x in contacts])
    await event.respond(response)


# @bot.on(events.NewMessage())
# async def handler(event):
#     return await event.respond(event.message)


def main():
    try:
        bot.run_until_disconnected()
    finally:
        bot.disconnect()


if __name__ == "__main__":
    main()
