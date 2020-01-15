import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import requests

# Create figure for plotting
# style.use('fivethirtyeight')

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
n = 0
url_labjack = "http://localhost:5000/labjackvalues"

# This function is called periodically from FuncAnimation
def animate(i):
    res = requests.get(url_labjack)
    respdata = res.json()
    print(respdata)
    global n
    global xs
    global ys
    xs.append(n + 1)
    n = n + 1
    ys.append(respdata[0])
    print(xs)
    print(ys)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Real time values of LabJack Controller')
    plt.ylabel('Power Measured')
    # ani = animation.FuncAnimation(fig1, animate, fargs=(xs, ys), interval=1000)
    plt.show()

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, interval=500)
plt.show()