---
tags:
  - Cpp
layout: post
---
## Style
constants: `PI`
types: upper case: `MyClass`
functions and variables: `lowerCase()`
member variables: `m_*`
global variables: `g_*`
function parameters: `t_*` or `p_*`

Use nullptr instead of NULL!

Use brace initialisation, so we don't have compile time narrowing.
```
int var{0};
```

When overloading stream operators `operator>>() operator<<()` do it as non member functions.

Avoid single parameter constructors, add `explicit` keyword, as they can be applied implicitly at compile time!
## Safety
Const as much as possible!

For return values, theres no real reason to return a reference to avoid a copy because copy ellison done by the compiler will try to remove needless copies here, so just return a value in most cases!
- <https://github.com/cpp-best-practices/cppbestpractices/issues/21#issuecomment-133760481>

Don't use new and delete to manage memory. Just use pointer handles to handle this memory!

Don't use c style casts, use cpp style `static_cast<int>()` instead. C style casts will try whatever casting it can find to make it work. C style casts
- Will just cast code that doesn't work
- Will breach private visibility
- Will even remove const keywords

## Maintainability
Don't use boolean parameters, as in cpp theres no keyword explicit-ness from the caller. You can use an enum or split the functions.

Avoid raw loops, notice that calling `[]` index access as a code smell, this helps you avoid bounding errors!
## Threadability
Pretty much all about avoid sharing state.
1. Stop using global variables
2. Stop using statics
3. Reduce shared pointer usage

## Performance
Use initialiser lists, far less copies and allocations!
```cpp
std::vector<int> a{1,2,3};
// instead of pushing back
```

Avoid needless copies! An `=` outside of the initial initialisations means **COPY** assignment.
- Can avoid with ternary or lambda assignments.

Prefer double to float, as we're on 64, honestly depends on the hardware.

On `++i vs i++`
- `i++` returns a copy old value, and does the increment
- `++i` just returns the value with no copy

Just use lambas not binds!

For utility functions you can directly indicate inplace initialisation with `std::in_place`
## Appendix
<https://lefticus.gitbooks.io/cpp-best-practices/content/>