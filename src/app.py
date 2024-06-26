import streamlit as st
import datetime
from snowflake.snowpark import Session
from snowflake.snowpark import functions as f
import spcs_helpers

# Get User from SPCS Headers
from streamlit.web.server.websocket_headers import _get_websocket_headers
user = _get_websocket_headers().get("Sf-Context-Current-User") or "Visitor"

# Make connection to Snowflake and cache it
@st.cache_resource
def connect_to_snowflake():
    return spcs_helpers.session()

session = connect_to_snowflake()

# Fetch data from Snowflake
@st.cache_data
def top_clerks(_sess: Session, begin, end, topn):
    return _sess.table('snowflake_sample_data.tpch_sf10.orders') \
                .filter(f.col('O_ORDERDATE') >= begin) \
                .filter(f.col('O_ORDERDATE') <= end) \
                .group_by(f.col('O_CLERK')) \
                .agg(f.sum(f.col('O_TOTALPRICE')).as_('CLERK_TOTAL')) \
                .order_by(f.col('CLERK_TOTAL').desc()) \
                .limit(topn) \
                .to_pandas()

st.sidebar.header(f"Hello, {user}")
st.title("Top Clerks")

c1,c2 = st.columns(2)
begin = c1.date_input("Beginning of window", 
                      value=datetime.date.fromisoformat("1993-01-01"),
                      min_value=datetime.date.fromisoformat("1992-01-01"),
                      max_value=datetime.date.fromisoformat("1998-08-02"))

end = c2.date_input("End of window", 
                      value=datetime.date.fromisoformat("1993-12-31"),
                      min_value=begin,
                      max_value=datetime.date.fromisoformat("1998-08-02"))

topn = st.slider("TopN", value=10, min_value=1, max_value=30)

df = top_clerks(session, begin, end, topn)
st.dataframe(df)