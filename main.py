import math
import keyboard

from random import uniform
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from robot import Robot, move_robots

def draw_robot(ax, robot):
    circle = plt.Circle((robot.x, robot.y), color='r', radius=0.5, fill=False)
    ax.add_patch(circle)
    ax.plot(robot.x, robot.y, 'o', color='black')
    dir_rad = math.radians(robot.dir)
    ax.plot((robot.x, robot.x+math.cos(dir_rad)), (robot.y, robot.y+math.sin(dir_rad)), color='r')

def animate(i, robots):
    move_robots(robots)

    ax.cla()
    ax.set(xlim=[0, 20], ylim=[0, 20])
    
    for robot in robots:
        draw_robot(ax, robot)

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(9, 9))
    robots = [Robot(uniform(3,17),uniform(3,17),uniform(0,360)) for i in range(40)]


    ani = FuncAnimation(fig, lambda i : animate(i, robots), interval=100)

    plt.show()

