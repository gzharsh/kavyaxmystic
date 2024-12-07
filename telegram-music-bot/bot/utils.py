# bot/utils.py

def format_playlist(songs):
    response = "📋 **Your Playlist:**\n\n"
    for idx, song in enumerate(songs, 1):
        response += f"{idx}. **{song.name}** by {song.artists}\n"
    return response
