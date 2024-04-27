https://leetcode.com/problems/reverse-linked-list/description/
Naive
- Just iterate through

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* last = NULL;
        ListNode* curr = head;
        while(curr != NULL){
            ListNode* l = curr->next;
            curr->next = last;
            last = curr;
            curr = l;
        }
        return last;
    }
};
```
https://leetcode.com/problems/merge-two-sorted-lists/description/

Good
- just zip the lists together

```cpp
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        ListNode* head;
        ListNode* curr;
        if(list1 && list2){
            if(list1->val > list2->val){
                head = list2;
                list2 = list2->next;
            } else{
                head = list1;
                list1 = list1->next;
            }
        } else if (list1){
            head = list1;
            list1 = list1->next;
        } else if (list2){
            head = list2;
            list2 = list2->next;
        } else {
            return head;
        }
        curr = head;
        while(list1 || list2){
            // compare both
            if(list1 && list2){
                if(list1->val > list2->val){
                    curr->next = list2;
                    curr = curr->next;
                    list2 = list2->next;
                } else{
                    curr->next = list1;
                    curr = curr->next;
                    list1 = list1->next;
                }
            } else if (list1){
                curr->next = list1;
                curr = curr->next;
                list1 = list1->next;
            } else {
                curr->next = list2;
                curr = curr->next;
                list2 = list2->next;
            }
        }
        return head;
    }
};
```
https://leetcode.com/problems/reorder-list/description/
Good
- I just dumped everything into a deque
- You can also just reverse and reverse and reverse the list til the end

```cpp
class Solution {
public:
    void reorderList(ListNode* head) {
        ListNode* ans = head;
        ListNode* curr = ans;
        deque<ListNode*> nodes;
        while(head != NULL){
            nodes.push_back(head);
            head = head -> next;
        }
        nodes.pop_front();
        bool flip = false;
        while(!nodes.empty()){
            if(flip){
                curr -> next = nodes.front();
                curr = curr->next;
                nodes.pop_front();
            } else {
                curr -> next = nodes.back();
                curr = curr->next;
                nodes.pop_back();
            }
            flip = !flip;
        }
        curr -> next = nullptr;
        head = ans;
    }
};
```
https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/
Good
- Think about what should happens in the base case
- Think about what happens in a normal case, step through it

```cpp
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        // how long is the list?
        int sz = 0;
        ListNode* c = head;
        while(c !=NULL){
            sz++;
            c = c->next;
        }
        if(sz == n){
            return head->next;
        }
        // step through and remove the node
        ListNode* ans = head;
        ListNode* last = ans;
        for(int i = 1 ; i < sz-n ; i++){
            last = last->next;
        }
        if (last != NULL && last->next != NULL){
            ListNode* n = last->next;
            last -> next = n->next;
        }
        return ans;
    }
};
```

https://leetcode.com/problems/copy-list-with-random-pointer/description/
Good
-Straightforward
- Can improve the find thing: as its nlogn time, n space right now

```cpp
class Solution {
public:
    Node* copyRandomList(Node* head) {
        vector<Node*> nodes;
        Node* curr = head;
        while(curr != NULL){
            nodes.push_back(curr);
            curr = curr->next;
        }
        if (nodes.empty()){
            return NULL;
        }
        vector<Node*> newNodes;
        //create copy
        for(int i = 0 ; i < nodes.size() ;i++){
            newNodes.push_back(new Node(nodes[i]->val));
        }
        //create next links
        for(int i = 0 ; i < nodes.size() -1 ;i++){
            newNodes[i]->next = newNodes[i+1];
        }
        //create random links
        for(int i = 0 ; i < nodes.size() ;i++){
            Node* rand = nodes[i]->random;
            if(rand == NULL){
                newNodes[i]->random = NULL;
            }
            else {
                auto it = find(nodes.begin(),nodes.end(), rand);
                newNodes[i]->random = newNodes[(it - nodes.begin())];
            }
        }
        return newNodes[0];
    }
};
```
https://leetcode.com/problems/add-two-numbers/description/
Naive
- Just pop all from both lists, creating numbers, and add those together

Good
- Read the question properly
- It is a reversed list!
- Also creating a dummy node to avoid dealing with initial NULL is quite nice.

```cpp
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* curr1 = l1;
        ListNode* curr2 = l2;
        ListNode* ans = new ListNode();
        ListNode* curr = ans;
        int carry = 0;
        while(curr1 != NULL || curr2 != NULL){
            int val1 = (curr1 != nullptr) ? curr1->val : 0;
            int val2 = (curr2 != nullptr) ? curr2->val : 0;
            int ansVal = val1 + val2 + carry;
            carry = 0;
            if (ansVal > 9){
                carry = 1;
                ansVal -= 10;
            }
            curr->next = new ListNode(ansVal);
            curr = curr->next;
            if(curr1 != nullptr) curr1 = curr1->next;
            if(curr2 != nullptr) curr2 = curr2->next;
        }
        if(carry){
            curr->next = new ListNode(1);
        }
        return ans->next;
    }
};
```

https://leetcode.com/problems/linked-list-cycle/description/
Naive:
- map

Good
- Floyds tortoise algorithm, have two pointers one moving 2 steps and other making 1 step. Guaranteed that eventually two will have same location if there is a cycle.

```cpp
class Solution {
public:
    bool hasCycle(ListNode *head) {
        unordered_set<ListNode*> st;
        ListNode* curr = head;
        while(curr != NULL){
            if(st.count(curr->next) != 0){
                return true;
            }
            st.insert(curr);
            curr = curr->next;
        }
        return false;
    }
};
```

https://leetcode.com/problems/find-the-duplicate-number/description/

https://leetcode.com/problems/lru-cache/description/

https://leetcode.com/problems/merge-k-sorted-lists/description/

https://leetcode.com/problems/reverse-nodes-in-k-group/description/