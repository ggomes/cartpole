clear
close all
global m M l g btheta bx

m = 0.2;
M = 0.4;
l = 0.3;
g = 9.8;

btheta = 0.2;
bx = 0.2;

tf = 20;
N = 200;
theta0 = 0.01;
omega0 = 0;
x0 = 0;
v0 = 0;

tspan = [0,tf];
y0 = [theta0, omega0, x0, v0];
[t,y] = ode45(@cartpole,tspan,y0);

figure('Position',[680 35 880 843])
subplot(411)
plot(t,y(:,1),'linewidth',2)
subplot(412)
plot(t,y(:,2),'linewidth',2)
subplot(413)
plot(t,y(:,3),'linewidth',2)
subplot(414)
plot(t,y(:,4),'linewidth',2)

% -------------------------------------------

function f = get_force(t,y)
    f = 0;
end

function yprime = cartpole(t,y)
    global m M l g btheta bx
    
    theta = y(1);
    omega = y(2);
    x     = y(3);
    v     = y(4);

    F = get_force(t,y);
    ct = cos(theta);
    st = sin(theta);

    A = [ct , 4*l/3 ; M+m  ,m*l*ct];
    b = [st*g - btheta*omega ; m*l*st*omega^2+F - bx*v];
        
    sol = A\b;
    
    theta_prime = omega;
    omega_prime = sol(2);
    x_prime = v;
    v_prime = sol(1);
    
    yprime = [theta_prime,omega_prime,x_prime,v_prime]';
end



