from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch


api_hash = 'c11b0da892cea5fd65f5091dab71003b'
username = 'k0kosics'
api_id = 14226922


client = TelegramClient(username,api_id,api_hash)
async def dump_all_paticipants(chanel):
    offset_user = 0
    limit_user = 100

    all_participants = []
    filter_user = ChannelParticipantsSearch('')

    while True:
        participiants = await client(GetParticipantsRequest(chanel,
                                                            filter_user,offset_user,limit_user,hash = 0))
        if not participiants.users:
            break
        all_participants.extend(participiants.users)
        offset_user = offset_user + len(participiants.users)
    all_users = []
    file = open('users.txt','w+')
    for participiant in all_participants:
        if (participiant.phone is None) and (participiant.username is None):
            pass
        elif participiant.phone is None:
            user_string = f"id:{participiant.id}  user_name:{participiant.username}\n"
            file.write(user_string)
        elif participiant.username is None:
            user_string = f"id:{participiant.id} phone:{participiant.phone}\n"
            file.write(user_string)
        else:
            user_string = f"id:{participiant.id}  user_name:{participiant.username} phone:{participiant.phone}\n"
            file.write(user_string)

async def main():
    url = input("Введите ссылку на канал или чат: ")
    chanel = await client.get_entity(url)
    await dump_all_paticipants(chanel)
with client:
    client.loop.run_until_complete(main())
client.start()



