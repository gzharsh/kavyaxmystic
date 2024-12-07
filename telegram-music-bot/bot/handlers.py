# bot/handlers.py

from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
from bot.spotify_integration import SpotifyClient
from bot.database import Database
from bot.utils import search_tracks, format_playlist

spotify = SpotifyClient()
db = Database()

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎵 Welcome to MusicBot! 🎵\n"
        "Use /search <song name> to find music.\n"
        "Use /save <song name> to add to your playlist.\n"
        "Use /playlist to view your saved songs."
    )

def search_command(update: Update, context: CallbackContext):
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text("Please provide a song name. Usage: /search <song name>")
        return

    tracks = spotify.search_tracks(query)
    if not tracks:
        update.message.reply_text("No tracks found.")
        return

    response = ""
    for idx, track in enumerate(tracks, 1):
        response += f"{idx}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}\n"

    update.message.reply_text(response)

def save_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text("Please provide a song name to save. Usage: /save <song name>")
        return

    track = spotify.get_track(query)
    if not track:
        update.message.reply_text("Track not found.")
        return

    db.add_song(user_id, track['id'], track['name'], track['artists'], track['preview_url'])
    update.message.reply_text(f"✅ Saved '{track['name']}' to your playlist.")

def playlist_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    songs = db.get_playlist(user_id)
    if not songs:
        update.message.reply_text("Your playlist is empty. Use /save <song name> to add songs.")
        return

    response = format_playlist(songs)
    update.message.reply_text(response)

def inline_query(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return

    tracks = spotify.search_tracks(query)
    results = []
    for track in tracks[:10]:
        results.append(
            InlineQueryResultArticle(
                id=track['id'],
                title=track['name'],
                input_message_content=InputTextMessageContent(f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}\n{track['preview_url']}")
            )
        )

    update.inline_query.answer(results)

def setup_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search", search_command))
    dispatcher.add_handler(CommandHandler("save", save_command))
    dispatcher.add_handler(CommandHandler("playlist", playlist_command))
    dispatcher.add_handler(InlineQueryHandler(inline_query))
