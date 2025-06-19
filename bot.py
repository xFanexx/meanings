import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

# Whitelisted user IDs who can add meanings
WHITELISTED_USERS = [
    ADD_USER_ID_HERE,  # Add more user IDs here
]


# Load meanings from JSON file
def load_meanings():
    try:
        with open("meanings.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Save meanings to JSON file
def save_meanings(meanings):
    with open("meanings.json", "w", encoding="utf-8") as f:
        json.dump(meanings, f, indent=2, ensure_ascii=False)


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
        meanings = load_meanings()

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
        save_meanings(meanings)

        embed = discord.Embed(
            title="✅ Meaning Added Successfully!",
            description=f"**{self.word.value.upper()}** has been added to the database!",
            color=0x00FF00,
        )
        embed.add_field(name="Word", value=self.word.value.upper(), inline=True)
        embed.add_field(
            name="Meaning",
            value=(
                self.meaning.value[:100] + "..."
                if len(self.meaning.value) > 100
                else self.meaning.value
            ),
            inline=False,
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


@bot.command(name="meaning")
async def meaning_command(ctx, *, word=None):
    """Shows the meaning of a word/phrase"""

    if not word:
        embed = discord.Embed(
            title="❌ Error",
            description="Please provide a word!\nExample: `?meaning sybau`",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
        return

    meanings = load_meanings()
    word_lower = word.lower()

    if word_lower in meanings:
        meaning_data = meanings[word_lower]

        embed = discord.Embed(
            title=f"📖 Meaning: {word.upper()}",
            description=meaning_data["meaning"],
            color=0x00FF88,
        )
        # Additional fields if available
        if "example" in meaning_data:
            embed.add_field(
                name="💡 Example", value=meaning_data["example"], inline=False
            )

        if "category" in meaning_data:
            embed.add_field(
                name="🏷️ Category", value=meaning_data["category"], inline=True
            )
        embed.set_footer(text="Meanings Bot | Know your slang!")
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
async def add_meaning_modal(ctx):
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


@bot.command(name="list")
async def list_meanings(ctx):
    """Shows all available words"""
    meanings = load_meanings()

    if not meanings:
        embed = discord.Embed(
            title="📝 Word List",
            description="No words in the database yet!",
            color=0xFFAA00,
        )
        await ctx.send(embed=embed)
        return

    # Split into multiple embeds if too many words
    word_list = list(meanings.keys())
    words_per_embed = 20

    for i in range(0, len(word_list), words_per_embed):
        chunk = word_list[i : i + words_per_embed]
        word_text = "\n".join([f"• {word.upper()}" for word in chunk])

        embed = discord.Embed(
            title=f"📝 Available Words ({i+1}-{min(i+words_per_embed, len(word_list))} of {len(word_list)})",
            description=word_text,
            color=0x0099FF,
        )
        embed.set_footer(text="Use ?meaning [word] for details")
        await ctx.send(embed=embed)


@bot.command(name="deletemeaning")
async def delete_meaning_command(ctx, *, word=None):
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

    meanings = load_meanings()
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
        value="Type `?yes` to confirm deletion or `?no` to cancel",
        inline=False,
    )

    await ctx.send(embed=embed)

    # Store deletion data for confirmation
    bot.pending_deletions = getattr(bot, "pending_deletions", {})
    bot.pending_deletions[ctx.author.id] = {
        "word": word_lower,
        "channel": ctx.channel.id,
        "original_word": word,
    }


@bot.command(name="yes")
async def confirm_deletion(ctx):
    """Confirms deletion of a meaning"""

    # Check if user has pending deletion
    pending_deletions = getattr(bot, "pending_deletions", {})

    if ctx.author.id not in pending_deletions:
        embed = discord.Embed(
            title="❌ No Pending Deletion",
            description="You don't have any pending deletions to confirm!",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
        return

    deletion_data = pending_deletions[ctx.author.id]

    # Check if in same channel
    if deletion_data["channel"] != ctx.channel.id:
        embed = discord.Embed(
            title="❌ Wrong Channel",
            description="Please confirm deletion in the same channel where you requested it!",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
        return

    # Delete the word
    meanings = load_meanings()
    word_to_delete = deletion_data["word"]
    original_word = deletion_data["original_word"]

    if word_to_delete in meanings:
        del meanings[word_to_delete]
        save_meanings(meanings)

        embed = discord.Embed(
            title="✅ Meaning Deleted",
            description=f"**{original_word.upper()}** has been successfully deleted from the database!",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Error", description="Word not found in database!", color=0xFF0000
        )
        await ctx.send(embed=embed)

    # Remove from pending deletions
    del pending_deletions[ctx.author.id]


@bot.command(name="no")
async def cancel_deletion(ctx):
    """Cancels deletion of a meaning"""

    # Check if user has pending deletion
    pending_deletions = getattr(bot, "pending_deletions", {})

    if ctx.author.id not in pending_deletions:
        embed = discord.Embed(
            title="❌ No Pending Deletion",
            description="You don't have any pending deletions to cancel!",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
        return

    deletion_data = pending_deletions[ctx.author.id]
    original_word = deletion_data["original_word"]

    embed = discord.Embed(
        title="❌ Deletion Cancelled",
        description=f"Deletion of **{original_word.upper()}** has been cancelled!",
        color=0x00FF00,
    )
    await ctx.send(embed=embed)

    # Remove from pending deletions
    del pending_deletions[ctx.author.id]


@bot.command(name="stats")
async def stats_command(ctx):
    """Shows bot statistics"""
    meanings = load_meanings()

    embed = discord.Embed(title="📊 Bot Statistics", color=0x00FF88)
    embed.add_field(name="📖 Total Words", value=len(meanings), inline=True)
    embed.add_field(name="🌐 Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="👥 Users", value=len(bot.users), inline=True)

    await ctx.send(embed=embed)


@bot.event
async def on_guild_join(guild):
    """Update status when bot joins a new server"""
    server_count = len(bot.guilds)
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"meanings on {server_count} servers ✨",
    )
    await bot.change_presence(activity=activity, status=discord.Status.dnd)


@bot.event
async def on_guild_remove(guild):
    """Update status when bot leaves a server"""
    server_count = len(bot.guilds)
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"meanings on {server_count} servers ✨",
    )
    await bot.change_presence(activity=activity, status=discord.Status.dnd)


@bot.command(name="ping")
async def ping_command(ctx):
    """Shows the bot's latency"""
    latency = bot.latency * 1000  # Convert to milliseconds
    embed = discord.Embed(
        title="🏓 Pong!", description=f"Latency: **{latency:.2f} ms**", color=0x00FF88
    )
    await ctx.send(embed=embed)


# Start the bot
if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
