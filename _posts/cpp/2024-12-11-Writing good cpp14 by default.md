---
layout: post
tags:
  - Cpp
---
<https://www.youtube.com/watch?v=hEx5DNLWGgA&list=WL&index=1&ab_channel=CppCon>
<https://www.youtube.com/watch?v=xnqTKD8uD64&list=WL&index=1&ab_channel=CppCon>

Guidelines
- <https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md>

How can we add guidelines that prevent default usage of grenades in cpp? Theres three main grenades we want to tackle.
1. Type safety
2. Bound safety
3. Lifetime safety

Strong idea of cpp is to have no runtime overhead.
### Type safety
Don't use a memory location of type T, that contains type U.

Basically 
- Don't use static cast downcasts, use dynamic casts.
- Use static cast pretty much otherwise.

### Bound safety
Don't access beyond the bounds of allocation.

Basically
- Use array_view and string_view. Lets you for each, but main benefit is that you can compile time assert on ranges.
- Only index into arrays using constant expressions

```cpp
for(auto& a: b){}
```
### Lifetime safety
Three things
1. Delete every heap object once
2. Only once, so you get no corruption
3. Don't reference deleted objects

Lots of previous approaches on this
1. Taking runtime overheads of cleanup with GC
2. Doing whole program analysis, static analysis.

Basically
- Be clear on if something is owning or pointing.
- Don't use `new`. Use smart pointers to abstract ownership. `make_unique or make_shared`
- DON'T pass shared_ptr as function parameters and returns, just use refs.
- Keep in mind the lifetime of temporary objects