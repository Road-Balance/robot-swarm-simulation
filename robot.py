import math

class Robot:
    def __init__(self, x=0, y=0, dir=0):
        self.x = x
        self.y = y
        self.dir = dir
        self.speed_linear = 0.1
        self.speed_angular = 5
        self.range = 15
        self.fov = 45

    #move each robots at given speed
    def move(self, v, w):
        self.dir += w*self.speed_angular
        self.dir %= 360
        self.dir += 0 if self.dir>=0 else self.dir+360
        self.x += v*self.speed_linear*math.cos(math.radians(self.dir))
        self.y += v*self.speed_linear*math.sin(math.radians(self.dir))

    #works as lidar detection
    def detect(self, robots):
        dets=list()
        for obj in robots: 
            if obj == self: #Self is the observer.
                continue

            dist_x = obj.x-self.x
            dist_y = obj.y-self.y
            dist = (dist_x**2+dist_y**2)**(0.5)
            
            cosine = math.degrees(math.acos(dist_x/dist))
            if dist_y < 0: cosine = 360-cosine
            angle = cosine-self.dir
            if angle<=-180: angle+=360
            elif angle>180: angle-=360

            if abs(angle)<obj.fov and dist<obj.range: #Object within fov and range
                dets.append(dict(dist=dist, angle=angle))

        return dets

#update simulation
def move_robots(robots):
    m = list()
    for robot in robots:
        dets = robot.detect(robots)

        #main logic
        v, w = (0, 0)
        if not dets:
            w=1
        else:
            avg_dist = sum(d['dist'] for d in dets)/float(len(dets))
            avg_angle = sum(d['angle'] for d in dets)/float(len(dets))

            # simulation parameters
            if avg_dist<2:
                v=0
            elif avg_dist<5:
                v=0.5
            else:               
                v=1
            if avg_angle>25:  
                w=+1
            elif avg_angle<25:  
                w=-1

        m.append(dict(v=v, w=w))

    for i in range(len(robots)):
        robots[i].move(m[i]['v'], m[i]['w'])
