# moving_charges

#DESCRIPTION
In this program, you can choose any amount of point charges, each with a charge, initial position and initial velocity. After inputting your desired initial conditions, a simulation runs which animates the interactions between the charges as time passes by. The electric field created by the moving particles is also shown. Simply download the program, run the code, input your desired values and wait for the animation to save (The code I created is pretty slow, so if you have a slower computer wait for the animation to save to a GIF file and watch that instead of the real-time animation).

#REQUIRED LIBRARIES:
Numpy
Matplotlib
Pillow

#DETAILS
The user is asked to input values for each charge, until he exits the prompt. Each point charge is then stored as an object with an assigned charge as well as initial positions and velocities. Two main functions doing the calculations exist, one which updates the positions of each particle over a time interval dt (position_Charge()), and one which updates the electric field over dt (calculate_Field()). These functions are called each time in an update function (update_Movement()) which is passed through FuncAnimation. The animation is downloaded as a GIF file before being showed on a real-time plot.

#POSSIBLE IMPROVEMENTS
I found my code to be very slow, because both the functions doing the calculations have time complexity O(n^2), given that there are two iterations in each function. The program therefore gets slower and slower the more charges you add and the more electric field patterns you display, as well as the longer you choose the animation to run. A possible solution is to use NumPy arrays. I also noted that in my update_Movement() function, I have to clear the axis for each iteration so that the new positions and field lines don't stack over each other. It works but I think a better approach would be to update the positions of the charges and electric field lines (each vector) in real time instead of recalculating and redisplaying the charges and field lines (vectors) every time.
