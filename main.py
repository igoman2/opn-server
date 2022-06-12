from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


@app.get("/analyze/", response_model=Report)
async def analyze(department: str, location: str):
    intro = {
        "department": '정형외과',
        "department_group": ['정형외과', '마취통증의학과', '재활의학과', '신경외과', '신경과'],
        "address_dong": '능곡동',
        "address_sido_sigungu": '경기도 시흥시',
        "address_realated_dongs": ['화정동', '능곡동', '광석동', '군자동', '장현동'],
        "hospital_count": 4,
        "big_hospital_count": 2,
        "big_hospital_departments": 2,
        "sales_reflection": '40%',
        "hospital_table": [
            {'name': '능곡늘푸른정형외과의원',
             'department': '정형외과',
             'open_year': 2009,
             'area': 39,
             'prof': '정형외과 외 1명'
             }
        ],
        "big_hospital_table": [
            {'name': '시흥서울대효요 양병원',
             'department': '요양병원',
             'open_year': 2020,
             'area': 1347,
             'prof': '내과 1명, 외과 1 명, 마취통증의학 과 1명, 재활의학 과 1명, 가정의학 과 1명'
             }
        ]
    }
    # market_analysis = {
    #     "market_size" : str(market_size_12m) + "만 원",
    #     "market_trend" : three_ident,
    #     "hospital_count" : str(hos_now_count) + "개",
    #     "hospital_count_trend" : count_tendency,
    #     "profit_per_area_size" : str(pp_short_cost) + "만 원",
    #     "profit_per_area_trend" : three_ident2,
    #     "address_dong" : user_input_loc_p1,
    #     "department" : user_input_type,
    #     "market_max_size" : str(max_msize) + "만 원",
    #     "market_max_year" : str(max_year) + "년",
    #     "market_max_month" : str(max_month) + "월",
    #     "market_min_size" : str(min_msize) + "만 원",
    #     "market_min_year" : str(min_year) + "년",
    #     "market_min_month" : str(min_month) + "월",
    #     "3y_trend_start_year" : str(early_year) + "년",
    #     "3y_trend_start_market_size" : str(early_size) + "만 원",
    #     "3y_trend_end_year" : str(late_year) + "년",
    #     "3y_trend_end_market_size" : str(late_size) + "만 원",
    #     "3y_trend_percent" : str(abs(three_percent)) + "%",
    #     "3y_trend_hospital_count_difference" : str(abs(hos_now_count - hos_2020_count)) + "개",
    #     "profit_per_50p" : str(pp_short_cost*50) + "만 원",
    #     "3y_trend_profit_per_area_start_year" : str(p_early_year) + "년",
    #     "3y_trend_profit_per_area_start_market_size" : str(p_early_size) + "만 원",
    #     "3y_trend_profit_per_area_end_year" : str(p_late_year) + "년",
    #     "3y_trend_profit_per_area_end_market_size" : str(p_late_size) + "만 원",
    #     "3y_trend_profit_per_area_percent" : str(abs(three_percent2)) + "%",
    #     "12m_trend_chart" : {
    #     },
    #     "hospital_count_chart" : {
    #     },
    #     "3y_trend_chart" : {
    #     }
    # }
    # competitive_analysis = {
    #     "all_hospital_average_profit" : str(round(np.mean(analysis_ppa_list)/ 10000)) + "만 원",
    #     "new_hospital_average_profit" : str(new_average_ppm) + "만 원",
    #     "competition_type" : percent_quali,
    #     "competition_rate" : round(sum(analysis_psq_list), 2),
    #     "address_dong" : user_input_loc_p1,
    #     "department" : user_input_type,
    #     "new_hospital_count" : str(len(vs_newhos_opendate_holder)) + "개",
    #     "all_to_new_compare" : vs_quali,
    #     "competition_table" : [
    #     ],
    #     "new_hospital_table" : [
    #     ],
    #     "closed_hospital_table" : [
    #     ]
    # }
    # user_analysis = {
    #     "major_customer_age_sex" : fm_ident,
    #     "major_customer_profit" : ic_ident,
    #     "average_profit_per_customer" : str(this_short_amt) + "원",
    #     "average_profit_per_customer_ratio" : str(ic_percent) + "%",
    #     "address_dong" : user_input_loc_p1,
    #     "department" : user_input_type,
    #     "customer_male_ratio" : m_percent,
    #     "customer_female_ratio" : f_percent,
    #     "sex_compare" : fm_percent_ident,
    #     "male_max_count_age" : m_ident,
    #     "male_max_count_ratio" : mm_percent,
    #     "female_max_count_age" : f_ident,
    #     "female_max_count_ratio" : ff_percent,
    #     "max_average_profit_per_customer" : str(this_max_amt) + "원",
    #     "max_average_profit_per_customer_year" : str(amt_short_year[my_avg_amt_short.index(max(my_avg_amt_short))]//100) + "년",
    #     "max_average_profit_per_customer_month" : str(amt_short_year[my_avg_amt_short.index(max(my_avg_amt_short))]%100) + "월",
    #     "min_average_profit_per_customer" : str(this_min_amt) + "원",
    #     "min_average_profit_per_customer_year" : str(amt_short_year[my_avg_amt_short.index(min(my_avg_amt_short))]//100) + "년",
    #     "min_average_profit_per_customer_month" : str(amt_short_year[my_avg_amt_short.index(min(my_avg_amt_short))]%100) + "월",
    #     "3year_trend_early_size" : str(this_3y_first_amt) + "원",
    #     "3year_trend_late_size" : str(this_3y_last_amt) + "원",
    #     "3year_trend_percent" : str(abs(this_3y_percent)) + "%",
    #     "3year_trend_compare" : maal_ident,
    #     "male_age_ratio" : {
    #         "20s" : str(round([m_sum_holder[i] / sum(m_sum_holder) for i in range(len(m_sum_holder))][0] * 100)) + "%",
    #         "30s" : str(round([m_sum_holder[i] / sum(m_sum_holder) for i in range(len(m_sum_holder))][1] * 100)) + "%",
    #         "40s" : str(round([m_sum_holder[i] / sum(m_sum_holder) for i in range(len(m_sum_holder))][2] * 100)) + "%",
    #         "50s" : str(round([m_sum_holder[i] / sum(m_sum_holder) for i in range(len(m_sum_holder))][3] * 100)) + "%",
    #         "60s_up" : str(round([m_sum_holder[i] / sum(m_sum_holder) for i in range(len(m_sum_holder))][4] * 100)) + "%"
    #     },
    #     "female_age_ratio" : {
    #         "20s" : str(round([f_sum_holder[i] / sum(f_sum_holder) for i in range(len(f_sum_holder))][0] * 100)) + "%",
    #         "30s" : str(round([f_sum_holder[i] / sum(f_sum_holder) for i in range(len(f_sum_holder))][1] * 100)) + "%",
    #         "40s" : str(round([f_sum_holder[i] / sum(f_sum_holder) for i in range(len(f_sum_holder))][2] * 100)) + "%",
    #         "50s" : str(round([f_sum_holder[i] / sum(f_sum_holder) for i in range(len(f_sum_holder))][3] * 100)) + "%",
    #         "60s_up" : str(round([f_sum_holder[i] / sum(f_sum_holder) for i in range(len(f_sum_holder))][4] * 100)) + "%"
    #     },
    #     "customer_profit_ratio" : {
    #         "no_data" : str(round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][0] * 100)) + "%",
    #         "2000_down" : str(round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][1] * 100)) + "%",
    #         "2000_to_3000" : str(round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][2] * 100)) + "%",
    #         "3000_to_4000" : str(round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][3] * 100)) + "%",
    #         "4000_to_6000" : str(round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][4] * 100)) + "%",
    #         "6000_to_8000" : str(round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][5] * 100)) + "%",
    #         "8000_to_10000" : str(round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][6] * 100)) + "%",
    #         "10000_up" : str(round([ic_sum_holder[i] / sum(ic_sum_holder) for i in range(len(ic_sum_holder))][7] * 100)) + "%"
    #     },
    #     "average_profit_per_customer_12m_chart" : {
    #     },
    #     "average_profit_per_customer_3y_chart" : {
    #     }
    # }
    return  {
        "intro": intro,
        "market_analysis": "market_analysis",
        "competitive_analysis": "competitive_analysis",
        "user_analysis": "user_analysis"
    }
