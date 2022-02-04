# contants and msgs
PATH_DATA = "private/"


NAME_PROHIBITED = ['all', ]


MSG_HELP = '''\
/help [명령어]
> 전체 도움말, 혹은 명령어에 대한 도움말을 제공합니다.

(기본 기능)
/daily <show|add|remove>
> 일일 리마인더 기능을 사용할 수 있습니다.

/weekly <show|add|remove>
> 주간 리마인더 기능을 사용할 수 있습니다.

/daysum <정수값|show|clear>
> 매일 자정에 초기화되는 누적 계산기입니다.

/goodbye
> 유저 정보를 지우고 더 이상 알림을 받지 않습니다.

(메이플)
/flag
> 다음 플래그 레이스 시작 시 알림을 줍니다.
'''

MSG_DAYSUM_USE = '''\
/daysum <정수값|show|clear>
> 매일 자정에 초기화되는 누적 계산기입니다.

/daysum 정수값
> 주어진 정수를 더합니다. 
/daysum show
> 현재 누적값을 보여줍니다.
/daysum clear
> 누적값을 초기화합니다.
'''

MSG_DAILYCHECK_USE = '''\
/daily <show|add|remove>
> 일일 리마인더 기능을 사용할 수 있습니다.

/daily show
> 현재 일일 리마인더 목록을 보여줍니다.
/daily add <이름> <HHMM> [설명]
> 일일 리마인더를 추가합니다.
/daily remove <이름|all>
> 지정된 일일 리마인더를 삭제합니다.

/help daily <명령어>를 통해 더 자세한 설명을 볼 수 있습니다. 
'''

MSG_DAILYCHECK_ADD_USE = '''\
/daily add: 일일 리마인더를 추가합니다.
사용법: /daily add <이름> <HHMM> [설명]
    <이름>: 리마인더 이름
    <HHMM>: 알림 시간 (24시간제) 
    [설명]: 리마인더 설명 (선택)

예시: /daily add 우르스 2250 아 맞다 우르스!
'''

MSG_DAILYCHECK_SHOW_USE = '''\
/daily show: 현재 일일 리마인더 목록을 보여줍니다.
사용법: /daily show
'''

MSG_DAILYCHECK_REMOVE_USE = '''\
/daily remove: 지정된 일일 리마인더를 삭제합니다. all 사용 시 전부 삭제합니다.
사용법: /daily remove <이름|all>
'''

MSG_WEEKLYCHECK_USE = '''\
/weekly <show|add|remove>
> 주간 리마인더 기능을 사용할 수 있습니다.

/weekly show
> 현재 주간 리마인더 목록을 보여줍니다.
/weekly add <이름> <HHMM> <요일> [설명]
> 주간 리마인더를 추가합니다.
/weekly remove <이름|all>
> 지정된 주간 리마인더를 삭제합니다.

/help weekly <명령어>를 통해 더 자세한 설명을 볼 수 있습니다. 
'''

MSG_WEEKLYCHECK_ADD_USE = '''\
/weekly add: 주간 리마인더를 추가합니다.
사용법: /weekly add <이름> <HHMM> <요일> [설명]
    <이름>: 리마인더 이름
    <HHMM>: 알림 시간 (24시간제) 
    <요일>: 알림 요일 (월~일)
    [설명]: 리마인더 설명 (선택)

예시1: /weekly add 카오스링 1000 월 아 맞다 카오스링!
예시2: /weekly add 잠 2330 월화수목금 슬슬 자라...
'''

MSG_WEEKLYCHECK_SHOW_USE = '''\
/weekly show: 현재 주간 리마인더 목록을 보여줍니다.
사용법: /weekly show
'''

MSG_WEEKLYCHECK_REMOVE_USE = '''\
/weekly remove: 지정된 주간 리마인더를 삭제합니다. all 사용 시 전부 삭제합니다.
사용법: /weekly remove <이름|all>
'''

MSG_FLAG_USE = '''\
/flag: 다음 플래그 레이스 시작 시 알림을 줍니다.
사용법: /flag

주의사항: 주간 정산은 고려하지만, 점검은 고려하지 않습니다.
'''

MSG_GOODBYE_USE = '''\
/goodbye: 유저 정보를 지우고 더 이상 알림을 받지 않습니다. 이후 명령어를 사용하면 다시 서비스를 이용할 수 있습니다.
'''