import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Mood Music Recommender", page_icon="🎵")

st.title("🎵 Emotion Regulation Music Recommender")

st.write("Type how you are feeling and let the system suggest music to balance your mood.")

# Load Emotion Model
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)

# Emotion → Regulation Music Mapping
emotion_music_map = {
    "anger": ("Calming instrumental / Lo-fi", 
              "You're feeling angry. Let's slow things down with calming music."),
    "sadness": ("Soft hopeful songs", 
                "You're feeling low. Let's gently lift your mood."),
    "fear": ("Soft piano / Ambient music", 
             "You're feeling anxious. Slow, peaceful music can help."),
    "joy": ("Feel-good pop music", 
            "You're already happy! Let’s keep that energy flowing."),
    "love": ("Romantic acoustic songs", 
             "Romantic vibes deserve warm love songs."),
    "surprise": ("Light energetic music", 
                 "Unexpected feelings? Let’s balance it with light energy."),
    "disgust": ("Soothing instrumental", 
                "Let's reset your mood with peaceful music.")
}

user_input = st.text_input("How are you feeling today?")

if user_input:
    result = emotion_model(user_input)
    detected_emotion = result[0]['label']
    confidence = result[0]['score']

    st.subheader(f"Detected Emotion: {detected_emotion}")
    st.write(f"Confidence Score: {confidence:.2f}")

    if detected_emotion in emotion_music_map:
        music_type, message = emotion_music_map[detected_emotion]

        st.success(message)
        st.write(f"🎧 Suggested Music Type: **{music_type}**")

    else:
        st.write("Emotion detected but no mapping found.")