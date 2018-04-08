# DSAI_search
##  DSAI hw2, boolean search through news title

---

This project uses trie tree data structure to solve the problem

Build with query text data, each phrase is a subtree of root

Example: if query has "籃球" , "選手"

then the trie will build like this

![image](https://imgur.com/5GZBNDD)


### Functions
* **insert_dic**: insert queries into Trie
* **search_trie**: for each title, do search from the root of trie, if the phrase matches, append the title index into the node list (title list) for further usage
* **boolean_search**: Search for queries again, this time consider the boolean operations, and do the set operations on every title number subsets of each query phrase
