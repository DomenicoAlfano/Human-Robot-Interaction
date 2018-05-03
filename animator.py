import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import numpy as np

plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'

def mapCreator():

    Grid = np.zeros((32,32),dtype = int)

    Grid = np.matrix(Grid)

    # Walls

    Grid[:2,:] = 1

    Grid[:,:2] = 1

    Grid[-2:,:] = 1

    Grid[:,-2:] = 1

    Grid[-2:,14:18] = 0

    Grid[6:,12:14] = 1

    Grid[6:8,6:14] = 1

    Grid[18:,18:20] = 1

    Grid[18:20,18:26] = 1

    Grid[16:18,:8] = 1

    Grid[2:6,22:24] = 1

    Grid[12:14,22:30] = 1

    Grid[10:12,22:24] = 1

    # Tables

    Grid[21:27,5:8]= 2

    Grid[2:5,27:30] = 3

    Grid[9:12,27:30] = 4

    Grid[20:25,21:23] = 5

    Grid[22,20] = 6

    # Customers

    Grid[26,6] = 7

    Grid[21,6] = 7

    return Grid


class planReader():

    def __init__(self, plan_file, q):

        self.file = plan_file

        self.q = np.asarray(q)

    def getState(self):

        return self.q.T

    def read(self):


        with open(self.file) as f:

            content = f.readlines()

            for l in content:

                action = l.split()[-3:]

                if 'moveup' in l:

                    x = int(action[0].replace('x',''))

                    y = int(action[2].replace('y','').replace(')',''))

                    self.q= np.vstack((self.q, np.asarray([x,y])))

                elif 'moveright' in l:

                    x = int(action[1].replace('x',''))

                    y = int(action[2].replace('y','').replace(')',''))

                    self.q= np.vstack((self.q, np.asarray([x,y])))

                elif 'moveleft' in l:

                    x = int(action[1].replace('x',''))

                    y = int(action[2].replace('y','').replace(')',''))

                    self.q= np.vstack((self.q, np.asarray([x,y])))

                elif 'movedown' in l:

                    x = int(action[0].replace('x',''))

                    y = int(action[2].replace('y','').replace(')',''))

                    self.q= np.vstack((self.q, np.asarray([x,y])))

                else:

                    stop_frame = 10

                    for i in range(stop_frame):

                        try :

                            q_stop = self.q[-1:][0]

                            self.q= np.vstack((self.q, q_stop))

                        except ValueError:

                            q_stop = self.q

                            self.q= np.vstack((self.q, q_stop))


class Animator(object):

    def __init__(self, plan_name,q):

        self.fig = plt.figure()

        self.ax = self.fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, 31), ylim=(0, 31))
        self.ax.grid(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.reader = planReader(plan_name,q)

        self.reader.read()

        self.q = self.reader.getState()

        self.line, = self.ax.plot([], [], 's-', lw=2)

        self.num_frame = self.reader.q.shape[0]

    def init_animator(self):

        self.line.set_data([], [])

        return self.line,

    def animate(self, i):

        self.line.set_data(self.q[0][i], self.q[1][i])

        if i == self.num_frame - 1:

            plt.close()

        return self.line,

    def plotter(self):

        self.animate(0)

        ani = animation.FuncAnimation(self.fig, self.animate, frames=self.num_frame, interval=100, blit=True)

        map = plt.imshow(np.flipud(mapCreator()))

        plt.show()

    def saver(self, episode):

        Writer = animation.writers['ffmpeg']

        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

        plt.title("Episode : " + str(episode + 1))

        ani = animation.FuncAnimation(self.fig, self.animate, frames=self.num_frame, interval=100, blit=True)

        ani.save('FinalTrajectory.mp4', writer=writer)
