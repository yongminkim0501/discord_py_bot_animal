import discord
from discord.ext import commands
import json
# config.json 파일에서 토큰 읽기
def connect_discord(path):
    with open(path) as f:
        config = json.load(f)
        TOKEN = config['token']
    return TOKEN

class set_discord:
    def __init__(self):
        self.intents = discord.Intents.all()
        self.client = commands.Bot(command_prefix='!',
                                intents=self.intents,
                                help_command=None)

    def set_discord_bot(self):
        # self.intents 는 봇 개발 시, 봇이 discord 서버에서 어떤 이벤트를 받을지 설정
        
        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return   
            if not message.content.startswith('!'):
                await message.channel.send("안녕하세요")
                await message.channel.send(message)
            await self.client.process_commands(message)

        @self.client.command()
        async def embed(ctx):
            embed = discord.Embed(title = "타이틀에 넣을 내용",
                                  description = "설명에 넣을 내용", color = 0x62c1cc)
            embed.add_field(name = "필드(field)의 name", value = "필드(field)의 value")
            embed.set_footer(text = "푸터에 넣을 내용") 
            await ctx.send(embed = embed)
        
        @self.client.command(name='도움말')  # help 대신 다른 이름 사용
        async def help_command(ctx):
            embed = discord.Embed(
                title="도움말",
                description="봇 사용에 대한 도움말입니다.",  # description은 필수 필드입니다
                color=0x00ff00
            )
            embed.add_field(name="!도움말", value="이 도움말을 표시합니다")
            embed.add_field(name="!embed", value="임베드 예시를 보여줍니다")
            await ctx.send(embed=embed)

    def start_client(self, TOKEN):
        self.client.run(TOKEN)