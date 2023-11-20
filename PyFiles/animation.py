import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import time

# Create figure for plotting
fig, (ax1, ax2) = plt.subplots(2)
xs = []
ys = []

xs2 = []
ys2 = []


# This function is called periodically from FuncAnimation
def animate(i, xs, ys, xs2, ys2):

    # Read temperature (Celsius) from TMP102

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(math.sin(time.time()))

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Add x and y to lists
    xs2.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys2.append(math.cos(time.time()))

    # Limit x and y lists to 20 items
    xs2 = xs2[-20:]
    ys2 = ys2[-20:]

    # Draw x and y lists
    ax1.clear()
    ax1.plot(xs, ys)

    ax2.clear()
    ax2.plot(xs2, ys2)

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, xs2, ys2), interval=10)
fig.suptitle("Atrial Graph")
plt.show()