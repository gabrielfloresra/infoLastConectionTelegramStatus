from telethon import TelegramClient, events
from telethon.tl.types import UserStatusEmpty
from time import sleep
import telethon.sync

USER_NAME = "tmp/xlucab"
API_HASH = ""
APP_ID = ""
BOT_TOKEN = ""

client = TelegramClient(USER_NAME, APP_ID, API_HASH)

client.connect()
client.start()
bot = TelegramClient('tmp/bot', APP_ID, API_HASH).start(bot_token=BOT_TOKEN)

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

@bot.on(events.NewMessage(pattern='^/stopMonitoring$'))
async def stop(event):
    global IS_RUNNING
    IS_RUNNING = False
    await event.respond('Monitoring has been stopped')

@bot.on(events.NewMessage(pattern='^/startMonitoring$'))
async def start(event):
    global IS_RUNNING
    if IS_RUNNING:
        return await event.respond('Monitoring is already started')

    if(len(contacts) < 1):
        return await event.respond('No contacts added')
        
    IS_RUNNING = True
    await event.respond(f'Monitoring has been started')

    while IS_RUNNING and len(contacts) > 0:
        for contact in contacts:
            try:
                cInfo = await client.get_entity(int(contact.id))
            except:
                await event.respond(f'{contact.name} is not your contact')
                continue
            if contact.status != cInfo.status:
                await event.respond(f'Status changed for {contact.name} \n\nFROM:\n{contact.status} \n\nTO:\n{cInfo.status}')
                contact.status = cInfo.status
        sleep(0.5)
    await event.respond(f'Monitoring has been stopped')


@bot.on(events.NewMessage(pattern='^/addContact'))
async def add(event):

    message = event.message
    person_info = message.message.split()
    if len(person_info) < 1 :
        return await event.respond(f'Phonenumber is requerided')
    if len(person_info) < 2 :
        return await event.respond(f'Name is requerided')

    id = person_info[1]
    name = person_info[2]
    contact = Contact(id, name)
    
    try:
        _ = await client.get_entity(int(contact.id))
    except:
        return await event.respond(f'{contact.name} is not your contact')

    contacts.append(contact)

    await event.respond(f'{str(contact)}, has been added')

@bot.on(events.NewMessage(pattern='^/rmContact'))
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

@bot.on(events.NewMessage(pattern='/listContacts'))
async def list(event):
    response = 'List is empty'
    if(len(contacts)):
        response = 'User list: \n'+'\n'.join([str(x) for x in contacts])
    await event.respond(response)

def main():
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()