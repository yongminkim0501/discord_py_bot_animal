import discord
import json
# config.json 파일에서 토큰 읽기
def connect_discord(path):
    with open(path) as f:
        config = json.load(f)
        TOKEN = config['token']
    return TOKEN

class set_discord:
    def __init__(self):
        self.intents = None
        self.client = None

    def set_discord_bot(self):
        self.intents = discord.Intents.all()
        self.client = discord.Client(intents = self.intents)

        @self.client.event
        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return        
            print(message)
        
    def start_client(self, TOKEN):
        self.client.run(TOKEN)