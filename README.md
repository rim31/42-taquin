# 42-taquin
resolution of taquin : (N-puzzle 42)

![alt text](https://github.com/rim31/42-taquin/blob/master/1.png)

```
 python run.py -h
usage: run.py [-h] [-l LENGTH | -f FILE] [-s | -u] [-a]

optional arguments:
  -h, --help            show this help message and exit
  -l LENGTH, --length LENGTH
                        Choose the size of your puzzle between 3 and 70
  -f FILE, --file FILE  Name of your file, if this option is selected, ignore:
                        -s/u
  -s, --solvable        Generate only solvable puzzle
  -u, --unsolvable      Generate only unsolvable puzzle
  -a, --anim            Launch an animation of the resolution of the puzzle
```

```
git clone ...
```
```
python run.py -l 5 -s -a
```
