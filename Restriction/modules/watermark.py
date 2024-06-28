# watermark.py

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from tempfile import NamedTemporaryFile
from config import OWNER_ID
from Restriction import app


async def apply_watermark(client: Client, message: Message):
    if len(message.command) < 6:
        await message.reply_text(
            "Incorrect format!\n\n"
            "/watermark <text> <position> <size> <duration_check> <font_style>\n\n"
            "Example:\n"
            "/watermark Gagan m 48 1800 f2"
        )
        return
    
    watermark_text = message.command[1]
    position = message.command[2]
    size = int(message.command[3])
    duration_check = int(message.command[4])
    font_style = message.command[5]

    # Check if the message is a video
    if message.video:
        video_path = await message.download()
        video_duration = VideoFileClip(video_path).duration

        if video_duration > duration_check:
            await message.reply_text(f"Video duration exceeds {duration_check} seconds. Skipping watermarking.")
            return
        
        temp_filename = f"watermarked_{os.path.basename(video_path)}"
        temp_video_path = os.path.join("temp", temp_filename)

        try:
            clip = VideoFileClip(video_path)
            txt_clip = TextClip(
                watermark_text,
                fontsize=size,
                color='white',
                font='Arial-Bold',
            )

            if font_style == 'f2':
                txt_clip = txt_clip.set_position(position)
            elif font_style == 'f3':
                txt_clip = txt_clip.set_position(position)
            elif font_style == 'f4':
                txt_clip = txt_clip.set_position(position)
            else:
                txt_clip = txt_clip.set_position(position)
                
            video = CompositeVideoClip([clip, txt_clip])
            video.write_videofile(temp_video_path)
        except Exception as e:
            await message.reply_text(f"Error applying watermark: {str(e)}")
            return

        await client.send_video(
            chat_id=message.chat.id,
            video=temp_video_path,
            reply_to_message_id=message.message_id,
            caption=f"Watermarked video with '{watermark_text}'"
        )

        # Cleanup
        os.remove(video_path)
        os.remove(temp_video_path)

    else:
        await message.reply_text("Please reply to a video file.")


# Register the handler for /watermark command
@app.on_message(filters.command("watermark") & filters.user(OWNER_ID))
async def watermark_command(client: Client, message: Message):
    await apply_watermark(client, message)
