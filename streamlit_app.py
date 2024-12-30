# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
#import requests
import pandas as Py

# Write directly to the app
st.title("Zena's Amazing Athleisure Catalog")
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("ZENAS_ATHLEISURE_DB.PRODUCTS.CATALOG_FOR_WEBSITE").select(col('COLOR_OR_STYLE'),col('PRICE'),col('SIZE_LIST'), col('UPSELL_PRODUCT_DESC'),col('FILE_NAME'))
#col_df = session.table("ZENAS_ATHLEISURE_DB.PRODUCTS.CATALOG_FOR_WEBSITE").select(col('COLOR_OR_STYLE'))
selected_style = st.selectbox(
    'Pick a sweatsuit color or style:', ('Burgundy','Charcoal Grey','Forest Green','Navy Blue','Orange','Pink','Purple','Red','Royal Blue','Yellow'))

pd_df = my_dataframe.to_pandas()

#if selected_style:
image_name = pd_df.loc[pd_df['COLOR_OR_STYLE'] == selected_style, 'FILE_NAME'].iloc[0]
price = pd_df.loc[pd_df['COLOR_OR_STYLE'] == selected_style, 'PRICE'].iloc[0]
image=session.file.get_stream("@sweatsuits/"+image_name , decompress=False).read()
product_caption = "Our Warm,Comfortable, "+ selected_style +" sweatsuit!"
st.image(image, width=400, caption=product_caption)
#st.write("Our Warm,Comfortable, "+ selected_style +" sweatsuit!")
st.write("Price: "+str(price))
sizes_avail = pd_df.loc[pd_df['COLOR_OR_STYLE'] == selected_style, 'SIZE_LIST'].iloc[0]
st.write("Sizes Available: "+sizes_avail)
upsell_prod_desc = pd_df.loc[pd_df['COLOR_OR_STYLE'] == selected_style, 'UPSELL_PRODUCT_DESC'].iloc[0]
if upsell_prod_desc == 'Consider: White, Black or Grey Sweat Accessories':
    st.write(upsell_prod_desc)
else:
    st.write(upsell_prod_desc.replace('Consider','BONUS'))
