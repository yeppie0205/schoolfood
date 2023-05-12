from bs4 import BeautifulSoup
import requests
import re
import streamlit as st
import pandas as pd

st.markdown("<h4>어떤 음식에 알레르기가 있습니까?</h4>", unsafe_allow_html=True)
st.markdown("<h8>숫자 사이 쉼표 표시를 정확히 해주시길 바랍니다.(0 입력 시 기본 식단표 제공)</h8>", unsafe_allow_html=True)
ask = st.text_input("")

data = {
    '숫자1': [1, 2, 3, 4, 5, 6],
    '정보1': ['계란(난류)', '우유', '메밀', '땅콩', '대두(콩)', '밀'],
    '숫자2': [7, 8, 9, 10, 11, 12],
    '정보2': ['고등어', '게', '새우', '돼지고기', '복숭아', '토마토'],
    '숫자3': [13,14,15,16,17,'18-19'],
    '정보3': ['아황산류', '호두', '닭고기', '쇠고기', '오징어', '조개류 - 잣'],
}

df = pd.DataFrame(data)

# 표 출력
st.table(df)

ask_list = ask.split(',')

url = "https://school.jbedu.kr/sangsan/MABAGAEAD/list"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
date = soup.find('ul', {"class": "tch-lnc-date"})
data = soup.find_all('li', {"class": "tch-lnc-wrap"})
if len(data) >= 3:
    bft = data[0]
    lunch = data[1]
    dinner = data[2]

bftlist = [bft.get_text()]
lunchlist = [lunch.get_text()]
dinnerlist = [dinner.get_text()]

menu_lists = [bft, lunch, dinner]
meal_types = ['조식', '중식', '석식']

for i, menu_list in enumerate(menu_lists):
    menu = menu_list.get_text().strip()  # 앞뒤 공백 제거
    menu_parts = menu.split('\n')  # 줄바꿈 문자를 기준으로 분리
    menu_data = []
    for part in menu_parts[1:]:
        if part.strip():
            match = re.search(r'\((.*?)\)', part)
            if match:
                menu_name = part[:match.start()].strip()
                numbers = match.group(1).split('.')
                menu_info = [menu_name] + numbers
                menu_data.append(menu_info)
    
    st.write(f'<br><b>{meal_types[i]}</b>', unsafe_allow_html=True)


    menu_names = []
    for menu_info in menu_data:
        allergens = menu_info[1:]
        exclude_menu = False
        for ask_num in ask_list:
            if ask_num in allergens:
                exclude_menu = True
                break
        if not exclude_menu:
            menu_names.append(menu_info[0])

    for menu_name in menu_names:
        st.write(menu_name)
    
    st.empty()
