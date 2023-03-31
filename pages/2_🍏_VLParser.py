import pandas as pd  # 데이터 프레임 처리 : df 
import numpy as np
from time import sleep
import urllib.request # openAPI 부동산 정보 불러오기 : asv? 
from bs4 import BeautifulSoup # csv 스크롤러
import re
import streamlit as st
import datetime

# page config
st.set_page_config(
    page_icon = "🇰🇷",
    page_title = "ddarunim streamlit",
    layout = "wide",
)

def query_sender_VLrentfee(localcode, timecode):
    url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHRent'
    code_info = '&LAWD_CD='+ localcode + '&DEAL_YMD=' + timecode
    key = '?serviceKey=teTA5vuN%2BNGd319y02AUNhSeDFVvfkS8NM9beUsc%2FFPN%2BtTnIpgPytg1nbcLG4jEeppsOfS%2BePwL1cp60X%2BuTA%3D%3D'
    request = urllib.request.Request(url+key+code_info)
    request.get_method = lambda: 'GET'
    response_body = urllib.request.urlopen(request).read()
    u = str(response_body, "utf-8")
    return u
# http://api.vworld.kr/req/address?service=address&request=getAddress&version=2.0&crs=epsg:4326&point=127.053266,37.515036&format=xml&type=parcel&zipcode=true&simple=false&key=E302C79A-C14D-34F5-BA26-8E933D2AC9E1

def query_sender_DANDOKrentfee(localcode, timecode):
    url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcSHRent'
    code_info = '&LAWD_CD='+ localcode + '&DEAL_YMD=' + timecode
    key = '?serviceKey=teTA5vuN%2BNGd319y02AUNhSeDFVvfkS8NM9beUsc%2FFPN%2BtTnIpgPytg1nbcLG4jEeppsOfS%2BePwL1cp60X%2BuTA%3D%3D'
    request = urllib.request.Request(url+key+code_info)
    request.get_method = lambda: 'GET'
    response_body = urllib.request.urlopen(request).read()
    u = str(response_body, "utf-8")
    return u

