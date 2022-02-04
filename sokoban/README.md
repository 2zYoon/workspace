# Sokoban (Warehouse Keeper)
The goal of [Warehouse Keeper](https://en.wikipedia.org/wiki/Sokoban) (a.k.a. Sokoban) is storing all of box to hole.

# How to Use
Note: Linux (or possibly MacOS) requires being a root to read hotkey.
It requires Python 3 and keyboard library:

```
$ pip3 install keyboard 
```

And then run `main.py` with gameboard file. If argument is omitted, use map.txt as default gameboard
```
$ main.py [gameboard].txt
```

- `W`: Up
- `A`: Left
- `S`: Down
- `D`: Right
- `Esc`: Quit
- `R`: Restart

# How to Make Gameboard
Gameboard consists of floor(`.`), wall(`#` or ` `(space)), box(`B`), hole(`O`), and unique player(`@`). You should follow these:

- Too large map makes it hard to see
- The number of boxes must be same with that of holes
- There must be only one player

