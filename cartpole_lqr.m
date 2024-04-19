clear
close all

m = 0.2;
M = 0.4;
l = 0.3;
g = 9.8;

% LQR
d = m*l - (4/3)*l*(M+m);
A = [0,1,0,0;-(M+m)*g/d,0,0,0;0,0,0,1;m*l*g/d,0,0,0];
b = [0;1/d;0;-(4/3)*l/d];
Q = eye(4);
R = 1;
[K,S,P] = lqr(A,b,Q,R,0);

K