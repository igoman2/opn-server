import warnings
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tabulate import tabulate

# In[3]:
warnings.filterwarnings(action='ignore')


app = FastAPI()
origin = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Report(BaseModel):
    intro: object
    market_analysis: object
    competitive_analysis: object
    user_analysis: object


@app.get("/")
async def root():
    return {"message": "Hello World!!"}


@app.get("/report/", response_model=Report)
async def report(department: str, location: str):
    # 행정동 코드용 파일
    hdong_code_df = pd.read_excel("행정동_법정동_220103.xlsx", sheet_name="행정동")
    # 행정동-법정동 연계용 파일
    loc_kikmix = pd.read_excel("KIKmix.20220401.xlsx")
    # 의원 정보 포함 파일
    hos_df = pd.read_excel("강남구_치과의원병원_목록.xlsx", sheet_name="meta")
    # 급여비율용 파일
    nonprofit_df = pd.read_excel("진료과별 급여비율.xlsx")
    simsa_percent = str(round(nonprofit_df[nonprofit_df['진료과목'] == user_input_type]['비율'].to_list()[0] * 100)) + "%"

    # simsa_percent = '58%'
    # In[49]:

    # 유저 input값 직접 기입
    user_input_type = department

    # 분석을 진행할 행정동 사전입력 (여기서는 경기도 시흥시 능곡동)
    my_hdong = location
    user_input_loc = hdong_code_df['행정기관코드'][((hdong_code_df['통합주소'].to_list()).index(my_hdong))]

    # In[58]:

    # 개원할 진료과
    # 분석에 활용되는 진료과
    # 나의 개원 매력도

    # 진료과목 묶음 정리
    normals = ['일반의원', '가정의학과', '내과']
    coughs_1 = ['가정의학과', '내과', '소아청소년과', '이비인후과', '일반의원']
    coughs_2 = ['가정의학과', '내과', '소아청소년과', '이비인후과']
    bones = ['마취통증의학과', '재활의학과', '정형외과', '신경외과', '신경과']
    mentals = ['신경과', '정신건강의학과']
    exs = ['병리과', '진단검사의학과']
    tubers = ['결핵과', '내과']
    chests = ['흉부외과', '외과']

    # 유저의 개원 진료과에 따른 데이터프레임 1차 분류 (해당 범위 내의 진료과 병의원들만 남겨놓기)
    if (user_input_type == "일반의원"):
        type_cf = normals
    elif (user_input_type == "가정의학과"):
        type_cf = coughs_1
    elif (user_input_type == "내과") | (user_input_type == "소아청소년과") | (user_input_type == "이비인후과"):
        type_cf = coughs_2
    elif (user_input_type == "마취통증의학과") | (user_input_type == "재활의학과") | (user_input_type == "정형외과") | (
            user_input_type == "신경외과"):
        type_cf = bones
    elif (user_input_type == "신경과") | (user_input_type == "정신건강의학과"):
        type_cf = mentals
    elif (user_input_type == "병리과") | (user_input_type == "진단검사의학과"):
        type_cf = exs
    elif (user_input_type == "결핵과"):
        type_cf = tubers
    elif (user_input_type == "흉부외과"):
        type_cf = chests
    else:
        type_cf = [user_input_type]

    # 개원 타겟 지역
    for n in range(len(loc_kikmix)):
        if user_input_loc == loc_kikmix['행정동코드'][n]:
            user_input_loc_p1 = loc_kikmix['읍면동명'][n]
            user_input_loc_p2 = loc_kikmix['시도명'][n] + " " + loc_kikmix['시군구명'][n]
            break
    user_input_loc_r = ""
    area_holder = []
    for i in range(len(loc_kikmix)):
        h_code = loc_kikmix['행정동코드'][i]
        if user_input_loc == h_code:
            area_name = loc_kikmix['동리명'][i]
            area_holder.append(area_name)
            user_input_loc_r += area_name + ", "
    user_input_loc_r = user_input_loc_r[:-2]

    # 분석 대상 병원 또는 의원 (b=병원급, s=의원급)
    b_hn_holder = []
    b_hod_holder = []
    b_ha_holder = []
    b_hp_holder = []
    b_ht_holder = []
    b_simcode_holder = []
    b_str_holder = ""

    s_hn_holder = []
    s_hod_holder = []
    s_ha_holder = []
    s_hp_holder = []
    s_ht_holder = []
    s_simcode_holder = []
    s_str_holder = ""

    norms_str = "일반의원|가정의학과|내과"
    coughs_str_1 = "가정의학과|내과|소아청소년과|이비인후과|일반의원"
    coughs_str_2 = "가정의학과|내과|소아청소년과|이비인후과"
    bones_str = "정형외과|마취통증의학과|재활의학과|신경외과|신경과"
    mentals_str = "신경과|정신건강의학과"
    exs_str = "병리과|진단검사의학과"
    tubers_str = "결핵과|내과"
    chests_str = "흉부외과|외과"
    nochests_str = "정형외과|성형외과|신경외과"

    if (user_input_type == "일반의원"):
        hos_df = hos_df[hos_df['진료과정보'].str.contains(norms_str)]
    elif (user_input_type == "가정의학과"):
        hos_df = hos_df[hos_df['진료과정보'].str.contains(coughs_str_1)]
    elif (user_input_type == "내과") | (user_input_type == "소아청소년과") | (user_input_type == "이비인후과"):
        hos_df = hos_df[hos_df['진료과정보'].str.contains(coughs_str_2)]
    elif (user_input_type == "마취통증의학과") | (user_input_type == "재활의학과") | (user_input_type == "정형외과") | (
            user_input_type == "신경외과"):
        hos_df = hos_df[hos_df['진료과정보'].str.contains(bones_str)]
    elif (user_input_type == "신경과") | (user_input_type == "정신건강의학과"):
        hos_df = hos_df[hos_df['진료과정보'].str.contains(mentals_str)]
    elif (user_input_type == "병리과") | (user_input_type == "진단검사의학과"):
        hos_df = hos_df[hos_df['진료과정보'].str.contains(exs_str)]
    elif (user_input_type == "결핵과"):
        hos_df = hos_df[hos_df['진료과정보'].str.contains(tubers_str)]
    elif (user_input_type == "흉부외과"):
        hos_df = hos_df[hos_df['진료과정보'].str.contains(chests_str)]
        hos_df = hos_df[hos_df['진료과정보'].str.contains(nochests_str) == False]
    else:
        hos_df = hos_df[hos_df['진료과정보'].str.contains(user_input_type)]

    # 유저 input을 이용해 각종 병의원 결과 정보 뽑는 과정
    for j in range(len(hos_df)):
        hos_name = hos_df['의원명'].to_list()[j]
        hos_h_code = hos_df['행정동코드'].to_list()[j]
        hos_open_date = hos_df['개설일자'].to_list()[j]
        hos_area = str(int(hos_df['총면적(평)'].to_list()[j])) + "평"
        hos_prof = hos_df['전문의수'].to_list()[j]
        hos_type = hos_df['진료과정보'].to_list()[j]
        hos_class = hos_df['구분'].to_list()[j]
        hos_simcode = hos_df['심평원코드'].to_list()[j]
        if user_input_loc == hos_h_code:
            if "의원" in hos_class:
                s_hn_holder.append(hos_name)
                s_hod_holder.append(hos_open_date)
                s_ha_holder.append(hos_area)
                s_hp_holder.append(hos_prof)
                s_ht_holder.append(hos_type)
                s_simcode_holder.append(hos_simcode)
            if "병원" in hos_class:
                b_hn_holder.append(hos_name)
                b_hod_holder.append(hos_open_date)
                b_ha_holder.append(hos_area)
                b_hp_holder.append(hos_prof)
                b_ht_holder.append(hos_type)
                b_simcode_holder.append(hos_simcode)

    # 병원급 세부설명
    for k2 in list(set(b_ht_holder)):
        count = b_ht_holder.count(k2)
        b_str_holder += k2 + " " + str(count) + "개, "
    b_str_holder = b_str_holder[:-2]

    # 용어 설명 Table
    explain_df = pd.DataFrame()
    e_holder = ["매출액", "시장규모", "객단가"]
    enums_holder = []
    e1 = '''
    월간 카드 매출 합계를 의미합니다.
    (심사평가원에 따르면 {}의 카드 매출은 보험급여가 포함된 실제 매출의 {}를 반영합니다)
    '''.format(user_input_type, simsa_percent)
    enums_holder.append(e1)
    e2 = "분석 대상 의원들의 월 매출액 합계이며, 지난 12개월의 평균값을 사용합니다."
    enums_holder.append(e2)
    e3 = "고객의 결제 건당 금액을 의미하며, 지난 12개월의 평균값을 사용합니다."
    enums_holder.append(e3)
    explain_df['지표 명칭'] = e_holder
    explain_df['지표 설명'] = enums_holder

    # 의원급 Table
    simple_holder = []
    simple_b_holder = []

    s_df = pd.DataFrame()
    s_df['사업장명'] = s_hn_holder
    s_df['진료과'] = s_ht_holder
    s_df['개원년도'] = s_hod_holder
    s_df['면적'] = s_ha_holder
    s_df['전문의'] = s_hp_holder
    s_df = s_df.sort_values(by="개원년도", ascending=False).reset_index().drop(labels="index", axis=1)

    for i in range(len(s_df)):
        simple_holder.append(s_df['개원년도'][i].year)
    s_df['개원년도'] = simple_holder

    b_df = pd.DataFrame()
    b_df['사업장명'] = b_hn_holder
    b_df['진료과'] = b_ht_holder
    b_df['개원년도'] = b_hod_holder
    b_df['면적'] = b_ha_holder
    b_df['전문의'] = b_hp_holder
    b_df = b_df.sort_values(by="개원년도", ascending=False).reset_index().drop(labels="index", axis=1)
    for i in range(len(b_df)):
        simple_b_holder.append(b_df['개원년도'][i].year)
    b_df['개원년도'] = simple_b_holder

    # 텍스트 생성
    my_print = ''
    for t in type_cf:
        my_print += t + ", "
    my_print = my_print[:-2]

    # 용어 설명

    # 의료기관 목록



    # JSON 출력을 위한 intro 딕셔너리 홀더에 담기
    intro = {
        "department": user_input_type,
        "department_group": my_print,
        "address_dong": user_input_loc_p1,
        "address_sido_sigungu": user_input_loc_p2,
        "address_realated_dongs": user_input_loc_r,
        "hospital_count": len(s_hn_holder),
        "big_hospital_count": len(b_hn_holder),
        "big_hospital_departments": b_str_holder,
        "sales_reflection": simsa_percent,
        "hospital_table": [
        ],
        "big_hospital_table": [
        ]
    }

    for i in range(len(s_df)):
        this_hospital = {}
        this_hospital['name'] = s_df['사업장명'].to_list()[i]
        this_hospital['department'] = s_df['진료과'].to_list()[i]
        this_hospital['open_year'] = s_df['개원년도'].to_list()[i]
        this_hospital['area'] = s_df['면적'].to_list()[i]
        this_hospital['prof'] = s_df['전문의'].to_list()[i]
        intro['hospital_table'].append(this_hospital)

    for j in range(len(b_df)):
        this_big_hospital = {}
        this_big_hospital['name'] = b_df['사업장명'].to_list()[j]
        this_big_hospital['department'] = b_df['진료과'].to_list()[j]
        this_big_hospital['open_year'] = b_df['개원년도'].to_list()[j]
        this_big_hospital['area'] = b_df['면적'].to_list()[j]
        this_big_hospital['prof'] = b_df['전문의'].to_list()[j]
        intro['big_hospital_table'].append(this_big_hospital)

    # # 2. 시장 분석

    # In[56]:

    # 시장분석용 파일 불러오기
    # 2020년, 2021년 병의원 목록 불러오기
    if (user_input_loc // 100000000) == 11:
        market_df = pd.read_excel("시장분석용_서울.xlsx")
        hos_4div_df = pd.read_excel("분기별_병의원목록_서울.xlsx")
    elif (user_input_loc // 100000000) == 41:
        market_df = pd.read_excel("시장분석용_경기.xlsx")
        hos_4div_df = pd.read_excel("분기별_병의원목록_경기.xlsx")
    elif (user_input_loc // 100000000) == 28:
        market_df = pd.read_excel("시장분석용_인천.xlsx")
        hos_4div_df = pd.read_excel("분기별_병의원목록_인천.xlsx")
    else:
        market_df = pd.read_excel("시장분석용_나머지.xlsx")
        hos_4div_df = pd.read_excel("분기별_병의원목록_나머지.xlsx")
    market_df = market_df[market_df['hdong_code'] == user_input_loc]

    # 시장 규모: 최근 12개월 기준 월평균매출
    # 시장 규모 장기 추세
    # 의원 1평당 매출액: 각 의원별 평당매출의 평균값
    # 1평당 매출액 장기 추세

    # 진료과목에 해당하는 병의원만 추려내기
    if (user_input_type == "일반의원"):
        market_df = market_df[market_df['hos_type'].str.contains(norms_str)]
    elif (user_input_type == "가정의학과"):
        market_df = market_df[market_df['hos_type'].str.contains(coughs_str_1)]
    elif (user_input_type == "내과") | (user_input_type == "소아청소년과") | (user_input_type == "이비인후과"):
        market_df = market_df[market_df['hos_type'].str.contains(coughs_str_2)]
    elif (user_input_type == "마취통증의학과") | (user_input_type == "재활의학과") | (user_input_type == "정형외과") | (
            user_input_type == "신경외과"):
        market_df = market_df[market_df['hos_type'].str.contains(bones_str)]
    elif (user_input_type == "신경과") | (user_input_type == "정신건강의학과"):
        market_df = market_df[market_df['hos_type'].str.contains(mentals_str)]
    elif (user_input_type == "병리과") | (user_input_type == "진단검사의학과"):
        market_df = market_df[market_df['hos_type'].str.contains(exs_str)]
    elif (user_input_type == "결핵과"):
        market_df = market_df[market_df['hos_type'].str.contains(tubers_str)]
    elif (user_input_type == "흉부외과"):
        market_df = market_df[market_df['hos_type'].str.contains(chests_str)]
        market_df = market_df[market_df['hos_type'].str.contains(nochests_str) == False]
    else:
        market_df = market_df[market_df['hos_type'].str.contains(user_input_type)]

    market_df = market_df.reset_index()
    ppa_holder = []
    for i in range(len(market_df)):
        if market_df['area'][i] == "-":
            ppa_holder.append(market_df['EST_HGA'][i] / (sum(market_df[market_df['area'] != "-"]['area']) / len(
                market_df[market_df['area'] != "-"]['area'])))
        else:
            ppa_holder.append(market_df['EST_HGA'][i] / market_df['area'][i])
    market_df['profit_per_area'] = ppa_holder

    # 가장 최근 12개월 정보 따로 추려내기 (단기 추세용)
    today_year = market_df['TA_YM'].max() // 100
    today_month = market_df['TA_YM'].max() % 100
    my_year = today_year - 1
    my_month = today_month + 1
    if my_month > 12:
        my_year += 1
        my_month = 1
    my_date = ""
    if my_month < 10:
        my_date += str(my_year) + "0" + str(my_month)
    else:
        my_date += str(my_year) + str(my_month)
    my_date = int(my_date)
    rec12m_df = market_df[market_df['TA_YM'] >= my_date]

    # 시장규모 (최근 12개월 기준)
    market_size_12m = round(
        (sum(rec12m_df.groupby('TA_YM').sum()['EST_HGA']) / len(rec12m_df.groupby('TA_YM').sum()['EST_HGA'])) / 10000)
    # 지난 12개월 중 시장규모 최대 (값, 시기)
    max_msize = round(
        rec12m_df.groupby('TA_YM').sum().sort_values(by='EST_HGA', ascending=False)['EST_HGA'].to_list()[0] / 10000)
    max_year = int(str(
        rec12m_df.groupby('TA_YM').sum().sort_values(by='EST_HGA', ascending=False).reset_index()['TA_YM'].to_list()[
            0])[:4])
    max_month = int(str(
        rec12m_df.groupby('TA_YM').sum().sort_values(by='EST_HGA', ascending=False).reset_index()['TA_YM'].to_list()[
            0])[-2:])
    # 지난 12개월 중 시장규모 최소
    min_msize = round(
        rec12m_df.groupby('TA_YM').sum().sort_values(by='EST_HGA', ascending=False)['EST_HGA'].to_list()[-1] / 10000)
    min_year = int(str(
        rec12m_df.groupby('TA_YM').sum().sort_values(by='EST_HGA', ascending=False).reset_index()['TA_YM'].to_list()[
            -1])[:4])
    min_month = int(str(
        rec12m_df.groupby('TA_YM').sum().sort_values(by='EST_HGA', ascending=False).reset_index()['TA_YM'].to_list()[
            -1])[-2:])

    # 연도별 정보 따로 추려내기 (장기 추세용)
    holding_df1 = market_df[market_df['year'] >= my_year - 2].groupby('year').sum().reset_index().sort_values(by='year')
    holding_df2 = market_df[market_df['year'] >= my_year - 2].groupby('TA_YM').sum().reset_index().sort_values(
        by='TA_YM')
    yy_holder = []
    ss_holder = []
    for i in range(len(holding_df1)):
        hyear = holding_df1['year'][i]
        hsize = holding_df1['EST_HGA'][i]
        hcount = len(holding_df2[holding_df2['TA_YM'] // 100 == hyear])
        yy_holder.append(hyear)
        ss_holder.append(round((hsize / hcount) / 10000))
    early_year = yy_holder[0]
    late_year = yy_holder[-1]
    early_size = ss_holder[0]
    late_size = ss_holder[-1]
    three_percent = round((late_size - early_size) / early_size * 100)
    if three_percent < 0:
        three_ident = "감소"
    else:
        three_ident = "증가"

    # 1평당 매출액 (단기 추세)
    pp_short_cost = round(sum(rec12m_df.groupby('TA_YM').mean()['profit_per_area']) / len(
        rec12m_df.groupby('TA_YM').mean()['profit_per_area']) / 10000)
    # 1평당 매출액 (장기 추세)
    holding_df3 = market_df[market_df['year'] >= my_year - 2].groupby('year').mean().reset_index().sort_values(
        by='year')
    ppyy_holder = []
    ppss_holder = []
    for i in range(len(holding_df3)):
        pyear = holding_df3['year'][i]
        psize = holding_df3['profit_per_area'][i]
        ppyy_holder.append(pyear)
        ppss_holder.append(round(psize / 10000))
    p_early_year = ppyy_holder[0]
    p_late_year = ppyy_holder[-1]
    p_early_size = ppss_holder[0]
    p_late_size = ppss_holder[-1]
    three_percent2 = round((p_late_size - p_early_size) / p_early_size * 100)
    if three_percent2 < 0:
        three_ident2 = "감소"
    else:
        three_ident2 = "증가"

    # 연도별 의원수 확인
    if (user_input_type == "일반의원"):
        hos_2020_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
            hos_4div_df['진료과분류'].str.contains(norms_str))])
        hos_2021_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
            hos_4div_df['진료과분류'].str.contains(norms_str))])
    elif (user_input_type == "가정의학과"):
        hos_2020_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
            hos_4div_df['진료과분류'].str.contains(coughs_str_1))])
        hos_2021_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
            hos_4div_df['진료과분류'].str.contains(coughs_str_1))])
    elif (user_input_type == "내과") | (user_input_type == "소아청소년과") | (user_input_type == "이비인후과"):
        hos_2020_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
            hos_4div_df['진료과분류'].str.contains(coughs_str_2))])
        hos_2021_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
            hos_4div_df['진료과분류'].str.contains(coughs_str_2))])
    elif (user_input_type == "마취통증의학과") | (user_input_type == "재활의학과") | (user_input_type == "정형외과") | (
            user_input_type == "신경외과"):
        hos_2020_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
            hos_4div_df['진료과분류'].str.contains(bones_str))])
        hos_2021_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
            hos_4div_df['진료과분류'].str.contains(bones_str))])
    elif (user_input_type == "신경과") | (user_input_type == "정신건강의학과"):
        hos_2020_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
            hos_4div_df['진료과분류'].str.contains(mentals_str))])
        hos_2021_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
            hos_4div_df['진료과분류'].str.contains(mentals_str))])
    elif (user_input_type == "병리과") | (user_input_type == "진단검사의학과"):
        hos_2020_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
            hos_4div_df['진료과분류'].str.contains(exs_str))])
        hos_2021_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
            hos_4div_df['진료과분류'].str.contains(exs_str))])
    elif (user_input_type == "결핵과"):
        hos_2020_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
            hos_4div_df['진료과분류'].str.contains(tubers_str))])
        hos_2021_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
            hos_4div_df['진료과분류'].str.contains(tubers_str))])
    elif (user_input_type == "흉부외과"):
        hos_2020_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
            hos_4div_df['진료과분류'].str.contains(chests_str))])
        hos_2020_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
                    hos_4div_df['진료과분류'].str.contains(nochests_str) == False)])
        hos_2021_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
            hos_4div_df['진료과분류'].str.contains(chests_str))])
        hos_2021_count = len(hos_4div_df[(hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
                    hos_4div_df['진료과분류'].str.contains(nochests_str) == False)])
    hos_now_count = len(s_hn_holder)

    # Key Metric

    if market_size_12m >= 10000:
        market_size_12m = str(market_size_12m // 10000) + "억 " + str(market_size_12m % 10000)

    if hos_now_count > hos_2020_count:
        count_tendency = "증가"
    elif hos_now_count == hos_2020_count:
        count_tendency = "유지"
    else:
        count_tendency = "감소"


    # Text
    if max_msize >= 10000:
        max_msize = str(max_msize // 10000) + "억 " + str(max_msize % 10000)
    if min_msize >= 10000:
        min_msize = str(min_msize // 10000) + "억 " + str(min_msize % 10000)
    if early_size >= 10000:
        early_size = str(early_size // 10000) + "억 " + str(early_size % 10000)
    if late_size >= 10000:
        late_size = str(late_size // 10000) + "억 " + str(late_size % 10000)


    # 테이블 구상하기
    t1 = rec12m_df.groupby('TA_YM').sum().reset_index()
    tt_holder = []
    for tt in t1['TA_YM'].to_list():
        tt_holder.append(datetime.strptime(str(tt), "%Y%m"))

    # Chart

    this_yy_holder = []
    for y in yy_holder:
        this_yy_holder.append(str(y))


    if (user_input_type == "일반의원"):
        hos_2020_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(norms_str))])
        hos_2020_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(norms_str))])
        hos_2020_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(norms_str))])
        hos_2020_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(norms_str))])
        hos_2021_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(norms_str))])
        hos_2021_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(norms_str))])
        hos_2021_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(norms_str))])
        hos_2021_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(norms_str))])
    elif (user_input_type == "가정의학과"):
        hos_2020_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_1))])
        hos_2020_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_1))])
        hos_2020_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_1))])
        hos_2020_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_1))])
        hos_2021_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_1))])
        hos_2021_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_1))])
        hos_2021_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_1))])
        hos_2021_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_1))])
    elif (user_input_type == "내과") | (user_input_type == "소아청소년과") | (user_input_type == "이비인후과"):
        hos_2020_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_2))])
        hos_2020_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_2))])
        hos_2020_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_2))])
        hos_2020_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_2))])
        hos_2021_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_2))])
        hos_2021_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_2))])
        hos_2021_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_2))])
        hos_2021_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(coughs_str_2))])
    elif (user_input_type == "마취통증의학과") | (user_input_type == "재활의학과") | (user_input_type == "정형외과") | (
            user_input_type == "신경외과"):
        hos_2020_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(bones_str))])
        hos_2020_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(bones_str))])
        hos_2020_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(bones_str))])
        hos_2020_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(bones_str))])
        hos_2021_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(bones_str))])
        hos_2021_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(bones_str))])
        hos_2021_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(bones_str))])
        hos_2021_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(bones_str))])
    elif (user_input_type == "신경과") | (user_input_type == "정신건강의학과"):
        hos_2020_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(mentals_str))])
        hos_2020_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(mentals_str))])
        hos_2020_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(mentals_str))])
        hos_2020_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(mentals_str))])
        hos_2021_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(mentals_str))])
        hos_2021_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(mentals_str))])
        hos_2021_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(mentals_str))])
        hos_2021_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(mentals_str))])
    elif (user_input_type == "병리과") | (user_input_type == "진단검사의학과"):
        hos_2020_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(exs_str))])
        hos_2020_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(exs_str))])
        hos_2020_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(exs_str))])
        hos_2020_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(exs_str))])
        hos_2021_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(exs_str))])
        hos_2021_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(exs_str))])
        hos_2021_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(exs_str))])
        hos_2021_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(exs_str))])
    elif (user_input_type == "결핵과"):
        hos_2020_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(tubers_str))])
        hos_2020_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(tubers_str))])
        hos_2020_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(tubers_str))])
        hos_2020_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(tubers_str))])
        hos_2021_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(tubers_str))])
        hos_2021_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(tubers_str))])
        hos_2021_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(tubers_str))])
        hos_2021_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(tubers_str))])
    elif (user_input_type == "흉부외과"):
        hos_2020_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(chests_str))])
        hos_2020_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(chests_str))])
        hos_2020_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(chests_str))])
        hos_2020_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(chests_str))])
        hos_2021_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_1Q") & (
                                         hos_4div_df['진료과분류'].str.contains(chests_str))])
        hos_2021_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_2Q") & (
                                         hos_4div_df['진료과분류'].str.contains(chests_str))])
        hos_2021_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_3Q") & (
                                         hos_4div_df['진료과분류'].str.contains(chests_str))])
        hos_2021_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
                                         hos_4div_df['진료과분류'].str.contains(chests_str))])
        hos_2020_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_1Q") & (
                                                 hos_4div_df['진료과분류'].str.contains(nochests_str) == False)])
        hos_2020_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_2Q") & (
                                                 hos_4div_df['진료과분류'].str.contains(nochests_str) == False)])
        hos_2020_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_3Q") & (
                                                 hos_4div_df['진료과분류'].str.contains(nochests_str) == False)])
        hos_2020_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2020_4Q") & (
                                                 hos_4div_df['진료과분류'].str.contains(nochests_str) == False)])
        hos_2021_1st_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_1Q") & (
                                                 hos_4div_df['진료과분류'].str.contains(nochests_str) == False)])
        hos_2021_2nd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_2Q") & (
                                                 hos_4div_df['진료과분류'].str.contains(nochests_str) == False)])
        hos_2021_3rd_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_3Q") & (
                                                 hos_4div_df['진료과분류'].str.contains(nochests_str) == False)])
        hos_2021_4th_count = len(hos_4div_df[
                                     (hos_4div_df['행정동코드'] == user_input_loc) & (hos_4div_df['분기'] == "2021_4Q") & (
                                                 hos_4div_df['진료과분류'].str.contains(nochests_str) == False)])
    hos_20to22_count_holder = [hos_2021_2nd_count, hos_2021_3rd_count, hos_2021_4th_count, hos_now_count]
    hos_divname_holder = ["2021_2", "2021_3", "2021_4", "2022_1"]





    t2 = rec12m_df.groupby('TA_YM').mean().reset_index()
    tt2_holder = []
    for tt in t2['TA_YM'].to_list():
        tt2_holder.append(datetime.strptime(str(tt), "%Y%m"))

    that_yy_holder = []
    for y in ppyy_holder:
        that_yy_holder.append(str(y))


    # JSON 출력을 위한 market_analysis 딕셔너리 홀더에 담기
    market_analysis = {
        "market_size": str(market_size_12m) + "만원",
        "market_trend": three_ident,
        "hospital_count_past": str(hos_2020_count) + "개",
        "hospital_count_now": str(hos_now_count) + "개",
        "hospital_count_trend": count_tendency,
        "profit_per_area_size": str(pp_short_cost) + "만원",
        "profit_per_area_trend": three_ident2,
        "address_dong": user_input_loc_p1,
        "department": user_input_type,
        "market_max_size": str(max_msize) + "만원",
        "market_max_year": str(max_year) + "년",
        "market_max_month": str(max_month) + "월",
        "market_min_size": str(min_msize) + "만원",
        "market_min_year": str(min_year) + "년",
        "market_min_month": str(min_month) + "월",
        "3y_trend_start_year": str(early_year) + "년",
        "3y_trend_start_market_size": str(early_size) + "만원",
        "3y_trend_end_year": str(late_year) + "년",
        "3y_trend_end_market_size": str(late_size) + "만원",
        "3y_trend_percent": str(abs(three_percent)) + "%",
        "3y_trend_hospital_count_difference": str(abs(hos_now_count - hos_2020_count)) + "개",
        "profit_per_50p": str(pp_short_cost * 50) + "만원",
        "3y_trend_profit_per_area_start_year": str(p_early_year) + "년",
        "3y_trend_profit_per_area_start_market_size": str(p_early_size) + "만원",
        "3y_trend_profit_per_area_end_year": str(p_late_year) + "년",
        "3y_trend_profit_per_area_end_market_size": str(p_late_size) + "만원",
        "3y_trend_profit_per_area_percent": str(abs(three_percent2)) + "%",
        "12m_trend_chart": {
        },
        "hospital_count_chart": {
        },
        "3y_trend_chart": {
        }
    }

    for i in range(len(tt_holder)):
        market_analysis['12m_trend_chart']['market_size_{}m'.format(i + 1)] = int(round(t1['EST_HGA'] / 10000)[i])
    for n in range(len(tt2_holder)):
        market_analysis['12m_trend_chart']['profit_per_area_size_{}m'.format(n + 1)] = int(
            round(t2['profit_per_area'] / 10000)[n])
    for j in range(len(hos_divname_holder)):
        market_analysis['hospital_count_chart']['{}'.format(hos_divname_holder[j])] = hos_20to22_count_holder[j]
    for k in range(len(this_yy_holder)):
        market_analysis['3y_trend_chart']['market_size_year_{}'.format(k + 1)] = ss_holder[k]
    for o in range(len(that_yy_holder)):
        market_analysis['3y_trend_chart']['profit_per_area_year_{}'.format(o + 1)] = ppss_holder[o]

    # # 3. 경쟁 분석

    # In[78]:

    # 전체 의원 평균 매출액
    # 신규 의원 평균 매출액
    # 경쟁 유형

    # 폐업 확인용 데이터파일 불러오기
    closed_hos_df = pd.read_excel("폐업_병의원목록.xlsx")

    # 위에서 가져온 심평원코드 활용
    vs_analysis_df = market_df[market_df['sim_cd'].isin(s_simcode_holder)]
    vs_analysis_df = vs_analysis_df[vs_analysis_df['TA_YM'] >= (my_date - 100)]

    # 각종 필요한 정보 산출해내기
    # 전체 의원 평균 매출액
    analysis_profit_list = vs_analysis_df.groupby('sim_cd').sum().sort_values(by="EST_HGA", ascending=False)[
        'EST_HGA'].to_list()
    # 해당 의원 코드들 리스트
    analysis_simcd_list = \
    vs_analysis_df.groupby('sim_cd').sum().sort_values(by="EST_HGA", ascending=False).reset_index()['sim_cd'].to_list()
    # 해당 의원들 개수 리스트
    analysis_count_list = []

    # 앞선 리스트에서 코드 리스트 정렬 기준 적용해서 의원개수 구해오기
    for_count_df = vs_analysis_df.groupby('sim_cd').count().reset_index()
    for i in range(len(analysis_simcd_list)):
        for j in range(len(for_count_df)):
            if analysis_simcd_list[i] == for_count_df['sim_cd'].to_list()[j]:
                analysis_count_list.append(for_count_df['index'].to_list()[j])

    print(analysis_profit_list)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # 의원별 평균 매출액 리스트
    analysis_ppa_list = []
    analysis_ppa_1000_list = []
    for i in range(len(analysis_profit_list)):
        analysis_ppa_list.append(analysis_profit_list[i] / analysis_count_list[i])
        analysis_ppa_1000_list.append(round(analysis_profit_list[i] / analysis_count_list[i] / 10000))
    analysis_ppa_list.sort(reverse=True)
    analysis_ppa_1000_list.sort(reverse=True)
    print(analysis_ppa_list)
    # 점유율 리스트
    analysis_percent_list = []
    for i in range(len(analysis_profit_list)):
        analysis_percent_list.append(round(analysis_ppa_list[i] / sum(analysis_ppa_list) * 100))
    # 점유율 제곱 리스트
    analysis_psq_list = []
    for i in range(len(analysis_profit_list)):
        analysis_psq_list.append(round((analysis_percent_list[i] / 100) ** 2, 2))
    vs_newhos_name_holder = []
    vs_newhos_opendate_holder = []
    vs_newhos_area_holder = []
    vs_newhos_prof_holder = []
    vs_newhos_profit_holder = []
    # 탐색 중 개업일자가 최근 24개월 내라면 holder에 값들 넣기
    for i in range(len(analysis_simcd_list)):
        vs_newhos_opendate = hos_df[hos_df['심평원코드'] == analysis_simcd_list[i]]['개설일자'].to_list()[0]
        # 신규 의원 목록 가려내는 작업
        if vs_newhos_opendate > (datetime.today() - relativedelta(years=2)):
            vs_newhos_opendate_holder.append(vs_newhos_opendate.strftime("%Y년 %m월 %d일"))
            vs_newhos_name_holder.append(hos_df[hos_df['심평원코드'] == analysis_simcd_list[i]]['의원명'].to_list()[0])
            vs_newhos_area_holder.append(hos_df[hos_df['심평원코드'] == analysis_simcd_list[i]]['총면적(평)'].to_list()[0])
            vs_newhos_prof_holder.append(hos_df[hos_df['심평원코드'] == analysis_simcd_list[i]]['전문의수'].to_list()[0])
            vs_newhos_profit_holder.append(analysis_ppa_list[i])

    # 최근 개원 의원 데이터프레임화 시키기
    recent_open_hos_df = pd.DataFrame()
    recent_open_hos_df['개업일자'] = vs_newhos_opendate_holder
    recent_open_hos_df['상호명'] = vs_newhos_name_holder
    recent_open_hos_df['면적'] = vs_newhos_area_holder
    recent_open_hos_df['전문의'] = vs_newhos_prof_holder
    recent_open_hos_df = recent_open_hos_df.sort_values(by="개업일자", ascending=False).reset_index()

    # 점유율 제곱 평균지표
    percent_squared = sum(analysis_psq_list)
    if percent_squared < 0.15:
        percent_quali = "치열함"
    elif (percent_squared >= 0.15) and (percent_squared < 0.25):
        percent_quali = "균형적"
    else:
        percent_quali = "독과점"

    if np.mean(analysis_ppa_list) < np.mean(vs_newhos_profit_holder):
        vs_quali = "높습니다"
    else:
        vs_quali = "낮습니다"

    # 폐업 의원 확인
    clh_df = pd.DataFrame()
    if (user_input_type == "일반의원"):
        closed_hos_df = closed_hos_df[closed_hos_df['진료과분류'].str.contains(norms_str)]
    elif (user_input_type == "가정의학과"):
        closed_hos_df = closed_hos_df[closed_hos_df['진료과분류'].str.contains(coughs_str_1)]
    elif (user_input_type == "내과") | (user_input_type == "소아청소년과") | (user_input_type == "이비인후과"):
        closed_hos_df = closed_hos_df[closed_hos_df['진료과분류'].str.contains(coughs_str_2)]
    elif (user_input_type == "마취통증의학과") | (user_input_type == "재활의학과") | (user_input_type == "정형외과") | (
            user_input_type == "신경외과"):
        closed_hos_df = closed_hos_df[closed_hos_df['진료과분류'].str.contains(bones_str)]
    elif (user_input_type == "신경과") | (user_input_type == "정신건강의학과"):
        closed_hos_df = closed_hos_df[closed_hos_df['진료과분류'].str.contains(mentals_str)]
    elif (user_input_type == "병리과") | (user_input_type == "진단검사의학과"):
        closed_hos_df = closed_hos_df[closed_hos_df['진료과분류'].str.contains(exs_str)]
    elif (user_input_type == "결핵과"):
        closed_hos_df = closed_hos_df[closed_hos_df['진료과분류'].str.contains(tubers_str)]
    elif (user_input_type == "흉부외과"):
        closed_hos_df = closed_hos_df[closed_hos_df['진료과분류'].str.contains(chests_str)]
        closed_hos_df = closed_hos_df[closed_hos_df['진료과분류'].str.contains(nochests_str) == False]
    clh_closed_date = closed_hos_df['폐업일자'].to_list()
    clh_opendate_holder = []
    clh_closedate_holder = []
    clh_hosname_holder = []
    clh_area_holder = []
    for i in range(len(clh_closed_date)):
        if (clh_closed_date[i] > (datetime.today() - relativedelta(years=2))) and (
                closed_hos_df['행정동코드'].to_list()[i] == user_input_loc):
            clh_opendate_holder.append(closed_hos_df['인허가일자'].to_list()[i].strftime("%Y년 %m월 %d일"))
            clh_closedate_holder.append(closed_hos_df['폐업일자'].to_list()[i].strftime("%Y년 %m월 %d일"))
            clh_hosname_holder.append(closed_hos_df['사업장명'].to_list()[i])
            clh_area_holder.append(round(closed_hos_df['총면적(평)'].to_list()[i]))
    clh_df['개업일자'] = clh_opendate_holder
    clh_df['폐업일자'] = clh_closedate_holder
    clh_df['상호명'] = clh_hosname_holder
    clh_df['면적(평)'] = clh_area_holder
    clh_df = clh_df.sort_values(by="폐업일자", ascending=False).reset_index()
    clh_df = clh_df.drop(labels="index", axis=1)

    # 경쟁 분석

    # Key Metric
    if len(vs_newhos_name_holder) == 0:
        new_average_ppm = ""
    else:
        new_average_ppm = round(np.mean(vs_newhos_profit_holder) / 10000)
        if new_average_ppm >= 10000:
            new_average_ppm = str(new_average_ppm // 10000) + "억 " + str(new_average_ppm % 10000)
    print("##############################################")
    print(analysis_ppa_list)
    # Text
    my_hdong_average_profit = round(sum(analysis_ppa_list) / len(analysis_ppa_list) / 10000)
    if my_hdong_average_profit >= 10000:
        my_hdong_average_profit = str(my_hdong_average_profit // 10000) + "억 " + str(my_hdong_average_profit % 10000)

    cc_holder = []
    for i in range(1, len(analysis_ppa_1000_list) + 1):
        cc_holder.append(str(i))

    vvs_df = pd.DataFrame()
    vvs1 = []
    vvs2 = []
    if len(analysis_ppa_1000_list) > 10:
        for i in range(len(analysis_ppa_1000_list[:10])):
            if analysis_ppa_1000_list[:10][i] > 10000:
                vvs1.append(str(int(analysis_ppa_1000_list[:10][i] // 10000)) + "억 " + str(
                    round(analysis_ppa_1000_list[:10][i] % 10000, 1)) + "만원")
            else:
                vvs1.append(str(analysis_ppa_1000_list[:10][i]) + "만원")
            vvs2.append(str(analysis_percent_list[:10][i]) + "%")
        vvs_df['매출액'] = vvs1[:10]
        vvs_df['점유율'] = vvs2[:10]
        vvs_df['점유율 제곱'] = analysis_psq_list[:10]
        vvs_df.loc[len(analysis_ppa_1000_list[:10])] = ['', '경쟁 지표 (점유율 제곱 합)', sum(analysis_psq_list[:10])]
    else:
        for i in range(len(analysis_ppa_1000_list)):
            if analysis_ppa_1000_list[i] > 10000:
                vvs1.append(str(int(analysis_ppa_1000_list[i] // 10000)) + "억 " + str(
                    round(analysis_ppa_1000_list[i] % 10000, 1)) + "만원")
            else:
                vvs1.append(str(analysis_ppa_1000_list[i]) + "만원")
            vvs2.append(str(analysis_percent_list[i]) + "%")
        vvs_df['매출액'] = vvs1
        vvs_df['점유율'] = vvs2
        vvs_df['점유율 제곱'] = analysis_psq_list
        vvs_df.loc[len(analysis_ppa_1000_list)] = ['', '경쟁 지표 (점유율 제곱 합)', sum(analysis_psq_list)]

    competitive_analysis = {
        "all_hospital_average_profit": str(round(np.mean(analysis_ppa_list) / 10000)) + "만원",
        "new_hospital_average_profit": str(new_average_ppm) + "만원",
        "competition_type": percent_quali,
        "competition_rate": round(sum(analysis_psq_list), 2),
        "address_dong": user_input_loc_p1,
        "department": user_input_type,
        "new_hospital_count": str(len(vs_newhos_opendate_holder)) + "개",
        "all_to_new_compare": vs_quali,
        "competition_table": [
        ],
        "new_hospital_table": [
        ],
        "closed_hospital_table": [
        ]
    }

    if new_average_ppm == "":
        competitive_analysis['new_hospital_average_profit'] = ""

    if len(vs_newhos_opendate_holder) == 0:
        competitive_analysis['new_hospital_count'] = ""

    if len(cc_holder) > 10:
        limit_cc_holder = cc_holder[:10]
        for i in range(len(limit_cc_holder)):
            this_competition = {}
            this_competition['profit'] = vvs1[i]
            this_competition['acquisition_rate'] = vvs2[i]
            this_competition['rate_squared'] = analysis_psq_list[i]
            competitive_analysis['competition_table'].append(this_competition)
    else:
        for i in range(len(cc_holder)):
            this_competition = {}
            this_competition['profit'] = vvs1[i]
            this_competition['acquisition_rate'] = vvs2[i]
            this_competition['rate_squared'] = analysis_psq_list[i]
            competitive_analysis['competition_table'].append(this_competition)

    for j in range(len(recent_open_hos_df)):
        this_new_hospital = {}
        this_new_hospital['open_date'] = recent_open_hos_df['개업일자'][j]
        this_new_hospital['hospital_name'] = recent_open_hos_df['상호명'][j]
        this_new_hospital['area'] = str(recent_open_hos_df['면적'][j]) + "평"
        this_new_hospital['prof'] = recent_open_hos_df['전문의'][j]
        competitive_analysis['new_hospital_table'].append(this_new_hospital)

    for k in range(len(clh_df)):
        this_closed_hospital = {}
        this_closed_hospital['open_date'] = clh_df['개업일자'][k]
        this_closed_hospital['closed_date'] = clh_df['폐업일자'][k]
        this_closed_hospital['hospital_name'] = clh_df['상호명'][k]
        this_closed_hospital['area'] = str(clh_df['면적(평)'][k]) + "평"
        competitive_analysis['closed_hospital_table'].append(this_closed_hospital)

    # # 4. 고객 분석

    # In[79]:

    # 주요 고객 성연령
    # 주요 고객 소득수준
    # 평균 객단가

    # 여기서의 주요 지표들은 모두 객단가를 사용
    # 우선, (추정건수 * 비율 / 100 * 평균건단가) 에 해당하는 지표 만들어서 붙이기

    # 추정건수
    est_cnt = market_df[market_df['TA_YM'] >= my_date]['EST_CNT'].to_list()
    # 평균건단가
    avg_amt = market_df[market_df['TA_YM'] >= my_date]['AVG_AMT'].to_list()
    # 성별 비중 정리
    f20_list = market_df[market_df['TA_YM'] >= my_date]['F20_RT'].to_list()
    f30_list = market_df[market_df['TA_YM'] >= my_date]['F30_RT'].to_list()
    f40_list = market_df[market_df['TA_YM'] >= my_date]['F40_RT'].to_list()
    f50_list = market_df[market_df['TA_YM'] >= my_date]['F50_RT'].to_list()
    f60_list = market_df[market_df['TA_YM'] >= my_date]['F60_RT'].to_list()
    m20_list = market_df[market_df['TA_YM'] >= my_date]['M20_RT'].to_list()
    m30_list = market_df[market_df['TA_YM'] >= my_date]['M30_RT'].to_list()
    m40_list = market_df[market_df['TA_YM'] >= my_date]['M40_RT'].to_list()
    m50_list = market_df[market_df['TA_YM'] >= my_date]['M50_RT'].to_list()
    m60_list = market_df[market_df['TA_YM'] >= my_date]['M60_RT'].to_list()
    ic0000_list = market_df[market_df['TA_YM'] >= my_date]['IC_0000_RT'].to_list()
    ic0002_list = market_df[market_df['TA_YM'] >= my_date]['IC_0002_RT'].to_list()
    ic0203_list = market_df[market_df['TA_YM'] >= my_date]['IC_0203_RT'].to_list()
    ic0304_list = market_df[market_df['TA_YM'] >= my_date]['IC_0304_RT'].to_list()
    ic0406_list = market_df[market_df['TA_YM'] >= my_date]['IC_0406_RT'].to_list()
    ic0608_list = market_df[market_df['TA_YM'] >= my_date]['IC_0608_RT'].to_list()
    ic0810_list = market_df[market_df['TA_YM'] >= my_date]['IC_0810_RT'].to_list()
    ic1099_list = market_df[market_df['TA_YM'] >= my_date]['IC_1099_RT'].to_list()

    amt_f20_holder = []
    amt_f30_holder = []
    amt_f40_holder = []
    amt_f50_holder = []
    amt_f60_holder = []
    amt_m20_holder = []
    amt_m30_holder = []
    amt_m40_holder = []
    amt_m50_holder = []
    amt_m60_holder = []
    amt_ic0000_holder = []
    amt_ic0002_holder = []
    amt_ic0203_holder = []
    amt_ic0304_holder = []
    amt_ic0406_holder = []
    amt_ic0608_holder = []
    amt_ic0810_holder = []
    amt_ic1099_holder = []
    for i in range(len(est_cnt)):
        amt_f20_holder.append(est_cnt[i] * f20_list[i] / 100 * avg_amt[i])
        amt_f30_holder.append(est_cnt[i] * f30_list[i] / 100 * avg_amt[i])
        amt_f40_holder.append(est_cnt[i] * f40_list[i] / 100 * avg_amt[i])
        amt_f50_holder.append(est_cnt[i] * f50_list[i] / 100 * avg_amt[i])
        amt_f60_holder.append(est_cnt[i] * f60_list[i] / 100 * avg_amt[i])
        amt_m20_holder.append(est_cnt[i] * m20_list[i] / 100 * avg_amt[i])
        amt_m30_holder.append(est_cnt[i] * m30_list[i] / 100 * avg_amt[i])
        amt_m40_holder.append(est_cnt[i] * m40_list[i] / 100 * avg_amt[i])
        amt_m50_holder.append(est_cnt[i] * m50_list[i] / 100 * avg_amt[i])
        amt_m60_holder.append(est_cnt[i] * m60_list[i] / 100 * avg_amt[i])
        amt_ic0000_holder.append(est_cnt[i] * ic0000_list[i] / 100 * avg_amt[i])
        amt_ic0002_holder.append(est_cnt[i] * ic0002_list[i] / 100 * avg_amt[i])
        amt_ic0203_holder.append(est_cnt[i] * ic0203_list[i] / 100 * avg_amt[i])
        amt_ic0304_holder.append(est_cnt[i] * ic0304_list[i] / 100 * avg_amt[i])
        amt_ic0406_holder.append(est_cnt[i] * ic0406_list[i] / 100 * avg_amt[i])
        amt_ic0608_holder.append(est_cnt[i] * ic0608_list[i] / 100 * avg_amt[i])
        amt_ic0810_holder.append(est_cnt[i] * ic0810_list[i] / 100 * avg_amt[i])
        amt_ic1099_holder.append(est_cnt[i] * ic1099_list[i] / 100 * avg_amt[i])

    fm_sum_holder = []
    f_sum_holder = []
    m_sum_holder = []
    ic_sum_holder = []
    fm_sum_holder.extend(
        [sum(amt_f20_holder), sum(amt_f30_holder), sum(amt_f40_holder), sum(amt_f50_holder), sum(amt_f60_holder),
         sum(amt_m20_holder), sum(amt_m30_holder), sum(amt_m40_holder), sum(amt_m50_holder), sum(amt_m60_holder)])
    f_sum_holder.extend(
        [sum(amt_f20_holder), sum(amt_f30_holder), sum(amt_f40_holder), sum(amt_f50_holder), sum(amt_f60_holder)])
    m_sum_holder.extend(
        [sum(amt_m20_holder), sum(amt_m30_holder), sum(amt_m40_holder), sum(amt_m50_holder), sum(amt_m60_holder)])
    ic_sum_holder.extend(
        [sum(amt_ic0000_holder), sum(amt_ic0002_holder), sum(amt_ic0203_holder), sum(amt_ic0304_holder),
         sum(amt_ic0406_holder), sum(amt_ic0608_holder), sum(amt_ic0810_holder), sum(amt_ic1099_holder)])

    fm_ident = fm_sum_holder.index(max(fm_sum_holder))
    if fm_ident == 0:
        fm_ident = "20대 여성"
    elif fm_ident == 1:
        fm_ident = "30대 여성"
    elif fm_ident == 2:
        fm_ident = "40대 여성"
    elif fm_ident == 3:
        fm_ident = "50대 여성"
    elif fm_ident == 4:
        fm_ident = "60대 이상 여성"
    elif fm_ident == 5:
        fm_ident = "20대 남성"
    elif fm_ident == 6:
        fm_ident = "30대 남성"
    elif fm_ident == 7:
        fm_ident = "40대 남성"
    elif fm_ident == 8:
        fm_ident = "50대 남성"
    else:
        fm_ident = "60대 이상 남성"

    # 성별 분포
    m_percent = round(sum(m_sum_holder) / sum(fm_sum_holder) * 100)
    f_percent = round(sum(f_sum_holder) / sum(fm_sum_holder) * 100)
    if m_percent > f_percent:
        fm_percent_ident = "남성"
    else:
        fm_percent_ident = "여성"

    # 남성 연령 분포
    m_ident = m_sum_holder.index(max(m_sum_holder))
    mm_percent = round(m_sum_holder[m_ident] / sum(m_sum_holder) * 100)
    if m_ident == 0:
        m_ident = "20대"
    elif m_ident == 1:
        m_ident = "30대"
    elif m_ident == 2:
        m_ident = "40대"
    elif m_ident == 3:
        m_ident = "50대"
    else:
        m_ident = "60대 이상"

    # 여성 연령 분포
    f_ident = f_sum_holder.index(max(f_sum_holder))
    ff_percent = round(f_sum_holder[f_ident] / sum(f_sum_holder) * 100)
    if f_ident == 0:
        f_ident = "20대"
    elif f_ident == 1:
        f_ident = "30대"
    elif f_ident == 2:
        f_ident = "40대"
    elif f_ident == 3:
        f_ident = "50대"
    else:
        f_ident = "60대 이상"

    # 소득 수준별 분포
    ic_ident = ic_sum_holder.index(max(ic_sum_holder))
    ic_percent = round(ic_sum_holder[ic_ident] / sum(ic_sum_holder) * 100)
    if ic_ident == 0:
        ic_ident = "정보 없음"
    elif ic_ident == 1:
        ic_ident = "2천만원 미만"
    elif ic_ident == 2:
        ic_ident = "2천~3천만원"
    elif ic_ident == 3:
        ic_ident = "3천~4천만원"
    elif ic_ident == 4:
        ic_ident = "4천~6천만원"
    elif ic_ident == 5:
        ic_ident = "6천~8천만원"
    elif ic_ident == 6:
        ic_ident = "8천만~1억원"
    else:
        ic_ident = "1억원 이상"

    # 객단가 단기 추세
    amt_short_year = market_df[market_df['TA_YM'] >= my_date].groupby("TA_YM").sum().reset_index()['TA_YM'].to_list()
    my_avg_amt_short = ((market_df[market_df['TA_YM'] >= my_date].groupby("TA_YM").sum())['EST_HGA'] /
                        (market_df[market_df['TA_YM'] >= my_date].groupby("TA_YM").sum())['EST_CNT']).to_list()

    # 객단가 장기 추세
    maal_df = market_df[market_df['year'] >= my_year - 2].groupby('TA_YM').sum().reset_index()
    maal_df['year'] = maal_df['TA_YM'] // 100
    maal_df['maal'] = maal_df['EST_HGA'] / maal_df['EST_CNT']
    amt_long_year = maal_df.groupby('year').mean().reset_index()['year'].to_list()
    my_avg_amt_long = maal_df.groupby('year').mean()['maal'].to_list()

    if my_avg_amt_long[0] > my_avg_amt_long[-1]:
        maal_ident = "감소"
    else:
        maal_ident = "증가"

    # 4. 고객 분석
    this_short_amt = round(np.mean(my_avg_amt_short))
    if this_short_amt >= 10000:
        this_short_amt = str(this_short_amt // 10000) + "만 " + str(this_short_amt % 10000)

    this_max_amt = round(max(my_avg_amt_short))
    if this_max_amt >= 10000:
        this_max_amt = str(this_max_amt // 10000) + "만 " + str(this_max_amt % 10000)
    this_min_amt = round(min(my_avg_amt_short))
    if this_min_amt >= 10000:
        this_min_amt = str(this_min_amt // 10000) + "만 " + str(this_min_amt % 10000)

    this_3y_first_amt = round(my_avg_amt_long[0])
    if this_3y_first_amt >= 10000:
        this_3y_first_amt = str(this_3y_first_amt // 10000) + "만 " + str(this_3y_first_amt % 10000)
    this_3y_last_amt = round(my_avg_amt_long[-1])
    if this_3y_last_amt >= 10000:
        this_3y_last_amt = str(this_3y_last_amt // 10000) + "만 " + str(this_3y_last_amt & 10000)
    this_3y_percent = round((round(my_avg_amt_long[-1]) - round(my_avg_amt_long[0])) / round(my_avg_amt_long[0]) * 100)


    # JSON 출력을 위한 user_analysis 딕셔너리 홀더에 담기
    user_analysis = {
        "major_customer_age_sex": fm_ident,
        "major_customer_profit": ic_ident,
        "major_customer_profit_ratio": str(ic_percent) + "%",
        "average_profit_per_customer": str(this_short_amt) + "원",
        "address_dong": user_input_loc_p1,
        "department": user_input_type,
        "customer_male_ratio": m_percent,
        "customer_female_ratio": f_percent,
        "sex_compare": fm_percent_ident,
        "male_max_count_age": m_ident,
        "male_max_count_ratio": mm_percent,
        "female_max_count_age": f_ident,
        "female_max_count_ratio": ff_percent,
        "max_average_profit_per_customer": str(this_max_amt) + "원",
        "max_average_profit_per_customer_year": str(
            amt_short_year[my_avg_amt_short.index(max(my_avg_amt_short))] // 100) + "년",
        "max_average_profit_per_customer_month": str(
            amt_short_year[my_avg_amt_short.index(max(my_avg_amt_short))] % 100) + "월",
        "min_average_profit_per_customer": str(this_min_amt) + "원",
        "min_average_profit_per_customer_year": str(
            amt_short_year[my_avg_amt_short.index(min(my_avg_amt_short))] // 100) + "년",
        "min_average_profit_per_customer_month": str(
            amt_short_year[my_avg_amt_short.index(min(my_avg_amt_short))] % 100) + "월",
        "3year_trend_early_size": str(this_3y_first_amt) + "원",
        "3year_trend_late_size": str(this_3y_last_amt) + "원",
        "3year_trend_percent": str(abs(this_3y_percent)) + "%",
        "3year_trend_compare": maal_ident,
        "male_age_ratio": {
            "20s": str(round([m_sum_holder[i] / sum(m_sum_holder) for i in range(len(m_sum_holder))][0] * 100)) + "%",
            "30s": str(round([m_sum_holder[i] / sum(m_sum_holder) for i in range(len(m_sum_holder))][1] * 100)) + "%",
            "40s": str(round([m_sum_holder[i] / sum(m_sum_holder) for i in range(len(m_sum_holder))][2] * 100)) + "%",
            "50s": str(round([m_sum_holder[i] / sum(m_sum_holder) for i in range(len(m_sum_holder))][3] * 100)) + "%",
            "60s_up": str(round([m_sum_holder[i] / sum(m_sum_holder) for i in range(len(m_sum_holder))][4] * 100)) + "%"
        },
        "female_age_ratio": {
            "20s": str(round([f_sum_holder[i] / sum(f_sum_holder) for i in range(len(f_sum_holder))][0] * 100)) + "%",
            "30s": str(round([f_sum_holder[i] / sum(f_sum_holder) for i in range(len(f_sum_holder))][1] * 100)) + "%",
            "40s": str(round([f_sum_holder[i] / sum(f_sum_holder) for i in range(len(f_sum_holder))][2] * 100)) + "%",
            "50s": str(round([f_sum_holder[i] / sum(f_sum_holder) for i in range(len(f_sum_holder))][3] * 100)) + "%",
            "60s_up": str(round([f_sum_holder[i] / sum(f_sum_holder) for i in range(len(f_sum_holder))][4] * 100)) + "%"
        },
        "customer_profit_ratio": {
            "no_data": str(
                round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][0] * 100)) + "%",
            "2000_down": str(
                round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][1] * 100)) + "%",
            "2000_to_3000": str(
                round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][2] * 100)) + "%",
            "3000_to_4000": str(
                round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][3] * 100)) + "%",
            "4000_to_6000": str(
                round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][4] * 100)) + "%",
            "6000_to_8000": str(
                round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][5] * 100)) + "%",
            "8000_to_10000": str(
                round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][6] * 100)) + "%",
            "10000_up": str(
                round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][7] * 100)) + "%"
        },
        "average_profit_per_customer_12m_chart": {
        },
        "average_profit_per_customer_3y_chart": {
        }
    }

    for i in range(len(tt_holder)):
        user_analysis['average_profit_per_customer_12m_chart']['profit_{}m'.format(i + 1)] = round(my_avg_amt_short[i])
    for j in range(len(my_avg_amt_long)):
        user_analysis['average_profit_per_customer_3y_chart']['year_{}'.format(j + 1)] = round(my_avg_amt_long[j])

    # JSON 형식 통합 결과물 내기
    result = {
        "intro": intro,
        "market_analysis": market_analysis,
        "competitive_analysis": competitive_analysis,
        "user_analysis": user_analysis
    }

    # In[80]:

    return result