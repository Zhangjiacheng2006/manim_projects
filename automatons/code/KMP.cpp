/*
这是一份KMP的代码，字符集为所有可以被char储存的字符。
仅供参考
*/
#include<string>
#include<cstring>
using namespace std;
const int MAXN=1000000;
int fail[MAXN],N; char ostr[MAXN];
inline void buildKMP(string str){
	N=str.length();int f;
	fail[0]=fail[1]=0; ostr[0]=str[0];
	for(int i=1;i<N;i++){
		ostr[i]=str[i]; f=fail[i];
		while(str[i]!=str[f]&&f)
			f=fail[f];
		fail[i+1]=(str[i]==str[f]?f+1:0);
	}
	ostr[N]='\0';
}
inline bool judge(string str){
	int u=0;
	for(auto c:str){
		while(c!=ostr[u]&&u)
			u=fail[u];
		u=(c==ostr[u]?u+1:0);
	}
	return u==N;
}
