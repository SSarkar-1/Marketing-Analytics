import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

def fetch_sql_data():
    # Define the connection parameters
    conn_str=(
        'Driver={SQL Server};'
        "Server=DESKTOP-U7Q3IPR\\SQLEXPRESS;"  
        "Database=PortfolioProject_MarketingAnalytics;"  
        "Trusted_Connection=yes;"  

    )
    conn=pyodbc.connect(conn_str)

    query="SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM dbo.customer_reviews"

    df=pd.read_sql(query,conn)

    conn.close()

    return df

sia=SentimentIntensityAnalyzer()

def calculate_sentiment(review):
    #Getting sentiment Scores
    sentiment=sia.polarity_scores(review)
    return sentiment['compound']

def sentiment_catagorization(score,rating):
    if score > 0.05:  # Positive sentiment score
        if rating >= 4:
            return 'Positive'  # High rating and positive sentiment
        elif rating == 3:
            return 'Mixed Positive'  # Neutral rating but positive sentiment
        else:
            return 'Mixed Negative'  # Low rating but positive sentiment
    elif score < -0.05:  # Negative sentiment score
        if rating <= 2:
            return 'Negative'  # Low rating and negative sentiment
        elif rating == 3:
            return 'Mixed Negative'  # Neutral rating but negative sentiment
        else:
            return 'Mixed Positive'  # High rating but negative sentiment
    else:  # Neutral sentiment score
        if rating >= 4:
            return 'Positive'  # High rating with neutral sentiment
        elif rating <= 2:
            return 'Negative'  # Low rating with neutral sentiment
        else:
            return 'Neutral'  # Neutral rating and neutral sentiment
    
def sentiment_binning(score):
    if score >= 0.5:
        return '0.5 to 1.0'  # Strongly positive sentiment
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'  # Mildly positive sentiment
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'  # Mildly negative sentiment
    else:
        return '-1.0 to -0.5'  # Strongly negative sentiment
    
customer_df=fetch_sql_data()

customer_df['Sentiment_Score']=customer_df['ReviewText'].apply(calculate_sentiment)

customer_df['Sentiment_Category']=customer_df.apply(lambda row:sentiment_catagorization(row['Sentiment_Score'],row['Rating']),axis=1)

customer_df['Sentiment_Score_Bins']=customer_df['Sentiment_Score'].apply(sentiment_binning)

print(customer_df.head())

customer_df.to_csv("Customer_reviews_with_Sentiment.csv")