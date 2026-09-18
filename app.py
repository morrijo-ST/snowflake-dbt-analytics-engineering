
import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def shell(name, title, subtitle, style):
    global PALETTE, INK, PANEL, BG, ACCENT
    themes = {
      'terminal': ('#091411','#10221d','#e7f5ee','#3fe0a0','#7e9c8d',4),
      'purple': ('#171625','#222137','#f5f1ff','#ba9bff','#9ca1c0',12),
      'indigo': ('#f4f5fb','#ffffff','#242746','#5149b9','#64708b',18),
      'coral': ('#faf7f2','#ffffff','#302a27','#c7543e','#796d65',20),
      'blue': ('#f2f6fa','#ffffff','#183348','#126bb5','#5d7486',8),
      'cyan': ('#07141d','#102330','#def5ff','#53d2ed','#8caab9',4),
      'ops': ('#0b1720','#132733','#e7f5f4','#4edbc4','#99b5bd',10),
      'editorial': ('#f8f7f3','#ffffff','#253b38','#317764','#6b7d77',6),
      'amber': ('#17212c','#223140','#f8f4e9','#efbc67','#a6b2bf',6),
    }
    BG,PANEL,INK,ACCENT,MUTED,RADIUS=themes[style]
    PALETTE=[ACCENT,'#4c9fd6','#d99455','#ae83c6','#6cae8b']
    px.defaults.color_discrete_sequence=PALETTE
    st.markdown(f"""<style>
    .stApp {{background:{BG};color:{INK}}}
    [data-testid="stHeader"] {{background:{BG};}}
    .block-container {{max-width:1480px;padding:2rem 2.5rem 4rem;}}
    [data-testid="stSidebar"] {{background:{PANEL};border-right:1px solid {MUTED}35;}}
    h1,h2,h3,p,label,[data-testid="stMarkdownContainer"], [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{color:{INK};}}
    h1 {{font-size:2.55rem!important;letter-spacing:-.055em;line-height:1.12!important;font-weight:650!important;}}
    h2,h3 {{letter-spacing:-.025em;}}
    [data-testid="stCaptionContainer"] p {{color:{MUTED}!important;}}
    [data-testid="stMetric"] {{background:{PANEL};border:1px solid {MUTED}30;border-top:2px solid {ACCENT};border-radius:{RADIUS}px;padding:18px 20px;}}
    [data-testid="stMetricValue"] {{font-variant-numeric:tabular-nums;font-size:1.8rem;}}
    [data-testid="stPlotlyChart"] {{background:{PANEL};border:1px solid {MUTED}30;border-radius:{RADIUS}px;overflow:hidden;}}
    [data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"], textarea {{background:{PANEL}!important;color:{INK}!important;}}
    input,textarea {{color:{INK}!important;-webkit-text-fill-color:{INK}!important;}}
    [data-baseweb="tag"] {{background:{ACCENT}25!important;color:{INK}!important;}}
    [data-baseweb="tag"] span {{color:{INK}!important;}}
    button[kind="secondary"], [data-testid="stDownloadButton"] button {{background:{PANEL};color:{INK};border-color:{MUTED}65;}}
    [data-baseweb="tab"] {{color:{INK}!important;}}
    [data-testid="stAlert"] {{background:{PANEL};color:{INK};}}
    .eyebrow {{font:600 11px ui-monospace,monospace;letter-spacing:.15em;color:{ACCENT};margin-bottom:16px;}}
    .hero {{border-bottom:1px solid {MUTED}40;padding:12px 0 25px;margin-bottom:24px;}}
    .hero p {{max-width:850px;color:{MUTED};font-size:1rem;}}
    .brief {{border-left:3px solid {ACCENT};background:{PANEL};padding:16px 20px;margin:18px 0;color:{INK};}}
    @media(max-width:700px){{.block-container{{padding:1rem;}}h1{{font-size:1.8rem!important;}}}}
    </style>""",unsafe_allow_html=True)
    st.markdown(f'<div class="hero"><div class="eyebrow">MORRIS / {html.escape(name.upper())} · SYNTHETIC DEMO</div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',unsafe_allow_html=True)
    st.sidebar.caption('MORRIS · PORTFOLIO LAB')
    st.sidebar.caption('Fictional data. Explore the workflow; no external systems are connected.')

def chart(fig, height=340):
    fig.update_layout(template='plotly_white',paper_bgcolor=PANEL,plot_bgcolor=PANEL,font=dict(color=INK,size=12),colorway=PALETTE,height=height,margin=dict(l=55,r=25,t=55,b=55),legend=dict(orientation='h',y=-.24,x=0),hoverlabel=dict(bgcolor=PANEL,font_color=INK))
    fig.update_xaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    fig.update_yaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    st.plotly_chart(fig,use_container_width=True,theme=None)

def brief(text):
    st.markdown('<div class="brief">'+html.escape(text)+'</div>',unsafe_allow_html=True)

def money(value):
    sign='−' if value<0 else ''
    return f'{sign}${abs(value)/1e6:,.2f}M' if abs(value)>=1e6 else f'{sign}${abs(value):,.0f}'

def metrics(items):
    for col,(label,value) in zip(st.columns(len(items)),items):col.metric(label,value)

