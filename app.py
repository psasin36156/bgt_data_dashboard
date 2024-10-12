import streamlit as st
import pandas as pd
import plotly.express as px

from PIL import Image

# Add this at the top of your app, right after the imports
st.markdown(
    """
    <style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load and display the logo
logo = Image.open("Screenshot_23.png")
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(logo, use_column_width=True)

# Add some space after the logo
st.markdown("<br>", unsafe_allow_html=True)

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv('clean_bgt_12OCT2024.csv')

df = load_data()

# Set page title
st.title("$BGT Rank Finder")

st.info("⚠️ Note: This webapp only shows addresses holding more than 1 BGT.")

########################################################################################
########################################################################################
# Feature 1: Address input to search rank
st.header("Search Your Wallet Rank")
address = st.text_input("Enter your wallet address:")

if address:
    # Assuming 'address' and 'amount' columns exist in the CSV
    if address in df['HolderAddress'].values:
        # Sort the dataframe by Balance in descending order and reset the index
        sorted_df = df.sort_values('Balance', ascending=False).reset_index(drop=True)
        
        # Find the index of the address, which will be its rank
        rank = sorted_df[sorted_df['HolderAddress'] == address].index[0] + 1  # Adding 1 because index starts at 0
        
        amount = df[df['HolderAddress'] == address]['Balance'].values[0]
        st.success(f"Your wallet rank is {rank} with an amount of {amount:.2f} $BGT")
    else:
        st.error("Address not found in the dataset(this dashboard only show wallet that holding more than 1 BGT).")

########################################################################################
########################################################################################
st.subheader("Distribution of Total Balance by Range")

# Define the bins for the ranges
bins = [1, 10, 100, 500, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]
labels = ['1-10', '10-100', '100-500', '500-1000', '1000-10000', '10000-100000', '100000-1M', '1M-10M', '10M-100M']

# Cut the Balance data into bins
df['BalanceRange'] = pd.cut(df['Balance'], bins=bins, labels=labels, right=False)\

# Calculate the sum of Balance for each range
balance_sum = df.groupby('BalanceRange')['Balance'].sum().sort_index()

# Create a pie chart
# Calculate the sum of Balance for each range
balance_sum = df.groupby('BalanceRange')['Balance'].sum().sort_index()
names=balance_sum.index,
# Create a DataFrame for the pie chart
pie_data = pd.DataFrame({
    'BalanceRange': balance_sum.index,
    'TotalBalance': balance_sum.values
})

earth_tones = [
    "#8B4513",  # Saddle Brown
    "#A0522D",  # Sienna
    "#CD853F",  # Peru
    "#D2691E",  # Chocolate
    "#DEB887",  # Burlywood
    "#F4A460",  # Sandy Brown
    "#D2B48C",  # Tan
    "#FFDAB9",  # Peach Puff
    "#F0E68C",  # Khaki
    "#BDB76B",  # Dark Khaki
    "#6B8E23",  # Olive Drab
    "#808000",  # Olive
    "#556B2F",  # Dark Olive Green
    "#8FBC8F",  # Dark Sea Green
    "#2F4F4F"   # Dark Slate Gray
]
# Create a pie chart
fig = px.pie(
    data_frame=pie_data,
    values='TotalBalance',
    names='BalanceRange',
    title="Distribution of Total Balance by Range",
    labels={'TotalBalance': 'Total Balance'},
    hover_data=['TotalBalance'],
    color_discrete_sequence=earth_tones
)

labels = ['0-1', '1-10', '10-100', '100-500', '500-1000', '1000-10000', '10000-100000', '100000-1M', '1M-10M', '10M-100M',]

st.plotly_chart(fig)



########################################################################################
########################################################################################
st.subheader("Number of Holders by Balance Range")

# Count the number of holders in each bin
holders_count = df['BalanceRange'].value_counts().sort_index()

# Create a DataFrame for the full table
holders_count_df = pd.DataFrame({
    'Balance Range ($BGT)': holders_count.index,
    'Number of Holders': holders_count.values,
})

st.table(holders_count_df)


########################################################################################
########################################################################################
st.subheader("Top 20 Wallets (without team wallet)")
top_20 = df.nlargest(20, 'Balance')[['HolderAddress', 'Balance']]
st.table(top_20)
# Add footer with additional information
st.info("⚠️ Last data update: 12 OCT 2024 (manually updated every 3days 🥺🥺)")

########################################################################################
########################################################################################

# Add contact information
st.markdown("---")
st.subheader("Contact Information")
st.markdown("For more information or support, reach out to me on:")
st.markdown("- Telegram: @sapiensp")
st.markdown("- Twitter: @0xsapiensp")
st.markdown("- Discord: @sapiensp")


# Add "Buy Me a Coffee" message with donation address
st.markdown("---")
st.subheader("☕️ Support My Work 🙏")
st.markdown("If you find this tool helpful, consider buying me a coffee! ✨")
st.markdown("To support, send donation to:")
st.code("0xcD6e45Aa577dd494C619D02Fc302f2FBBC3c6D29", language="text")
st.markdown("Your support keeps me caffeinated and updating! 💖")
