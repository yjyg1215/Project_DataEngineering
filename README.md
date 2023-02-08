# 🍿*영화 및 OTT 플랫폼 추천 웹 서비스*🍿

## ✔️*기획 배경*
1. 영화 추천을 받아도 여러 OTT에 흩어져 있어서 하나하나 어딨는지 찾아서 보기가 번거롭게 느껴짐
2. OTT 플랫폼이 너무 많아서 다 구독할 수 없음

### **=> 내가 좋아할만 한 영화가 가장 많은 OTT 플랫폼을 알 수 있다면 그거 하나로 뽕을 뽑을텐데...**

## ✔️*구현 파이프라인*
<img width="500" alt="스크린샷 2023-02-09 오전 12 05 59" src="https://user-images.githubusercontent.com/62207156/217568217-0d200720-84f7-4eab-bffd-0b7636cf5dda.png">

- 동적 크롤링으로 데이터 수집
    - Selenium 이용
- 로컬에 데이터 적재
    - MySQL 이용
- 영화 추천 API 구현
    - XGBoost 모델 사용
    - 모델 피클링
- 프론트엔드 구현
    - Flask 이용
- 대시보드 구성
    - Google Data Studio 이용

## ✔️*데이터 스키마*
<img width="500" alt="image" src="https://user-images.githubusercontent.com/62207156/217568964-8d476ce4-574f-463d-8dec-404e09904aa3.png">

- movies: 영화 id, 제목
- details: 영화 세부 정보
- reviews: 유저들의 리뷰 정보
- available: 현재 OTT에서 시청 가능한 영화만 포함된 테이블

## ✔️*서비스 시연*

### 메인 페이지

<img width="500" alt="스크린샷 2023-02-09 오전 12 19 56" src="https://user-images.githubusercontent.com/62207156/217573284-144c986a-a238-4086-af65-22172602bca3.png">

→ 유저에게 선호하는 영화 옵션들을 입력 받음

### 리포트 페이지

<img width="500" alt="스크린샷 2023-02-09 오전 12 21 29" src="https://user-images.githubusercontent.com/62207156/217573876-1503e399-7961-4b1f-b531-478334871ff9.png">

→ 입력받은 옵션을 가진 영화들의 정보를 데이터베이스에서 불러와 모델에 넣고 선호도를 예측. 그 결과를 바탕으로 추천 영화 리스트와 추천 OTT 플랫폼을 제시

### 대시보드

<img width="300" alt="스크린샷 2023-02-09 오전 12 22 07" src="https://user-images.githubusercontent.com/62207156/217576162-9411990f-4ccc-4f3d-9898-f604180d6f3b.png">
<img width="300" alt="스크린샷 2023-02-09 오전 12 22 18" src="https://user-images.githubusercontent.com/62207156/217576173-e70f5c46-52e4-499a-8a25-d76c58c456b3.png">
<img width="300" alt="스크린샷 2023-02-09 오전 12 22 35" src="https://user-images.githubusercontent.com/62207156/217576178-7340b115-e154-4acd-bc26-858d6631a57a.png">
<img width="300" alt="스크린샷 2023-02-09 오전 12 22 47" src="https://user-images.githubusercontent.com/62207156/217576182-1be033ef-f9e2-47f4-aabe-ba035ea167b1.png">

----------------------
`Python` `VSCode` `XGBoost` `Flask` `MySQL` `Google Data Studio` `Selenium` `Git`
