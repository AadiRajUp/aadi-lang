NO AI OR EVEN GOOGLE WAS USED TO CREATE THIS PROJECT
EVERYTHING WAS BUILT USING THE CONCEPTS LEARNT IN THEORY OF COMPUTATION (TOC ENCT-203)

This is the reason why prolly most stuff I did are wildly ineffecient, non-sacalble and bad code. (and this was coded in at most a day)

This is me trying to create and implemet a 
1) Working Lexer
2) Working Parser ( which parses in my own format )
3) Working Evaluater

This Currently can only "Interpret" simple arithmetic operations.
As of currently addition, subtraction, multiplication, division and assignment are supported

You can create and Use variables, but thats about it.

I hope I continue on this.

(days later)

Yayy I continued it.

It was pointed out to me that my variable declatration system and arithmetic evaluation system collapses when 
int a = -2; is written, it couldnt handle -ve numbers (thx mandip). 
finally that has been fixed.
now int a = -2; behaves as int a = 0 - 2; so all is well

the by product of this is that a = 5+ - + - + - 5 = 10

April 30 15:45
(yes aaba dekhi date ni halxu lol)
2 hrs later 
boolean expression added 0= false 1 = true
unary statements chai evaluate garna sakdaina like !a a++ etc etc, but i have a dream ( and a theory)