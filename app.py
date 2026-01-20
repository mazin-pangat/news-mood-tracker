# 1. INSTALL DEPENDENCIES
!pip install pyngrok streamlit newsapi-python pandas nltk plotly wordcloud -q

# 2. CREATE THE APP FILE
with open('app.py', 'w') as f:
    f.write("""
import streamlit as st
import pandas as pd
import plotly.express as px
import nltk
from newsapi import NewsApiClient
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Setup
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

st.set_page_config(page_title="News Pulse AI", layout="wide")

# UI Styling
st.markdown('''
    <style>
    .stTextInput>div>div>input { background-color: #f0f2f6 !important; color: black !important; }
    label { font-size: 16px !important; font-weight: bold !important; }
    footer {visibility: hidden;}
    </style>
    ''', unsafe_allow_html=True)

st.title("📊 News Pulse AI: Global Sentiment Dashboard")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter NewsAPI Key", type="password")
    topic = st.text_input("Search Topic", value="Artificial Intelligence")
    num_articles = st.slider("Number of Articles", 10, 50, 20)
    run_btn = st.button("🚀 GENERATE DASHBOARD")

if run_btn:
    if not api_key:
        st.error("Missing API Key! Get one at newsapi.org")
    else:
        try:
            newsapi = NewsApiClient(api_key=api_key)
            articles = newsapi.get_everything(q=topic, language='en', sort_by='relevancy', page_size=num_articles)

            if articles['totalResults'] == 0:
                st.warning("No news found for this topic.")
            else:
                data = []
                for a in articles['articles']:
                    score = sia.polarity_scores(a['title'])['compound']
                    mood = 'Positive' if score > 0.05 else ('Negative' if score < -0.05 else 'Neutral')
                    data.append({'Title': a['title'], 'Source': a['source']['name'], 'Score': score, 'Mood': mood})

                df = pd.DataFrame(data)

                # Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Articles", len(df))
                m2.metric("Avg Sentiment", round(df['Score'].mean(), 2))
                m3.metric("Top Mood", df['Mood'].mode()[0])

                # Charts
                c1, c2 = st.columns([1, 2])
                with c1:
                    fig_pie = px.pie(df, names='Mood', title="Mood Distribution",
                                   color='Mood', color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'})
                    st.plotly_chart(fig_pie, use_container_width=True)

                with c2:
                    fig_bar = px.bar(df, x='Score', y='Title', color='Mood',
                                   title="Sentiment Score by Headline", orientation='h',
                                   color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'})
                    st.plotly_chart(fig_bar, use_container_width=True)

                st.dataframe(df[['Title', 'Source', 'Mood']])
        except Exception as e:
            st.error(f"Error: {e}")
""")

# --- STEP 3: START TUNNEL AND RUN (REFINED VERSION) ---
from pyngrok import ngrok
import os
import time

# 1. Provide your token
NGROK_TOKEN = "38Vn8dHtRa6QLm1DjLoV2B2r46Q_2gF8tqX6nzhrgvuACtcQo"
!ngrok config add-authtoken {NGROK_TOKEN}

# 2. FORCE KILL any hidden ngrok or streamlit processes
!pkill ngrok
!pkill streamlit
time.sleep(2) # Wait 2 seconds for processes to fully close

# 3. Start Streamlit in background
# We redirect output to a log file so it doesn't clutter Colab
os.system("streamlit run app.py > /dev/null 2>&1 &")
time.sleep(3) # Give Streamlit time to initialize its server

# 4. Open the tunnel
try:
    # Use bind_tls=True to ensure an https link
    public_url = ngrok.connect(8501, bind_tls=True)
    print(f"\n✅ DASHBOARD IS ONLINE")
    print(f"URL: {public_url.public_url}")
except Exception as e:
    print(f"❌ Error starting Ngrok: {e}")
    print("TIP: If it says 'Already Online', wait 1 minute and run this cell again.")
