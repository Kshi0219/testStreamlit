import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from math import pi #각도 조정을 위해서 필요함
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from unidecode import unidecode as ucd
import json
st.set_page_config(layout='wide')
st.title('선수 조회 및 비교')

st.divider()    # 구분선

gkStatsDf=pd.read_csv('data/GK.csv',index_col=0,encoding='utf-16').\
    drop(['player_position','player_overall','player_potential'],axis=1)     # 골키퍼 DF

gkPlayer=[]
for idx,rows in gkStatsDf.iterrows():
    gkPlayer.append(ucd(rows['player_nm']))     # 선수이름 모두 영어로 변환
gkStatsDf['player_nm']=gkPlayer

ngkStatsDf=pd.read_csv('data/UNGK.csv',index_col=0,encoding='utf-16').\
    drop(['player_overall','player_potential'],axis=1)      # 필드플레이어 DF

ngkPlayer=[]
for idx,rows in ngkStatsDf.iterrows():
    ngkPlayer.append(ucd(rows['player_nm']))        # 선수이름 모두 영어로 변환

file_path='data/stat_column_dict.json'      # 스탯 딕셔너리 로드 
with open(file_path,'r') as json_file:      # {GK:{상위컬럼:[스탯 이름]},nGK:{상위컬럼:[스탯 이름]}}
    columnDict=json.load(json_file)

tab1,tab2=st.tabs(['Gk','Non-Gk'])      # GK, Non-GK 탭 구분
with tab1:      # 키퍼 탭
    st.subheader('키퍼')
    with st.container(border=True):
        st.dataframe(gkStatsDf,use_container_width=True,hide_index=True)
    with st.container(border=True):
        viewMode=st.radio('Select View Mode',['One Player','Compare Two players'],captions=['한 명의 선수 조회','두 명의 선수 비교'],horizontal=True)
        if viewMode=='One Player':
            gk_Goalkeeping=gkStatsDf[['player_nm','player_team','player_country','player_age','player_foot','player_height','player_Weight']+
                                     columnDict['GK']['GoalKeeping']]
            keeperName=st.selectbox('Select player name 👇',gk_Goalkeeping['player_nm'],placeholder='Search',index=None)
            gkNameSelectedDf=gk_Goalkeeping.query(f"player_nm=='{keeperName}'")
    st.divider()
    with st.container(border=True):
        st.dataframe(gkNameSelectedDf,hide_index=True)
with tab2:      # 필드플레이어 탭
    st.subheader('필드 플레이어')
    with st.container(border=True):
        st.dataframe(ngkStatsDf,use_container_width=True,hide_index=True)