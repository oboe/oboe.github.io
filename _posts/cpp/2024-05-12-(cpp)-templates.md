
You can specify templates to make your functions generic 
```cpp
template<typename T>
T square(T x) {
	return x*x;
}

//this stuff actually calls two different functions!
square(5);
square(5.5);
```
