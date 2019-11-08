from bs4 import BeautifulSoup
import requests

url = "http://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_cd=404&panel_type=&search_optional_item=n&search_done=y&panel_count=y"
response = requests.get(url)

html = BeautifulSoup(response.text, 'html.parser')

'''
company_names = html.select('.company_name')
recruit_names = html.select('.recruit_name')
recruit_conditions = html.select('.list_recruit_condition')


for company_name, recruit_name, condition in zip(company_names, recruit_names, recruit_conditions):
    print(f'{company_name.text}- {recruit_name.text}')
    print(condition.text)
'''

'''
company = html.select('.part_top')
for com in company:
    print(f'{com.select_one(".company_name").text}- {com.select_one(".recruit_name").text}')
    print(com.select_one('.list_recruit_condition').text)
    break
'''

company_list = html.select('ul.product_list li')

for com in company_list:
    idx = com.select_one('a')['href'].split('=')[-1]
    company_info_url = 'http://www.saramin.co.kr/zf_user/jobs/relay/view-ajax'
    company_info_params = { 'rec_idx': idx }
    company_response = requests.post(company_info_url, params=company_info_params)
    print(company_response)
    company_html = BeautifulSoup(company_response.text, 'html.parser')
    company_title = company_html.select_one('a.company').text
    print(company_title.strip())
    
    break

