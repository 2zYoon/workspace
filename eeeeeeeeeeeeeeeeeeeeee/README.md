# eeeeeeeeeeeeeeeeeeeeee
Simple obfuscation tool for C code that converts your code to eeeeeeeeee..

와, e가 22개!

# Getting Started
## Environment & Preparation
Clone this repository. 

```
$ git clone https://github.com/EunSeong-Park/eeeeeeeeeeeeeeeeeeeeee.git
```

You only need to make sure Python3 is available.

## How to Use
Run `main.py`

```
$ python3 main.py <input> <output> [char]
```

- `<input>`: C source code you want to convert
- `<output>`: Converted source code.
- `[char]`: If you want eeeeeeeeeeeeeee, you can designate other character (alphabet or underscore("\_"))
  - Default: `e` 


## Exmaples
Some example codes and outputs are provided. You can find these in `this_repo/exmaples`

## Notes
- This does not change the code's semantics
- This assumes that the input C source code is valid
- This can modify the source code format and eliminate some comments
- **Don't use for obfuscation (it does not work effectively)**

# Issues
Currently, this does not support function-like macro. For example:
```
#define ABC(x, y) ((x) + (y))
#define eee(x) ((x))
```

If there are more issues (i.e., an error occur even if the source code is valid), please let me know via:
- E-mail: [dmstjd517@unist.ac.kr](mailto:dmstjd517@unist.ac.kr)
- Blog guestbook: [link](https://esp-ark.com/guestbook/)

Thank you.
