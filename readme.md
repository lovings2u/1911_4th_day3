# Day 3

- parameter
  - query string
  - path parameter
- 웹툰 데이터를 요일별로 다르게 url 세우기
- html파일로 view 만들기(render template)
- Beautiful soup 
  - 사이트 구조 분석하는 방법 (html은 어떻게 하는지)
  - URL 구조(query string) 분석하는 방법
  - **사람인** 크롤링해보기
  - 데이터가 xml 형태로 주고 받는 사이트 제외 모두 크롤링 가능(로그인 안한 상태에서 볼 수 있는 것만)



### 사람인 크롤링해보기

- 요청 보내서 html 문서 받기

  ```python
  from bs4 import BeautifulSoup
  import requests
  
  url = "http://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_cd=404&panel_type=&search_optional_item=n&search_done=y&panel_count=y"
  response = requests.get(url)
  
  html = BeautifulSoup(response.text, 'html.parser')
  
  ```

- 원하는 부분 뽑아내기

  - select
    - select_one
    - select
  - find
    - find
    - find_all

  ```python
  company_names = html.select('.company_name')
  recruit_names = html.select('.recruit_name')
  recruit_conditions = html.select('.list_recruit_condition')
  ```

- 한꺼번에 순회하면서 각각에서 원하는 부분 출력하기

  ```python
  for company_name, recruit_name, condition in zip(company_names, recruit_names, recruit_conditions):
      print(f'{company_name.text}- {recruit_name.text}')
      print(condition.text)
  ```

> 또다른 방법으로 원하는 부분 출력하기
>
> ```python
> company = html.select('.part_top')
> for com in company:
>     print(f'{com.select_one(".company_name").text}- {com.select_one(".recruit_name").text}')
>     print(com.select_one('.list_recruit_condition').text)
> ```



#### 각 기업 상세 페이지까지 drill-down 하기

- 페이지의 구성 방식이 틀을 짜는 html 파일이 있고, ajax call을 통해 기업 정보들을 유동적으로 붙여주는 형태로 페이지를 구성하고 있음
- 리스트에서 제공하는 url은 틀을 요청하는 주소이기 때문에 기업 상세 주소를 검색하기 위해서는 **각 기업의 id** 값에 해당하는 부분을 찾아내야함

- url에서 기업 코드 찾아내기

  ```python
  company_list = html.select('ul.product_list li')
  
  for com in company_list:
      idx = com.select_one('a')['href'].split('=')[-1]
  ```

- 기업코드를 붙여 기업 상세정보 요청하기

  ```python
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
  ```

  