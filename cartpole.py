import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.animation as animation

m = 0.2
M = 0.4
l = 0.3
g = 9.8

btheta = 0.2
bx = 0.2

tf = 20
N = 200
theta0 = 0.1
omega0 = 0*np.pi
x0 = 1 
v0 = 0

def get_force(t,y):
    f = 0
    # K = np.array([18.15,3.5,1.0,1.87])
    # f = np.sum(K*y)
    return f

def cartpole(t,y):
    theta, omega, x, v = y
    theta_prime = omega
    x_prime = v

    F = get_force(t,y)
    ct = np.cos(theta)
    st = np.sin(theta)

    A = np.array([[  ct , 4*l/3],
                  [M+m  ,m*l*ct]])
    b = np.array([st*g - btheta*omega,
                  m*l*st*omega**2+F - bx*v])

    sol = np.linalg.inv(A)@b
    v_prime = sol[0]
    omega_prime = sol[1]

    return theta_prime, omega_prime, x_prime, v_prime


sol = solve_ivp( fun=cartpole,                 # the state equation
                 t_span=[0,tf],                # initial and final time
                 y0=(theta0, omega0, x0, v0),  # initial state
                 t_eval=np.linspace(0,tf,N))   # evaluation instants

t = sol.t
theta = sol.y[0,:]
omega = sol.y[1,:]
x = sol.y[2,:]
v = sol.y[3,:]

fig, ax = plt.subplots(figsize=(6,8),nrows=4,sharex=True)
ax[0].plot(t,theta)
ax[0].set_ylabel('theta',fontsize=16)
ax[0].grid()
ax[1].plot(t,omega,label='omega')
ax[1].set_ylabel('omega',fontsize=16)
ax[1].grid()
ax[2].plot(t,x,label='x')
ax[2].set_ylabel('x',fontsize=16)
ax[2].grid()
ax[3].plot(t,v,label='v')
ax[3].set_ylabel('v',fontsize=16)
ax[3].grid()

################################
# ANIMATION
################################

cart_width  = 0.2
cart_height = 0.2

def update_fig(frame):
    theta = sol.y[0,frame]
    x = sol.y[2,frame]
    cart.set_x(x-cart_width/2)
    rod.set_data([x,x+l*np.sin(theta)],[0,l*np.cos(theta)])
    text.set_text(f't={sol.t[frame]:.2f} sec')

fig, ax = plt.subplots(figsize=(10,5))

ax.axhline(0,color='gray',linewidth=3)
cart_rect =  Rectangle((x[0]-cart_width/2,-cart_height/2), cart_width, cart_height,color='gray') 
cart = ax.add_patch(cart_rect)
rod, = ax.plot([x[0],x[0]+l*np.sin(theta[0])],[0,l*np.cos(theta[0])],linewidth=3)
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
text = ax.text(1,1,f't=0 sec',fontsize=20)

ax.spines[:].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

ani = animation.FuncAnimation(fig=fig, func=update_fig, 
                              frames=len(sol.t), 
                              interval=1000*tf/N)

plt.show()



