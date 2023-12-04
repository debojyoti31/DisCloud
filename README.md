---
# DisCloud
---

# Introduction

Discord provides unlimited space to upload your files, but you can
upload files with a max 25 MB size. DisCloud is a Python-based
application designed to facilitate the management of large files within
a Discord server. This bot offers functionality to split a file into
parts, upload them to a Discord channel, and later combine those parts
to reconstruct the original file. Ultimately, you get UNLIMITED STORAGE
SPACE. The use of encryption ensures the security of the file content
during the split and combine operations.

## Key Features

-   \*\*File Splitting:\*\* Break down large files into manageable parts
    for sharing on Discord.

-   \*\*Encryption:\*\* Ensure the security of file content by
    encrypting each part using the Fernet encryption algorithm.

-   \*\*File Combining:\*\* Reassemble file parts on Discord to recreate
    the original file.

-   \*\*Deletion of File Parts:\*\* Manage server storage by providing
    the ability to delete previously uploaded file parts.

-   \*\*List Uploaded Files:\*\* Get a list of all uploaded files in the
    Discord channel.

-   \*\*File Details:\*\* Get details of a specific uploaded file.

## How it Works

The bot utilizes discord.py for interaction with Discord servers and the
cryptography library for file encryption. Users can trigger commands in
a Discord channel to split, combine, or delete file parts. Additionally,
users can list all uploaded files and get details of a specific file.
Each file part is encrypted before upload to maintain data privacy.

This application is particularly useful in scenarios where file size
limitations on Discord may pose challenges, offering a seamless solution
for sharing large files while ensuring data security.


# Create a Discord Server

1.  Open Discord and log in to your account.

2.  On the left sidebar, click the ’+’ button to create a new server.

3.  Choose "Create My Own" and enter a name for your server.

4.  Customize your server settings and click "Create."

# Create a Discord Bot

1.  Go to the [Discord Developer
    Portal](https://discord.com/developers/applications).

2.  Click on "New Application" and give your application a name.

3.  Navigate to the "Bot" tab and click "Reset Token."

4.  Under the "Token" section, click "Copy" to copy your bot token.

# Add the Bot to the Server

1.  Go back to the [Discord Developer
    Portal](https://discord.com/developers/applications).

2.  In your application, go to the "OAuth2" tab.

3.  Under the "OAuth2 URL Generator," select the "bot" scope.

4.  Scroll down, select the "Administrator" bot permission, and copy the
    generated URL.

5.  Paste the URL into your browser, choose your server, and authorize
    the bot.

# Create a Private Text Channel

1.  In your Discord server.

2.  Go to the "Text Channel" tab and click on the "+" button to create a
    new channel.

3.  Give it a name.

4.  Set the channel to "Private" and select the bot as a member.

5.  Create the channel

# Prerequisites

Before using the bot, ensure that you have the following prerequisites:

-   Python installed on your machine.

-   Discord bot token obtained from the Discord Developer Portal.

# Setup

1.  Clone the repository containing the Discord bot code.

2.  Install the required Python packages by running:

    ``` sh
    pip install discord.py cryptography
    ```

3.  Set the `BOT_TOKEN` variable in `discloud.py` with your Discord bot
    token.

4.  Run `genkey.py` to generate the encryption key `enckey.key` if you
    need a new key.

5.  Never ever lose the encryption key. If you do, you won’t be able to
    use the files ever again. The key you used to encrypt the part files
    when uploading is needed to decrypt the downloaded part to its
    original form.

# Usage

## Splitting a File and Upload

To split a file and upload its parts to Discord, use the following
command in a Discord channel where the bot is present:

``` sh
!split <file_path>
```

Replace `<file_path>` with the path to the file you want to split.

## Combining File Parts and Downloading

To combine file parts and download the original file, use the following
command:

``` sh
!combine <output\_file\_path>
```

Replace `<output_file_path>` with the desired path for the combined
file. Suppose the file you want to download is `fileName.ext`, and the
path where you want to download it is `my/custom/path`. So, the
`output_file_path` will be: `my/custom/path/filename.ext`

## Deleting File Parts

To delete all uploaded file parts from the Discord channel, use the
following command:

``` sh
!delete <file\_name>
```

## Listing Uploaded Files

To get a list of all uploaded files in the Discord channel, use the
following command:

``` sh
!listfiles
```

## File Details

To get details of a specific uploaded file, use the following command:

``` sh
!filedetails <file\_name>
```

Replace `<file_name>` with the name of the file you want details for.



#### Before using this Discord bot, it is important to familiarize yourself with Discord's privacy policy. This application interacts with Discord servers and processes file-related operations. Ensure that you comply with Discord's terms of service and privacy policy to protect user data and adhere to the platform's guidelines.
