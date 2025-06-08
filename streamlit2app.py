import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(layout="wide", page_title="Interactive Media Intelligence Dashboard")

st.title("Interactive Media Intelligence Dashboard")

## 1. Upload File
st.header("1. Upload File")
uploaded_file = st.file_uploader("Upload your CSV file here", type=["csv"])

df = None
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.dataframe(df.head()) # Display the first few rows for confirmation
    except Exception as e:
        st.error(f"Error reading file: {e}")

if df is not None:
    ## 2. Data Cleaning
    st.header("2. Data Cleaning")

    # Convert 'Date' column to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        st.write("Converted 'Date' column to datetime format.")
    else:
        st.warning("'Date' column not found. Skipping date conversion.")

    # Fill missing values in 'Engagements' with 0
    if 'Engagements' in df.columns:
        df['Engagements'] = df['Engagements'].fillna(0)
        st.write("Filled missing 'Engagements' values with 0.")
    else:
        st.warning("'Engagements' column not found. Skipping filling missing values.")

    # Normalize column names (lowercase and strip whitespace)
    original_columns = df.columns.tolist()
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    new_columns = df.columns.tolist()
    if original_columns != new_columns:
        st.write("Normalized column names (lowercase and stripped whitespace).")
        st.write(f"Original Columns: {original_columns}")
        st.write(f"Normalized Columns: {new_columns}")

    st.dataframe(df.head()) # Display cleaned data head

    ## 3. Data Visualization
    st.header("3. Data Visualization")

    # Ensure required columns exist after cleaning and normalization
    required_columns = ['date', 'platform', 'sentiment', 'location', 'engagements', 'media_type']
    if not all(col in df.columns for col in required_columns):
        st.error(f"Missing one or more required columns after cleaning. Please ensure your CSV has: {', '.join(required_columns)}")
        st.stop() # Stop execution if essential columns are missing

    col1, col2 = st.columns(2)

    with col1:
        # 📊 Pie Chart: Sentiment Breakdown
        st.subheader("Sentiment Breakdown")
        sentiment_counts = df['sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        fig_sentiment = px.pie(sentiment_counts, values='Count', names='Sentiment', title='Distribution of Sentiment')
        st.plotly_chart(fig_sentiment, use_container_width=True)
        st.markdown("""
        **Insights:**
        * This chart provides a quick overview of the overall sentiment (e.g., positive, negative, neutral) expressed across your media data.
        * A higher proportion of positive sentiment indicates a generally favorable public perception.
        * Conversely, a significant negative sentiment share might flag areas needing attention or crisis management.
        """)

    with col2:
        # 📈 Line Chart: Engagement Trend Over Time
        st.subheader("Engagement Trend Over Time")
        engagement_over_time = df.groupby('date')['engagements'].sum().reset_index()
        fig_engagement_trend = px.line(engagement_over_time, x='date', y='engagements', title='Total Engagements Over Time')
        st.plotly_chart(fig_engagement_trend, use_container_width=True)
        st.markdown("""
        **Insights:**
        * This line chart reveals fluctuations in engagement over time, helping to identify peak activity periods.
        * Spikes in engagement might correlate with specific campaigns, events, or news cycles.
        * Consistent low engagement could signal a need to re-evaluate content strategy or platform presence.
        """)

    col3, col4 = st.columns(2)

    with col3:
        # 📊 Bar Chart: Engagements by Platform
        st.subheader("Engagements by Platform")
        engagements_by_platform = df.groupby('platform')['engagements'].sum().reset_index()
        engagements_by_platform = engagements_by_platform.sort_values('engagements', ascending=False)
        fig_platform_engagement = px.bar(engagements_by_platform, x='platform', y='engagements', title='Total Engagements by Platform')
        st.plotly_chart(fig_platform_engagement, use_container_width=True)
        st.markdown("""
        **Insights:**
        * This bar chart highlights which platforms are generating the most engagement for your media.
        * Focus your resources on platforms with higher engagement to maximize impact.
        * Low engagement on certain platforms might suggest they are not reaching your target audience effectively.
        """)

    with col4:
        # 🥧 Pie Chart: Media Type Mix
        st.subheader("Media Type Mix")
        media_type_counts = df['media_type'].value_counts().reset_index()
        media_type_counts.columns = ['Media Type', 'Count']
        fig_media_type = px.pie(media_type_counts, values='Count', names='Media Type', title='Distribution of Media Types')
        st.plotly_chart(fig_media_type, use_container_width=True)
        st.markdown("""
        **Insights:**
        * This pie chart illustrates the variety and prevalence of different media types in your dataset (e.g., text, image, video).
        * Understanding your media mix can help in optimizing content creation and distribution strategies.
        * A dominant media type might indicate audience preference or a current content focus.
        """)

    # 📊 Bar Chart: Top 5 Locations by Engagement
    st.subheader("Top 5 Locations by Engagement")
    engagements_by_location = df.groupby('location')['engagements'].sum().reset_index()
    top_5_locations = engagements_by_location.sort_values('engagements', ascending=False).head(5)
    fig_top_locations = px.bar(top_5_locations, x='location', y='engagements', title='Top 5 Locations by Engagement')
    st.plotly_chart(fig_top_locations, use_container_width=True)
    st.markdown("""
    **Insights:**
    * This bar chart identifies the geographical areas where your media is generating the most engagement.
    * Use this information to tailor content for specific regional audiences or identify new target markets.
    * Understanding top locations can inform localized marketing campaigns and outreach efforts.
    """)
