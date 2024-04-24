import streamlit as st
import numpy as np
import pandas as pd
from unidecode import unidecode as ucd  # 선수 이름 영어로 변환을 위해 사용
import json     # json으로 저장한 딕셔너리 파일을 불러오기 위해 사용
import plotly.graph_objects as go   # 스탯 시각화를 위해 사용 : plotly

st.set_page_config(layout='wide')   # 페이지 폭 넓게
st.title('선수 조회 및 비교')

st.divider()    # 구분선

# 골키퍼 데이터프레임
gkStatsDf=pd.read_csv('data/GK.csv',index_col=0,encoding='utf-16').\
    drop(['player_position','player_overall','player_potential'],axis=1)

# 선수이름 모두 영어로 변환
gkPlayer=[]
for idx,rows in gkStatsDf.iterrows():
    gkPlayer.append(ucd(rows['player_nm']))
gkStatsDf['player_nm']=gkPlayer

# 필드플레이어 데이터프레임
ngkStatsDf=pd.read_csv('data/UNGK.csv',index_col=0,encoding='utf-16').\
    drop(['player_overall','player_potential'],axis=1)

# 선수이름 모두 영어로 변환
ngkPlayer=[]
for idx,rows in ngkStatsDf.iterrows():
    ngkPlayer.append(ucd(rows['player_nm']))

file_path='data/stat_column_dict.json'      # 스탯 딕셔너리 로드 
with open(file_path,'r') as json_file:      # {GK:{상위컬럼:[스탯 이름]},nGK:{상위컬럼:[스탯 이름]}}
    columnDict=json.load(json_file)

