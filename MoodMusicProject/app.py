import streamlit as st
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Emotion Regulation Music Recommender",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Emotion Regulation Music Recommender")

st.write(
    "Describe how you're feeling today. "
    "The system will analyze your emotion and suggest music to help regulate your mood."
)

# ---------------------------------------------------
# Spotify Authentication
# ---------------------------------------------------

CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

auth_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager=auth_manager)

# ---------------------------------------------------
# Emotion Detection Function
# ---------------------------------------------------

def detect_emotion(text):

    text_lower = text.lower()

    # Keyword-based detection
    if any(word in text_lower for word in ["angry", "mad", "furious", "irritated"]):
        return "anger"
    elif any(word in text_lower for word in ["sad", "down", "depressed", "upset", "crying"]):
        return "sadness"
    elif any(word in text_lower for word in ["anxious", "scared", "afraid", "nervous", "worried"]):
        return "fear"
    elif any(word in text_lower for word in ["excited", "thrilled", "surprised", "shocked"]):
        return "surprise"
    elif any(word in text_lower for word in ["love", "romantic", "caring", "attached"]):
        return "love"

    # Sentiment fallback
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.3:
        return "joy"
    elif polarity < -0.3:
        return "sadness"
    else:
        return "neutral"

# ---------------------------------------------------
# Emotion → Query Mapping (Spotify Search)
# ---------------------------------------------------

emotion_query_map = {
    "anger": "calming instrumental music",
    "sadness": "uplifting acoustic songs",
    "fear": "relaxing piano music",
    "joy": "happy upbeat pop songs",
    "love": "romantic love songs",
    "surprise": "energetic indie music",
    "neutral": "chill lofi beats"
}

# ---------------------------------------------------
# Emotion → Music Explanation Mapping
# ---------------------------------------------------

emotion_music_map = {
    "anger": (
        "Calming instrumental / Lo-fi beats",
        "You're feeling angry. Slow, calming music can help regulate intense emotions."
    ),
    "sadness": (
        "Soft hopeful songs / Acoustic ballads",
        "You're feeling low. Gentle uplifting music can gradually improve mood."
    ),
    "fear": (
        "Soft piano / Ambient relaxation music",
        "You're feeling anxious. Peaceful and slow music can reduce stress."
    ),
    "joy": (
        "Feel-good pop / Upbeat music",
        "You're already happy! Let’s maintain that positive energy."
    ),
    "love": (
        "Romantic acoustic / Soft love songs",
        "Romantic emotions pair beautifully with warm acoustic tracks."
    ),
    "surprise": (
        "Light energetic indie music",
        "Unexpected emotions can be balanced with light energetic music."
    ),
    "neutral": (
        "Chill lo-fi / Background focus music",
        "You're feeling neutral. Relaxed music can maintain emotional balance."
    )
}

# ---------------------------------------------------
# User Input Section
# ---------------------------------------------------

user_input = st.text_input("How are you feeling today?")

if user_input:

    # 1️⃣ Detect emotion first
    detected_emotion = detect_emotion(user_input)

    st.subheader(f"🧠 Detected Emotion: {detected_emotion.capitalize()}")

    # 2️⃣ Show explanation + music type
    if detected_emotion in emotion_music_map:
        music_type, message = emotion_music_map[detected_emotion]
        st.success(message)
        st.write(f"🎧 **Suggested Music Type:** {music_type}")
    else:
        st.warning("Emotion detected but no music mapping found.")

    # 3️⃣ Fetch Spotify songs
    query = emotion_query_map[detected_emotion]

    results = sp.search(q=query, type="track", limit=5)

    st.subheader("🎵 Recommended Songs:")

    for track in results["tracks"]["items"]:
        name = track["name"]
        artist = track["artists"][0]["name"]
        url = track["external_urls"]["spotify"]

        st.write(f"**{name}** - {artist}")
        st.markdown(f"[Play on Spotify]({url})")