def table(df, name='detail', height=360):
    config={}
    for col in df.columns:
        label=str(col).replace('_',' ').title()
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            if any(x in str(col) for x in ['pct','margin','confidence','attainment','probability','achievement']):
                config[col]=st.column_config.NumberColumn(label,format='%.3f')
            elif any(x in str(col) for x in ['amount','revenue','arr','acv','cost','expense','cash','earned','capitalized','amortization','balance','asset','budget','forecast','variance','value','backlog','receipts','payroll','subcontractor','materials','labor']):
                config[col]=st.column_config.NumberColumn(label,format='$%.2f')
            else:config[col]=st.column_config.NumberColumn(label)
        else:config[col]=st.column_config.Column(label)
    st.dataframe(df,use_container_width=True,hide_index=True,height=height,column_config=config)
    st.download_button('Download '+name.replace('_',' ')+' CSV',df.to_csv(index=False),name+'.csv','text/csv',key='export_'+name)

def nonempty(df):
    if df.empty:
        st.info('No records in this selection. Choose at least one filter value to continue.')
        st.stop()

import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Snowflake dbt Analytics Engineering",layout="wide")
shell('DATA SYSTEMS','Inspect the path from source to mart.','Explore a local transformation simulation, inspect model lineage, and deliberately test data-quality failures.','cyan')
random.seed(5)
customers=pd.DataFrame({"customer_id":[f"C{i:03}" for i in range(1,81)],"segment":[random.choice(["Enterprise","Mid-Market","SMB"]) for _ in range(80)],"region":[random.choice(["North America","Europe","APAC"]) for _ in range(80)]})
rows=[]
for i in range(600):
    rows.append({"booking_id":f"B{i+1:04}","customer_id":random.choice(customers.customer_id.tolist()),"booking_date":pd.Timestamp("2026-01-01")+pd.Timedelta(days=random.randint(0,250)),"acv":round(random.uniform(5000,220000),2),"stage":random.choice(["Closed Won","Closed Won","Commit","Pipeline"])})
raw=pd.DataFrame(rows)
staging=raw.merge(customers,on="customer_id",how="left")
mart=staging.groupby(["region","segment","stage"],as_index=False).agg(bookings=("booking_id","count"),acv=("acv","sum"))


fault=st.sidebar.selectbox('Quality test scenario',['Clean data','Duplicate booking ID','Missing customer reference','Negative ACV'])
if fault=='Duplicate booking ID':raw.loc[1,'booking_id']=raw.loc[0,'booking_id']
if fault=='Missing customer reference':raw.loc[0,'customer_id']='UNKNOWN'
if fault=='Negative ACV':raw.loc[0,'acv']=-50000
staging=raw.merge(customers,on='customer_id',how='left',validate='many_to_one')
mart=staging.groupby(['region','segment','stage'],as_index=False,dropna=False).agg(bookings=('booking_id','count'),acv=('acv','sum'))
tests=pd.DataFrame([
 ['raw_bookings.booking_id','unique',raw.booking_id.is_unique],
 ['raw_bookings.customer_id','not_null',raw.customer_id.notna().all()],
 ['stg_bookings.customer_fk','relationships',staging.region.notna().all()],
 ['stg_bookings.acv','non_negative',bool((staging.acv>=0).all())],
],columns=['model_column','test','passed'])
metrics([('Source records',str(len(raw))),('Transformed rows',str(len(staging))),('Mart groups',str(len(mart))),('Quality checks',f'{tests.passed.sum()} / {len(tests)}')])
brief('Local pandas simulation of warehouse concepts. No Snowflake session or dbt run is active. Use the quality scenario control to inject a defect and inspect the failed gate.')
lineage,models,quality=st.tabs(['Model lineage','Data explorer','Quality gate'])
with lineage:
    nodes=['CRM bookings','Customers','Enriched staging','Revenue mart']
    fig=go.Figure(go.Sankey(node=dict(label=nodes,color=[ACCENT,'#ae83c6','#4c9fd6','#6cae8b'],pad=30,thickness=20),link=dict(source=[0,1,2],target=[2,2,3],value=[len(raw),len(customers),len(staging)],color=['rgba(83,210,237,.25)']*3)))
    fig.update_layout(title='Transformation dependencies · schematic record volumes')
    chart(fig,340)
    st.caption('Customer records enrich bookings through a many-to-one join; the diagram shows dependencies, not additive financial flows.')
    st.code("select b.booking_id, b.acv, c.region, c.segment\nfrom {{ ref('stg_bookings') }} b\nleft join {{ ref('stg_customers') }} c\n  on b.customer_id = c.customer_id",language='sql')
with models:
    layer=st.radio('Model',['Raw bookings','Customers','Enriched staging','Revenue mart'],horizontal=True)
    data={'Raw bookings':raw,'Customers':customers,'Enriched staging':staging,'Revenue mart':mart}[layer]
    table(data,'model_extract')
with quality:
    if tests.passed.all():st.success('All checks pass for the selected fixture.')
    else:st.error('Quality gate failed. Resolve the failing source condition before publishing this model.')
    st.dataframe(tests,hide_index=True,use_container_width=True)
    if fault!='Clean data':st.dataframe(staging.head(3),hide_index=True,use_container_width=True)
