import asyncio
import discord
from utility import get_news



class MyClient(discord.Client):
    async def write_news(self):
        
        channel = self.get_channel(self.news_channel)
        while True:
            
            new_news=get_news()
            for i in range(len(new_news[0])):
                title=new_news[0][i].get_text()
                description=new_news[1][i].get_text()
                if not (title in self.news):
                    await channel.send(f"""**{title}**
                                    
    {description}
                                    """)
                    self.news.append(title)
            if len(self.news)>20:
                self.news=self.news[-10:]
            await asyncio.sleep(2) 
    async def on_ready(self):
        self.news=[]
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        if message.content.startswith('!news'):
            self.news_channel=message.channel.id
            await self.write_news()

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

client.run('')
