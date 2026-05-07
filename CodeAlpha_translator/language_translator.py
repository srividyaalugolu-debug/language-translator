import streamlit as st
from deep_translator import GoogleTranslator
st.title("🌍 Language Translator")
languages = {
    "Hindi": "hi",
    "English": "en",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Odia": "or",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Turkish": "tr",
    "Dutch": "nl",
    "Thai": "th"
}
if "source" not in st.session_state:
    st.session_state.source = "English"
if "target" not in st.session_state:
    st.session_state.target = "Hindi"
if "translated" not in st.session_state:
    st.session_state.translated = ""
col1, col2 = st.columns(2)
with col1:
    source = st.selectbox("From", list(languages.keys()), index=list(languages.keys()).index(st.session_state.source))
    text = st.text_area("Enter text")
with col2:
    target = st.selectbox("To", list(languages.keys()), index=list(languages.keys()).index(st.session_state.target))
if st.button("🔄 Swap Languages"):
    st.session_state.source, st.session_state.target = st.session_state.target, st.session_state.source
    st.rerun()
if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter some text")
    else:
        try:
            translated = GoogleTranslator(
                source=languages[source],
                target=languages[target]
            ).translate(text)
            st.session_state.translated = translated
        except:
            st.error("Translation failed")
if st.session_state.translated:
    st.text_area("Translation", value=st.session_state.translated, height=200)
if st.button("copy text"):
    st.success("text copied! (now press ctrl + C to copy manually)")
    st.code(st.session_state.translated)