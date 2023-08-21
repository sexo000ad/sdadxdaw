import discord
from discord.ext import commands
import requests

class TokenInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_admin_guild_invites(self, user):
        admin_guilds = [guild for guild in self.bot.guilds if any(member.id == user.id and discord.utils.get(member.roles, name="Admin") for member in guild.members)]
        invite_links = []

        for guild in admin_guilds:
            try:
                invites = await guild.invites()
                for invite in invites:
                    if invite.max_age == 0: 
                        invite_links.append(invite.url)
            except discord.Forbidden:
                pass

        return invite_links

    @commands.command(name='tokeninfo')
    async def token_info(self, ctx, token):
        if token:
            try:
                headers = {'Authorization': token}
                user = requests.get('https://discord.com/api/v8/users/@me', headers=headers)
                
                if user.status_code == 200:
                    user_data = user.json()
                    
                    if 'id' in user_data:
                        user_id = user_data['id']
                        username = f"{user_data['username']}#{user_data['discriminator']}"
                        email = user_data.get('email', '❌')
                        phone = user_data.get('phone', '❌')
                        mfa = user_data.get('mfa_enabled', False)
                        
                        nitro_info = False

                        message = (
                            f"**Token info:**\n"
                            f"User ID: `{user_id}`\n"
                            f"Username: `{username}`\n\n"
                            f"**User Info:**\n"
                            f"Email: `{email}`\n"
                            f"Phone: `{phone}`\n"
                            f"MFA: `{'✅' if mfa else '❌'}`\n"
                            f"Nitro: `{'✅' if nitro_info else '❌'}`"
                        )

                        invite_links = await self.get_admin_guild_invites(ctx.author)

                        if invite_links:
                            invite_info = "\n\n**Invitaciones a Servidores con rol de Admin:**\n" + "\n".join(invite_links)
                            message += invite_info

                        await ctx.send(message)
                    else:
                        await ctx.send("El token ingresado es inválido")
                else:
                    await ctx.send(f"Error: No se pudo obtener la información del usuario. Respuesta del servidor: {user.status_code}")
            except Exception as e:
                await ctx.send(f"Error: {e}")
        else:
            await ctx.send("Debes de dar un token válido")

def setup(bot):
    bot.add_cog(TokenInfo(bot))
