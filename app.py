import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Use full width
st.set_page_config(layout="wide")

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Select a Page",
        options=["Dashboard", "Cluster Table", "Data"],
        icons=["📊", "🧩", "📄"],
        menu_icon="cast",
        default_index=0
    )

# Load data
df = pd.read_excel('model_summary_v1.xlsx')
df3 = pd.read_excel('model_summary_v1.xlsx', sheet_name='data')

# Initialize session state for tracking selected customer and selected metric
if "selected_customer" not in st.session_state:
    st.session_state.selected_customer = None
if "selected_metric" not in st.session_state:
    st.session_state.selected_metric = None

# Function to open profile page
def open_profile(customer_name):
    st.session_state.selected_customer = customer_name

def toggle_metric(metric):
    """Function to update session state to ensure only one dataframe is shown at a time."""
    if st.session_state.selected_metric == metric:
        st.session_state.selected_metric = None  # If same button is clicked again, hide data
    else:
        st.session_state.selected_metric = metric  # Set to newly clicked button

# ------------------------------------------ Profile Page ------------------------------------------
if st.session_state.selected_customer:
    st.title(f"👤 Profile of {st.session_state.selected_customer}")

    # Get customer data
    customer_data = df3[df3['name'] == st.session_state.selected_customer].iloc[0]

    # Basic Information
    st.subheader("📌 Basic Info")
    st.write(f"**Customer ID:** {customer_data['customer_id']}")
    st.write(f"**Email:** {customer_data['email']}")
    st.write(f"**Phone:** {customer_data['phone']}")
    st.write(f"**Cluster:** {customer_data['cluster_name']}")

    st.markdown("---")

    # Purchase History
    st.subheader("🛒 Purchase History")
    st.write(f"**Total Headsets Purchased:** {customer_data['total_headset_quantity']}")
    st.write(f"**Average Spend per Purchase:** ${customer_data['average_spent_per_purchase_headset']}")

    st.markdown("---")

    # Engagement Metrics
    st.subheader("📊 Engagement Metrics")
    st.write(f"**Total Minutes Spent:** {customer_data['Total_minutes_spent']}")
    st.write(f"**Unique Sessions Listened:** {customer_data['Unique_sessions_listened']}")
    st.write(f"**Last Purchase Date:** {customer_data['last_headset_purchase_date']}")

    st.markdown("---")

    # Subscription Status
    st.subheader("🔔 Subscription Status")
    st.write(f"**Status:** {customer_data['status']}")
    st.write(f"**Cancellation Flag:** {customer_data['flag_canceled']}")
    st.write(f"**Used to Buy More Headsets?** {customer_data['flag_used_to_buy_more_headset']}")

    st.markdown("---")
    # Back Button
    if st.button("🔙 Back to Data Page"):
        st.session_state.selected_customer = None
    st.stop()  # Prevents rendering other pages when viewing a profile

# ------------------------------------------ Dashboard Page ------------------------------------------
# ------------------------------------------ Dashboard Page ------------------------------------------
if selected == "Dashboard":
    st.title('📊 Dashboard')



    # Display Partner Model Summary
    st.subheader('Partner Model Summary')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("No of Partners")
        st.metric("No of Partners", df['Counts'][0])
    
    with col2:
        st.info("Active Partners")
        st.metric("Active Partners", df['Counts'][1])

    with col3:
        st.info("Canceled Partners")
        st.metric("Canceled Partners", df['Counts'][2])
    
    with col4:
        st.info("Paused/Past ")
        st.metric("Paused/Past Due Partners", df['Counts'][3])
    
    with st.expander("Click here to see more details"):
        st.dataframe(df.head(4))


    # Display Insights
    st.subheader('📈 Insights')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("Past Potential Not Buying")
        st.metric("", df3['flag_past_potential_not_buying'].sum())
        if st.button("Show Data", key="past_potential_btn", on_click=toggle_metric, args=("past_potential",)):
            pass

    with col2:
        st.info("Canceled Partners")
        st.metric("", df3['flag_active_freq_buyer_cancel'].sum())
        if st.button("Show Data", key="canceled_btn", on_click=toggle_metric, args=("canceled",)):
            pass

    with col3:
        st.info("Active Frequent Buyers")
        st.metric("", df3['flag_active_freq_buyer_active'].sum())
        if st.button("Show Data", key="active_btn", on_click=toggle_metric, args=("active",)):
            pass

    with col4:
        st.info("Active No Wholesale Buyers")
        st.metric("", df3['flag_active_no_wholesale'].sum())
        if st.button("Show Data", key="no_wholesale_btn", on_click=toggle_metric, args=("no_wholesale",)):
            pass


    with st.expander("Click here to see more details"):
        st.dataframe(df.tail(4))

    # Show only the selected dataframe
    if st.session_state.selected_metric == "past_potential":
        st.subheader("📊 Past Potential Not Buying")
        st.dataframe(df3[df3['flag_past_potential_not_buying'] == 1][['customer_id', 'userid', 'name', 'phone', 'email']])

    elif st.session_state.selected_metric == "canceled":
        st.subheader("📊 Canceled Partners Data")
        st.dataframe(df3[df3['flag_active_freq_buyer_cancel'] == 1][['customer_id', 'userid', 'name', 'phone', 'email']])

    elif st.session_state.selected_metric == "active":
        st.subheader("📊 Active Frequent Buyers")
        st.dataframe(df3[df3['flag_active_freq_buyer_active'] == 1][['customer_id', 'userid', 'name', 'phone', 'email']])

    elif st.session_state.selected_metric == "no_wholesale":
        st.subheader("📊 Active No Wholesale Buyers")
        st.dataframe(df3[df3['flag_active_no_wholesale'] == 1][['customer_id', 'userid', 'name', 'phone', 'email']])

    # Line separator
    st.markdown("---")

# ------------------------------------------ Cluster Table Page ------------------------------------------
elif selected == "Cluster Table":
    st.title('🧩 Cluster Def Table')
    df2 = pd.read_excel('model_summary_v1.xlsx', sheet_name='Cluster Def')
    st.dataframe(df2)

# ------------------------------------------ Data Page ------------------------------------------
elif selected == "Data":
    st.title("📄 Data")

    # Search bar for filtering by name
    search_query = st.text_input("Search by Name", "")
    filtered_df = df3[df3["name"].str.contains(search_query, case=False, na=False)] if search_query else df3

    # Display data in markdown format
    st.markdown("### Customer List")
    for _, row in filtered_df.iterrows():
        st.markdown(f"""
        **Customer ID:** {row['customer_id']}  
        **User ID:** {row['userid']}  
        **Name:** {row['name']}  
        **Phone:** {row['phone']}  
        **Email:** {row['email']}  
        """)
        if st.button(f"View Profile: {row['name']}", key=f"view_profile_{row['customer_id']}"):
            open_profile(row['name'])
