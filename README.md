# 29-2nd-GREAM-backend

> 본 repository는 웹 개발 학습을 위해 크림(https://kream.co.kr/) 사이트를 클론코딩하였습니다.
> 짧은 기간동안 기능 구현에 보다 집중하기 위해 Users, Products 앱까지 기능 구현하였습니다.


## 개발 인원 및 기간

+ 개발기간: 2021.2.14. ~ 2022.02.25.
	+ Backend: 이도운, 이강일 (repository: https://github.com/wecode-bootcamp-korea/29-2nd-GREAM-backend)
	
	+ Backend
		+ Backend 공통: ERD, CSV Uploader
		+ 이도운 : 상품 상세 View, 상품 입찰 목록 View, 관심 상품 추가/삭제 View, 상품 사이즈별 가격 View, 상품 시세 View, 검색 View
		+ 이강일 : 상품 리스트 View, 소셜 로그인 View


## Demo

> 영상


## ERD

![MRMRZARA](https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fa70f5b38-5045-4776-803d-e5de8122f4de%2FUntitled.png?table=block&id=6da7bd07-f6b4-4048-939f-dfed76aa5941&spaceId=5261a9e7-e5b9-4e71-b383-63b7ad738cb5&width=2000&userId=5e824c0e-3b9f-4749-993a-65e855a84977&cache=v2)


## 협업 도구

+ Github
+ [Trello 바로가기](https://trello.com/b/d2vsMmbG/gream-we-draw)
+ Slack


## 사용 기술

+ Git
+ Django
+ Python
+ MySQL
+ AWS


## Library

+ JWT


## 구현 기능

### User
+ 소셜 로그인: 카카로 로그인 API 활용 (GET)

### Product
+ 상품 정보 조회 (GET)

+ 상품 입찰 목록 (GET)

+ 상품 사이즈별 가격 조회 (GET)

+ Decorator 적용하여 token 통해서 유저 인증 후 관심 상품 추가 삭제 기능 구현 (POST)

+ 상품 시세 차트 (GET)

+ 상품 검색 (POST)

## Reference

+ 이 프로젝트는 Kream 사이트를 참조하여 학습 목적으로 만들었습니다.
+ 실무 수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제가 될 수 있습니다.
+ 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.

