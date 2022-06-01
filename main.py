import discord
from mcstatus import JavaServer
import requests


intents = discord.Intents.default()
intents.messages = True


class FrostyBot(discord.Client):

    # heart event
    async def on_heartbeat(self):
        print('heartbeat')

    async def on_ready(self):
        self.server = JavaServer('54.39.49.125', 27050)
        self.server_status = self.server.status()

        print('Logged in as')
        print(self.user)
        print("Minecraft server: " + self.server_status.description)

    async def on_message(self, message):
        message_content = message.content.lower()

        # Try to get the Minecraft server status
        try: 
            self.server_status = self.server.status()
        except:
            self.server_status = None


        # Update the bot's activity
        if self.server_status is not None:
            await self.change_presence(activity=discord.Game("Minecraft with " + str(self.server_status.players.online) + " players."))
        else:
            await self.change_presence(activity=discord.Game("Server is offline."))


        # If the command is !players
        if message_content == "!players":
            if self.server_status is None:
                await message.channel.send("Minecraft server is offline.")
                pass
            else:
                players = self.server_status.players.sample
                players_names = ""
                if players is not None:
                    for player in players:
                        players_names += player.name + "\n"

                    embed = discord.Embed(title="Players", color=0x00ffff).add_field(
                        name="Online:", value=players_names)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("No players online")

                pass
        
        #Does the message_content start with !insult?
        if message_content.startswith("!insult"):
            #Get the insult
            print("Getting insult")
            async with message.channel.typing():
                insult = requests.get("https://insult.mattbas.org/api/insult.txt").text
                await message.channel.send(insult)
                pass
            




def main():
    token = open('token.txt', 'r').read()
    frostyBot = FrostyBot(intents=intents)

    frostyBot.run(token)


if __name__ == '__main__':
    main()
