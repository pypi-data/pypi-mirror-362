# Functional Iterators (Fiterators)

do you like functional style programming?

do you not like `list(map(lambda x: x * 2, filter(lambda x: x < 5, [2, 4, 6, 8])))`?

try `Fiterators` today! it lets you do this:

```py
into_iter([2, 4, 6, 8]).filter(lambda x: x < 5).map(lambda x: x * 2).collect()
```

much nicer, and much better for my rusty brain \~.\~

made by me because i got frustrated ~Vivian <3

> But what functions does it have???

i'm glad you asked. with Fiterators you can:
- `filter`
- `map`
- `reduce`
- `enumerate`
- `chain`
- `any`
- `all`
- `find`
- `for_each`  
and  
- `collect`

i might add more if i wanna use them
