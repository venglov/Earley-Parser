# Earley-parser (dev)

Na pewno działa na python 3.7.9\
Przykładowe inputy oraz outputy. Proszę żeby ktoś ogarnięty to sprawdził. W razie problemów proszę się kontaktować.

![Earley-parser%20d9476b0cb9174a8fb3cadd26920c712b/Untitled.png](Earley-parser%20d9476b0cb9174a8fb3cadd26920c712b/Untitled.png)

S'->.S [0, 0]  sytuacja startowa\
S->.aXbX [0, 0]  przewidywanie\
S->.abX [0, 0]  przewidywanie\
S->.aXb [0, 0]  przewidywanie\
S->.ab [0, 0]  przewidywanie

i=1\
S->a.XbX [0, 1]  wczytanie\
S->a.bX [0, 1]  wczytanie\
S->a.Xb [0, 1]  wczytanie\
S->a.b [0, 1]  wczytanie\
X->.aY [1, 1]  przewidywanie\
X->.bY [1, 1]  przewidywanie\
X->.a [1, 1]  przewidywanie\
X->.c [1, 1]  przewidywanie

i=2\
S->ab.X [0, 2]  wczytanie\
S->ab. [0, 2]  wczytanie\
X->b.Y [1, 2]  wczytanie\
X->.aY [2, 2]  przewidywanie\
X->.bY [2, 2]  przewidywanie\
X->.a [2, 2]  przewidywanie\
X->.c [2, 2]  przewidywanie\
S'->S. [0, 2]  uzupelnienie\
Y->.X [2, 2]  przewidywanie\
Y->.c [2, 2]  przewidywanie

i=3\
X->a.Y [2, 3]  wczytanie\
X->a. [2, 3]  wczytanie\
Y->.X [3, 3]  przewidywanie\
Y->.c [3, 3]  przewidywanie\
Y->X. [2, 3]  uzupelnienie\
S->abX. [0, 3]  uzupelnienie\
X->.aY [3, 3]  przewidywanie\
X->.bY [3, 3]  przewidywanie\
X->.a [3, 3]  przewidywanie\
X->.c [3, 3]  przewidywanie\
X->bY. [1, 3]  uzupelnienie\
S'->S. [0, 3]  uzupelnienie\
S->aX.bX [0, 3]  uzupelnienie\
S->aX.b [0, 3]  uzupelnienie

i=4\
Y->c. [3, 4]  wczytanie\
X->c. [3, 4]  wczytanie\
X->aY. [2, 4]  uzupelnienie\
Y->X. [3, 4]  uzupelnienie\
Y->X. [2, 4]  uzupelnienie\
S->abX. [0, 4]  uzupelnienie\
X->bY. [1, 4]  uzupelnienie\
S'->S. [0, 4]  uzupelnienie\
S->aX.bX [0, 4]  uzupelnienie\
S->aX.b [0, 4]  uzupelnienie

![Earley-parser%20d9476b0cb9174a8fb3cadd26920c712b/Untitled%201.png](Earley-parser%20d9476b0cb9174a8fb3cadd26920c712b/Untitled%201.png)

S'->.S [0, 0]  sytuacja startowa\
S->.aSa [0, 0]  przewidywanie\
S->.bSb [0, 0]  przewidywanie\
S->.A [0, 0]  przewidywanie\
A->.a [0, 0]  przewidywanie\
A->.b [0, 0]  przewidywanie

i=1\
S->[a.Sa](http://a.sa/) [0, 1]  wczytanie\
A->a. [0, 1]  wczytanie\
S->.aSa [1, 1]  przewidywanie\
S->.bSb [1, 1]  przewidywanie\
S->.A [1, 1]  przewidywanie\
S->A. [0, 1]  uzupelnienie\
A->.a [1, 1]  przewidywanie\
A->.b [1, 1]  przewidywanie\
S'->S. [0, 1]  uzupelnienie

i=2\
S->[a.Sa](http://a.sa/) [1, 2]  wczytanie\
A->a. [1, 2]  wczytanie\
S->.aSa [2, 2]  przewidywanie\
S->.bSb [2, 2]  przewidywanie\
S->.A [2, 2]  przewidywanie\
S->A. [1, 2]  uzupelnienie\
A->.a [2, 2]  przewidywanie\
A->.b [2, 2]  przewidywanie\
S->aS.a [0, 2]  uzupelnienie

i=3\
S->[a.Sa](http://a.sa/) [2, 3]  wczytanie\
A->a. [2, 3]  wczytanie\
S->aSa. [0, 3]  wczytanie\
S->.aSa [3, 3]  przewidywanie\
S->.bSb [3, 3]  przewidywanie\
S->.A [3, 3]  przewidywanie\
S->A. [2, 3]  uzupelnienie\
S'->S. [0, 3]  uzupelnienie\
A->.a [3, 3]  przewidywanie\
A->.b [3, 3]  przewidywanie\
S->aS.a [1, 3]  uzupelnienie

![Earley-parser%20d9476b0cb9174a8fb3cadd26920c712b/Untitled%202.png](Earley-parser%20d9476b0cb9174a8fb3cadd26920c712b/Untitled%202.png)

S'->.E [0, 0]  sytuacja startowa\
E->.T [0, 0]  przewidywanie\
E->.E+T [0, 0]  przewidywanie\
T->.P [0, 0]  przewidywanie\
T->.T*P [0, 0]  przewidywanie\
P->.a [0, 0]  przewidywanie

i=1\
P->a. [0, 1]  wczytanie\
T->P. [0, 1]  uzupelnienie\
E->T. [0, 1]  uzupelnienie\
T->T.*P [0, 1]  uzupelnienie\
S'->E. [0, 1]  uzupelnienie\
E->E.+T [0, 1]  uzupelnienie

i=2\
E->E+.T [0, 2]  wczytanie\
T->.P [2, 2]  przewidywanie\
T->.T*P [2, 2]  przewidywanie\
P->.a [2, 2]  przewidywanie

i=3\
P->a. [2, 3]  wczytanie\
T->P. [2, 3]  uzupelnienie\
E->E+T. [0, 3]  uzupelnienie\
T->T.*P [2, 3]  uzupelnienie\
S'->E. [0, 3]  uzupelnienie\
E->E.+T [0, 3]  uzupelnienie

i=4\
T->T*.P [2, 4]  wczytanie\
P->.a [4, 4]  przewidywanie

i=5\
P->a. [4, 5]  wczytanie\
T->T*P. [2, 5]  uzupelnienie\
E->E+T. [0, 5]  uzupelnienie\
T->T.*P [2, 5]  uzupelnienie\
S'->E. [0, 5]  uzupelnienie\
E->E.+T [0, 5]  uzupelnienie\
