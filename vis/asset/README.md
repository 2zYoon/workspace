# Script
## keys
- `choice`: number of choice (default: [])
- `bg`: background image code
- `bgm`: BGM (repeat)
  - `none`: no BGM
  - `soundname`: some sound
- `speaker`: speaker
  - `none`: no speaker
- `sound`: sound (once)
- `color`: color (r, g, b, a)
  - `none`: no sound
  - `soundname`: some sound
- `dialog`: option for dialog (default: 1(enabled))
- `text[1-2]`: n-th line dialog text 
- `next`: code of next script (default: [cur+1])
- `bg-fadein`: background fade in (default: 1(enabled))
- `auto-branch`: auto-branch based on specific score (`"score": [key, threshold, if, else]`)
- `comment`: just a comment.

## TODOs
- 특정 스위치에 반응해서 분기하는 scene
- image
  - `c[1-3]`: 캐릭터 위치
  - `c[1-3]b`: 캐릭터 위치, blurred
# image
- bg: 스케일 맞추긴 하지만 가급적 800x600 (4:3)
- ch: 가급적 1:2, 위쪽 여백 적게, 아래는 대충해도 무방
