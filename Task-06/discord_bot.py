import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('Bot is online!')

# -------- Welcome + Role Assignment --------
@bot.event
async def on_member_join(member):
    # Send welcome message
    channel = discord.utils.get(member.guild.text_channels, name='orientation')
    if channel:
        await channel.send(f"Welcome {member.mention}! Become an aspiring hero of Midtown Tech!")

    # Assign role
    role = discord.utils.get(member.guild.roles, name='Aspiring Hero')
    if role:
        await member.add_roles(role)

forbidden_keywords = ["villainous spam", "unauthorized link", "off-topic disruption", "menacing threats", "nigga", "noob", "hacker", "cheater"]

# -------- Message Moderation --------

@bot.event
async def on_message(message):
    if message.author == bot.user:  # Ignore bot’s own messages
        return

    # Check for forbidden keywords
    if any(word in message.content.lower() for word in forbidden_keywords):
        await message.delete()
        await message.author.send(
            "⚠️ Your message was removed. Please follow Midtown Tech's code of conduct."
        )

    await bot.process_commands(message)  # Important to allow other commands to work


# -------- Commands --------
@bot.command()
@commands.has_role("Faculty")
async def bugle(ctx, *, msg):
    channel = discord.utils.get(ctx.guild.text_channels, name='announcements')
    if channel:
        announcement = await channel.send(f"📢 {msg}")
        await asyncio.sleep(24*3600)
        if not announcement.pinned:
            await announcement.delete()

#wisdom command
@bot.command()
async def wisdom(ctx, topic):
    topic = topic.lower()  # make it case-insensitive
    
    if topic == "rules":
        await ctx.send(
            "📜 Midtown Tech Rules:\n"
            "1. Be respectful.\n"
            "2. No spamming.\n"
            "3. Stay on-topic.\n"
            "4. Follow faculty instructions.\n" \
            "5. No unauthorized links.\n" \
            "6. Report issues to faculty.\n" \
            "7. Keep personal info private.\n" \
            "8. Use appropriate channels.\n" 
            "9. No hate speech or bullying.\n" \
            "10. Have fun and learn!\n"

        )
    elif topic == "resources":
        await ctx.send(
            "📚 Essential Resources:\n"
            "- Discord Server Guidelines\n"
            "- Learning Materials in #resources\n"
            "- Coding Docs and Tutorials\n"
            "- Support Channels for Help\n"
            "- Faculty Office Hours\n"
            "- Community Forums\n"
            "- Mental Health Resources\n"
            "- Career Services\n"
            "- Library Access\n"
            "- Tech Support\n" 
        )
    elif topic == "contact":
        await ctx.send(
            "📞 Contact Faculty/Admin:\n"
            "- @Faculty Role on Discord\n"
            "- Email: faculty@midtowntech.edu"
        )
    else:
        await ctx.send("❌ Unknown topic. Available: rules, resources, contact.")


bot.run('<bot-token>')
