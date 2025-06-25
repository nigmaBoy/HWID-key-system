import os
import discord
from discord import app_commands, ui
from supabase import create_client, Client
import uuid

# --- Load secrets from Replit's "Secrets" tab ---
TOKEN = os.environ.get('DISCORD_TOKEN')
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!                      PUT YOUR SERVER ID HERE                             !!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
MY_SERVER_ID = "MY_SERVER_ID"
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# --- Set up Supabase and Discord clients ---
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# This is a helper object for our server ID
GUILD_OBJECT = discord.Object(id=int(MY_SERVER_ID))

# ==========================================================
# ==                     GENERATEKEY                      ==
# ==========================================================
@tree.command(name="generatekey", description="Generates a new script key for a specific user.")
@app_commands.describe(user="The user who will receive this key")
async def generatekey(interaction: discord.Interaction, user: discord.User):
    if str(interaction.user.id) != "YOUR_DISCORD_USER_ID_HERE":
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    new_key = str(uuid.uuid4())
    try:
        supabase.table('keys').insert({"key": new_key, "owner_discord_id": str(user.id)}).execute()
        try:
            await user.send(f"A new key has been generated for you by the admin:\n```\n{new_key}\n```")
            await interaction.response.send_message(f"✅ A new key has been generated and sent to {user.mention}!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f"⚠️ Could not DM {user.mention}.\nHere is their key:\n```\n{new_key}\n```", ephemeral=True)
    except Exception as e:
        print(f"Error generating key: {e}")
        await interaction.response.send_message(f"❌ An error occurred while talking to the database.", ephemeral=True)

# ==========================================================
# ==         PANEL CLASS (CONTAINS THE BUTTONS)           ==
# ==========================================================
class ControlPanelView(ui.View):
    def __init__(self, admin_id: str):
        super().__init__(timeout=None)
        self.admin_id = admin_id

    @ui.button(label="Get My Script", style=discord.ButtonStyle.green, custom_id="get_script_button")
    async def get_script(self, interaction: discord.Interaction, button: ui.Button):
        user_id = str(interaction.user.id)
        if user_id == self.admin_id:
            loader_code = f'```lua\nlocal script_key = "{user_key}"\nloadstring(game:HttpGet("YOUR_RAW_GITHUB_URL_HERE"))()(script_key)\n```'
            await interaction.response.send_message(f"Admin Template:\n{loader_code}", ephemeral=True)
            return
        try:
            data, count = supabase.table('keys').select('key').eq('owner_discord_id', user_id).execute()
            if not data[1]:
                await interaction.response.send_message("❌ No key found for your account.", ephemeral=True)
                return
            user_key = data[1][0]['key']
            user_loader = f'```lua\nlocal script_key = "{user_key}"\nloadstring(game:HttpGet("YOUR_RAW_GITHUB_URL_HERE"))()(script_key)\n```'
            await interaction.response.send_message(f"Your Personal Loader:\n{user_loader}", ephemeral=True)
        except Exception as e:
            print(f"Error getting script for {user_id}: {e}")
            await interaction.response.send_message("❌ Error fetching your script.", ephemeral=True)

    @ui.button(label="Reset HWID", style=discord.ButtonStyle.red, custom_id="reset_hwid_button")
    async def reset_hwid(self, interaction: discord.Interaction, button: ui.Button):
        user_id = str(interaction.user.id)
        try:
            data, count = supabase.table('keys').select('key').eq('owner_discord_id', user_id).execute()
            if not data[1]:
                await interaction.response.send_message("❌ You do not have a key to reset.", ephemeral=True)
                return
            supabase.table('keys').update({'hwid': None}).eq('owner_discord_id', user_id).execute()
            await interaction.response.send_message("✅ Your HWID has been successfully reset.", ephemeral=True)
        except Exception as e:
            print(f"Error resetting HWID for {user_id}: {e}")
            await interaction.response.send_message("❌ An error occurred.", ephemeral=True)

# ==========================================================
# ==         PANEL COMMAND (INSTANT UPDATE)               ==
# ==========================================================
@tree.command(name="panel", description="Opens your personal control panel.")
async def panel(interaction: discord.Interaction):
    view = ControlPanelView(admin_id="YOUR_DISCORD_USER_ID_HERE")
    # This is the line you changed to make the panel public
    await interaction.response.send_message("Here is your script control panel:", view=view)

# --- Code to start the bot and sync commands ---
@client.event
async def on_ready():
    client.add_view(ControlPanelView(admin_id="YOUR_DISCORD_USER_ID_HERE"))

    # --- THIS IS THE NEW, AGGRESSIVE SYNC LOGIC ---
    try:
        print("Clearing old commands from the server...")
        tree.clear_commands(guild=GUILD_OBJECT)
        await tree.sync(guild=GUILD_OBJECT)
        print("Syncing new commands to the server...")
        await tree.sync(guild=GUILD_OBJECT)
        print("Commands synced successfully!")
    except Exception as e:
        print(f"Error during command sync: {e}")
    # ---------------------------------------------

    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

client.run(TOKEN)
# --------------------------------------------
