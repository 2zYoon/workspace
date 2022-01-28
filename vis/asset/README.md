# Script
## keys
- `choice`: number of choice (default: [])
- `bg`: background image code
- `bgm`: BGM (repeat)
  - `none`: no BGM
  - `soundname`: some sound
- `speaker`: speaker
- `sound`: sound (once)
  - `none`: no sound
  - `soundname`: some sound
- `dialog`: option for dialog (default: 1(enabled))
- `textn`: n-th line dialog text 
- `next`: code of next script (default: +1)
- `bg-fadein`: background fade in (default: 1(enabled))
- `date`: 날짜
  
## TODOs
- 특정 스위치에 반응해서 분기하는 scene
- image
  - `c:[1-3]:[0-3]`: 캐릭터 위치, n인 구도, n-번째 캐릭터 하이라이트(0은 no highlight)
  - `m`: 중앙 이미지

# image
- bg: 스케일 맞추긴 하지만 가급적 800x600 (4:3)
- ch: 초상화는 144x108에 최적화됨 (4:3)
