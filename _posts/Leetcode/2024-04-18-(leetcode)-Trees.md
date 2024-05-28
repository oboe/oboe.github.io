<<https://leetcode.com/problems/invert-binary-tree>>
Just recursively swap left and rights.

```cpp
 */
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if(root == nullptr){
            return nullptr;
        }
        TreeNode* l = invertTree(root->left);
        TreeNode* r = invertTree(root->right);
        root->left = r;
        root->right = l;
        return root;
    }
};
```

<<https://leetcode.com/problems/maximum-depth-of-binary-tree>>
Just recursively step downwards.

```cpp
class Solution {
public:
    int maxDepth(TreeNode* root) {
        if (!root) return 0;
        return 1 + max(maxDepth(root->left),maxDepth(root->right));
    }
};
```

<<https://leetcode.com/problems/diameter-of-binary-tree>>
Naive
- Don;t code until I have a plan
- guaranteed that it will pass through the left and right of one node
- So could calculate longest path assuming it goes through 

```cpp
class Solution {
public:
    int ans;
    int diameterOfBinaryTree(TreeNode* root) {
        ans = 0;
        getLongestPath(root);
        return ans;
    }

    int getLongestPath(TreeNode* root){
        if(!root) return 0;
        int l = getLongestPath(root->left);
        int r = getLongestPath(root->right);
        ans = max(ans, l + r);
        return 1 + max(l,r);
    }
};
```

<<https://leetcode.com/problems/balanced-binary-tree>>
Naive
- Are all these questions just going to be depth questions?

Good
- Guess it's just dfs

```cpp
class Solution {
public:
    bool isBalanced(TreeNode* root) {
        bool balanced = true;
        getDepth(root, balanced);
        return balanced;
    }

    int getDepth(TreeNode* root, bool& balanced){
        if(!root) return 0;
        int l = getDepth(root->left, balanced);
        int r = getDepth(root->right, balanced);
        if(balanced && abs(l-r) > 1){
            balanced = false;
        }
        return 1 + max(l,r);
    }
};
```

<<https://leetcode.com/problems/same-tree>>
Simple recursive

```cpp
class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if(p == NULL && q == NULL) return true;
        if(p == NULL || q == NULL) return false;
        if(p->val == q->val && isSameTree(p->left,q->left) && isSameTree(p->right, q->right)){
            return true;
        }
        return false;
    }
};
```

<<https://leetcode.com/problems/subtree-of-another-tree>>
Simple recrusive

```cpp
class Solution {
public:
    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        if(!root && !subRoot) return true;
        if(!subRoot) return true;
        if(isSame(root, subRoot)) return true;
        if(!root) return false;
        return (isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot));
    }

    bool isSame(TreeNode* root, TreeNode* copyRoot) {
        if(!root && !copyRoot) return true;
        if(!root || !copyRoot) return false;
        if(root->val == copyRoot->val){
            return (isSame(root->left,copyRoot->left) && isSame(root->right,copyRoot->right));
        }
        return false;
    }
};
```

<<https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree>>
Naive
- Intuition is that lowest common ancestor of left and right is also lowest common ancestor of root.
- return null if cannot find

Good
- read the question, it's a binary search tree, so it's sorted!

```cpp
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if(root->val > p->val && root->val > q->val){
            return lowestCommonAncestor(root->left,p,q);
        }
        else if(root->val < p->val && root->val < q->val){
            return lowestCommonAncestor(root->right,p,q);
        }
        else{
            return root;
        }
    }
};
```

<<https://leetcode.com/problems/binary-tree-level-order-traversal>>
Naive
- initial impression just BFS
- or could just DFS and keep track of depth at each point so we can append to right vector

```cpp
// recursive dfs
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> ans;
        dfs(root,0,ans);
        return ans;
    }

    void dfs(TreeNode* root, int depth, vector<vector<int>>& ans) {
        if(!root) return;
        if(ans.size() <= depth){
            ans.push_back({});
        }
        ans[depth].push_back(root->val);
        dfs(root->left,depth+1,ans);
        dfs(root->right,depth+1,ans);
    }
};
```

```cpp 
// bfs batched per level
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> ans;
        if(!root) return ans;
        //bfs but each iteration is a level
        deque<TreeNode*> q;
        q.push_back(root);
        while(!q.empty()){
            vector<int> level;
            vector<TreeNode*> newQ;
            for(TreeNode* a: q){
                level.push_back(a->val);
                newQ.push_back(a->left);
                newQ.push_back(a->right);
            }
            q.clear();
            for(auto a : newQ){
                if(a) q.push_back(a);
            }
            ans.push_back(level);
        }

        return ans;
    }
};
```

```cpp
// bfs normal
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> ans;
        if(!root) return ans;
        queue<pair<TreeNode*,int>> q;
        q.push(make_pair(root,0));
        while(!q.empty()){
            pair<TreeNode*,int> curr = q.front(); q.pop();
            if(!curr.first) continue;
            // custom ====
            if(ans.size() <= curr.second){
                ans.push_back({});
            }
            ans[curr.second].push_back(curr.first->val);
            // custom====
            q.push(make_pair(curr.first->left,curr.second+1));
            q.push(make_pair(curr.first->right,curr.second+1));
        }
        return ans;
    }
};
```

