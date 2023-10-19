import math
import cv2 as cv

from point import Point

def angle_between_vectors(a1, a2, b1, b2):

    ax = a2.x - a1.x
    ay = a2.y - a1.y 
    bx = b2.x - b1.x
    by = b2.y - b1.y

    ab = ax*bx + ay*by
    a = a1.dist_to(a2)
    b = b1.dist_to(b2)

    if a*b == 0:
        return 360
    else:
        cos = round(ab / (a * b), 5)
        # print(f"angle = {math.acos(cos)*180/math.pi}")
        return math.acos(cos)*180/math.pi

# def angle_between_vectors(a1, a2, b1, b2):

#     ax = a2.x - a1.x
#     ay = a2.y - a1.y 
#     bx = b2.x - b1.x
#     by = b2.y - b1.y

#     normA = (ax ** 2 + ay ** 2) ** 0.5
#     normB = (bx ** 2 + by ** 2) ** 0.5

#     ax = ax / normA
#     ay = ay / normA
#     bx = bx / normB
#     by = by / normB

#     print(ax*bx + ay*by)

#     res = round(ax*bx + ay*by, 5)
#     res = math.asin(res) * 180 /math.pi
    
#     print(f"angle = {res}")
#     assert(res<181)
#     return res

def line_of_sight(a, b, image):

    dx = b.x - a.x
    dy = b.y - a.y

    d = dy - (dx/2)
    x = a.x
    y = a.y

    points = []

    points.append(Point(x, y))
    
    while (x < b.x): 
        
        x=x+1
        
        if(d < 0): 
            d = d + dy  

        else: 
            d = d + (dy - dx)  
            y=y+1

        points.append(Point(x, y))
    
    for i in points:
        if not i.is_empty(image):
            return False

    return True

def Expand(a, delta, goal, a_m, bp, g, CLOSED, image):

    points = midpoint(a, delta)
    
    if a.dist_to(goal) < delta and goal not in points:
        points.append(goal)
    open = []
    
    for point in points:
        if not point.is_empty(image):
            continue
        if bp[(a.x, a.y)] != None and abs(angle_between_vectors(bp[(a.x, a.y)], a, a, point)) > a_m:
            continue
        for close_point in CLOSED:
            if point == close_point and bp[(point.x, point.y)] == close_point:
                continue
        if not line_of_sight(a, point, image):
            continue

        g[(point.x, point.y)] = g[(a.x, a.y)] + a.dist_to(point)
        open.append(point)
    return open

def midpoint(point: Point, r: int):

    points = []
    x_centre = point.x
    y_centre = point.y

    x = r
    y = 0
    points.append(Point(x + x_centre, y + y_centre))
    if r > 0:
        points.append(Point(x + x_centre, -y + y_centre))
        points.append(Point(y + x_centre, x + y_centre))
        points.append(Point(-y + x_centre, x + y_centre))
	
    P = 1 - r 

    while x > y:
	
        y += 1
        if P <= 0: 
            P = P + 2 * y + 1
			
        else:		 
            x -= 1
            P = P + 2 * y - 2 * x + 1
		
        if (x < y):
            break
		
        points.append(Point(x + x_centre, y + y_centre))
        points.append(Point(-x + x_centre, y + y_centre))
        points.append(Point(x + x_centre, -y + y_centre))
        points.append(Point(-x + x_centre, -y + y_centre))
		
        if x != y:
            points.append(Point(y + x_centre, x + y_centre))
            points.append(Point(-y + x_centre, x + y_centre))
            points.append(Point(y + x_centre, -x + y_centre))
            points.append(Point(-y + x_centre, -x + y_centre))

    return points

def unwindingPath(end, path):

    # global image
    # imgMapSteps = image.copy()


    res = [end]
    current = end
    iterCounter=0
    while path[(current.x, current.y)] != None:
        
        current = path[(current.x, current.y)]
        # imgMapSteps = cv.circle(imgMapSteps, (current.x, current.y), 4, (230,99,240), -1)
        res.append(current)
        # if iterCounter != 0 and iterCounter % 150 == 0:
        #     plt.imshow(imgMapSteps)
        #     plt.show()
        iterCounter += 1
    
    res.reverse()

    return res

def LIAN(start, end, delta, a_m, image):

    OPEN = []
    CLOSE = []
    bp = {}
    bp[(start.x, start.y)] = None
    g = {}
    g[(start.x, start.y)] = 0

    current_point = None

    OPEN.append(start)

    iterCounter = 0

    imgMapSteps = image.copy()
    while len(OPEN) > 0:
        s = sorted(OPEN, key=lambda x: x.priority)
        a = sorted(OPEN, key=lambda x: x.priority)[0]
        OPEN.remove(a)
        
        imgMapSteps = cv.circle(imgMapSteps, (a.x, a.y), 2, (127, 127, 127), -1)

        bp[(a.x, a.y)] = current_point

        if a == end:
            print("Path found!")
            path = unwindingPath(end, bp)
            return path, imgMapSteps

        CLOSE.append(a)
        imgMapSteps = cv.circle(imgMapSteps, (a.x, a.y), 5, (127,127,127), -1)

        print(f"iteration -> {iterCounter}")
        # if iterCounter != 0 and iterCounter % 90 == 0:
        #     plt.imshow(imgMapSteps)
        #     plt.show()
        iterCounter += 1

        # OPEN.extend(Expand(a, delta, end, a_m, bp, g, CLOSE))
        openExtend = Expand(a, delta, end, a_m, bp, g, CLOSE, image)
        for point in openExtend:
            if not point in OPEN:
                OPEN.append(point)

        current_point = a

    print("Path not found :(")