tab1,tab2=st.tabs(['Gk','Non-Gk'])      # GK, Non-GK 탭 구분
with tab1:      # 키퍼 탭
    st.subheader('키퍼')
    
    # 키퍼 데이터프레임 컨테이너
    # boder=True -> 컨테이너 경계선
    with st.container(border=True):
        st.dataframe(gkStatsDf,use_container_width=True,hide_index=True)
    
    # 키퍼 스탯 시각화 컨테이너
    # try - except : 키퍼를 선택하지 않았을 때 차트를 그리지 못하는 오류 해결을 위해 사용
    with st.container(border=True):
        try:
            # 키퍼 스탯 상위 속성별로 데이터프레임 구분
            # columnsDict 활용
            gk_Goalkeeping=gkStatsDf[['player_nm','player_team','player_country','player_age','player_foot','player_height','player_Weight']+
                                        columnDict['GK']['GoalKeeping']]
            gk_Mental=gkStatsDf[['player_nm','player_team','player_country','player_age','player_foot','player_height','player_Weight']+
                                    columnDict['GK']['Mental']]
            gk_Physical=gkStatsDf[['player_nm','player_team','player_country','player_age','player_foot','player_height','player_Weight']+
                                    columnDict['GK']['Physical']]
            gk_Technical=gkStatsDf[['player_nm','player_team','player_country','player_age','player_foot','player_height','player_Weight']+
                                    columnDict['GK']['Technical']]
            
            # 키퍼 select box
            keeperName=st.selectbox('Search player name 👇',gkStatsDf['player_nm'],placeholder='Search',index=None)
            st.subheader(f"{keeperName} vs Mean")
            gkNameSelectedDf=gkStatsDf.query(f"player_nm=='{keeperName}'")
            
            # 골키핑 스탯 컨테이너
            # 스탯 종류가 많아서 두 개 컬럼으로 나눠서 시각화
            with st.container(border=True):
                st.markdown('''##### **Goalkeeping Stats**''')
                gk_categoryGoalkeeping=columnDict['GK']['GoalKeeping']
                col1_1,col2_1=st.columns(2)
                with col1_1:
                    gk_categoryGoalkeeping_1=gk_categoryGoalkeeping[:7]
                    gk_Goalkeeping_1=gkNameSelectedDf[gk_categoryGoalkeeping_1].reset_index().drop('index',axis=1)
                    gk_Goalkeeping_1_mean=pd.DataFrame(gkStatsDf[gk_categoryGoalkeeping_1].mean()).transpose()
                    
                    # 선택한 선수 스탯 레이더 차트
                    fig_gk_goalkeeping_1=go.Figure()
                    fig_gk_goalkeeping_1.add_trace(go.Scatterpolar(
                        r=list(gk_Goalkeeping_1.iloc[0]),
                        theta=gk_categoryGoalkeeping_1,
                        fill='tonext',
                        name=gkNameSelectedDf['player_nm'].tolist()[0]))
                    
                    # 평균 스탯 레이더 차트
                    fig_gk_goalkeeping_1.add_trace(go.Scatterpolar(
                        r=list(gk_Goalkeeping_1_mean.iloc[0]),
                        theta=gk_categoryGoalkeeping_1,
                        fill='toself',
                        name='Average'))
                    
                    # 차트 레이아웃 업데이트
                    fig_gk_goalkeeping_1.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0,20])),
                        showlegend=True,
                        width=600,height=600
                    )

                    # 스트림릿에서 plotly 차트 표시
                    st.plotly_chart(fig_gk_goalkeeping_1,use_container_width=True)
                with col2_1:
                    gk_categoryGoalkeeping_2=gk_categoryGoalkeeping[7:]
                    gk_Goalkeeping_2=gkNameSelectedDf[gk_categoryGoalkeeping_2].reset_index().drop('index',axis=1)
                    gk_Goalkeeping_2_mean=pd.DataFrame(gkStatsDf[gk_categoryGoalkeeping_2].mean()).transpose()
                    fig_gk_goalkeeping_2=go.Figure()
                    fig_gk_goalkeeping_2.add_trace(go.Scatterpolar(
                        r=gk_Goalkeeping_2.iloc[0].tolist(),
                        theta=[i for i in gk_categoryGoalkeeping_2],
                        fill='tonext',
                        name=gkNameSelectedDf['player_nm'].tolist()[0]))
                    fig_gk_goalkeeping_2.add_trace(go.Scatterpolar(
                        r=list(gk_Goalkeeping_2_mean.iloc[0]),
                        theta=gk_categoryGoalkeeping_2,
                        fill='toself',
                        name='Average'))
                    fig_gk_goalkeeping_2.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0,20])),
                        showlegend=True,
                        width=600,height=600
                    )            
                    st.plotly_chart(fig_gk_goalkeeping_2,use_container_width=True)
            st.divider()
            
            # 멘탈 스탯 컨테이너
            # 골키핑 스탯과 같은 이유로 두 개 컬럼으로 나눠서 시각화
            with st.container(border=True):
                st.markdown('''##### **Mental Stats**''')
                gk_categoryMental=columnDict['GK']['Mental']
                col1_2,col2_2=st.columns(2)
                with col1_2:
                    gk_categoryMental_1=gk_categoryMental[:7]
                    gk_Mental_1=gkNameSelectedDf[[i for i in gk_categoryMental_1]].reset_index().drop('index',axis=1)
                    gk_Mental_1_mean=pd.DataFrame(gkStatsDf[gk_categoryMental_1].mean()).transpose()
                    fig_gk_mental_1=go.Figure()
                    fig_gk_mental_1.add_trace(go.Scatterpolar(
                        r=list(gk_Mental_1.iloc[0]),
                        theta=gk_categoryMental_1,
                        fill='tonext',
                        name=gkNameSelectedDf['player_nm'].tolist()[0]))
                    fig_gk_mental_1.add_trace(go.Scatterpolar(
                        r=list(gk_Mental_1_mean.iloc[0]),
                        theta=gk_categoryMental_1,
                        fill='toself',
                        name='Average'))
                    fig_gk_mental_1.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0,20])),
                        showlegend=True,
                        width=600,height=600
                    )
                    st.plotly_chart(fig_gk_mental_1,use_container_width=True)
                with col2_2:
                    gk_categoryMental_2=gk_categoryMental[7:]
                    gk_Mental_2=gkNameSelectedDf[gk_categoryMental_2].reset_index().drop('index',axis=1)
                    gk_Mental_2_mean=pd.DataFrame(gkStatsDf[gk_categoryMental_2].mean()).transpose()
                    fig_gk_mental_2=go.Figure()
                    fig_gk_mental_2.add_trace(go.Scatterpolar(
                        r=gk_Mental_2.iloc[0].tolist(),
                        theta=[i for i in gk_categoryMental_2],
                        fill='tonext',
                        name=gkNameSelectedDf['player_nm'].tolist()[0]))
                    fig_gk_mental_2.add_trace(go.Scatterpolar(
                        r=list(gk_Mental_2_mean.iloc[0]),
                        theta=gk_categoryMental_2,
                        fill='toself',
                        name='Average'))
                    fig_gk_mental_2.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0,20])),
                        showlegend=True,
                        width=600,height=600
                    )            
                    st.plotly_chart(fig_gk_mental_2,use_container_width=True)
            st.divider()

            # 피지컬 & 테크니컬 스탯 컨테이너
            # 스탯 종류가 적어서 하나의 컨테이너에 한꺼번에 표시
            with st.container(border=True):
                gk_categoryPhysical=columnDict['GK']['Physical']
                gk_categoryTechnical=columnDict['GK']['Technical']
                col1_3,col2_3=st.columns(2)
                with col1_3:    # 피지컬 스탯 컬럼
                    st.markdown('''##### **Physical Stats**''')
                    gk_Physical_1=gkNameSelectedDf[[i for i in gk_categoryPhysical]].reset_index().drop('index',axis=1)
                    gk_Physical_1_mean=pd.DataFrame(gkStatsDf[gk_categoryPhysical].mean()).transpose()
                    fig_gk_physical_1=go.Figure()
                    fig_gk_physical_1.add_trace(go.Scatterpolar(
                        r=list(gk_Physical_1.iloc[0]),
                        theta=gk_categoryPhysical,
                        fill='tonext',
                        name=gkNameSelectedDf['player_nm'].tolist()[0]))
                    fig_gk_physical_1.add_trace(go.Scatterpolar(
                        r=list(gk_Physical_1_mean.iloc[0]),
                        theta=gk_categoryPhysical,
                        fill='toself',
                        name='Average'))
                    fig_gk_physical_1.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0,20])),
                        showlegend=True,
                        width=600,height=600
                    )
                    st.plotly_chart(fig_gk_physical_1,use_container_width=True)
                with col2_3:    # 테크니컬 스탯 컬럼
                    st.markdown('''##### **Technical Stats**''')
                    gk_Technical_1=gkNameSelectedDf[[i for i in gk_categoryTechnical]].reset_index().drop('index',axis=1)
                    gk_Technical_1_mean=pd.DataFrame(gkStatsDf[gk_categoryTechnical].mean()).transpose()
                    fig_gk_technical_1=go.Figure()
                    fig_gk_technical_1.add_trace(go.Scatterpolar(
                        r=list(gk_Technical_1.iloc[0]),
                        theta=gk_categoryTechnical,
                        fill='tonext',
                        name=gkNameSelectedDf['player_nm'].tolist()[0]))
                    fig_gk_technical_1.add_trace(go.Scatterpolar(
                        r=list(gk_Technical_1_mean.iloc[0]),
                        theta=gk_categoryTechnical,
                        fill='toself',
                        name='Average'))
                    fig_gk_technical_1.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0,20])),
                        showlegend=True,
                        width=600,height=600
                    )
                    st.plotly_chart(fig_gk_physical_1,use_container_width=True)
        except:
            pass

