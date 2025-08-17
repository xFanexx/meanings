import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import aiofiles  # Use async file handling
import asyncio
import paginator  # Import the paginator

ButtonPaginator = paginator.ButtonPaginator  # Import the Paginator Class

# Load environment variables
load_dotenv()

# Bot Setup

up_time = 0


class MeaningsBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="?", intents=intents)

    async def setup_hook(self):
        asyncio.get_event_loop().set_debug(True)  # Set up debugging for blocking code
        global up_time
        up_time = discord.utils.utcnow().timestamp()


bot = MeaningsBot()

# Whitelisted user IDs who can add meanings
WHITELISTED_USERS = [ADD_USER_ID_HERE]  # Add more user IDs here


@bot.command()
@commands.is_owner()  # Only allow the the owner of the bot to sync
async def sync(ctx: commands.Context):
    await ctx.message.delete()
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"Synced len({synced}) commands!", delete_after=5.0)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


# Load meanings from JSON file
async def load_meanings():
    try:
        async with aiofiles.open("meanings.json", "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)
    except FileNotFoundError:
        return {}


# Save meanings to JSON file
async def save_meanings(meanings):
    async with aiofiles.open("meanings.json", "w", encoding="utf-8") as f:
        data = json.dumps(meanings, indent=2, ensure_ascii=False)
        await f.write(data)


# Load slang origins from JSON file
async def load_slang_origins():
    try:
        async with aiofiles.open("slang_origins.json", "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)
    except FileNotFoundError:
        return {}


# Save slang origins to JSON file
async def save_slang_origins(origins):
    async with aiofiles.open("slang_origins.json", "w", encoding="utf-8") as f:
        data = json.dumps(origins, indent=2, ensure_ascii=False)
        await f.write(data)


class AddMeaningModal(discord.ui.Modal, title="Add New Meaning"):
    def __init__(self):
        super().__init__()

    word = discord.ui.TextInput(
        label="Word/Phrase",
        placeholder='Enter the word or phrase (e.g., "sybau")',
        required=True,
        max_length=100,
    )

    meaning = discord.ui.TextInput(
        label="Meaning/Definition",
        placeholder='Enter the meaning (e.g., "Shut Your Bitch Ass Up")',
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=1000,
    )

    example = discord.ui.TextInput(
        label="Example (Optional)",
        placeholder="Enter an example usage (optional)",
        style=discord.TextStyle.paragraph,
        required=False,
        max_length=500,
    )

    category = discord.ui.TextInput(
        label="Category (Optional)",
        placeholder='Enter a category (e.g., "Slang", "Internet")',
        required=False,
        max_length=50,
    )

    async def on_submit(self, interaction: discord.Interaction):
        meanings = await load_meanings()

        # Create meaning entry
        meaning_entry = {
            "meaning": self.meaning.value,
            "added_by": str(interaction.user),
            "added_at": str(interaction.created_at),
        }

        if self.example.value:
            meaning_entry["example"] = self.example.value

        if self.category.value:
            meaning_entry["category"] = self.category.value

        meanings[self.word.value.lower()] = meaning_entry
        await save_meanings(meanings)

        embed = discord.Embed(
            title=f"✅ Successfully added `{self.word.value.upper()}`!",
            color=0x00FF00,
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(
            name="Meaning",
            value=(
                f"{f"- {self.meaning.value[:100]}" + "..."\
                if len(self.meaning.value) > 100\
                else f"- {self.meaning.value}"}"
            ),
            inline=False,
        )
        embed.set_footer(
            text=f"Added by @{interaction.user}",
            icon_url=interaction.user.display_avatar.url,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class AddOriginModal(discord.ui.Modal, title="Add Slang Origin"):
    def __init__(self):
        super().__init__()

    word = discord.ui.TextInput(
        label="Word/Phrase",
        placeholder='Enter the slang word (e.g., "GOAT")',
        required=True,
        max_length=100,
    )

    origin = discord.ui.TextInput(
        label="Origin/Background",
        placeholder="Enter the historical or cultural origin",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=1500,
    )

    time_period = discord.ui.TextInput(
        label="Time Period (Optional)",
        placeholder='When it originated (e.g., "2000s", "1990s")',
        required=False,
        max_length=50,
    )

    culture = discord.ui.TextInput(
        label="Culture/Context (Optional)",
        placeholder='Cultural context (e.g., "Hip Hop", "Internet Culture")',
        required=False,
        max_length=100,
    )

    async def on_submit(self, interaction: discord.Interaction):
        origins = await load_slang_origins()

        # Create origin entry
        origin_entry = {
            "origin": self.origin.value,
            "added_by": str(interaction.user),
            "added_at": str(interaction.created_at),
        }

        if self.time_period.value:
            origin_entry["time_period"] = self.time_period.value

        if self.culture.value:
            origin_entry["culture"] = self.culture.value

        origins[self.word.value.lower()] = origin_entry
        await save_slang_origins(origins)

        embed = discord.Embed(
            title=f"✅ Successfully added origin for `{self.word.value.upper()}`!",
            color=0x00FF00,
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(
            name="Origin",
            value=(
                f"{self.origin.value[:100]}" + "..."
                if len(self.origin.value) > 100
                else f"{self.origin.value}"
            ),
            inline=False,
        )
        embed.set_footer(
            text=f"Added by @{interaction.user}",
            icon_url=interaction.user.display_avatar.url,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

    # Fancy status with server count and DND status
    server_count = len(bot.guilds)
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"meanings on {server_count} servers ✨",
    )
    await bot.change_presence(activity=activity, status=discord.Status.dnd)


# Slash command for slang origins
@bot.tree.command(
    name="slangorigin",
    description="Get the historical or cultural origin of a slang term",
)
async def slang_origin_slash(interaction: discord.Interaction, word: str):
    """Shows the origin of a slang word/phrase"""
    origins = await load_slang_origins()
    word_lower = word.lower()

    if word_lower in origins:
        origin_data = origins[word_lower]

        embed = discord.Embed(
            title=f"🏛️ Origin of `{word.upper()}`",
            color=0x9932CC,
            timestamp=discord.utils.utcnow(),
        )

        embed.add_field(
            name="📜 Historical/Cultural Origin",
            value=origin_data["origin"],
            inline=False,
        )

        if "time_period" in origin_data:
            embed.add_field(
                name="📅 Time Period", value=origin_data["time_period"], inline=True
            )

        if "culture" in origin_data:
            embed.add_field(
                name="🌍 Cultural Context", value=origin_data["culture"], inline=True
            )

        # Check if there's also a meaning for this word
        meanings = await load_meanings()
        if word_lower in meanings:
            embed.add_field(
                name="💡 Current Meaning",
                value=meanings[word_lower]["meaning"],
                inline=False,
            )

        embed.set_footer(text="Slang Origins Database | Know your history!")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="❓ Origin not found",
            description=f"**{word.upper()}** origin is not in our database yet.\n\nYou can suggest it to the bot owner so they can add it!",
            color=0xFFAA00,
        )
        embed.set_footer(text="New origins are added regularly!")
        await interaction.response.send_message(embed=embed)


@bot.command(name="meaning")
async def meaning_command(ctx: commands.Context, *, word: str = None):
    """Shows the meaning of a word/phrase"""

    if not word:
        embed = discord.Embed(
            title="❌ Error",
            description="Please provide a word!\nExample: `?meaning sybau`",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
        return

    meanings = await load_meanings()
    word_lower = word.lower()

    if word_lower in meanings:
        meaning_data = meanings[word_lower]

        embed = discord.Embed(
            title=f"Word: `{word_lower}`",
            color=0x00FF88,
        )
        # Additional fields if available
        embed.add_field(name="📖 Meaning", value=f"- {meaning_data["meaning"]}")
        if "example" in meaning_data:
            embed.add_field(
                name="💡 Example", value=f"- {meaning_data["example"]}", inline=False
            )

        if "category" in meaning_data:
            embed.add_field(
                name="🏷️ Category", value=f"- {meaning_data["category"]}", inline=True
            )
        embed.set_footer(text="Meanings Bot | Know your slang!")
        embed.set_footer(
            text=f"Requested by @{ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="❓ I don't know this word yet",
            description=f"**{word.upper()}** is not in my database.\n\nYou can suggest it to the bot owner so they can add it!",
            color=0xFFAA00,
        )
        embed.set_footer(text="New words are added regularly!")
        await ctx.send(embed=embed)


@bot.command(name="addmeaning")
async def add_meaning_modal(ctx: commands.Context):
    """Opens a modal to add a new meaning (whitelisted users only)"""

    # Check if user is whitelisted
    if ctx.author.id not in WHITELISTED_USERS:
        embed = discord.Embed(
            title="🚫 Access Denied",
            description="Only whitelisted users can add new meanings!",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
        return

    # Send modal
    modal = AddMeaningModal()
    await ctx.send(
        "Click the button below to add a new meaning!", view=ModalView(modal)
    )


@bot.command(name="addorigin")
async def add_origin_modal(ctx: commands.Context):
    """Opens a modal to add a new slang origin (whitelisted users only)"""

    # Check if user is whitelisted
    if ctx.author.id not in WHITELISTED_USERS:
        embed = discord.Embed(
            title="🚫 Access Denied",
            description="Only whitelisted users can add new origins!",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
        return

    # Send modal
    modal = AddOriginModal()
    await ctx.send(
        "Click the button below to add a slang origin!", view=OriginModalView(modal)
    )


class ModalView(discord.ui.View):
    def __init__(self, modal):
        super().__init__(timeout=300)
        self.modal = modal

    @discord.ui.button(
        label="Add Meaning", style=discord.ButtonStyle.primary, emoji="➕"
    )
    async def add_meaning_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(self.modal)


class OriginModalView(discord.ui.View):
    def __init__(self, modal):
        super().__init__(timeout=300)
        self.modal = modal

    @discord.ui.button(
        label="Add Origin", style=discord.ButtonStyle.secondary, emoji="🏛️"
    )
    async def add_origin_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(self.modal)


@bot.command(name="list")
async def list_meanings(ctx: commands.Context):
    """Shows all available words"""
    meanings: dict = await load_meanings()

    if not meanings:
        embed = discord.Embed(
            title="📝 Word List",
            description="No words in the database yet!",
            color=0xFFAA00,
        )
        await ctx.send(embed=embed)
        return

    # Uses pagination if too many words
    word_list = list(meanings.keys())
    words_per_embed = 3
    embeds = [
        discord.Embed(
            title=f"Available words ({i+1}-{min(i+words_per_embed, len(word_list))} of {len(word_list)})",
            description=f"1. {"\n- ".join(word.upper() for word in word_list[i : i + words_per_embed])}",
            color=0x0099FF,
        )
        for i in range(0, len(word_list), words_per_embed)
    ]  # List of embeds
    paginator = ButtonPaginator(embeds)
    await paginator.start(ctx.channel)  # Start the paginator


@bot.command(name="deletemeaning")
async def delete_meaning_command(ctx: commands.Context, *, word: str = None):
    """Deletes a meaning from the database (whitelisted users only)"""

    # Check if user is whitelisted
    if ctx.author.id not in WHITELISTED_USERS:
        embed = discord.Embed(
            title="🚫 Access Denied",
            description="Only whitelisted users can delete meanings!",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
        return

    if not word:
        embed = discord.Embed(
            title="❌ Error",
            description="Please provide a word to delete!\nExample: `?deletemeaning sybau`",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
        return

    meanings = await load_meanings()
    word_lower = word.lower()

    if word_lower not in meanings:
        embed = discord.Embed(
            title="❓ Word Not Found",
            description=f"**{word.upper()}** is not in the database!",
            color=0xFFAA00,
        )
        await ctx.send(embed=embed)
        return

    # Show confirmation embed
    embed = discord.Embed(
        title="⚠️ Confirm Deletion",
        description=f"Do you really want to delete **{word.upper()}**?",
        color=0xFF9900,
    )
    embed.add_field(
        name="Current Meaning",
        value=(
            meanings[word_lower]["meaning"][:200] + "..."
            if len(meanings[word_lower]["meaning"]) > 200
            else meanings[word_lower]["meaning"]
        ),
        inline=False,
    )
    embed.add_field(
        name="⚡ Action Required",
        value="Type `yes` to confirm deletion or `no` to cancel.",
        inline=False,
    )

    await ctx.send(embed=embed)

    def check(msg: discord.Message):
        return (
            msg.channel == ctx.channel
            and msg.author == ctx.author
            and msg.content.lower() in ("yes", "no")
        )

    try:
        answer = await bot.wait_for("message", check=check, timeout=180)
    except asyncio.TimeoutError:
        return await ctx.send(f"Took too long, deletion cancelled.")

    if answer.content.lower() == "yes":
        del meanings[word.lower()]
        await save_meanings(meanings)

        embed = discord.Embed(
            title="✅ Meaning Deleted",
            description=f"**`{word.upper()}`** has been successfully deleted from the database!",
            color=0x00FF00,
            timestamp=discord.utils.utcnow(),
        )
        embed.set_footer(
            text=f"Deleted by @{ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        await ctx.send(embed=embed)

    else:
        meanings = await load_meanings()
        embed = discord.Embed(
            title="❌ Deletion Cancelled",
            description=f"Deletion of **`{word.upper()}`** has been cancelled!",
            color=0x00FF00,
            timestamp=discord.utils.utcnow(),
        )
        embed.set_footer(
            text=f"Cancelled by @{ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        await ctx.send(embed=embed)


@bot.command(name="deleteorigin")
async def delete_origin_command(ctx: commands.Context, *, word: str = None):
    """Deletes a slang origin from the database (whitelisted users only)"""

    # Check if user is whitelisted
    if ctx.author.id not in WHITELISTED_USERS:
        embed = discord.Embed(
            title="🚫 Access Denied",
            description="Only whitelisted users can delete origins!",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
        return

    if not word:
        embed = discord.Embed(
            title="❌ Error",
            description="Please provide a word to delete its origin!\nExample: `?deleteorigin GOAT`",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
        return

    origins = await load_slang_origins()
    word_lower = word.lower()

    if word_lower not in origins:
        embed = discord.Embed(
            title="❓ Origin Not Found",
            description=f"**{word.upper()}** origin is not in the database!",
            color=0xFFAA00,
        )
        await ctx.send(embed=embed)
        return

    # Show confirmation embed
    embed = discord.Embed(
        title="⚠️ Confirm Deletion",
        description=f"Do you really want to delete the origin for **{word.upper()}**?",
        color=0xFF9900,
    )
    embed.add_field(
        name="Current Origin",
        value=(
            origins[word_lower]["origin"][:200] + "..."
            if len(origins[word_lower]["origin"]) > 200
            else origins[word_lower]["origin"]
        ),
        inline=False,
    )
    embed.add_field(
        name="⚡ Action Required",
        value="Type `yes` to confirm deletion or `no` to cancel.",
        inline=False,
    )

    await ctx.send(embed=embed)

    def check(msg: discord.Message):
        return (
            msg.channel == ctx.channel
            and msg.author == ctx.author
            and msg.content.lower() in ("yes", "no")
        )

    try:
        answer = await bot.wait_for("message", check=check, timeout=180)
    except asyncio.TimeoutError:
        return await ctx.send(f"Took too long, deletion cancelled.")

    if answer.content.lower() == "yes":
        del origins[word_lower]
        await save_slang_origins(origins)

        embed = discord.Embed(
            title="✅ Origin Deleted",
            description=f"Origin for **`{word.upper()}`** has been successfully deleted from the database!",
            color=0x00FF00,
            timestamp=discord.utils.utcnow(),
        )
        embed.set_footer(
            text=f"Deleted by @{ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title="❌ Deletion Cancelled",
            description=f"Deletion of **`{word.upper()}`** origin has been cancelled!",
            color=0x00FF00,
            timestamp=discord.utils.utcnow(),
        )
        embed.set_footer(
            text=f"Cancelled by @{ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        await ctx.send(embed=embed)


@bot.command(name="stats")
async def stats_command(ctx: commands.Context):
    """Shows bot statistics"""
    global up_time
    """Get uptime and convert to words"""
    current_uptime = int(discord.utils.utcnow().timestamp() - up_time)
    days = current_uptime // 86400
    hours = (current_uptime % 86400) // 3600
    minutes = (current_uptime % 3600) // 60
    seconds = current_uptime % 60
    up_time_list = []
    if days > 0:
        up_time_list.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        up_time_list.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        up_time_list.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0:
        up_time_list.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    uptime_to_words = " and ".join(up_time_list)
    meanings: dict = await load_meanings()
    origins: dict = await load_slang_origins()

    embed = discord.Embed(
        title="📊 Bot Statistics",
        description=f">>> **Total Words:** {len(meanings.keys())}\n**Total Origins:** {len(origins.keys())}\n**Servers:** {len(bot.guilds)}\
                            \n**Users:** {len(bot.users)}\n**Uptime:** {uptime_to_words}",
        color=0x00FF88,
    )
    embed.set_author(name=f"Meannings Bot", icon_url=bot.user.display_avatar.url)
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    await ctx.send(embed=embed)


@bot.event
async def on_guild_join(guild: discord.Guild):
    """Update status when bot joins a new server"""
    server_count = len(bot.guilds)
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"meanings on {server_count} servers ✨",
    )
    await bot.change_presence(activity=activity, status=discord.Status.dnd)


@bot.event
async def on_guild_remove(guild: discord.Guild):
    """Update status when bot leaves a server"""
    server_count = len(bot.guilds)
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"meanings on {server_count} servers ✨",
    )
    await bot.change_presence(activity=activity, status=discord.Status.dnd)


@bot.command(name="ping")
async def ping_command(ctx: commands.Context):
    """Shows the bot's latency"""
    latency = bot.latency * 1000  # Convert to milliseconds
    embed = discord.Embed(
        title="🏓 Pong!", description=f"Latency: **{latency:.2f} ms**", color=0x00FF88
    )
    await ctx.send(embed=embed)


# Start the bot
if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
