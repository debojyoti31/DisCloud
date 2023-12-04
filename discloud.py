import os
import shutil
import discord
import random
from discord.ext import commands
from cryptography.fernet import Fernet
import math
import io
import pytz

# Set 'BOT_TOKEN' with your actual bot token
BOT_TOKEN = 'your_bot_token'

# Set the Chunk Size
chunk_size = 15 * 1024 * 1024

# Set your Time Zone 
your_timezone = 'Asia/Kolkata'

path_separator = os.path.sep

# Function to load a key from a file
with open("enckey.key", 'rb') as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)

intents = discord.Intents.all()

# Create an instance of the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Command not found, send available commands and their descriptions
        command_list = "\n".join([f"**{command.name}**: {command.help}" for command in bot.commands])
        await ctx.send(f"Command not found. Available commands:\n{command_list}")
    else:
        raise error

@bot.command(name='split', help='Split a file and upload its parts to Discord.')
async def split(ctx, *, file_path: str):
    """
    Split a file into parts and upload them to the Discord server.
    Usage: !split <file_path>
    """
    file_name = file_path.split(path_separator)[-1]

    # Check if the file has already been uploaded to Discord
    if await is_file_uploaded(ctx, file_name):
        await ctx.send(f"File '{file_name}' has already been uploaded.")
        return

    if not os.path.exists(file_path):
        await ctx.send(f"File '{file_name}' not found.")
        return

    part_num = 1

    try:
        with open(file_path, 'rb') as file:
            total_parts = (os.path.getsize(file_path) + chunk_size - 1) // chunk_size  # Calculate total parts
            while True:
                chunk = file.read(chunk_size)
                encrypted_chunk = cipher_suite.encrypt(chunk)
                if not chunk:
                    break

                # Upload the part to Discord
                await ctx.send(f"Uploading part {part_num}/{total_parts} of: {file_name}")
                await ctx.send(file=discord.File(io.BytesIO(encrypted_chunk), filename=f"{file_name}_part{part_num}.txt"))
                part_num += 1

        await ctx.send(f"{file_name} has been split into parts and uploaded.")
    except IsADirectoryError:
        await ctx.send(f"'{file_path}' is a directory, NOT a File! ")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command(name='combine', help='Download the files from Discord and Combine Them.')
async def combine(ctx, *, combined_file_path: str):
    """
    Combine file parts and download the original file.
    Usage: !combine <output_file_path>
    """

    file_name = combined_file_path.split(path_separator)[-1]

    # Check if the file has already been uploaded to Discord
    if not await is_file_uploaded(ctx, file_name):
        await ctx.send(f"File '{file_name}' not found.")
        return
    
    # Check if the combined file already exists
    if os.path.exists(combined_file_path):
        await ctx.send(f"File **{file_name}** already exists at **{combined_file_path.rsplit(path_separator, 1)[0]}**.\nPlease choose a different output path.")
        return

    # Download file parts from Discord
    parts_folder = await download_file_parts(ctx, combined_file_path)

    if not parts_folder:
        await ctx.send(f"Error downloading parts for '{file_name}'.")
        return

    try:
        # Combine file parts into the original file
        await ctx.send(f"Combining parts for '{file_name}'")
        combine_parts(combined_file_path, parts_folder)
        # Send the combined file to the user
        await ctx.send(f"Saved '{file_name}' at '{combined_file_path.rsplit(path_separator, 1)[0]}'")

    finally:
        # Clean up: Delete the temporary folder
        shutil.rmtree(parts_folder, ignore_errors=True)


@bot.command(name='delete', help='Delete parts of uploaded file.')
async def delete(ctx, *, file_name: str):
    """
    Delete all uploaded file parts from the Discord channel.
    Usage: !delete <file_name>
    """
    # Check if the file parts are uploaded
    if not await is_file_uploaded(ctx, file_name):
        await ctx.send(f"File parts for '{file_name}' not found.")
        return

    # Delete file parts from the channel
    await delete_file_parts(ctx, file_name)

    await ctx.send(f"All file parts for '{file_name}' have been deleted.")


@bot.command(name='listfiles', help='Get all the uploaded files.')
async def listfiles(ctx):
    """
    Display a list of all uploaded files in the Discord channel.
    Usage: !listfiles
    """
    uploaded_files = await get_uploaded_files(ctx)

    if not uploaded_files:
        await ctx.send("No files have been uploaded.")
    else:
        file_list = "\n".join(f"**{index + 1}.** {file}" for index, file in enumerate(uploaded_files))
        await ctx.send(f"**Uploaded Files:**\n{file_list}")


