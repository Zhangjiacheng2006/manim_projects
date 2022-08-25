/*
这是一份AC自动机的代码，字符集为所有小写英文字母。
仅供参考
*/
#include<queue>
#include<string>
using namespace std;
const int MAXN=1000000;
struct NACAM{
	int val; NACAM *fail,*nxt[26];
}pool[MAXN],*bdN=&pool[0],*rt=bdN;
inline NACAM *insert(string str){
	NACAM *u=rt;
	for(auto c:str){
		if(!u->nxt[c-'a'])
			u->nxt[c-'a']=++bdN;
		u=u->nxt[c-'a'];
	}
	u->val=1; return u;
}
inline void buildACAM(string str){
	queue<NACAM*> q; rt->fail=rt;
	for(int i=0;i<26;i++){
		if(rt->nxt[i]){
			rt->nxt[i]->fail=rt;
			q.push(rt->nxt[i]);
		}
		else rt->nxt[i]=rt;
	}
	while(!q.empty()){
		NACAM *p=q.front();q.pop();
		for(int i=0;i<26;i++){
			if(p->nxt[i]){
				p->nxt[i]->fail=p->fail->nxt[i];
				q.push(p->nxt[i]);
			}
			else p->nxt[i]=p->fail->nxt[i];
		}
	}
}
inline bool judge(string str){
	NACAM *u=rt;
	for(auto c:str){
		u=u->nxt[c-'a'];
		if(!u) break;
	}
	return u->val;
}