with tab2:      # 필드플레이어 탭
    st.subheader('필드 플레이어')
    with st.container(border=True):
        st.dataframe(ngkStatsDf,use_container_width=True,hide_index=True)
    with st.container(border=True):
        try:
            ngk_Technical=ngkStatsDf[['player_nm','player_team','player_country','player_age','player_foot','player_height','player_Weight']+
                                        columnDict['GK']['Technical']]
            ngk_Mental=gkStatsDf[['player_nm','player_team','player_country','player_age','player_foot','player_height','player_Weight']+
                                    columnDict['GK']['Mental']]
            ngk_Physical=gkStatsDf[['player_nm','player_team','player_country','player_age','player_foot','player_height','player_Weight']+
                                    columnDict['GK']['Physical']]
            nkeeperName=st.selectbox('Search player name 👇',ngkStatsDf['player_nm'],placeholder='Search',index=None)
            ngkNameSelectedDf=ngkStatsDf.query(f"player_nm=='{nkeeperName}'")
            st.subheader(f"{nkeeperName} vs Mean")
            # 테크니컬 스탯 컨테이너
            with st.container(border=True):
                st.markdown('''##### **Technical Stats**''')
                ngk_categoryTechnical=columnDict['nGK']['Technical']
                col3_1,col4_1=st.columns(2)
                with col3_1:
                    ngk_categoryTechnical_1=ngk_categoryTechnical[:7]
                    ngk_Technical_1=ngkNameSelectedDf[ngk_categoryTechnical_1].reset_index().drop('index',axis=1)
                    ngk_Technical_1_mean=pd.DataFrame(ngkStatsDf[ngk_categoryTechnical_1].mean()).transpose()
                    fig_ngk_technical_1=go.Figure()
                    fig_ngk_technical_1.add_trace(go.Scatterpolar(
                        r=list(ngk_Technical_1.iloc[0]),
                        theta=ngk_categoryTechnical_1,
                        fill='tonext',
                        name=ngkNameSelectedDf['player_nm'].tolist()[0]))
                    fig_ngk_technical_1.add_trace(go.Scatterpolar(
                        r=list(ngk_Technical_1_mean.iloc[0]),
                        theta=ngk_categoryTechnical_1,
                        fill='toself',
                        name='Average'))
                    fig_ngk_technical_1.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0,20])),
                        showlegend=True,
                        width=600,height=600
                    )
                    st.plotly_chart(fig_ngk_technical_1,use_container_width=True)
                with col4_1:
                    ngk_categoryTechnical_2=ngk_categoryTechnical[7:]
                    ngk_Technical_2=ngkNameSelectedDf[ngk_categoryTechnical_2].reset_index().drop('index',axis=1)
                    ngk_Technical_2_mean=pd.DataFrame(ngkStatsDf[ngk_categoryTechnical_2].mean()).transpose()
                    fig_ngk_technical_2=go.Figure()
                    fig_ngk_technical_2.add_trace(go.Scatterpolar(
                        r=list(ngk_Technical_2.iloc[0]),
                        theta=ngk_categoryTechnical_2,
                        fill='tonext',
                        name=ngkNameSelectedDf['player_nm'].tolist()[0]))
                    fig_ngk_technical_2.add_trace(go.Scatterpolar(
                        r=list(ngk_Technical_2_mean.iloc[0]),
                        theta=ngk_categoryTechnical_2,
                        fill='toself',
                        name='Average'))
                    fig_ngk_technical_2.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0,20])),
                        showlegend=True,
                        width=600,height=600
                    )
                    st.plotly_chart(fig_ngk_technical_2,use_container_width=True)
            st.divider()
            
            # 멘탈 스탯 컨테이너
            with st.container(border=True):
                st.markdown('''##### **Mental Stats**''')
                ngk_categoryMental=columnDict['nGK']['Mental']
                col3_2,col4_2=st.columns(2)
                with col3_2:
                    ngk_categoryMental_1=ngk_categoryMental[:7]
                    ngk_Mental_1=ngkNameSelectedDf[[i for i in ngk_categoryMental_1]].reset_index().drop('index',axis=1)
                    ngk_Mental_1_mean=pd.DataFrame(ngkStatsDf[ngk_categoryMental_1].mean()).transpose()
                    fig_ngk_mental_1=go.Figure()
                    fig_ngk_mental_1.add_trace(go.Scatterpolar(
                        r=list(ngk_Mental_1.iloc[0]),
                        theta=ngk_categoryMental_1,
                        fill='tonext',
                        name=ngkNameSelectedDf['player_nm'].tolist()[0]))
                    fig_ngk_mental_1.add_trace(go.Scatterpolar(
                        r=list(ngk_Mental_1_mean.iloc[0]),
                        theta=ngk_categoryMental_1,
                        fill='toself',
                        name='Average'))
                    fig_ngk_mental_1.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0,20])),
                        showlegend=True,
                        width=600,height=600
                    )
                    st.plotly_chart(fig_ngk_mental_1,use_container_width=True)
                with col4_2:
                    ngk_categoryMental_2=ngk_categoryMental[7:]
                    ngk_Mental_2=ngkNameSelectedDf[ngk_categoryMental_2].reset_index().drop('index',axis=1)
                    ngk_Mental_2_mean=pd.DataFrame(ngkStatsDf[ngk_categoryMental_2].mean()).transpose()
                    fig_ngk_mental_2=go.Figure()
                    fig_ngk_mental_2.add_trace(go.Scatterpolar(
                        r=ngk_Mental_2.iloc[0].tolist(),
                        theta=[i for i in ngk_categoryMental_2],
                        fill='tonext',
                        name=ngkNameSelectedDf['player_nm'].tolist()[0]))
                    fig_ngk_mental_2.add_trace(go.Scatterpolar(
                        r=list(ngk_Mental_2_mean.iloc[0]),
                        theta=ngk_categoryMental_2,
                        fill='toself',
                        name='Average'))
                    fig_ngk_mental_2.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0,20])),
                        showlegend=True,
                        width=600,height=600
                    )            
                    st.plotly_chart(fig_ngk_mental_2,use_container_width=True)
            st.divider()

            # 피지컬 스탯 컨테이너
            with st.container(border=True):
                ngk_categoryPhysical=columnDict['nGK']['Physical']
                st.markdown('''##### **Physical Stats**''')
                ngk_Physical_1=ngkNameSelectedDf[[i for i in ngk_categoryPhysical]].reset_index().drop('index',axis=1)
                ngk_Physical_1_mean=pd.DataFrame(ngkStatsDf[ngk_categoryPhysical].mean()).transpose()
                fig_ngk_physical_1=go.Figure()
                fig_ngk_physical_1.add_trace(go.Scatterpolar(
                    r=list(ngk_Physical_1.iloc[0]),
                    theta=ngk_categoryPhysical,
                    fill='tonext',
                    name=ngkNameSelectedDf['player_nm'].tolist()[0]))
                fig_ngk_physical_1.add_trace(go.Scatterpolar(
                    r=list(ngk_Physical_1_mean.iloc[0]),
                    theta=ngk_categoryPhysical,
                    fill='toself',
                    name='Average'))
                fig_ngk_physical_1.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0,20])),
                    showlegend=True,
                    width=600,height=600)
                st.plotly_chart(fig_ngk_physical_1,use_container_width=True)
        except:
            pass