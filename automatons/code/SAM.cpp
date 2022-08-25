/*
这是一份后缀自动机的代码，字符集为所有小写英文字母。
仅供参考
*/
#include<string>
using namespace std;
const int MAXN=1000000;
struct NSAM{
	int len,val; NSAM *link,*nxt[26];
}pool[MAXN],*bdN=&pool[0],*rt=bdN,*ed;
inline NSAM *__ins(const int c,NSAM *ed){
	NSAM *u=++bdN,*p=ed;
	u->len=ed->len+1;
	for(;p&&(!p->nxt[c]);p=p->link) p->nxt[c]=u;
	if(!p){ u->link=rt; return u; }
	NSAM *q=p->nxt[c];
	if(p->len+1==q->len){ u->link=q;return u; }
	NSAM *clone=++bdN; clone->link=q->link;
	for(int i=0;i<26;i++) clone->nxt[i]=q->nxt[i];
	clone->len=p->len+1; u->link=q->link=clone;
	for(;p&&p->nxt[c]==q;p=p->link) p->nxt[c]=clone;
	return u;
}
inline NSAM *insert(string str){
	ed=rt; for(auto c:str) ed=__ins(c-'a',ed);
	for(NSAM *p=ed;p;p=p->link) p->val=1;
	return ed;
}
inline bool judge(string str){
	NSAM *u=rt;
	for(auto c:str){
		u=u->nxt[c-'a'];
		if(!u) break;
	}
	return u->val;
}
