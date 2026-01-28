import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Page Configuration and Title
st.set_page_config(page_title="Used Car Search Engine", layout="wide")
st.title("🚗 Used Car Inventory Search System")
st.markdown("This application allows you to filter and search for cars based on specific criteria.")

# 2. Data Loading with Cache
@st.cache_data
def load_data():
    # Pandas can read a CSV directly from a ZIP file if it's the only file inside it
    df = pd.read_csv('New_Data.zip', compression='zip') 
    return df

df = load_data()

# 3. Sidebar Search Filters
st.sidebar.header("🔍 Search Filters")

# --- Manufacturer Filter ---
brands = df['manufacturer'].unique().tolist()
selected_brands = st.sidebar.multiselect("Select Manufacturer:", brands, default=brands[:3])

# --- Price Range Filter ---
min_price = int(df['price'].min())
max_price = int(df['price'].max())
# Set slider max to 100,000 for better usability
price_range = st.sidebar.slider("Price Range ($):", min_price, 100000, (5000, 30000))

# --- Year Filter ---
min_year = int(df['year'].min())
max_year = int(df['year'].max())
selected_year = st.sidebar.slider("Manufacturing Year:", min_year, max_year, (2010, 2021))

# --- Condition Filter ---
conditions = df['condition'].unique().tolist()
selected_condition = st.sidebar.multiselect("Car Condition:", conditions, default=conditions)

# 4. Applying Filters to the Dataframe
filtered_df = df[
    (df['manufacturer'].isin(selected_brands)) &
    (df['price'].between(price_range[0], price_range[1])) &
    (df['year'].between(selected_year[0], selected_year[1])) &
    (df['condition'].isin(selected_condition))
]

# 5. Displaying the Results
st.subheader(f"Search Results: {len(filtered_df)} cars found")

if not filtered_df.empty:
    # Display interactive data table
    st.dataframe(filtered_df)
    
    # 6. Interactive Visualizations
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📊 Price Distribution for Selected Results:")
        fig1, ax1 = plt.subplots()
        sns.histplot(filtered_df['price'], bins=20, kde=True, ax=ax1, color='blue')
        st.pyplot(fig1)
        
    with col2:
        # Note: Using 'type' as 'model' column was not present in the cleaned data
        st.write("📈 Top 5 Car Types in Search Results:")
        if 'type' in filtered_df.columns:
            top_types = filtered_df['type'].value_counts().head(5)
            fig2, ax2 = plt.subplots()
            sns.barplot(x=top_types.values, y=top_types.index, ax=ax2, palette='viridis')
            plt.xlabel("Count of Cars")
            st.pyplot(fig2)
        else:
            st.info("The 'type' column is not available in the dataset.")

else:
    st.warning("No cars match your search criteria. Please try broadening your filters.")
