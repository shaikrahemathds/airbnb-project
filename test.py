import mysql.connector
import streamlit as st 
from streamlit_option_menu import option_menu
import pandas as pd 
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots


mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1000Shaik#1',
    database = 'airbnb_project_latest'
)

# Set up page configuration 
st.set_page_config ( 
                    page_title = 'AIRBNB ',
                    page_icon = 'icon.png',
                    initial_sidebar_state = 'expanded',
                    layout = 'wide'
                    )

col1, col2 = st.columns([1,9])
with col1:
    st.image('icon.png')
with col2:
    st.markdown("""
        <h1 style="text-align: center; font-size: 50px; color: #ff5a5f;">
            AIRBNB StayExplorer 🏡📊
        </h1>        
        <p style="text-align: center; font-size: 18px; color: #555;">
            Explore Global Properties, Trends, and Geo Insights!!!
        </p>
    """, unsafe_allow_html=True)
    
# set up home page and optionmenu 
selected = option_menu("MainMenu",
                        options=["HOME","DISCOVER","MapQuest","INSIGHTS"],
                        icons=["house", "globe","compass", "lightbulb"],
                        default_index = 0,
                        orientation="horizontal",
                        styles={"container": {"width": "100%","border": "1px ridge  ","background-color": "#002b36","primaryColor": "#FF69B4"},
                                "icon": {"color": "#F8CD47", "font-size": "20px"}})

# ======================================= / HOME / =========================================================

