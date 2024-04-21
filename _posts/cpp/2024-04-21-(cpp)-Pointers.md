### What are pointers?
Pointers, point to memory addresses, pretty self explanatory.
1. Declare them with `int *ptr;`
2. Initialise them with `ptr = &x`
3. Dereference them (get the inner value) `int val = *ptr`
4. Create and delete memory with `new` and `delete`

### How do you deal with pointers?
Cpp also provides some nice syntactic sugar to access variables through pointers easier.

Instead of 
1. dereferencing the pointer and access a variable: `(*ptr).x`
2. You can just do `ptr->x`

Ain't that nice!

