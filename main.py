import streamlit as st
import folium
import altair as alt
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(
    page_title="Vancouver Real Estate Scanner",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

st.write("# Properties for sale")

area = st.selectbox(
    "Select area",
    ("Terra Nova", "Point Grey")
    )

with st.sidebar:
    st.write("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/jason-lee-cfa/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Jason Lee`</a>', unsafe_allow_html=True)
    
    st.divider()
    min_price, max_price = st.slider("Price Range:", value =[0, 10000000])

if area == "Terra Nova":
    df = pd.read_csv("data/TerraNova_full_details.csv")
    df = df.query("Price > @min_price & Price < @max_price")

elif area == "Point Grey":
    df = pd.read_csv("data/PointGrey_full_details.csv")
    df = df.query("Price > @min_price & Price < @max_price")

m = folium.Map(location=(df['Latitude'].astype(float).mean(), df['Longitude'].astype(float).mean()),
               control_scale=True,
               zoom_start=15)

for index, row in df.iterrows():
    formatted_price = "${:,.2f}".format(row['Price'])
    html = html = f"<b>{row['Address']}</b><br>Price: {formatted_price}<br>Sqft: {row['Sqft']}"
    folium.Marker([row['Latitude'], row['Longitude']], popup=html, parse_html=True).add_to(m)

# call to render Folium map in Streamlit
c1, c2 = st.columns(2)
with c1:
    st_data = st_folium(m, width=700, height=700, returned_objects=["last_object_clicked"])

with c2:
    if st_data and "last_object_clicked" in st_data and st_data["last_object_clicked"]:
        # Extract latitude and longitude of the clicked marker
        clicked_lat = st_data["last_object_clicked"]["lat"]
        clicked_lon = st_data["last_object_clicked"]["lng"]
        
        # Find the corresponding property in the DataFrame
        property_info = df[(df['Latitude'] == clicked_lat) & (df['Longitude'] == clicked_lon)]

        if not property_info.empty:
            # Display property details
            property_info = property_info.iloc[0]  # Get the first matching row
            st.markdown(f"### Property Details")
            st.write(f"**Address**: {property_info['Address']}")
            st.write(f"**Price**: ${property_info['Price']:,}")
            st.write(f"**Year Built**: {property_info['ConstructedDate'].astype(int)}")
            st.write(f"**Square Footage**: {property_info['Sqft']} sqft")
            st.write(f"**Bedrooms**: {property_info['Bedrooms']}")
            st.write(f"**Bathrooms**: {property_info['Bathroom']}")
            st.write(f"**Description**: {property_info['PublicRemarks_x']}")

            # Handle image
            img1, img2, img3 = st.columns(3)
            with img1:
                if pd.notna(property_info['image_1']):
                    st.image(property_info['image_1'], use_container_width=True)
                else:
                    st.write("No image available.")
            with img2:
                if pd.notna(property_info['image_2']):
                    st.image(property_info['image_2'], use_container_width=True)
                else:
                    st.write("No image available.")
            with img3:
                if pd.notna(property_info['image_3']):
                    st.image(property_info['image_3'], use_container_width=True)
                else:
                    st.write("No image available.")

        else:
            st.write("No property details found for the clicked location.")

    else:
        st.write("Click on a marker to see more details about the property.")

st.write("# Summary")

#st.dataframe(df)

m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label = "Average Price", value= round(df["Price"].mean(),0))
with m2:
    st.metric(label = "Highest Price", value= round(df["Price"].max(),0))
with m3:
    st.metric(label = "Lowest Price", value= round(df["Price"].min(),0))

price_distribution = alt.Chart(df, title = "Price Distribution").mark_bar().encode(
    x=alt.X('Price').bin(maxbins=10),
    y='count()'
)
st.altair_chart(price_distribution)

