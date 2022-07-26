from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

import sqlite3


api_hash = 'здесь api_hash'
username = 'здесь твой ник в тг'
api_id = #десь api_id без кавычек


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
    for participiant in all_participants:
        all_users.append({'id': participiant.id,
                          'last_name':participiant.username,
                          'user':participiant.username})

    for i in all_users:
        conn = sqlite3.connect("usears_data.db")
        curs = conn.cursor()
        curs.execute(f"""INSERT INTO users VALUES(?,?,?)""",(i['id'],i['last_name'],i['user']))
        conn.commit()
        conn.close()





async def main():
    url = input("Введите ссылку на канал или чат: ")
    chanel = await client.get_entity(url)
    await dump_all_paticipants(chanel)
with client:
    client.loop.run_until_complete(main())
client.start()







