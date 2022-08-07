# AnonymousForum

-----------
## 초기 세팅
### 1. 파이썬 버전
```
$ python -v 

# 3.9.5
```

### 2. mysql 버전 확인 (mysql 쿼리로 확인)
```
SELECT version(); -- 8.0.29
```

### 2. 필요한 패키지 설치
```
$ pip install -r requirements.txt
```

### 3. mysqldump 테이블 구조 복구하기
```
$ mysql -u -p anonymous_forum < anonymous_forum.sql
```

### 4. API 실행하기
```
$ python3 manage.py
```

### 5. API 주소는 로컬 호스트로 생성
```
http://127.0.0.1:5000/
```


-----------
## 각 API 기능
+ forum/board
    + [GET] : 게시판 리스트 출력 API
+ forum/detail
    + [GET] : 게시글 상세 데이터 조회
    + [POST] : 게시글 상세 데이터 추가
    + [PUT] : 게시글 상세 데이터 수정(제목, 내용만 수정 가능)
    + [DELETE] : 게시글 상세 데이터 삭제
+ forum/comment
    + [GET] : 특정 게시글의 댓글 조회 (상위 댓글에 대한 페이지네이션 가능)
    + [POST] : 특정 게시글의 댓글 추가
+ forum/alert
    + [GET] : 특정 게시글, 댓글이 추가되었을 때 등록된 키워드에 해당하는 내용이 있는 유저 리스트 출력
