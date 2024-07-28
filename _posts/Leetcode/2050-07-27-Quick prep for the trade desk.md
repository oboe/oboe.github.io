
### Qs
<https://leetcode.com/problems/lru-cache/>
```java
class LRUCache {
    int capacity;
    LinkedHashMap<Integer, Integer> kvMap = new LinkedHashMap<>();

    public LRUCache(int capacity) {
        this.capacity = capacity;
    }
    
    public int get(int key) {
        //get value
        if(!kvMap.containsKey(key)){
            //System.out.printf("GET not found: %d%n", key);
            return -1;
        }
        int val = kvMap.get(key);
        //move value to front
        kvMap.remove(key);
        kvMap.put(key, val);
        return val;
    }
    
    public void put(int key, int value) {
        //put value move value to front
        kvMap.remove(key);
        kvMap.put(key, value);

        //if adding 1, evict last
        if(kvMap.size() > capacity){
            int last = kvMap.firstEntry().getKey();
            kvMap.remove(last);
        }
    }
}

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache obj = new LRUCache(capacity);
 * int param_1 = obj.get(key);
 * obj.put(key,value);
 */
```



### Java map thread safety
Java concurrent
```java
ConcurrentHashMap<Integer, Integer> cmap = new ConcurrentHashMap<>();
// Segments hashmap into n shards each with their own writer lock
```
java collections
```java
Map<Integer,Integer> smap = Collections.synchronizedMap(new HashMap<>());
```
Can use synchronised keyword
```java
synchronized (Object reference_object) {

}
```
You can use locks
```
private final ReentrantLock lock = new ReentrantLock()
lock.lock()
try{}finally{
	lock.unlock();
}
```

