#Import required libraries and objects
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from objects import Store_Charges

#CONSTANTS
K = 9 * np.pow(10, 9)
E = 1.6 * np.pow(1 / 10, 19) #Charge of an electron
M = 9.1093837015 * np.pow(1 / 10, 31) #We assume each charge weighs the same as an electron

#VARIABLES
stop = False
count = 0

num_vectors = 40 #Number of vectors in the electric field
max_bound = num_vectors // 2 #Max bounds of the figure

#Declare the time variables
s = 10 #Amount of seconds
frames = 300 #Total frames, fps will then be frames / s
t = np.linspace(0, s, frames) #Match the time variable with seconds and frames
t_span = (0, s)

dt = s / frames #Delta time

#Initialize charge storage
charge_Storage = Store_Charges()

#Create user input for each point charge
print('Welcome to moving point charges! \n')
while stop == False:
    valid = False
    while valid == False:
        print(f'Input information for charge {count+1}:')
        rerun = False

        #Input charge and coordinates to test
        try:
            print('Charge (+ or - value): ', end = '')
            charge = float(input())

            print(f'Coordinate X ({-max_bound} <= X <= {max_bound}): ', end = '')
            x = float(input())
            if (not -max_bound <= x <= max_bound):
                print(f'X-Coordinates provided are out of bounds. Please choose between {-max_bound} and {max_bound} meters. \n')
                rerun = True
                x = float('STOP')

            print(f'Coordinate Y ({-max_bound} <= Y <= {max_bound}): ', end = '')
            y = float(input())
            if (not -max_bound <= y <= max_bound):
                print(f'Y-Coordinates provided are out of bounds. Please choose between {-max_bound} and {max_bound} meters. \n')
                rerun = True
                x = float('STOP')
                

            print('Velocity in X-direction: ', end = '')
            vx = float(input())

            print('Velocity in Y-direction: ', end = '')
            vy = float(input())

        except:
            if rerun == False:
                print("You can only input a float number! \n")

        else:
            valid = True

    #Add values after validity passed
    charge_Storage.add_Charge(charge, [x, y], [vx, vy])

    #Ask if user wants to add another charge
    valid = False
    while valid == False:
        print('Would you like to add another charge? (Y/N): ', end = '')
        choice = str(input())
        if choice == 'N':
            stop = True
            valid = True
        elif choice == 'Y':
            count += 1
            print('')
            valid = True
        else:  
            print('You can either choose "Y" or "N"! \n')

#Function that calculates position at any given instant
def position_Charge():
    global dt
    charges = charge_Storage.Charge_Arr
    for i in range(charge_Storage.count):
        Fx = 0
        Fy = 0
        Ax = 0
        Ay = 0
        
        vx = charges[i].velocity[0]
        vy = charges[i].velocity[1]

        #Calculate the electrostatic force due to every other charge
        for k in range(charge_Storage.count):
            if charges[i] != charges[k]:
                x_dist = charges[k].position[0] - charges[i].position[0]
                y_dist = charges[k].position[1] - charges[i].position[1]
                r = np.sqrt(x_dist**2 + y_dist**2)

                if -0.1 <= x_dist <= 0.1:
                    dFx = 0
                else:
                    dFx = - K * E**2 * (charges[i].charge * charges[k].charge) / (r**2) * (x_dist / r)

                if -0.1 <= y_dist <= 0.1:
                    dFy = 0
                else:
                    dFy = - K * E**2 * (charges[i].charge * charges[k].charge) / (r**2) * (y_dist / r)

                Fx += dFx
                Fy += dFy

                Ax = Fx / M
                Ay = Fy / M

        dx = vx * dt + 0.5 * Ax * dt**2
        dy = vy * dt + 0.5 * Ay * dt**2

        charge_Storage.Charge_Arr[i].velocity[0] += Ax * dt
        charge_Storage.Charge_Arr[i].velocity[1] += Ay * dt

        charge_Storage.Charge_Arr[i].position[0] += dx
        charge_Storage.Charge_Arr[i].position[1] += dy

#Initialize function that calculates the electric field
def calculate_Field():
    #Create the meshgrid for all the vectors in the electric field (vector field)
    global num_vectors, max_bound
    
    x = np.linspace(-max_bound, max_bound, num_vectors*2)
    y = np.linspace(-max_bound, max_bound, num_vectors*2)

    X, Y = np.meshgrid(x, y)

    E_X = np.zeros_like(X)
    E_Y = np.zeros_like(Y)
    
    #Calculate the electric field for each vector
    for i in range(len(x)):
        for j in range(len(y)):
            net_X = 0
            net_Y = 0

            #Iterate through each point charge
            for point_charge in charge_Storage.Charge_Arr:
                #Find the distance between the vector and each point charge
                x_dist = x[i] - point_charge.position[0]
                y_dist = y[j] - point_charge.position[1]
                r = np.sqrt(x_dist**2 + y_dist**2)

                q = point_charge.charge

                if (x_dist == 0):
                    dEx = 0
                else:
                    dEx = (K * q) / (r**2) * (x_dist / (r))

                if (y_dist == 0):
                    dEy = 0
                else:
                    dEy = (K * q) / (r**2) * (y_dist / (r))

                net_X += dEx
                net_Y += dEy

            E_X[j, i] = net_X
            E_Y[j, i] = net_Y

    #Plot the vectors as a streamplot
    ax.streamplot(X, Y, E_X, E_Y, density = 1)

    #Plot each point charge
    for point_charge in charge_Storage.Charge_Arr:
        charge_x = point_charge.position[0]
        charge_y = point_charge.position[1]
        charge_val = point_charge.charge

        #Assign point charge color depending on charge
        if charge_val > 0:
            charge_color = 'red'
        elif charge_val < 0:
            charge_color = 'blue'
        else:
            charge_color = 'green'

        #Plot the charge and its info
        plt.plot(charge_x, charge_y, 'o', color=f'{charge_color}', markersize = 10)
        plt.text(charge_x, charge_y+1, f'{charge_val} C', color = f'{charge_color}', fontsize = 12, ha = 'center', va = 'baseline', fontweight = 'bold')

#Setup the plot
electric_field, ax = plt.subplots()

#Setup the function updating the coordinates of each charge
def update_movement(frame):
    ax.clear()
    ax.set_title('Moving point charges')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_xlim(-max_bound, max_bound)
    ax.set_ylim(-max_bound, max_bound)
    ax.set_aspect('equal')

    calculate_Field()
    position_Charge()

#Animate the moving charges
ani = FuncAnimation(electric_field, update_movement, frames = len(t), interval = ((s / frames) * 1000), blit = False)
ani.save('animation.gif', writer = 'Pillow')
plt.show()