def get_VL_DANDOK_renthistory(localcode, timecode, typecode) : 
    localcode = str(localcode)
    timecode = str(timecode)
    regex = re.compile(r'\d{4}')
    yeartxt = regex.search(timecode)
    timecode_year = yeartxt.group() # 정규식 검출결과 실제 값을 구하기 위해서는 무조건 re.compile사용
    
    building_type = []
    idx = []  
    area_code = []
    apt_name = [] 
    build_age = []
    price = []
    monthfee = []
    region = []
    address = []
    year = []
    month = []
    day = []
    area_jibun = []
    area_used = []
    story = []
    renew_activate = []
    before_price = []
    before_monthfee = []
    navermap_link = []
    
    #jibun_pyung = []
    #price_per_jibun = []
    
    blankdeletepattern = re.compile(r'\s+') #string 안 공백 삭제용 pattern
    
    xml_VL_string = [] # 실제 사용하기전 변수할당하여 추후 if에 true / false 로 사용
    xml_DANDOK_string = [] # 실제 사용하기전 변수할당하여 추후 if에 true / false 로 사용
    
    if typecode == 2:
        xml_DANDOK_string = query_sender_DANDOKrentfee(localcode,timecode)
    elif typecode == 1:
        xml_VL_string = query_sender_VLrentfee(localcode,timecode)
    else:
        xml_DANDOK_string = query_sender_DANDOKrentfee(localcode,timecode)
        xml_VL_string = query_sender_VLrentfee(localcode,timecode)
    
    if (xml_VL_string):
        print('VL rentfee parsing ready...for :' + timecode)
        BS_VL = BeautifulSoup(xml_VL_string, 'lxml-xml')
        rng = range(0, len(BS_VL.find_all('item'))) #item 으로 찾으면 각 매물별 한묶음씩 처리
        for i in rng:
            idx.append(i+1)
            building_type.append('연립다세대')
            apt_name.append(BS_VL.find_all('item')[i].find('연립다세대').get_text())
            build_age.append(BS_VL.find_all('item')[i].find('건축년도').get_text())

            price_str = BS_VL.find_all('item')[i].find('보증금액').get_text()
            price_str = price_str.replace(",","")
            price_float = float(price_str)
            price.append(price_float)

            monthfee_str = BS_VL.find_all('item')[i].find('월세금액').get_text()
            monthfee_str = monthfee_str.replace(",","")
            monthfee_float = float(monthfee_str)
            monthfee.append(monthfee_float)
            dong_str = BS_VL.find_all('item')[i].find('법정동').get_text()
            dong_str = re.sub(blankdeletepattern, '', dong_str) #string 안 모든 공백 삭제

            region.append(dong_str)
            year.append(timecode_year)
            month.append(BS_VL.find_all('item')[i].find('월').get_text())
            day.append(BS_VL.find_all('item')[i].find('일').get_text())

            #area_jibun_str = xsoup.find_all('item')[i].find('대지권면적').get_text()
            #area_jibun.append(area_jibun_str)

            #jibun_pyung_float = round( (float(area_jibun_str) / 3.3) , 2)

            #jibun_pyung.append(jibun_pyung_float)

            area_used_str = BS_VL.find_all('item')[i].find('전용면적').get_text()
            area_used.append(area_used_str)

            address_jibeon_str = BS_VL.find_all('item')[i].find('지번').get_text()
            address.append(address_jibeon_str)

            story_str = BS_VL.find_all('item')[i].find('층').get_text()
            story.append(story_str)
            
            area_code_str = BS_VL.find_all('item')[i].find('지역코드').get_text()
            area_code.append(area_code_str)
            
            if (BS_VL.find_all('item')[i].find('갱신요구권사용').get_text() == '사용'):
                renew_activate_str = BS_VL.find_all('item')[i].find('갱신요구권사용').get_text()
                renew_activate.append(renew_activate_str)
                before_price_str = BS_VL.find_all('item')[i].find('종전계약보증금').get_text()
                before_price.append(before_price_str)
                before_monthfee_str = BS_VL.find_all('item')[i].find('종전계약월세').get_text()
                before_monthfee.append(before_monthfee_str)
                #print(renew_activate_str+'/'+before_price_str+'/'+before_monthfee_str)
            else:
                renew_activate.append('N/A')
                before_price.append('N/A')
                before_monthfee.append('N/A')
            
            navermap_link_str = 'https://map.naver.com/v5/search/'+ \
                                dong_str + '%20' + address_jibeon_str
            navermap_link.append(navermap_link_str)
            
            #price_per_jibun_float = round( (price_float / jibun_pyung_float) )
            #price_per_jibun.append(price_per_jibun_float)
        
        print('VL rentfee parsing DONE... item count : ' + str(len(rng)))
    else:
        print('WARNING : VL rentfee data is missing... check the status')
   

    if (xml_DANDOK_string):
        print('DANDOK rentfee parsing ready...for :' + timecode)
        BS_DANDOK = BeautifulSoup(xml_DANDOK_string, 'lxml-xml')
        rng_DANDOK = range(0, len(BS_DANDOK.find_all('item'))) #item 으로 찾으면 각 매물별 한묶음씩 처리
        #for i in tqdm_notebook(rng):
        for i in rng_DANDOK:
            idx.append(i+1)
            building_type.append('단독/다가구')
            apt_name.append('No Info')
            #apt_name.append(BS_DANDOK.find_all('item')[i].find('연립다세대').get_text())
            ## 단독의 경우 연립다세대 태그 없으므로 삭제
            if (BS_DANDOK.find_all('item')[i].find('건축년도')):
                build_age.append(BS_DANDOK.find_all('item')[i].find('건축년도').get_text())
            else:
                build_age.append('No Info')

            price_str = BS_DANDOK.find_all('item')[i].find('보증금액').get_text()
            price_str = price_str.replace(",","")
            price_float = float(price_str)
            price.append(price_float)

            monthfee_str = BS_DANDOK.find_all('item')[i].find('월세금액').get_text()
            monthfee_str = monthfee_str.replace(",","")
            monthfee_float = float(monthfee_str)
            monthfee.append(monthfee_float)
            dong_str = BS_DANDOK.find_all('item')[i].find('법정동').get_text()
            dong_str = re.sub(blankdeletepattern, '', dong_str) #string 안 모든 공백 삭제

            region.append(dong_str)
            year.append(timecode_year)
            month.append(BS_DANDOK.find_all('item')[i].find('월').get_text())
            day.append(BS_DANDOK.find_all('item')[i].find('일').get_text())

            area_used_str = BS_DANDOK.find_all('item')[i].find('계약면적').get_text()
            area_used.append(area_used_str) ## 계약면적으로 갈음 - 단독/다가구의 경우

            #address_jibeon_str = BS_DANDOK.find_all('item')[i].find('지번').get_text()
            address.append('No Info')
            #단독다가구의 경우 지번 없으므로 삭제

            #story_str = BS_DANDOK.find_all('item')[i].find('층').get_text()
            story.append('No Info')
            #단독다가구의 경우 층 없으므로 삭제
            
            area_code_str = BS_DANDOK.find_all('item')[i].find('지역코드').get_text()
            area_code.append(area_code_str)
            
            navermap_link.append('N/A')

            #price_per_jibun_float = round( (price_float / jibun_pyung_float) )
            #price_per_jibun.append(price_per_jibun_float)
            
            if (BS_DANDOK.find_all('item')[i].find('갱신요구권사용').get_text() == '사용'):
                renew_activate_str = BS_DANDOK.find_all('item')[i].find('갱신요구권사용').get_text()
                renew_activate.append(renew_activate_str)
                before_price_str = BS_DANDOK.find_all('item')[i].find('종전계약보증금').get_text()
                before_price.append(before_price_str)
                before_monthfee_str = BS_DANDOK.find_all('item')[i].find('종전계약월세').get_text()
                before_monthfee.append(before_monthfee_str)
                #print(renew_activate_str+'/'+before_price_str+'/'+before_monthfee_str)
            else:
                renew_activate.append('N/A')
                before_price.append('N/A')
                before_monthfee.append('N/A')
        
        print('DANDOK rentfee parsing DONE... item count : ' + str(len(rng_DANDOK)))
    else:
        print('WARNING : DANDOK rentfee data is missing... check the status')
    

    data = {'지역코드':area_code, '유형':building_type, '아파트명':apt_name, '건축년도':build_age,
            '보증금액':price, '월세':monthfee,
            '법정동':region,'지번':address, '층':story, '전용면적':area_used, '년':year,
            '월':month, '일':day, '계약갱신청구':renew_activate,
            '종전보증금':before_price, '종전월세':before_monthfee, '지도링크':navermap_link }

    df = pd.DataFrame(data)
    df = df.sort_values(by='보증금액', ascending=True)
    