@bot.command(name='filedetails', help='Get details of an uploaded file.')
async def filedetails(ctx, *, file_name: str):
    """
    Display details of a specific uploaded file in the Discord channel.
    Usage: !details <file_name>
    """
    file_details = await get_file_details(ctx, file_name)

    if not file_details:
        await ctx.send(f"File '{file_name}' not found.")
    else:
        await ctx.send(f"**Details for:** '{file_name}'\n{file_details}")


def combine_parts(combined_file_path, parts_folder):
    file_name = combined_file_path.split(path_separator)[-1]

    with open(combined_file_path, 'wb') as combined_file:
        part_num = 1

        while True:
            part_file_path = os.path.join(parts_folder, f"{file_name}_part{part_num}.txt")
            if not os.path.exists(part_file_path):
                # print(part_file_path)
                break

            with open(part_file_path, 'rb') as part_file:
                read_part_file = part_file.read()
                decrypted_part_file = cipher_suite.decrypt(read_part_file)
                combined_file.write(decrypted_part_file)
                os.remove(part_file_path)

            part_num += 1


async def download_file_parts(ctx, combined_file_path):
    file_name = combined_file_path.rsplit(path_separator,1)[1]
    # Create a temporary folder to store downloaded file parts
    parts_folder = os.path.join(combined_file_path.rsplit(path_separator,1)[0], f"discloud_temp_parts_{random.randint(1000, 9000)}")
    os.makedirs(parts_folder, exist_ok=True)

    # Search for messages in the channel with file parts matching the file name
    async for message in ctx.channel.history(limit=None):
        for attachment in message.attachments:
            if attachment.filename.rsplit('_', 1)[0] == file_name:
                part_file_path = os.path.join(parts_folder, attachment.filename)
                await ctx.send(f"Downloading part {attachment.filename}")
                await attachment.save(part_file_path)

    return parts_folder


async def is_file_uploaded(ctx, file_name):
    # Search for messages in the channel with attachments matching the file name
    async for message in ctx.channel.history(limit=None):
        for attachment in message.attachments:
            if attachment.filename.rsplit('_', 1)[0] == file_name:
                return True
    return False


async def delete_file_parts(ctx, file_name):
    # Search for messages in the channel with file parts matching the file name
    async for message in ctx.channel.history(limit=None):
        for attachment in message.attachments:
            if attachment.filename.rsplit('_', 1)[0] == file_name:
                await ctx.send(f"Deleting part {attachment.filename}")
                await message.delete()


async def get_uploaded_files(ctx):
    """
    Retrieve a list of uploaded original files in the Discord channel.
    """
    uploaded_files = set()

    async for message in ctx.channel.history(limit=None):
        for attachment in message.attachments:
            file_name = attachment.filename
            # Extract the original file name
            original_file_name = file_name.rsplit('_', 1)[0]
            uploaded_files.add(original_file_name)

    return uploaded_files


def format_size(size_in_bytes):
    """
    Format the size in bytes to a human-readable format.
    """
    if size_in_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_in_bytes, 1024)))
    p = math.pow(1024, i)
    size = round(size_in_bytes / p, 2)
    return f"{size} {size_name[i]}"


async def get_file_details(ctx, file_name):
    """
    Retrieve details of a specific uploaded file in the Discord channel.
    """
    total_parts, total_size, last_uploaded_timestamp = 0, 0, None

    async for message in ctx.channel.history(limit=None):
        for attachment in message.attachments:
            if attachment.filename.rsplit('_', 1)[0] == file_name:
                total_parts += 1
                total_size += attachment.size
                current_timestamp = message.created_at.replace(tzinfo=pytz.UTC)
                if last_uploaded_timestamp is None or current_timestamp > last_uploaded_timestamp:
                    last_uploaded_timestamp = current_timestamp

    if total_parts == 0:
        return None

    formatted_size = format_size(total_size)
    last_uploaded_timestamp_local = last_uploaded_timestamp.astimezone(pytz.timezone(your_timezone))

    return f"**Total Parts:** {total_parts}\n**Total Size:** {formatted_size}\n**Last Uploaded at:** {last_uploaded_timestamp_local.strftime('%Y-%m-%d %H:%M:%S %Z')}"


bot.run(BOT_TOKEN)