```cpp 
// dfs stack, note swapped stack insert right side first!
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> ans;
        if(!root) return ans;
        stack<pair<TreeNode*,int>> q;
        q.push(make_pair(root,0));
        while(!q.empty()){
            pair<TreeNode*,int> curr = q.top(); q.pop();
            if(!curr.first) continue;
            // custom ====
            if(ans.size() <= curr.second){
                ans.push_back({});
            }
            ans[curr.second].push_back(curr.first->val);
            // custom====
            q.push(make_pair(curr.first->right,curr.second+1));
            q.push(make_pair(curr.first->left,curr.second+1));
        }
        return ans;
    }
};
```
<<https://leetcode.com/problems/binary-tree-right-side-view>>
Naive:
- we just need to left tor right order traversal

```cpp
class Solution {
public:
    vector<int> rightSideView(TreeNode* root) {
        vector<int> ans;
        if(!root) return ans;
        queue<pair<TreeNode*,int>> q;
        q.push(make_pair(root,0));
        while(!q.empty()){
            pair<TreeNode*,int> curr = q.front(); q.pop();
            if(!curr.first) continue;
            //==
            if(ans.size() <= curr.second) ans.push_back(0);
            ans[curr.second] = curr.first->val;
            //==
            q.push(make_pair(curr.first->left,curr.second+1));
            q.push(make_pair(curr.first->right,curr.second+1));
        }
        return ans;
    }
};
```

<<https://leetcode.com/problems/count-good-nodes-in-binary-tree>>
Naive
- DFS traversal, maintaining last max state

```cpp
class Solution {
public:
    int goodNodes(TreeNode* root) {
        return dfs(root, INT_MIN);
    }

    // return good nodes
    int dfs(TreeNode* root, int m) {
        if(!root) return 0;
        int ans = 0;
        if(root->val >= m){
            ans = 1;
        }
        int newMax = max(m,root->val);
        return dfs(root->left,newMax) + dfs(root->right,newMax) + ans;
    }
};
```

<<https://leetcode.com/problems/validate-binary-search-tree>>
Naive
- check left and right to root each node?
- Maintain a left and right bound and recursively check

Good
- you don't need to do a left and right check, you can just check the node you're on only

```cpp
class Solution {
public:
    bool isValidBST(TreeNode* root) {
        return dfs(root,LONG_MIN,LONG_MAX);
    }

    bool dfs(TreeNode* root, long l, long r) {
        if(!root) return true;
        if(l >= root->val || r <= root->val){
            return false;
        }
        return dfs(root->left,l,min((long)root->val,r)) && dfs(root->right,max((long)root->val,l),r);
    }
};
```

<<https://leetcode.com/problems/kth-smallest-element-in-a-bst>>
Naive
- unsure
- Its a binary search tree
- I need to get the kth smallest value
- I don't know how many values are in the tree
- guess I can count the number of nodes to get an indication of values larger or smaller than the current node I'm at
- So if the node I'm on has k-1 nodes which are less than it then I know it's the smallest node.
- I'll need left and right counts for this.

Good
- Break it down more, all you need to do is in order traversal

```cpp
class Solution {
public:
    int ans;
    int kthSmallest(TreeNode* root, int k) {
        ans = -1;
        int pos = 0;
        dfs(root,k,pos);
        return ans;
    }

    // return counts
    void dfs(TreeNode* root, int k, int& pos) {
        if(!root) return;
        dfs(root->left,k,pos);
        if(k==pos+1){
            ans = root->val;
        }
        pos++;
        dfs(root->right,k,pos);
    }
};
```


<<https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal>>
Naive
- recursively split preorder and inorder and create the tree
- nothing too surprising just recursive

```cpp
class Solution {
public:
TreeNode* constructTree(vector < int > & preorder, int preStart, int preEnd, vector 
 < int > & inorder, int inStart, int inEnd, map < int, int > & mp) {
    if (preStart > preEnd || inStart > inEnd) return NULL;

    TreeNode* root = new TreeNode(preorder[preStart]);
    int elem = mp[root -> val];
    int nElem = elem - inStart;

    root -> left = constructTree(preorder, preStart + 1, preStart + nElem, inorder,
    inStart, elem - 1, mp);
    root -> right = constructTree(preorder, preStart + nElem + 1, preEnd, inorder, 
    elem + 1, inEnd, mp);

    return root;
}

TreeNode* buildTree(vector < int > & preorder, vector < int > & inorder) {
    int preStart = 0, preEnd = preorder.size() - 1;
    int inStart = 0, inEnd = inorder.size() - 1;

    map < int, int > mp;
    for (int i = inStart; i <= inEnd; i++) {
        mp[inorder[i]] = i;
    }

    return constructTree(preorder, preStart, preEnd, inorder, inStart, inEnd, mp);
    }
};
```
<<https://leetcode.com/problems/binary-tree-maximum-path-sum>>
Naive
- Just dfs with a update single ans value, and passing correct value through the dfs

```cpp
class Solution {
public:
    int ans;
    int maxPathSum(TreeNode* root) {
        ans = INT_MIN;
        maxPathIncludingRoot(root);
        return ans;
    }

    int maxPathIncludingRoot(TreeNode* root) {
        if(!root) return 0;
        int l = maxPathIncludingRoot(root->left);
        int r = maxPathIncludingRoot(root->right);
        //update ans with best passing through root
        int a = root->val;
        a += max(0,l) + max(0,r);
        ans = max(ans,a);
        // return val of highest single path
        int b = root->val;
        b += max(max(l,r),0);
        return b;
    }
};
```

<<https://leetcode.com/problems/serialize-and-deserialize-binary-tree>>
Naive
- so many ways to do this
- inorder,preorder traversal and rejoin
- quick json encoding? Rely on some kind of standard library
- BST, level encoding, populating the lack of nodes with nulls
- preorder traversal with blocking nulls to indicate dead ends
