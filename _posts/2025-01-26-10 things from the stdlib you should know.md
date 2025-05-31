No one really uses the whole span of any standard library but theres going to be the top 20% of libraries you use all the time, what are they and what do you need to know here.
## General utilities
#### Optional
#### Expected
#### Variant
#### `std::numeric_limits`
## Views
<https://hackingcpp.com/cpp/cheat_sheets.html >
#### `std::string_view`
For your functions, if you want read only access, use a string view, if not use a reference! Means you won't have any copies!
- Just use it as a function param, `std::string_view sv = std::string("yo")` will explode.

#### `std::span`
Span is just the generic read only version of string view, nothing special.
- Lets you avoid function parameter copies.
- But also spans will directly point to the memory, a reference points to the container which points to the memory, so can be faster.
- Never return a view!
```cpp
void print_ints(std::span<int> s) {
     for (auto i : s) {
         std::cout << i << ",";
     }
 }

 int main(){
     std::vector<int> v{1,2,3,4};
     print_ints(v);
 }
```

## Ranges

## Algorithms
<https://hackingcpp.com/cpp/std/algorithms.html>
#### Non modifying
You never really need to do a for loop to do these kind of checks
```cpp
int main(){
     std::vector<int> v{1,2,3,4};
     auto even = [](int i){
         return (i%2 == 0);
     };

     std::cout << "any even: " <<  std::ranges::any_of(v, even) << "\n";
     std::cout << "all even: " <<  std::ranges::all_of(v, even) << "\n";
     std::cout << "none even: " <<  std::ranges::none_of(v, even) << "\n";
     std::cout << "how many even: " <<  std::ranges::count_if(v, even) << "\n";
 }
```

and of course theres
- finds, just scanning
- finds, assuming span is sorted (binary search)
- range comparisons

And snazzy for each functions!
```cpp
int main(){
     std::vector<int> v{1,2,3,4};
     auto p = [](int i){
         std::cout << i << ",";
     };

     for_each(v.begin(), v.end(), p);
 }
```
#### Reordering
Mainly just rotating and partitioning could be useful here.
```cpp
 void p(std::span<int> s, std::string_view ss) {
     std::cout << ss << " ";
     for(auto i : s) {
         std::cout << i << ",";
     }
     std::cout << "\n";
 }

 int main(){
     std::vector<int> v{1,2,3,4};

     reverse(v.begin(), v.end());
     p(v, "reversing:");

     rotate(v.begin(), v.begin() + 1, v.end());
     p(v, "rotating:");

     partition(v.begin(), v.end(), [](int i){return (i%2 == 0);});
     p(v, "even paritioning:");
 }
```
#### Mutating
transform, reducing and doing both!
- Use `st::execution::par_unseq` to vectorise your compute! This is the SSE and AVE SIMD stuff!

```cpp
 void p(std::span<int> s, std::string_view ss) {
     std::cout << ss << " ";
     for(auto i : s) {
         std::cout << i << ",";
     }
     std::cout << "\n";
 }

 int main(){
     std::vector<int> v{1,2,3,4};

     std::transform(v.begin(), v.end(), v.begin(),[](int i){return i*2;});
     p(v, "transform:");

     auto a = std::reduce(v.begin(), v.end(), 0,
                          [](int l, int r){return l+r;});
     std::cout << "reducing: " << a << "\n";

     auto b = std::transform_reduce(v.begin(), v.end(), 0,
                                    [](int l, int r){return l+r;},
                                    [](int i){return i*2;});
     std::cout << "both: " << b << "\n";
 }
```
## Strings and Text
#### Formatting with print
## Appendix

```
Things not immediately doing
## Concurrency
## Containers
## Input/Output
## Regex
```

<https://hackingcpp.com/cpp/cheat_sheets.html>
