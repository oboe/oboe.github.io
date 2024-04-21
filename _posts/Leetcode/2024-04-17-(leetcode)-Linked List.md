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

https://leetcode.com/problems/copy-list-with-random-pointer/description/

https://leetcode.com/problems/add-two-numbers/description/

https://leetcode.com/problems/linked-list-cycle/description/

https://leetcode.com/problems/find-the-duplicate-number/description/

https://leetcode.com/problems/lru-cache/description/

https://leetcode.com/problems/merge-k-sorted-lists/description/

https://leetcode.com/problems/reverse-nodes-in-k-group/description/