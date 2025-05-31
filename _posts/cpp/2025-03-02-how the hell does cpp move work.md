---
layout: post
tags:
  - Cpp
---
## What is the problem?
The key problem this solves is with the handling of large objects we DONT WANT TO COPY. This usually happens when we.
1. Want to return our fat object
2. Want to give a function our fat object

Previously to do this we're kinda stuck and we need to either (for returning)
1. Handle the memory yourself: by passing around a pointer that was created
2. Modify memory that was provided: mutating a reference parameter

This is painful, if only there was a way to just return the result and have cpp just handle all this crap for us?
## What is move semantics?
Basically on terminology
1. lvalue: is something you can mutate, like a reference `&bean` 
2. rvalue: something you can't mutate `&&bean` (and you can plunder 😱)

So move semantics is just the art of 
1. realising that something is an rvalue
2. specifying a function that works with these rvalues (a move constructor and a move assignment)

simple!

If its a temporary object like a function return, or an object thats going out of scope, you can just move it freely!
## How does `std::move` solve our problem?
`std::move` simply just tells cpp that this lvalue is actually an rvalue. Just that.
## What are the best practices here and why?

#### Keep in mind the rule of zero
If you define any of the 5 basic special functions, you won't get your move functions! This means that `std::move` will just not do anything!
#### Handling fundamental types
Guess what. When you move that int, it'll call your nice move constructor or assignment, but that will simply still do a copy as its faster.
#### Moving const variables
Keeping that const variable a const and not mutating it sounds sane. And thats what happens.
#### Don't move return values.
cpp does copy ellison/RVO. This means that instead of having that return value be copied back into the calling scope, it will actually just completely removes it!
- These temporary r values are called pure r values, and are always directly constructed where they need to be!
- AKA when you initialise a returned object in a return statement
- Or when you initialise and object and construct crap in its parameters

Removing the copy itself is always better than a move. A move is still a cheaper copy:
1. Copy the memory address
2. Nullify the memory address of the thing you've copied

#### Moving `std::array`
Lmao, this guy is moving std arrays, don't you know that moving that still copies all underlying elements. A `std::array` is still a trivial type and therefore copied.
## Appendix
<https://mbevin.wordpress.com/2012/11/20/move-semantics/ >
<https://www.nutrient.io/blog/when-cpp-doesnt-move/>
<https://subscription.packtpub.com/book/programming/9781839216541/2/ch02lvl1sec08/move-semantics-explained>