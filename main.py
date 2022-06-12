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
    return {
        "intro": {
            "department": "치과",
            "department_group": "치",
            "address_dong": "신사동",
            "address_sido_sigungu": "서울특별시 강남구",
            "address_realated_dongs": "신사동, 압구정동",
            "hospital_count": 53,
            "big_hospital_count": 0,
            "big_hospital_departments": "",
            "sales_reflection": "58%",
            "hospital_table": [
                {
                    "name": "드림치과교정과치과의원",
                    "department": "치과",
                    "open_year": 2021,
                    "area": "23평",
                    "prof": "치과교정과 1명"
                },
                {
                    "name": "플란치과의원",
                    "department": "치과",
                    "open_year": 2021,
                    "area": "424평",
                    "prof": "구강악안면외과 2명, 예방치과 1명, 치과보철과 2명, 치주과 1명, 통합치의학과 6명"
                },
                {
                    "name": "이안맨하튼치과의원",
                    "department": "치과",
                    "open_year": 2018,
                    "area": "69평",
                    "prof": "-"
                },
                {
                    "name": "켈리치과의원",
                    "department": "치과",
                    "open_year": 2018,
                    "area": "44평",
                    "prof": "-"
                },
                {
                    "name": "그린몰치과의원",
                    "department": "치과",
                    "open_year": 2017,
                    "area": "32평",
                    "prof": "-"
                },
                {
                    "name": "뉴라인치과의원",
                    "department": "치과",
                    "open_year": 2016,
                    "area": "44평",
                    "prof": "-"
                },
                {
                    "name": "서울원치과의원",
                    "department": "치과",
                    "open_year": 2016,
                    "area": "19평",
                    "prof": "-"
                },
                {
                    "name": "김앤김치과의원",
                    "department": "치과",
                    "open_year": 2015,
                    "area": "26평",
                    "prof": "-"
                },
                {
                    "name": "오세홍치과의원",
                    "department": "치과",
                    "open_year": 2015,
                    "area": "30평",
                    "prof": "-"
                },
                {
                    "name": "줌구강악안면외과치과의원",
                    "department": "치과",
                    "open_year": 2014,
                    "area": "53평",
                    "prof": "구강악안면외과 1명"
                },
                {
                    "name": "매직키스치과의원",
                    "department": "치과",
                    "open_year": 2014,
                    "area": "44평",
                    "prof": "-"
                },
                {
                    "name": "바른웅치과의원",
                    "department": "치과",
                    "open_year": 2013,
                    "area": "29평",
                    "prof": "-"
                },
                {
                    "name": "압구정현치과의원",
                    "department": "치과",
                    "open_year": 2013,
                    "area": "23평",
                    "prof": "-"
                },
                {
                    "name": "드림치과의원",
                    "department": "치과",
                    "open_year": 2012,
                    "area": "37평",
                    "prof": "-"
                },
                {
                    "name": "이다듬치과의원",
                    "department": "치과",
                    "open_year": 2011,
                    "area": "29평",
                    "prof": "-"
                },
                {
                    "name": "유씨서울치과교정과치과의원",
                    "department": "치과",
                    "open_year": 2010,
                    "area": "53평",
                    "prof": "치과교정과 1명"
                },
                {
                    "name": "와이케이콜럼비아치과의원",
                    "department": "치과",
                    "open_year": 2010,
                    "area": "63평",
                    "prof": "-"
                },
                {
                    "name": "디아트치과의원",
                    "department": "치과",
                    "open_year": 2008,
                    "area": "33평",
                    "prof": "-"
                },
                {
                    "name": "후즈후치과의원",
                    "department": "치과",
                    "open_year": 2008,
                    "area": "53평",
                    "prof": "-"
                },
                {
                    "name": "아너스치과교정과치과의원",
                    "department": "치과",
                    "open_year": 2007,
                    "area": "36평",
                    "prof": "치과교정과 1명"
                },
                {
                    "name": "유앤아이아덴스치과의원",
                    "department": "치과",
                    "open_year": 2006,
                    "area": "36평",
                    "prof": "-"
                },
                {
                    "name": "세인트루이스치과의원",
                    "department": "치과",
                    "open_year": 2006,
                    "area": "44평",
                    "prof": "-"
                },
                {
                    "name": "압구정현대부부치과의원",
                    "department": "치과",
                    "open_year": 2006,
                    "area": "30평",
                    "prof": "-"
                },
                {
                    "name": "오성진치과의원",
                    "department": "치과",
                    "open_year": 2006,
                    "area": "28평",
                    "prof": "-"
                },
                {
                    "name": "압구정연치과의원",
                    "department": "치과",
                    "open_year": 2006,
                    "area": "66평",
                    "prof": "-"
                },
                {
                    "name": "미드미치과의원",
                    "department": "치과",
                    "open_year": 2006,
                    "area": "62평",
                    "prof": "치과교정과 1명"
                },
                {
                    "name": "바롬치과의원",
                    "department": "치과",
                    "open_year": 2006,
                    "area": "97평",
                    "prof": "-"
                },
                {
                    "name": "제이엠치과의원",
                    "department": "치과",
                    "open_year": 2005,
                    "area": "25평",
                    "prof": "-"
                },
                {
                    "name": "테라스치과의원",
                    "department": "치과",
                    "open_year": 2005,
                    "area": "74평",
                    "prof": "-"
                },
                {
                    "name": "비너스치과의원",
                    "department": "치과",
                    "open_year": 2003,
                    "area": "25평",
                    "prof": "-"
                },
                {
                    "name": "장종언치과의원",
                    "department": "치과",
                    "open_year": 2002,
                    "area": "40평",
                    "prof": "-"
                },
                {
                    "name": "압구정예치과의원",
                    "department": "치과",
                    "open_year": 2002,
                    "area": "64평",
                    "prof": "-"
                },
                {
                    "name": "유앤아이치과의원",
                    "department": "치과",
                    "open_year": 2002,
                    "area": "55평",
                    "prof": "-"
                },
                {
                    "name": "연치과의원",
                    "department": "치과",
                    "open_year": 2002,
                    "area": "84평",
                    "prof": "치과교정과 1명"
                },
                {
                    "name": "하루에치과의원",
                    "department": "치과",
                    "open_year": 2002,
                    "area": "122평",
                    "prof": "-"
                },
                {
                    "name": "압구정웰치과의원",
                    "department": "치과",
                    "open_year": 2001,
                    "area": "37평",
                    "prof": "-"
                },
                {
                    "name": "이와이치과의원",
                    "department": "치과",
                    "open_year": 2000,
                    "area": "49평",
                    "prof": "-"
                },
                {
                    "name": "노영서치과의원",
                    "department": "치과",
                    "open_year": 2000,
                    "area": "20평",
                    "prof": "-"
                },
                {
                    "name": "강우진치과의원",
                    "department": "치과",
                    "open_year": 2000,
                    "area": "43평",
                    "prof": "-"
                },
                {
                    "name": "이스트만치과의원",
                    "department": "치과",
                    "open_year": 1998,
                    "area": "87평",
                    "prof": "치과교정과 1명"
                },
                {
                    "name": "홍수진어린이치과의원",
                    "department": "치과",
                    "open_year": 1997,
                    "area": "31평",
                    "prof": "-"
                },
                {
                    "name": "아이비라인치과의원",
                    "department": "치과",
                    "open_year": 1995,
                    "area": "48평",
                    "prof": "치과교정과 1명"
                },
                {
                    "name": "홍정욱치과의원",
                    "department": "치과",
                    "open_year": 1994,
                    "area": "25평",
                    "prof": "-"
                },
                {
                    "name": "에스앤케이치과의원",
                    "department": "치과",
                    "open_year": 1994,
                    "area": "45평",
                    "prof": "-"
                },
                {
                    "name": "영철이치과의원",
                    "department": "치과",
                    "open_year": 1993,
                    "area": "24평",
                    "prof": "-"
                },
                {
                    "name": "리즈윤정아치과의원",
                    "department": "치과",
                    "open_year": 1992,
                    "area": "26평",
                    "prof": "-"
                },
                {
                    "name": "오렌지치과의원",
                    "department": "치과",
                    "open_year": 1992,
                    "area": "29평",
                    "prof": "-"
                },
                {
                    "name": "백치과의원",
                    "department": "치과",
                    "open_year": 1991,
                    "area": "53평",
                    "prof": "-"
                },
                {
                    "name": "이근국치과의원",
                    "department": "치과",
                    "open_year": 1987,
                    "area": "6평",
                    "prof": "-"
                },
                {
                    "name": "김승기치과의원",
                    "department": "치과",
                    "open_year": 1986,
                    "area": "3평",
                    "prof": "-"
                },
                {
                    "name": "김철호치과의원",
                    "department": "치과",
                    "open_year": 1983,
                    "area": "4평",
                    "prof": "-"
                },
                {
                    "name": "김계용치과의원",
                    "department": "치과",
                    "open_year": 1982,
                    "area": "4평",
                    "prof": "-"
                },
                {
                    "name": "성심치과의원",
                    "department": "치과",
                    "open_year": 1982,
                    "area": "6평",
                    "prof": "-"
                }
            ],
            "big_hospital_table": [

            ]
        },
        "market_analysis": {
            "market_size": "33억 9854만 원",
            "market_trend": "증가",
            "hospital_count": "53개",
            "hospital_count_trend": "감소",
            "profit_per_area_size": "115만 원",
            "profit_per_area_trend": "감소",
            "address_dong": "신사동",
            "department": "치과",
            "market_max_size": "45억 9362만 원",
            "market_max_year": "2022년",
            "market_max_month": "3월",
            "market_min_size": "22억 2153만 원",
            "market_min_year": "2021년",
            "market_min_month": "8월",
            "3y_trend_start_year": "2020년",
            "3y_trend_start_market_size": "24억 0만 원",
            "3y_trend_end_year": "2022년",
            "3y_trend_end_market_size": "42억 2146만 원",
            "3y_trend_percent": "76%",
            "3y_trend_hospital_count_difference": "1개",
            "profit_per_50p": "5750만 원",
            "3y_trend_profit_per_area_start_year": "2020년",
            "3y_trend_profit_per_area_start_market_size": "122만 원",
            "3y_trend_profit_per_area_end_year": "2022년",
            "3y_trend_profit_per_area_end_market_size": "116만 원",
            "3y_trend_profit_per_area_percent": "5%",
            "12m_trend_chart": {
                "market_size_1m": 264021,
                "market_size_2m": 258839,
                "market_size_3m": 222153,
                "market_size_4m": 255289,
                "market_size_5m": 303756,
                "market_size_6m": 352870,
                "market_size_7m": 392885,
                "market_size_8m": 392798,
                "market_size_9m": 414485,
                "market_size_10m": 459362,
                "market_size_11m": 421939,
                "profit_per_area_size_1m": 120,
                "profit_per_area_size_2m": 115,
                "profit_per_area_size_3m": 93,
                "profit_per_area_size_4m": 111,
                "profit_per_area_size_5m": 101,
                "profit_per_area_size_6m": 124,
                "profit_per_area_size_7m": 138,
                "profit_per_area_size_8m": 126,
                "profit_per_area_size_9m": 112,
                "profit_per_area_size_10m": 107,
                "profit_per_area_size_11m": 120
            },
            "hospital_count_chart": {
                "2021_2": 54,
                "2021_3": 55,
                "2021_4": 55,
                "2022_1": 53
            },
            "3y_trend_chart": {
                "market_size_year_1": 240000,
                "market_size_year_2": 273347,
                "market_size_year_3": 422146,
                "profit_per_area_year_1": 122,
                "profit_per_area_year_2": 116,
                "profit_per_area_year_3": 116
            }
        },
        "competitive_analysis": {
            "all_hospital_average_profit": "6661만 원",
            "new_hospital_average_profit": "5억 3320만 원",
            "competition_type": "치열함",
            "competition_rate": 0.11,
            "address_dong": "신사동",
            "department": "치과",
            "new_hospital_count": "2개",
            "all_to_new_compare": "높습니다",
            "competition_table": [
                {
                    "profit": "10억 4303만 원",
                    "acquisition_rate": "30%",
                    "rate_squared": 0.09
                },
                {
                    "profit": "4억 5768만 원",
                    "acquisition_rate": "13%",
                    "rate_squared": 0.02
                },
                {
                    "profit": "2억 557만 원",
                    "acquisition_rate": "6%",
                    "rate_squared": 0.0
                },
                {
                    "profit": "1억 7216만 원",
                    "acquisition_rate": "5%",
                    "rate_squared": 0.0
                },
                {
                    "profit": "1억 6450만 원",
                    "acquisition_rate": "5%",
                    "rate_squared": 0.0
                },
                {
                    "profit": "1억 814만 원",
                    "acquisition_rate": "3%",
                    "rate_squared": 0.0
                },
                {
                    "profit": "8208만 원",
                    "acquisition_rate": "2%",
                    "rate_squared": 0.0
                },
                {
                    "profit": "6708만 원",
                    "acquisition_rate": "2%",
                    "rate_squared": 0.0
                },
                {
                    "profit": "6682만 원",
                    "acquisition_rate": "2%",
                    "rate_squared": 0.0
                },
                {
                    "profit": "6643만 원",
                    "acquisition_rate": "2%",
                    "rate_squared": 0.0
                }
            ],
            "new_hospital_table": [
                {
                    "open_date": "2021년 07월 23일",
                    "hospital_name": "드림치과교정과치과의원",
                    "area": "23.87272727272727평",
                    "prof": "치과교정과 1명"
                },
                {
                    "open_date": "2021년 06월 14일",
                    "hospital_name": "플란치과의원",
                    "area": "424.0909090909091평",
                    "prof": "구강악안면외과 2명, 예방치과 1명, 치과보철과 2명, 치주과 1명, 통합치의학과 6명"
                }
            ],
            "closed_hospital_table": [
                {
                    "open_date": "2019년 08월 07일",
                    "closed_date": "2021년 07월 14일",
                    "hospital_name": "네비플란트치과의원",
                    "area": "24평"
                },
                {
                    "open_date": "2017년 06월 02일",
                    "closed_date": "2021년 06월 02일",
                    "hospital_name": "클라인치과의원",
                    "area": "74평"
                },
                {
                    "open_date": "1988년 05월 13일",
                    "closed_date": "2020년 06월 29일",
                    "hospital_name": "금강치과의원",
                    "area": "27평"
                }
            ]
        },
        "user_analysis": {
            "major_customer_age_sex": "60대 이상 남성",
            "major_customer_profit": "4천~6천만 원",
            "average_profit_per_customer": "32만 7283원",
            "average_profit_per_customer_ratio": "39%",
            "address_dong": "신사동",
            "department": "치과",
            "customer_male_ratio": 49,
            "customer_female_ratio": 51,
            "sex_compare": "여성",
            "male_max_count_age": "60대 이상",
            "male_max_count_ratio": 30,
            "female_max_count_age": "40대",
            "female_max_count_ratio": 23,
            "max_average_profit_per_customer": "41만 5712원",
            "max_average_profit_per_customer_year": "2022년",
            "max_average_profit_per_customer_month": "3월",
            "min_average_profit_per_customer": "23만 545원",
            "min_average_profit_per_customer_year": "2021년",
            "min_average_profit_per_customer_month": "8월",
            "3year_trend_early_size": "25만 4803원",
            "3year_trend_late_size": "38만 9472원",
            "3year_trend_percent": "52%",
            "3year_trend_compare": "증가",
            "male_age_ratio": {
                "20s": "7%",
                "30s": "15%",
                "40s": "17%",
                "50s": "30%",
                "60s_up": "30%"
            },
            "female_age_ratio": {
                "20s": "15%",
                "30s": "19%",
                "40s": "23%",
                "50s": "23%",
                "60s_up": "19%"
            },
            "customer_profit_ratio": {
                "no_data": "2%",
                "2000_down": "1%",
                "2000_to_3000": "0%",
                "3000_to_4000": "15%",
                "4000_to_6000": "39%",
                "6000_to_8000": "19%",
                "8000_to_10000": "10%",
                "10000_up": "15%"
            },
            "average_profit_per_customer_12m_chart": {
                "profit_1m": 278063,
                "profit_2m": 264743,
                "profit_3m": 230545,
                "profit_4m": 281839,
                "profit_5m": 300006,
                "profit_6m": 330899,
                "profit_7m": 360213,
                "profit_8m": 374236,
                "profit_9m": 391873,
                "profit_10m": 415712,
                "profit_11m": 371982
            },
            "average_profit_per_customer_3y_chart": {
                "year_1": 254803,
                "year_2": 280094,
                "year_3": 388451
            }
        }
    }
