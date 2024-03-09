import asyncio
import discord
from utility import get_news
import sqlite3
from language_detector import detect_language
from deep_translator import GoogleTranslator
con = sqlite3.connect("server.db")
cur = con.cursor()

class MyClient(discord.Client):
    async def write_news(self):
        #guild_list=list(map(e:e.id,self.guilds))
        
        
        while True:
            new_news=get_news()
            
            for i in range(len(new_news[0])):
                for k in self.guilds:
                    g=self.get_guild(k.id)
                    res = cur.execute(f"SELECT channelID FROM news WHERE serverID = {g.id}")
                    try:
                        ch=int(res.fetchone()[0])
                    except:
                        continue
                    channel = g.get_channel(ch)
                    title=new_news[0][i].get_text()
                    description=new_news[1][i].get_text()
                    if not (title in self.news):
                        await channel.send(f""":no_entry: **{title}**
                                    
{description}
 ------------------------------------""")
                self.news.append(title)
            if len(self.news)>50:
                self.news=self.news[-20:]
            await asyncio.sleep(30) 
    async def on_ready(self):
        self.news=[]
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        await self.write_news()
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        self.channel=int(message.channel.id)
        self.server=int(message.guild.id)
        if message.author.id == self.user.id:
            return
        if message.content.startswith('!hello'):
            channel=self.get_channel(message.channel.id)
            await channel.send("hiiii")
        if message.content.startswith('!news'):
            res = cur.execute("SELECT channelID FROM news WHERE serverID = ? AND channelID =?",(self.server,self.channel))
            if res.fetchone() is None:
                cur.execute("INSERT INTO news VALUES (?,?)",(self.server,self.channel))
                con.commit()
            else :
                cur.execute("UPDATE news SET channelID = ? WHERE serverID =?",(self.channel,self.server))
            
        if message.content.startswith('!translate'):
            lang=message.content.split()[1].lower().strip()
            channelT=self.get_channel(message.channel.id)
            messageT = await channelT.fetch_message(message.reference.message_id)
            translated = GoogleTranslator(source='auto', target=lang).translate(messageT.content)
            await message.reply(translated)
            
        if message.content.startswith('!langss'):
            lang=message.content.split()[1].title().strip()
            res = cur.execute("SELECT language FROM lang WHERE serverID =? AND channelID =?",(self.server,self.channel))
            r=res.fetchone()
            if not(r is None):
                if lang in r:
                    channel=self.get_channel(message.channel.id)
                    await channel.send("language Aleardy set")
                else:
                
                    cur.execute("INSERT INTO lang VALUES (?,?,?)",(self.server,self.channel,lang))
                    con.commit()
                    channel=self.get_channel(self.channel)
                    await channel.send("language Added to channel ")
        else :
            detected_language=detect_language(message.content)
            res=cur.execute("SELECT language FROM lang WHERE serverID =? AND channelID =? AND language=?",(self.server,self.channel,detected_language))
            if res.fetchone() is None:
                res=cur.execute("SELECT language FROM lang WHERE serverID =? AND channelID =?",(self.server,self.channel))
                if not res.fetchone() is None:
                	await message.delete()
                

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

client.run('token')
