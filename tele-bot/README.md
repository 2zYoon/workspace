# Telegram Chatbot

## 사용법
텔레그램 챗봇 아이디는 `@esp_ark_bot`입니다. 텔레그램 내에서 해당 아이디를 검색하거나, [링크](https://t.me/esp_ark_bot)를 통해 서비스를 이용할 수 있습니다.

챗봇 내에서 `/help` 명령어를 통해 각 명령어에 대한 도움말을 얻을 수 있습니다.

현재 제공하는 기능은 다음과 같습니다.

- 일일 누적 계산기: 매일 초기화되는 누적 계산기입니다.
- 일일 리마인더: 매일 정해진 시간에 알림을 보내줍니다.
- 주간 리마인더: 매주 정해진 요일, 정해진 시간에 알림을 보내줍니다.
- 플래그 레이스 알림: 바로 다음 열리는 플래그 레이스 시작 시 알림을 보내줍니다.

## 사용 예시

도움말 관련

- `/help`: 전체 도움말 보기
- `/help daily`: 일일 리마인더에 대한 도움말 보기
- `/help weekly add`: 주간 리마인더 등록을 위한 도움말 보기

리마인더 관련

- `/daily add 우르스 2250`: 매일 오후 10시 50분에 "우르스"라는 이름의 알림 받기 (설명 생략)
- `/daily add 우르스 2250 아 맞다 우르스!`: 매일 오후 10시 50분에 "우르스"라는 이름의 알림 받기 (설명 포함)
- `/weekly add 카오스링 1000 월 아 맞다 카오스링!`: 매주 월요일 10시에 "카오스링"이라는 이름의 알림 받기
- `/weekly add 재획 1400 월수금 재획 할 시간~`: 매주 월,수,금요일 오후 2시에 "재획"이라는 이름의 알림 받기
- `/daily remove 우르스`: "우르스"라는 이름의 일일 리마인더 제거
- `/weekly remove all`: 주간 리마인더 전부 제거

플래그 관련

- `/flag`: 바로 다음에 열리는 플래그 레이스 시작 시 알림 받기
  - 예시 1: 10시 10분에 설정 시 10시 30분에 알림
  - 예시 2: 일요일 오후 11시에 설정 시 월요일 오전 1시 30분에 알림 (주간 정산)

## 버그 및 문의사항
버그를 발견하거나 문의사항이 있다면 dmstjd517@unist.ac.kr으로 연락 부탁드립니다. (조만간 이를 위한 별도의 페이지나 문의 기능을 추가할 예정입니다.)

## Instruction for Setup 
Expected to use Linux, but partly supports Windows. (In Windows, data creation should performed manually)

Only telegram module should be installed.

```bash
$ pip install python-telegram-bot
```

Run shell command. (Check permission if not work)

```bash
./setup.sh
```

Manually put your admin chat ID and telegram bot token.
```bash
cd private
echo "YOUR_CHAT_ID" > admin
echo "YOUR_TOKEN" > token
```

Run `main.py`.

```bash
python3 main.py
```

or

```bash
python main.py
```
