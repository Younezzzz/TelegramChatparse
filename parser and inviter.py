from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest,InviteToChannelRequest
from telethon.tl.types import ChannelParticipantsSearch

api_hash = ''
username = ''
api_id = 


client = TelegramClient(username,api_id,api_hash)
async def dump_all_paticipants(chanel,chanel_2):
    chanel_2 = await client.get_entity(chanel_2)
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
        if ((participiant.phone is None) and (participiant.username is None)) or participiant.bot==True:
            pass
        elif participiant.phone is None:
            try:
                await client(InviteToChannelRequest(channel=chanel_2.username, users=[participiant.username]))
            except:
                print("Error")
            user_string = f"id:{participiant.id}  user_name:{participiant.username}\n"
            file.write(user_string)
        elif participiant.username is None:
            user_string = f"id:{participiant.id} phone:{participiant.phone}\n"
            file.write(user_string)
        else:
            user_string = f"id:{participiant.id}  user_name:{participiant.username} phone:{participiant.phone}\n"
            file.write(user_string)

async def main():
    await client.get_dialogs()
    url = input("Введите ссылку на чат: ")

    chanel = await client.get_entity(url)
    chanel_2 =input("Введите ссылку на канал или чат для добавления пользователей:")

    await dump_all_paticipants(chanel,chanel_2)
with client:
    client.loop.run_until_complete(main())
client.start()



