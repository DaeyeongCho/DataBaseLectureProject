파일 구조
================================

```txt
main.py: 메인 함수 코드. 프로그램 실행 시 이 파일 실행


modules/: ui와 연결되는 모듈이나 기타 파이썬(.py) 모듈들 모음 폴더
│
├─── MainWindow.py: main_window.ui 파일과 연결하여 메인 윈도우 창 구현
│
└─── functions.py: 각종 유용한 사용자 함수 모음 모듈


user_interfaces/: .ui 파일들 모음 폴더
│
└─── main_window.ui: 메인 윈도우의 ui를 구성하는 파일


defines/: 상수 값 모음 .py 파일들 모음 폴더
│
├─── strings.py: 프로그램에서 사용되는 문자열 지정
│
└─── paths.py: 각종 필요한 파일의 절대/상대 경로 지정


.gitignore: 깃허브에 업로드 되지 않는 파일들 지정


README.md: 도움말 파일


readme_resource/: README.md 파일에서 사용 할 이미지 등 소스
```



> 필요 시 내용 추가하기