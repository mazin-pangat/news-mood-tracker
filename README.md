# News Pulse AI: Global Sentiment Dashboard 📊

An automated news tracking tool that fetches live headlines using NewsAPI and performs real-time sentiment analysis using NLTK's VADER. The results are visualized in an interactive Streamlit dashboard.

## 🚀 Features
* **Live News Fetching:** Real-time headlines via NewsAPI.
* **Sentiment Analysis:** Categorizes news as Positive, Negative, or Neutral.
* **Interactive Visualizations:** Pie charts and bar graphs powered by Plotly.
* **Automated Workflow:** Designed to run seamlessly in Google Colab using Ngrok.

## 🛠️ How to Run
Since this project is optimized for **Google Colab**, follow these steps:

1. **Open the Notebook:** Upload the `app.ipynb` file to Google Colab.
2. **Install Dependencies:**
   ```bash
   pip install pyngrok streamlit newsapi-python pandas nltk plotly
