/*
这是一份字典树的代码，字符集为所有小写英文字母。
仅供参考
*/
#include<string>
using namespace std;
const int MAXN=1000000;
struct NTrie{
	int val; NTrie *nxt[26];
}pool[MAXN],*bdN=&pool[0],*rt=bdN;
inline NTrie *insert(string str){
	NTrie *u=rt;
	for(auto c:str){
		if(!u->nxt[c-'a'])
			u->nxt[c-'a']=++bdN;
		u=u->nxt[c-'a'];
	}
	u->val=1; return u;
}
inline bool judge(string str){
	NTrie *u=rt;
	for(auto c:str){
		u=u->nxt[c-'a'];
		if(!u) break;
	}
}
