import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Snowflake dbt Analytics Engineering",layout="wide")
st.title("Snowflake + dbt Analytics Engineering")
st.caption("Synthetic raw → staging → mart pipeline with dimensional modeling, lineage, and data-quality tests.")
random.seed(5)
customers=pd.DataFrame({"customer_id":[f"C{i:03}" for i in range(1,81)],"segment":[random.choice(["Enterprise","Mid-Market","SMB"]) for _ in range(80)],"region":[random.choice(["North America","Europe","APAC"]) for _ in range(80)]})
rows=[]
for i in range(600):
    rows.append({"booking_id":f"B{i+1:04}","customer_id":random.choice(customers.customer_id.tolist()),"booking_date":pd.Timestamp("2026-01-01")+pd.Timedelta(days=random.randint(0,250)),"acv":round(random.uniform(5000,220000),2),"stage":random.choice(["Closed Won","Closed Won","Commit","Pipeline"])})
raw=pd.DataFrame(rows)
staging=raw.merge(customers,on="customer_id",how="left")
mart=staging.groupby(["region","segment","stage"],as_index=False).agg(bookings=("booking_id","count"),acv=("acv","sum"))

tests=pd.DataFrame([
    ["raw_bookings.booking_id","unique",raw.booking_id.is_unique],
    ["raw_bookings.customer_id","not_null",raw.customer_id.notna().all()],
    ["stg_bookings.customer_fk","relationships",staging.region.notna().all()],
    ["mart_bookings.acv","accepted_range",bool((mart.acv>=0).all())],
],columns=["model_column","test","passed"])

c1,c2,c3,c4=st.columns(4)
c1.metric("Raw rows",len(raw))
c2.metric("Staging rows",len(staging))
c3.metric("Mart rows",len(mart))
c4.metric("Tests passing",f"{tests.passed.sum()}/{len(tests)}")

st.subheader("Pipeline lineage")
st.code("raw.crm_bookings + raw.customers\n        ↓\nstg_bookings / stg_customers\n        ↓\nfct_bookings + dim_customer\n        ↓\nmart_bookings_by_region_segment")

left,right=st.columns(2)
with left:
    st.subheader("Mart output")
    st.plotly_chart(px.bar(mart,x="region",y="acv",color="stage",facet_col="segment"),use_container_width=True)
with right:
    st.subheader("Data-quality tests")
    st.dataframe(tests,use_container_width=True,hide_index=True)

st.subheader("Example dbt model")
st.code("""select
    b.booking_id,
    b.booking_date,
    b.acv,
    c.customer_id,
    c.segment,
    c.region
from {{ ref('stg_bookings') }} b
join {{ ref('stg_customers') }} c
  on b.customer_id = c.customer_id""",language="sql")

st.subheader("Synthetic modeled data")
st.dataframe(staging.head(75),use_container_width=True,hide_index=True)