#     print(len(area_code))   ## 코멘트 변환 단축키 : cmd + /
#     print(len(building_type))
#     print(len(apt_name))
#     print(len(build_age))
#     print(len(price))
#     print(len(monthfee))
#     print(len(region))
#     print(len(address))
#     print(len(story))
#     print(len(area_used))
#     print(len(year))
#     print(len(month))
#     print(len(day))
    
    return df

def getYearMonthList(start_year, start_month, end_year, end_month) :
    date = []
    #startdate, enddate = YYYYMM
    for i in range(start_year, end_year + 1):
        for j in range(start_month,end_month + 1):
            if j < 10 :
                month = '0'+str(j)
            else :
                month = str(j)    

            year = str(i)
            date.append(int(year+month))
            
    return date

def getAreaCode(input_area_name):
    if input_area_name == '강남구':
        output_area_code = 11680
    elif input_area_name == '서초구':
        output_area_code = 11650
    elif input_area_name == '송파구':
        output_area_code = 11710
    elif input_area_name == '상당구':
        output_area_code = 43111
    elif input_area_name == '서원구':
        output_area_code = 43112
    elif input_area_name == '흥덕구':
        output_area_code = 43113
    elif input_area_name == '청원구':
        output_area_code = 43114
    else:
        output_area_code = 00000
        
    return output_area_code

