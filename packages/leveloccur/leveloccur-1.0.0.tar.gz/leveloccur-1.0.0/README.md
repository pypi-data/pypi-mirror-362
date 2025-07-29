Provides a class to specify a level of something.

Like this: The `'shackles'` string has 6 values, two of them are `'s'`. The probability of occurrence of `'s'` is 2/8 = 0.25. It has a *low* level of occurrence, so when you code
```
leveloccur.Level('s', 'shackles')
```
It would return `Low`.

Another example, ratio of 3 to 6 is 3/6 = 0.5 , so 
```
leveloccur.Level(3, 6)
```
would return `Exactly half`