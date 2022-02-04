# NONOGRAM SOLVER
```
                             1  1  1
                       1  1  1  1  1
           2  4  4  8  1  1  2  4  4  9
          ______________________________
       3 | X  X  X  X  X  X  X █████████
    2  1 | X  X  X  X  X ██████ X  X ███
    2  3 | X  X  X ██████ X  X █████████
 1  2  1 | X  X  X ███ X ██████ X  X ███
    2  1 | X  X  X ██████ X  X  X  X ███
    1  1 | X  X  X ███ X  X  X  X  X ███
    1  3 | X  X  X ███ X  X  X █████████
    3  4 | X █████████ X  X ████████████
    4  4 |████████████ X  X ████████████
    4  2 |████████████ X  X  X ██████ X
       2 | X ██████ X  X  X  X  X  X  X
```

Basic nonogram (a.k.a. nemo-nemo logic) solver

## Required
- python3
- numpy

## Usage
```
python3 solver.py [json-path]
```

or

```
python solver.py [json-path]
```

## TODO
- 더 이어갈 수 있는 블록 잇기
- 명백히 들어갈 수 없는 곳 막기
- 특정 블록이 어느 condition에 속하는지 확인 후 분할 정복