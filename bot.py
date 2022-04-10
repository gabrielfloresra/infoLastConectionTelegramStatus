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

contacts = []
IS_RUNNING = False


class Contact:
    status = UserStatusEmpty
    id = ''
    name = ''

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.status = UserStatusEmpty

    def __str__(self):
        return f'{self.name} ({self.id})'


@bot.on(events.NewMessage(pattern='^/stop$'))
async def stop(event):
    global IS_RUNNING
    IS_RUNNING = False
    await event.respond('Monitoring has been stopped')


@bot.on(events.NewMessage(pattern='^/start$'))
async def start(event):
    global IS_RUNNING

    if IS_RUNNING:
        return await event.respond('Monitoring is already started')

    if(len(contacts) < 1):
        contact = Contact('1528080160', 'b')
        try:
            cInfo = await client.get_entity(int(contact.id))
            contacts.append(contact)
        finally:
            contact = None
        contact = Contact('1774983671', 'blanca')
        try:
            cInfo = await client.get_entity(int(contact.id))
            contacts.append(contact)
        finally:
            contact = None
        contact = Contact('1996192868', 'gabriel')
        try:
            cInfo = await client.get_entity(int(contact.id))
            contacts.append(contact)
        finally:
            contact = None

    IS_RUNNING = True
    await bot.send_message(event.chat, 'starting...', buttons=[
        [
            Button.text('/start'),
            Button.text('/stop'),
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
        for contact in contacts:
            try:
                cInfo = await client.get_entity(int(contact.id))
            except:
                await event.respond(f'{contact.name} is not your contact')
                continue
            if contact.status != cInfo.status:
                if isinstance(cInfo.status, UserStatusOnline):
                    await event.respond(f'{contact.name} is online')
                    contact.status = cInfo.status
                elif isinstance(cInfo.status, UserStatusOffline):
                    await event.respond(f'{contact.name} is offline')
                    contact.status = cInfo.status
                elif isinstance(cInfo.status, UserStatusRecently):
                    await event.respond(f'{contact.name} is online recently')
                    contact.status = cInfo.status
                elif isinstance(cInfo.status, UserStatusLastWeek):
                    await event.respond(f'{contact.name} is online last week')
                    contact.status = cInfo.status
                elif isinstance(cInfo.status, UserStatusLastMonth):
                    await event.respond(f'{contact.name} is online last month')
                    contact.status = cInfo.status
                else:
                    await event.respond(f'{contact.name} not has status')
        sleep(0.5)
    return


@bot.on(events.NewMessage(pattern='^/add'))
async def add(event):

    message = event.message
    person_info = message.message.split()
    if len(person_info) < 1:
        return await event.respond(f'Phonenumber is required')
    if len(person_info) < 2:
        return await event.respond(f'Name is required')

    id = person_info[1]
    name = person_info[2]
    contact = Contact(id, name)

    try:
        _ = await client.get_entity(int(contact.id))
    except:
        return await event.respond(f'{contact.name} is not your contact')

    contacts.append(contact)

    return await event.respond(f'{str(contact)}, has been added')


@bot.on(events.NewMessage(pattern='^/rm'))
async def remove(event):
    message = event.message
    person_info = message.message.split()
    id = person_info[1]
    name = person_info[2]

    contact = Contact(id, name)
    try:
        contacts.remove(contact)
        await event.respond(f'User {str(contact)}, has been deleted')
    except:
        await event.respond("not found contact")


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
