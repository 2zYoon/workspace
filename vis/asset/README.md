# Script
## keys
- `choice`: number of choice
  - `0`: normal
  - `-1`: game over
  - `n ([1,4])`: choice
- `bg`: background image code
- `bgm`: BGM (repeat)
  - `none`: no BGM
  - `soundname`: some sound
- `speaker`: speaker
- `sound`: sound (once)
  - `none`: no sound
  - `soundname`: some sound
- `dialog`: option for dialog
  - `1` enabled
- `text`: dialog text
- `next`: code of next script
  - `choice 0`: int
  - `choice n`: int arr
  
## TODOs
- 특정 스위치에 반응해서 분기하는 scene
- image
  - `c:[1-3]:[0-3]`: 캐릭터 위치, n인 구도, n-번째 캐릭터 하이라이트(0은 no highlight)
  - `m`: 중앙 이미지
- 일부 key 생략 가능하게(fontsize, color, bgm, date)