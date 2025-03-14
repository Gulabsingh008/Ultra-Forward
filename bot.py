#Dont Remove My Credit @Silicon_Bot_Update 
#This Repo Is By @Silicon_Official 
# For Any Kind Of Error Ask Us In Support Group @Silicon_Botz 

import asyncio
import logging 
import logging.config
from database import db 
from config import Config  
from pyrogram import Client, __version__, filters
from pyrogram.raw.all import layer 
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait 
from aiohttp import web
from plugins import web_server 

#Dont Remove My Credit @Silicon_Bot_Update 
#This Repo Is By @Silicon_Official 
# For Any Kind Of Error Ask Us In Support Group @Silicon_Botz 

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

class Bot(Client): 
    def __init__(self):
        super().__init__(
            Config.BOT_SESSION,
            api_hash=Config.API_HASH,
            api_id=Config.API_ID,
            bot_token=Config.BOT_TOKEN,   
            sleep_threshold=10,
            workers=200,
            plugins={"root": "plugins"}
        )
        self.log = logging

    async def start(self):
        await super().start()
        me = await self.get_me()
        logging.info(f"{me.first_name} with for pyrogram v{__version__} (Layer {layer}) started on @{me.username}.")
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Config.PORT).start()
        self.id = me.id
        self.username = me.username
        self.first_name = me.first_name
        self.set_parse_mode(ParseMode.DEFAULT)
        text = "<b>๏[-ิ_•ิ]๏ ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ !</b>"
        logging.info(text)
        success = failed = 0

        #Dont Remove My Credit @Silicon_Bot_Update 
        #This Repo Is By @Silicon_Official 
        # For Any Kind Of Error Ask Us In Support Group @Silicon_Botz 
        users = await db.get_all_frwd()
        async for user in users:
           chat_id = user['user_id']
           try:
              await self.send_message(chat_id, text)
              success += 1
           except FloodWait as e:
              await asyncio.sleep(e.value + 1)
              await self.send_message(chat_id, text)
              success += 1
           except Exception:
              failed += 1 
        if (success + failed) != 0:
           await db.rmve_frwd(all=True)
           logging.info(f"Restart message status"
                 f"success: {success}"
                 f"failed: {failed}")

    async def stop(self, *args):
        msg = f"@{self.username} stopped. Bye."
        await super().stop()
        logging.info(msg)

app = Bot()

# ✅ Auto Forward New Messages Feature ✅
@app.on_message(filters.channel)
async def forward(client, message):
    """हर नए मैसेज को यूज़र के सेट किए चैनल में भेजें"""
    try:
        user_id = message.chat.id  # यूज़र की ID प्राप्त करें
        user_data = await db.get_channels(user_id)  # यूज़र के सेट किए चैनल लाएं

        if not user_data:
            return  # अगर कोई डेटा नहीं मिला, तो कुछ न करें

        from_channel = user_data["from_channel"]  # यूज़र द्वारा सेट Source Channel
        to_channel = user_data["to_channel"]  # यूज़र द्वारा सेट Target Channel

        if message.chat.id == int(from_channel):
            await message.copy(int(to_channel))  # मैसेज को Target Channel में भेजें
            print(f"✅ Message Forwarded: {from_channel} → {to_channel}")
    
    except Exception as e:
        print(f"❌ Error in Forwarding: {e}")


app.run()

#Dont Remove My Credit @Silicon_Bot_Update 
#This Repo Is By @Silicon_Official 
# For Any Kind Of Error Ask Us In Support Group @Silicon_Botz