if selected == 'HOME':

    st.markdown("""
        <style>
            .content-box {
                background-color: #002b36;
                padding: 32px;
                border-radius: 10px;
                color: white;
            }
            h1, h2, h3 {
                color: #ff5a5f;
                font-size: 36px; /* Heading font size */
            }
            p, li {
                font-size: 20px; /* General text and list font size */
                line-height: 1.6; /* Line spacing for better readability */
                color: #ffffff;
            }
            ul {
                padding-left: 20px; /* Indent for unordered lists */
            }
            .footer {
                font-size: 16px;
                color: gray;
                padding-top: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("🌟 Welcome to the Airbnb Explorer App 🌟")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="content-box">
            <h2>🏠 Overview</h2>
            <p>Airbnb was born in 2007 when two hosts welcomed three guests to their San Francisco home. Since then, it has grown to over 5 million hosts who have welcomed more than 2 billion guest arrivals across almost every country in the world. Every day, hosts offer unique stays and experiences, making it possible for guests to connect with communities in a more authentic way.</p>
            <p>This app serves as a stay explorer, built using a subset of Airbnb's dataset from 2019. The data focuses on selected countries to provide meaningful insights. The goal of this web app is not just to create an interactive dashboard, but also to extract insights from the dataset, draw meaningful conclusions, and offer potential suggestions.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="content-box">
            <h2>🗂️ What's Inside?</h2>
            <p>The app is divided into three sections:</p>
            <ul>
                <li>🔍 <b>Discover:</b> This allows the user to input the country, street, and name of the listing. Upon providing these details, the basic information of the listing, including host and comment details, is displayed. This helps the user match their expectations and make informed decisions.</li>
                <li>🗺️ <b>MapQuest:</b> This feature visualizes the spread of Airbnb listings on a map based on the selected country. Users can further refine their search by selecting property type, room type, minimum and maximum nights, and then visualize listings that suit their preferences.</li>
                <li>📊 <b>Insights:</b> This section provides a dropdown menu with multiple options. Each selection aims to unlock patterns from the data, draw actionable insights, make fitting suggestions, and highlight trends.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image("image")
        st.markdown("""
        <div class="content-box">
            <h2>🔎 Project Details</h2>
            <p><b>Project Title:</b> Airbnb Analysis</p>
            <p><b>Domain:</b> Travel Industry, Property Management, and Tourism</p>
            <p><b>Technologies:</b> Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly</p>            
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer" style="text-align: center;">
        Made with ❤️ using Streamlit | Powered by Airbnb Data
    </div>
    """, unsafe_allow_html=True)


# ======================================= / Reusable Functions / ============================================

def get_country_list():
    """Fetch the distinct countries from the database."""
    return pd.read_sql('''SELECT DISTINCT country FROM listing_info''', con=mydb)

def get_street_list(country):
    """Fetch distinct streets for a specific country."""
    return pd.read_sql('''SELECT DISTINCT street FROM listing_info WHERE country = %s''', con=mydb, params=[country])

def get_hotel_list(street):
    """Fetch distinct hotel names for a specific street."""
    return pd.read_sql('''SELECT DISTINCT name FROM listing_info WHERE street = %s''', con=mydb, params=[street])

def get_property_details(hotel_name):
    """Fetch detailed information for a selected hotel."""
    return pd.read_sql('''SELECT name, listing_url, description, country, price, picture_url, property_type, room_type, amenities,
                                  host_picture_url, host_name, host_url, host_about, host_location, accuracy_score, rating, number_of_reviews
                          FROM listing_info
                          JOIN host_info ON listing_info.listing_id = host_info.listing_id
                          JOIN review_info ON listing_info.listing_id = review_info.listing_id
                          WHERE name = %s''', con=mydb, params=[hotel_name])


def get_top_comments(hotel_name):
    """Fetch top 5 comments for a selected hotel."""
    return pd.read_sql('''SELECT reviewer_name, comments FROM comments_info
                          JOIN listing_info ON comments_info.listing_id = listing_info.listing_id
                          WHERE name = %s LIMIT 5''', con=mydb, params=[hotel_name])


def get_property_data(country):
    """fetch property data for a specific country"""
    return pd.read_sql('''  
        SELECT name AS 'PropertyName', price, longitude, latitude, property_type, room_type,
        bed_type, cancellation_policy, minimum_nights, maximum_nights
        FROM listing_info WHERE country = %s''', con=mydb, params=[country])
    

def generate_map(df):
    """Function to generate a map"""
    fig = px.scatter_mapbox(
        df, 
        lat="latitude", 
        lon="longitude",
        hover_name='PropertyName', 
        zoom=10,
        hover_data={'longitude': False, 'latitude': False, 'price': True},        
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


# ===================================== / DISCOVER / ==========================================================

if selected == 'DISCOVER':
    df_country = get_country_list()
    selected_country = st.selectbox("Search destinations", options=df_country['country'].tolist(), index=None)
    st.write(' ')

    df_street = get_street_list(selected_country)
    selected_street = st.selectbox("Select Street", options=df_street['street'].tolist(), index=None)
    st.write(' ')

    df_hotels = get_hotel_list(selected_street)
    selected_hotel = st.selectbox('Select Hotel', options=df_hotels['name'].tolist(), index=None)
    st.write(' ')
    
    if selected_hotel:
        more = st.button('Click for Details')

        if more:

            df = get_property_details(selected_hotel)
            extract_detail = df.to_dict(orient='records')[0]
            c1, c2 = st.columns(2)
            with c1:
                st.write('**:green[Basic Details]**')
                st.write("**:violet[Name :]**", f'**{extract_detail["name"]}**')
                st.write("**:violet[Website Url :]**", extract_detail['listing_url'])
                st.write("**:violet[country :]**", f'**{extract_detail["country"]}**')
                st.write("**:violet[Description :]**", extract_detail['description'])
                st.write("**:violet[Price in $ :]**", f'**{extract_detail["price"]}**')
                st.write("**:violet[Total Reviews :]**", f'**{extract_detail["number_of_reviews"]}**')
                st.write("**:violet[Overall Score:]**", f"**{extract_detail['accuracy_score']} &nbsp;&nbsp;&nbsp; **:violet[Rating:]** {extract_detail['rating']}**")
                st.write("**:violet[Room Picture :]**")
                st.image(extract_detail['picture_url'], width=300)

            with c2:
                st.write('**:green[Room Details]**')
                st.write("**:violet[Property Type :]**", f'**{extract_detail["property_type"]}**')
                st.write("**:violet[Room Type :]**", f'**{extract_detail["room_type"]}**')
                st.write("**:violet[Amenities :]**", f'**{extract_detail["amenities"]}**')
                st.write('**:green[Host Details]**')
                st.write("**:violet[Host Name :]**", f'**{extract_detail["host_name"]}**')
                st.write("**:violet[Host Url :]**", extract_detail['host_url'])
                st.write("**:violet[Host location :]**", f'**{extract_detail["host_location"]}**')
                st.write("**:violet[Host About :]**", f'**{extract_detail["host_about"]}**')
                st.write("**:violet[Host Picture :]**")
                st.image(extract_detail['host_picture_url'], width=300)

            df_comments = get_top_comments(selected_hotel)
            st.write('**:green[Top Comments]**')
            st.dataframe(df_comments, hide_index=True, use_container_width=True)

# ==================================== / MapQuest / ===========================================================

if selected == 'MapQuest':
    
    tab1, tab2 = st.tabs(["Without Filters", "With Filters"])

    df_country = get_country_list()

    with tab1:
        selected_country = st.selectbox("Select country", options=df_country['country'].tolist(), key="country_without_filters")
        btn = st.button("Explore Properties", key='without_filters')

        if btn:
            df = get_property_data(selected_country)
            fig = generate_map(df)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        selected_country = st.selectbox("Select country", options=df_country['country'].tolist(), key="country_with_filters")
        df = get_property_data(selected_country)

        property_type_values = df['property_type'].unique().tolist()
        room_type_values = df['room_type'].unique().tolist()

        col1, col2 = st.columns(2)
        with col1:
            property_type_filter = st.selectbox("Select Property Type", options=property_type_values, key="property_type_filter")
        with col2:
            room_type_filter = st.selectbox("Select Room Type", options=room_type_values, key="room_type_filter")

        col3, col4 = st.columns(2)
        with col3:
            min_nights_filter = st.slider(
                "Minimum Nights",
                min_value=int(df['minimum_nights'].min()),
                max_value=int(df['minimum_nights'].max()),
                value=(int(df['minimum_nights'].min()), int(df['minimum_nights'].max())),
                key="min_nights_filter"
            )
        with col4:
            max_nights_filter = st.slider(
                "Maximum Nights",
                min_value=int(df['maximum_nights'].min()),
                max_value=int(df['maximum_nights'].max()),
                value=(int(df['maximum_nights'].min()), int(df['maximum_nights'].max())),
                key="max_nights_filter"
            )

        btn = st.button("Filtered Results", key="with_filters")

        if btn:
            filtered_df = df
            if property_type_filter:
                filtered_df = filtered_df[filtered_df['property_type'] == property_type_filter]
            if room_type_filter:
                filtered_df = filtered_df[filtered_df['room_type'] == room_type_filter]
            filtered_df = filtered_df[
                (filtered_df['minimum_nights'] >= min_nights_filter[0]) &
                (filtered_df['minimum_nights'] <= min_nights_filter[1]) &
                (filtered_df['maximum_nights'] >= max_nights_filter[0]) &
                (filtered_df['maximum_nights'] <= max_nights_filter[1])
            ]

            fig = generate_map(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
            
            
# ========================================= / Insights / ======================================================

if selected == "INSIGHTS":
    
    options = ['',
        'Frequency Distribution of Property Types',
        'Property Type vs Room Type vs Price',
        'Average availability Analysis',
        'Top 10 and Bottom 10 Listings',
        'Average Price Analysis',
        'Additional Price analysis',
        'Listings Per Country',
        'Superhost Analysis',
        'Top 10 Host w.r.t Number of Listings'
    ]
    
    query = st.selectbox("Choose Insight", options=options)
    
    # -----------------------------------------------------------------------------------------------------------
    
    if query == 'Frequency Distribution of Property Types':
        
        df_property = pd.read_sql('''Select property_type, count(property_type) as Frequency, avg(price) as average_price
                                    from listing_info group by property_type order by Frequency desc''', con = mydb)

        fig = px.bar(df_property, 
                    x='property_type', 
                    y='Frequency', 
                    title='Frequency of Property Types',
                    labels={'Property Type': 'Property Type'},
                    color='Frequency', 
                    color_continuous_scale='Rainbow')
        fig.update_layout(
            yaxis_type="log", 
            yaxis=dict(title='Frequency (Log Scale)'),
        )        
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(df_property, 
                    x='property_type', 
                    y='average_price', 
                    title='Average Price vs Property Types',
                    labels={'Property Type': 'Property Type', 'average_price': 'Average Price'},
                    color='average_price', 
                    color_continuous_scale='Rainbow')                
        st.plotly_chart(fig, use_container_width=True)                       
                                
        st.markdown("""
                    ### 📊 **Insights on Property Types and Pricing**

                    #### 1️⃣ **Property Type vs Count** 
                    - **Apartment** stands out with 3000+ listings 🏢.
                    - Other popular properties include **House** and **Condominium** 🏠🏙️.
                    - **Houseboat**, **Heritage Hotel**, **Tree House** are **rare**, with only 1 or 2 listings 🛶🏨🌳.

                    #### 2️⃣ **Property Type vs Average Price**
                    - **Apartment** has the **lowest average price** (under $100) 💸.
                    - **Houseboat**, **Heritage Hotel**, and **Casa Particular (Cuba)** have **higher average prices** (around $400) 🏖️💰.

                    #### 🧐 **Common Insight:**
                    - **Affordable and abundant properties** like **Apartments** dominate the market in terms of quantity and availability, making them the most common choice for travelers 🏙️.
                    - On the other hand, **specialty properties** like **Houseboat** and **Heritage Hotels** are rare but can **command higher prices** due to their unique and exclusive nature 🌟.

                    #### 🔑 **Suggestions:**
                    - **For Hosts:**
                    - **Apartments** could attract more bookings due to their affordability and availability 🏢.
                    - Consider **offering unique stays** like **Houseboats** or **Heritage Hotels** for travelers seeking exclusive and high-end experiences 🌴.
                    
                    - **For Guests:**
                    - If you're on a **budget**, apartments are the most economical option 💵.
                    - For a **luxury experience**, exploring niche properties like **Houseboats** or **Heritage Hotels** will give you a special and unforgettable stay 🌅.

                    #### 📈 **Business Insight:**
                    - There’s an opportunity to **expand unique listings** while keeping **affordable apartments** to maintain market balance ⚖️.
                    """)

    
    # -----------------------------------------------------------------------------------------------------------
        
    if query == 'Property Type vs Room Type vs Price':
        
        df = pd.read_sql('''Select property_type, room_type, avg(price) as mean_price from listing_info
                            group by property_type, room_type''', con = mydb)
    
        fig = px.density_heatmap(df, 
                                y='property_type', 
                                x='room_type', 
                                z='mean_price', 
                                title='Property Type vs Room Type vs Price',
                                labels={'property_type': 'Property Type', 'room_type': 'Room Type'},
                                color_continuous_scale='viridis')
        
        st.plotly_chart(fig, use_container_width=True)
        
        df=pd.read_sql('''SELECT country,room_type,count(room_type) as 'count of room type' 
                            from listing_info GROUP by country, room_type''',con=mydb)
                
        fig = px.sunburst(df, path=['country', 'room_type'], values='count of room type',
                title='Distribution of Room Types by Country', color_continuous_scale='RdBu')
        st.plotly_chart(fig,use_container_width=True)
        
        st.markdown("""
                    ## 🧐 Key Insights
                    - **🏠 Room Type Dominance**: Entire home/apt is the most dominant room type across various property types, often leading to higher average prices. This suggests that guests are willing to pay a premium for privacy and exclusive access to entire properties.
                    - **🏡 Property Type Influence**: Barns and Camper/RV properties, when offered as entire homes/apartments, stand out with significantly higher average prices. This could be due to unique experiences, luxurious conversions, or high demand for these specific property types.
                    - **💸 Shared Room Economy**: Shared rooms are generally associated with lower average prices, irrespective of the property type. This aligns with the shared economy model, where guests opt for affordable accommodations in exchange for shared amenities and spaces.
                    - **🛏️ Private Room Variation**: Private rooms within different property types show a wide range of prices. This variation could be influenced by factors like room size, amenities, and location within the property.
                    """)

        st.markdown("""
                    ## 💡 Suggestions
                    - **💵 Targeted Pricing Strategies**: Implement dynamic pricing strategies based on property type, room type, and peak seasons to optimize revenue. Consider offering premium packages for entire home/apartment bookings, especially for high-demand property types like barns and camper/RVs.
                    - **🏠 Room Type Optimization**: Analyze the demand for different room types within each property type to identify opportunities for maximizing revenue. Consider offering flexible room configurations to cater to various guest preferences and budgets.
                    - **✨ Guest Experience Enhancement**: Invest in upgrading amenities and services for private rooms to justify higher prices. Create unique experiences for guests staying in barns, camper/RVs, and other distinctive property types.
                    - **📊 Data-Driven Decision Making**: Continuously monitor booking data, pricing trends, and guest feedback to refine pricing strategies and improve the overall guest experience.
                    """)
        
    # ----------------------------------------------------------------------------------------------------------
    
    if query == 'Average availability Analysis':  
        
        df=pd.read_sql('''SELECT country,AVG(availability_30) as 'avg_availability_30',AVG(availability_60)
                                    as 'avg_availability_60', AVG(availability_90) as 'avg_availability_90',
                                    AVG(availability_365) as 'avg_availability_365' from listing_info
                                    GROUP by country ''',con=mydb)
                
        fig = px.bar(df, x='country',
                    y=['avg_availability_30', 'avg_availability_60', 'avg_availability_90', 'avg_availability_365'],
                    title='Average Availability of Stays by Country',
                    labels={'value': 'Average Availability', 'variable': 'Availability Period', 'country': 'Country'},
                    barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
                    ## 📅 Average Availability Insight
                    - **🗓️ Average Availability** refers to the average number of days a property is available for booking within a specific timeframe.
                    - **🌍 Higher "Avg Availability"** in countries like **Portugal** and **Turkey** suggests properties are available more frequently, possibly due to:
                        - **👥 Lower tourist demand**.
                        - **🏠 A larger number of properties**.
                        - **📜 Fewer regulations** on short-term rentals.
                    - **🇺🇸 US**, **🇦🇺 Australia**, and **🇨🇦 Canada** show **lower availability**, indicating:
                        - **🏙️ Higher Airbnb adoption**.
                        - **💼 Constant occupancy** due to increased demand.
                    """)
        
        df=pd.read_sql('''SELECT room_type,AVG(availability_30) as 'avg_availability_30',AVG(availability_60)  as 'avg_availability_60',
                                    AVG(availability_90) as 'avg_availability_90',AVG(availability_365) as 'avg_availability_365' from listing_info
                                    GROUP by room_type ''',con=mydb)
        
        fig = px.bar(df, x='room_type', y=['avg_availability_30', 'avg_availability_60','avg_availability_90', 'avg_availability_365'],
                    title='Average Availability of Stays by Country',
                    labels={'value': 'Average Availability', 'variable': 'Availability Period', 'room_type': 'Room type'},
                    barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
                    ## 🏠 Room Type vs Average Availability
                    - **🏠 Entire Homes/Apartment** and **🛏️ Private Rooms** are becoming more popular, with increasing demand, leading to **Lower availability**.
                    - **🚪 Shared Rooms** are seeing a decline in popularity, reflected in **country-wise frequency distribution**.
                    - The previous analysis showed **lesser adoption of shared rooms** across countries, aligning with the trend of more guests opting for private accommodations.
                    """)
        
        df=pd.read_sql('''SELECT property_type,AVG(availability_30) as 'avg_availability_30',AVG(availability_60)
                        as 'avg_availability_60', AVG(availability_90) as 'avg_availability_90',AVG(availability_365)
                        as 'avg_availability_365' from listing_info GROUP by property_type; ''',con=mydb)
        
        fig = make_subplots(
            rows=2, cols=2, 
            subplot_titles=['avg_availability_30', 'avg_availability_60', 'avg_availability_90', 'avg_availability_365'],
            specs=[[{"type": "bar"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "bar"}]]
        )

        fig.add_trace(go.Bar(
            x=df['property_type'], 
            y=df['avg_availability_30'],
            name='Availability 30',
            marker=dict(color='blue'),
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=df['property_type'], 
            y=df['avg_availability_60'],
            name='Availability 60',
            marker=dict(color='green'),
        ), row=1, col=2)

        fig.add_trace(go.Bar(
            x=df['property_type'], 
            y=df['avg_availability_90'],
            name='Availability 90',
            marker=dict(color='red'),
        ), row=2, col=1)

        fig.add_trace(go.Bar(
            x=df['property_type'], 
            y=df['avg_availability_365'], 
            name='Availability 365',
            marker=dict(color='purple'),
        ), row=2, col=2)

        fig.update_layout(
            height=800,
            width=800,
            title_text="Availability Pattern by Property Type",
            showlegend=False,
            xaxis=dict(title="Property Type"),
            yaxis=dict(title="Average Availability"),
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)
    
        st.markdown('''
                    ## 🏡 **Availability Patterns and Insights** 🏠

                    ### 📊 **Trend Summary**:

                    Upon comparing the availability patterns for various property types across different time frames (30, 60, 90, and 365 days), the following common trend emerges:

                    ### 🌟 **Unique and Niche Properties**:
                    Properties like **Train**, **Castle**, **Houseboat**, **Heritage Hotels**, **Earth House**, and **Tree House** show **higher availability** across all categories. 
                    - **Reasons for Higher Availability**:
                    - **Premium Price** 💵: These properties often come with a higher price tag, making them less affordable for long-term stays.
                    - **Tourist Appeal** 🌍: These unique properties cater more to short-term, tourist-focused stays rather than long-term tenants. Tourists are willing to pay a premium for a unique experience.

                    ### 🏙️ **Economical Properties**:
                    On the other hand, more **affordable** properties like **Apartments** and **Condominiums** exhibit **lower availability**.
                    - **Reasons for Lower Availability**:
                    - **Lower Price** 💲: These properties are in higher demand due to their affordability, making them quickly occupied.
                    - **Convenience for Long-Term Stays** 🏠: Apartments and condominiums are more suitable for people looking for long-term accommodation. The combination of affordability and convenience results in these properties having fewer vacancies.

                    ### 🔄 **Conclusion**:

                    - **Premium Properties**: Higher availability due to high cost and tourist-focused nature. Great for short-term stays and unique experiences.
                    - **Economical Properties**: Lower availability as they are often chosen for long-term stays, driven by price and convenience.

                    ---

                    This insight can be helpful for property owners and real estate professionals in understanding booking patterns and making strategic decisions about pricing, marketing, and targeting the right audience.

                    ✨ **Suggestions**:
                    - **For Unique Properties**: Focus on attracting tourists and consider pricing strategies that reflect the premium nature of these properties.
                    - **For Economical Properties**: Emphasize affordability and long-term stay convenience to ensure higher occupancy rates.
                    ''')
    # -----------------------------------------------------------------------------------------------------------
    
    if query == 'Top 10 and Bottom 10 Listings':
        df = pd.read_sql('''select name, price,room_type, property_type, country from listing_info order by price desc limit 10''', con = mydb)
        df_sorted = df.sort_values(by='price', ascending=False)
        fig = px.bar(df, x='price', y='name', 
                 hover_name='country',
                 color='country', 
                 color_discrete_sequence=px.colors.qualitative.Pastel1)
        fig.update_layout(showlegend=False,   yaxis=dict(
            categoryorder='total ascending' 
        ))
        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(df_sorted,hide_index=True)
        
        df = pd.read_sql('''select name, price,room_type, property_type, country from listing_info order by price limit 10''', con = mydb)
        df_sorted = df.sort_values(by='price', ascending=False)
        fig = px.bar(df, x='price', y='name', 
                 hover_name='country',
                 color='country', 
                 color_discrete_sequence=px.colors.qualitative.Pastel1)
        fig.update_layout(showlegend=False, yaxis=dict(
            categoryorder='total ascending' 
        ))
        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(df_sorted,hide_index=True)
        
        st.markdown("""
                    ## 💡 Key Insights

                    - **💸 Price Disparity**: Top listings range from **$2,000** to **$8,303**, offering **luxury** and **exclusive** experiences, while bottom listings are as low as **$4.42**, providing **budget-friendly** stays.
                    - **🏠 Property & Room Type**: Top listings feature **entire homes/apartments** (e.g., **Villa**, **Townhouse**), while bottom listings focus on **private rooms** and **shared rooms**.
                    - **🌍 Location Matters**: **High-demand locations** (e.g., **Istanbul**, **Greenwich Village**) justify premium prices. In contrast, **Turkey** offers affordable options in popular areas like **Kadıköy**.
                    - **✨ Unique vs. Basic**: **Premium properties** offer unique experiences, while **budget stays** cater to those seeking affordable, no-frills accommodation.

                    ## 🚀 Suggestions

                    - **🎯 Target Market Segments**: For **luxury listings**, focus on **exclusivity** and **premium amenities**. For **budget options**, emphasize **affordability** and **authenticity**.
                    - **🌟 Promote Unique Experiences**: Highlight the **luxury** of entire homes and offer **personalized services**. For **budget properties**, suggest **local tours** or **host experiences**.
                    - **🗺️ Location-Specific Deals**: Promote the **high-value** locations of **Istanbul**, **New York**, and **Miami** for premium stays, and affordable areas like **Kadıköy** for budget-conscious travelers.
                    - **🔄 Dynamic Pricing**: Implement **dynamic pricing** based on **seasonality** and local demand to maximize revenue without compromising occupancy.
                    """)
    
    # -------------------------------------------------------------------------------------------------------------
        
    if query == 'Average Price Analysis':
        df = pd.read_sql("""select cancellation_policy, avg(price) as average_price from listing_info
                            group by cancellation_policy order by average_price desc""", con = mydb)
        
        fig = px.bar(df, 
             x='average_price', 
             y='cancellation_policy', 
             color='cancellation_policy', 
             orientation='h')
        st.plotly_chart(fig, use_container_width=True)
        
        df = pd.read_sql("""select country, avg(price) as average_price from listing_info
                            group by country order by average_price desc""", con = mydb)
        
        fig = px.bar(df, 
             x='average_price', 
             y='country', 
             color='country', 
             orientation='h')
        st.plotly_chart(fig, use_container_width=True) 
        
        
        df = pd.read_sql("SELECT name, price, amenities FROM listing_info", con = mydb)

        df['amenities'] = df['amenities'].str.split(',')  
        df_exploded = df.explode('amenities')  
        df_exploded['amenities'] = df_exploded['amenities'].str.strip() 

        avg_price_by_amenity = df_exploded.groupby('amenities')['price'].mean().reset_index()

        fig = px.bar(avg_price_by_amenity, 
                    x='price', 
                    y='amenities', 
                    color='amenities', 
                    orientation='h', 
                    title="Average Price by Amenity")

        st.plotly_chart(fig, use_container_width=True)

        df = pd.read_sql("""select accommodates, avg(price) as average_price from listing_info
                            group by accommodates order by accommodates""", con = mydb)
        
        fig = px.line(df, 
                x='accommodates', 
                y='average_price', 
                title="Average Price vs. Accommodates",
                labels={"accommodates": "Number of People", "average_price": "Average Price"},
                template="plotly")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
                    ## 💡 Key Insights on Listing Prices

                    - **📅 Cancellation Policy vs. Price**: Stricter **cancellation policies** lead to higher prices. A flexible policy typically reflects a **lower price**.
                    - **🌍 Country vs. Average Price**: **US**, **Australia**, and **Brazil** dominate with **$140-$180** prices, while **China** and **Turkey** have more affordable options.
                    - **🛋️ Amenities vs. Price**: Premium amenities like **alfresco showers**, **chef's kitchens**, and **home theatres** can raise prices drastically, pushing averages up to $2,000.
                    - While 90 percent of listings with average prices of $200 offer standard amenities, the remaining 10 percent with luxurious features can drive the price up.
                    - **👥 Accommodates vs. Price**: More guests per listing leads to a **higher average price**. Listings with larger accommodations are priced higher.

                    ## 🚀 Suggestions

                    - **🎯 Focus on Value**: For **high-priced listings**, highlight **luxury amenities** and **strict cancellation policies**. For **affordable listings**, offer **flexible policies** and basic amenities to attract budget-conscious travelers.
                    - **🌎 Regional Promotions**: Promote **high-demand** countries like the **US** and **Australia** for premium stays, while **China** and **Turkey** can cater to budget travelers.
                    - **🏠 Capitalize on Amenities**: Offer **premium amenities** to justify higher pricing. Consider **dynamic pricing** for properties with unique features.
                    - **👨‍👩‍👧‍👦 Tailor Pricing by Accommodates**: Ensure the pricing reflects the number of people the listing accommodates. **Larger properties** should have **higher prices** to align with guest expectations.
                    """)
    
    # -----------------------------------------------------------------------------------------------------------
        
    if query == 'Additional Price analysis':
        df = pd.read_sql("""SELECT rating, avg(security_deposit + cleaning_fee) AS additional_fee from listing_info l
                            join review_info r on l.listing_id = r.listing_id group by rating 
                            order by rating""", con = mydb)
        
        fig = px.line(df, 
                x='rating', 
                y='additional_fee', 
                title="Average Price vs. Rating",
                labels={"additional_fee": "additional_fee", "average_price": "Average Price"},
                template="plotly")
        st.plotly_chart(fig, use_container_width=True)
        
        df = pd.read_sql("""SELECT country, avg(security_deposit + cleaning_fee) AS additional_fee
                         from listing_info group by country """, con = mydb)
        
        fig = px.bar(df, 
             x='additional_fee',  
             y='country',         
             title="Additional Price vs. Country",
             labels={"additional_fee": "Additional Fee", "country": "Country"},
             template="plotly")

        st.plotly_chart(fig, use_container_width=True)

        df = pd.read_sql("""
            SELECT name, amenities, AVG(security_deposit + cleaning_fee) AS additional_fee
            FROM listing_info
            GROUP BY name, amenities
        """, con = mydb)

        df['amenities'] = df['amenities'].str.split(',')  
        df_exploded = df.explode('amenities')  
        df_exploded['amenities'] = df_exploded['amenities'].str.strip() 

        avg_price_by_amenity = df_exploded.groupby('amenities')['additional_fee'].mean().reset_index()

        fig = px.bar(avg_price_by_amenity, 
                    x='additional_fee', 
                    y='amenities', 
                    color='additional_fee', 
                    orientation='h', 
                    title="Additional Fee by Amenity")

        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
                    ### **Additional Fee Insights:**

                    1. **No Impact on Rating**:  
                    The additional fee (security deposit + cleaning fee) does not significantly affect the ratings of listings. Ratings tend to remain relatively constant across listings, regardless of the additional fees charged. This indicates that guests may not perceive a direct relationship between the cost of extra fees and the overall satisfaction or rating of their stay.

                    2. **Country-Specific Trends**:  
                    Countries like **Hong Kong**, **Brazil**, and **China** tend to charge higher additional fees when compared to other countries in the dataset. This could be due to several factors:
                    - **Regulatory Factors**: In some regions, stricter cleaning standards or insurance requirements may lead to higher fees.
                    - **Operational Costs**: Higher service and maintenance costs in these regions could drive up the fees, especially for cleaning and damage protection.
                    - **Cultural and Market Differences**: In some markets, guests may expect more frequent cleaning or higher-quality service, which could be reflected in the additional charges.

                    3. **Trend with Premium Amenities**:  
                    As seen in the **Average Price** analysis, properties with **premium amenities** (such as alfresco showers, chef’s kitchens, home theatres) tend to charge higher additional fees. This trend is consistent in both the average price and additional fee analyses, where luxury features correlate with higher service costs (cleaning, maintenance, etc.).
                    """)

    # ----------------------------------------------------------------------------------------------------------
        
    if query == 'Listings Per Country':
        df = pd.read_sql("""select country, count(name) as listing_count from listing_info
                         group by country""", con = mydb)
        fig = px.pie(
            df, 
            names='country',  
            values='listing_count',  
            title="Listings per Country",
            labels={'listing_count': 'Number of Listings', 'country': 'Country'},
            template="plotly"
        )
        fig.update_traces(textinfo='label+percent', pull=[0.1, 0.1, 0.1])
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
                    ### **Key Insights from Listings per Country Pie Chart:**

                    1. **🇺🇸 Dominance of the United States**:  
                    The United States leads with 22% of the total listings, highlighting its significant presence on the platform. Popular tourist destinations like New York and strategic islands contribute to this dominance.

                    2. **🌍 Global Representation**:  
                    The chart shows diverse representation across countries such as Canada, Spain, Australia, Brazil, Hong Kong, Portugal, and China. This demonstrates Airbnb's strong global presence and appeal to international markets.

                    3. **📉 Smaller Market Shares**:  
                    While the US dominates, other countries have relatively smaller shares. This could be influenced by factors like tourism popularity, economic conditions, and Airbnb's marketing efforts in different regions.

                    ---

                    ### **Possible Reasons for the US Dominance:**

                    1. **🏨 Strong Tourist Industry**:  
                    The US has a well-established tourism sector, drawing millions of visitors annually, increasing demand for vacation rentals.

                    2. **🏠 High Property Ownership Rates**:  
                    Higher rates of property ownership in the US result in more listings on the platform.

                    3. **🌐 Popularity of Airbnb in the US**:  
                    The platform is more popular in the US, leading to a higher number of listings from local property owners.

                    ---

                    ### **Suggestions for Expansion:**

                    1. **🌱 Expand in Emerging Markets**:  
                    Focus on growing in emerging markets like India, Southeast Asia, and Africa. Use targeted marketing campaigns, partnerships with local businesses, and localization to appeal to these regions.

                    2. **🏠 Diversify Property Types**:  
                    Encourage unique listings such as villas, boutique hotels, and historic homes. This will attract a wider range of travelers and make the platform more diverse.

                    3. **💻 Enhance User Experience**:  
                    Improve the platform's usability by optimizing search features, filters, and mobile responsiveness. A better user experience will attract more users and encourage property owners to list their properties.

                    4. **🤝 Strengthen Partnerships**:  
                    Collaborate with local tourism boards, travel agencies, and airlines to promote the platform and attract more listings.

                    5. **🛠️ Offer Value-Added Services**:  
                    Provide additional services like concierge, property management, and insurance to attract more property owners and increase the platform’s appeal.
                    """)
    
    # ----------------------------------------------------------------------------------------------------------
    
    if query == 'Superhost Analysis':
        
        df = pd.read_sql("""select avg(rating) as average_rating, host_is_superhost from review_info r join host_info h
                         on r.listing_id = h.listing_id group by host_is_superhost """, con = mydb)
        df['host_is_superhost'] = df['host_is_superhost'].map({0: 'Non-Superhost', 1: 'Superhost'})
        
        fig = px.bar(df, y = 'host_is_superhost', x = 'average_rating', color = 'host_is_superhost',
                     title="Rating:  superhost vs. Non-Superhost", orientation='h')
        
        st.plotly_chart(fig, use_container_width=True)
        
        df = pd.read_sql("""select avg(host_response_rate) as avg_response_rate, host_is_superhost from host_info
                            group by host_is_superhost """, con = mydb)
        df['host_is_superhost'] = df['host_is_superhost'].map({0: 'Non-Superhost', 1: 'Superhost'})
        
        fig = px.bar(df, y = 'host_is_superhost', x = 'avg_response_rate', color = 'host_is_superhost',
                     title="Rating:  superhost vs. Non-Superhost", orientation='h')
        
        st.plotly_chart(fig, use_container_width=True)
        
        df = pd.read_sql("""select host_response_rate, host_is_superhost, host_response_time from host_info """,
                         con = mydb)
        
        df['host_is_superhost'] = df['host_is_superhost'].map({0: 'Non-Superhost', 1: 'Superhost'})
        
        df_pivot = df.pivot_table(
            values='host_response_rate', 
            index='host_is_superhost',  
            columns='host_response_time', 
            aggfunc='mean' 
        )

        fig = px.imshow(
            df_pivot,
            title="Heatmap: Host Response Rate by Superhost and Response Time",
            labels={'host_is_superhost': 'Superhost Status', 'host_response_time': 'Response Time'},
            color_continuous_scale='Viridis'  
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
                    ### **Comprehensive Analysis of Superhost vs. Non-Superhost**

                    #### **Key Insights from the Plots:**

                    1. **⭐ Higher Ratings**:  
                    Superhosts consistently receive higher ratings compared to Non-Superhosts, suggesting superior guest experiences. This can be attributed to factors like cleanliness, amenities, and host responsiveness.

                    2. **⏱️ Faster Response Times**:  
                    Superhosts respond to inquiries much faster than Non-Superhosts, reflecting a commitment to timely communication and positive guest interaction.

                    3. **💎 Commitment to Quality**:  
                    The combination of higher ratings and faster responses indicates that Superhosts are committed to providing excellent quality and service to their guests.

                    4. **📋 Strict Platform Standards**:  
                    Platforms like Airbnb enforce strict Superhost criteria, such as high response rates, low cancellation rates, and excellent reviews, ensuring a consistent level of service.

                    5. **🎁 Incentives and Recognition**:  
                    Superhosts receive various platform rewards and recognition, motivating them to maintain high standards and superior service.

                    ---

                    #### **Implications for Travelers and Hosts:**

                    **For Travelers:**
                    - **🔍 Prioritize Superhosts**: When booking accommodations, choosing Superhosts increases the chances of having a positive experience.
                    - **⏳ Expect Timely Responses**: Superhosts are more likely to respond promptly to inquiries, making the booking process smoother.
                    - **🏠 Higher Quality Accommodations**: Superhosts typically offer well-maintained, clean properties with top-notch amenities.

                    **For Hosts:**
                    - **🌟 Strive for Superhost Status**: Achieving Superhost status can lead to higher bookings, better earnings, and an improved reputation.
                    - **📩 Prioritize Guest Communication**: Quick, professional responses to guest inquiries can help secure a Superhost title.
                    - **🧼 Maintain High Standards**: Focus on cleanliness, comfort, and hospitality to meet and exceed guest expectations.
                    - **🎯 Leverage Platform Benefits**: Take advantage of Superhost benefits and recognition to enhance your visibility and reputation on the platform.
                    """)
                            
    # -------------------------------------------------------------------------------------------------------------
        
    if query == 'Top 10 Host w.r.t Number of Listings':
        df = pd.read_sql("""SELECT distinct host_name, host_location, host_total_listings
                            FROM host_info
                            ORDER BY host_total_listings DESC
                            LIMIT 10""", con = mydb
                        )
        fig = px.bar(df, x = 'host_total_listings', y = 'host_name', color = 'host_name',
                     title="Top Host Names", orientation='h')
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
                    ### **Analyzing the Top Host Names Chart**

                    #### **Key Insights:**

                    1. **🏆 Sonder Dominates**:  
                    Sonder stands out as the clear leader, significantly outpacing other hosts in total listings. This reflects a strong, possibly large-scale operation.

                    2. **👥 Kara and Claudia Follow Closely**:  
                    Kara and Claudia occupy the second and third spots, indicating a substantial number of listings under their management.

                    3. **🌍 Diverse Host Types**:  
                    The chart showcases a mix of individual hosts (e.g., Holly, Feels Like Home, Grand Welcome) and companies (e.g., Sonder, Condominium Rentals Hawaii), reflecting various types of property management strategies.

                    4. **📊 Long Tail of Smaller Hosts**:  
                    Although the top hosts dominate, there’s a long tail of smaller hosts, each managing fewer properties.

                    ---

                    #### **Possible Interpretations:**

                    1. **🏢 Professional Property Management Companies**:  
                    Hosts like Sonder and Condominium Rentals Hawaii are likely large, professional property management companies, managing multiple properties.

                    2. **👤 Individual Hosts**:  
                    Other hosts, such as Holly and Feels Like Home, are likely individual property owners or smaller property management companies.

                    3. **🎯 Market Strategy**:  
                    Sonder's dominance suggests an effective market strategy for acquiring and managing a large number of properties.

                    4. **🛋️ Brand Recognition**:  
                    Hosts like "Feels Like Home" and "Grand Welcome" may have built strong brand identities and customer loyalty, contributing to their success.
                    """)

    
    # ----------------------------------------------------------------------------------------------------------
    