### following under is for webpage_streamlit

st.subheader("연립/다세대 및 단독/다가구 전월세 실거래 조회")

def doStateChange_to_visible(input_state):
    input_state = "visible"
def doStateChange_to_collapsed(input_state):
    input_state = "collapsed"
def doStateChange_to_hidden(input_state):
    input_state = "hidden"

def doStateChagne_to_false_end_date_disb():
    st.session_state.end_date_disb = False
def doStateChange_to_false_region_disb():
    st.session_state.region_disb = False

@st.cache_data ## @st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

if "end_date_disb" not in st.session_state:
    st.session_state.end_date_disb = True
if "region_disb" not in st.session_state:
    st.session_state.region_disb = True

st.write("1.조회하고 싶은 년/월 범위 입력")

col_a1, col_a2 = st.columns([1,1])

with col_a1:
    d_start = st.date_input(
        "조회년월 선택 (시작), 년/월 선택되며 일은 무시됨",
        datetime.date(2023, 3, 1),
        on_change=doStateChagne_to_false_end_date_disb)
    #st.write('조회년월(시작):', d_start)
    st.write("시작 -- 조회 년도:", d_start.year, "조회 월", d_start.month)
    
with col_a2:
    d_end = st.date_input(
        "조회년월 선택 (종료) 년/월 선택되며 일은 무시됨",
        datetime.date(2023, 3, 8),
        disabled = st.session_state.end_date_disb,
        on_change = doStateChange_to_false_region_disb)
    st.write("종료 -- 조회 년도:", d_end.year, "조회 월", d_end.month)

listdate = getYearMonthList(d_start.year,d_start.month,d_end.year,d_end.month)
st.write(listdate)

## column B start
st.write("2.조회하고 싶은 지역 및 부동산 유형 선택")
col_b1, col_b2 = st.columns([1,1])
with col_b1:
    opt_region_si = st.selectbox(
    '지역 선택 (시/도)',
    ('서울특별시', '청주시'),
    disabled = st.session_state.region_disb)  
    if opt_region_si == '서울특별시':
        opt_region_gu = st.selectbox(
        '지역 선택 (구/군)',
        ('강남구', '서초구', '송파구'),
        disabled = st.session_state.region_disb)
    if opt_region_si == '청주시':
        opt_region_gu = st.selectbox(
        '지역 선택 (구/군)',
        ('상당구','서원구','흥덕구','청원구'),
        disabled = st.session_state.region_disb)


    opt_areacode = getAreaCode(opt_region_gu)

    st.write('선택 지역 :', opt_region_gu, '... 선택 코드 :', opt_areacode)

with col_b2:
    opt_type_str = st.radio(
        "부동산 유형 선택",
        ('연립/다세대', '단독/다가구'))

    if opt_type_str == '연립/다세대':
        opt_type_int = 1
    if opt_type_str == '단독/다가구':
        opt_type_int = 2

    st.write('선택 유형 :', opt_type_str, '... 선택유형코드 :', opt_type_int)

## column C start
st.write("3.조회하기")
if st.button('조회하기'):
    with st.spinner('Wait for it...'):

        for i in range(0,len(listdate)):
            if i == 0:
                prev_data = get_VL_DANDOK_renthistory(opt_areacode,listdate[i],opt_type_int)
            else :
                tmp_data = get_VL_DANDOK_renthistory(opt_areacode,listdate[i],opt_type_int)
                sum_data = pd.concat([prev_data,tmp_data]) 
                prev_data = sum_data
    
    st.success('Done!')
    st.write("조회결과")

    st.dataframe(prev_data)
    csv_data = convert_df(prev_data)

    st.download_button(
        label="CSV 파일로 다운로드",
        data=csv_data,
        file_name='data.csv',
        mime='text/csv',
    )
