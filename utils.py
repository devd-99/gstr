import numpy as np
import math

#returns whether the time difference given is lesser than a second or not
def isTimeDiffOkay(f1, f2):
    td = abs(f1-f2)
    if (td < 2.0) and (td > 0.1):
        return True
    else:
        return False



def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def length(v):
    return math.sqrt(dotproduct(v, v))
def angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

# def smileRatio(mouth):


# Returns EAR given eye landmarks
def eye_aspect_ratio(eye):
    # Compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])

    # Compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = np.linalg.norm(eye[0] - eye[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # Return the eye aspect ratio
    return ear

def eyebrowRaise(leftEye, rightEye, lbrow, rbrow, jaw):
    A = np.linalg.norm(leftEye[4] - lbrow[2])
    B = np.linalg.norm(rightEye[5] - rbrow[2])
    D1 = A+B

    A = np.linalg.norm(jaw[8] - lbrow[2])
    B = np.linalg.norm(jaw[8] - rbrow[2])
    D2 = A+B/2
    return D1/D2   

def unit_vector(vector):
    return vector/ np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

#Smile Ratio
def smileRatio(mouth):
    u1 = mouth[0] - mouth[2]
    u2 = mouth[2] - mouth[3]

    v1 = mouth[4] - mouth[6]
    v2 = mouth[3] - mouth[4]

    return max(angle_between(u1, u2), angle_between(v1, v2))


# Returns MAR given eye landmarks
def mouth_aspect_ratio(mouth):
    # Compute the euclidean distances between the three sets
    # of vertical mouth landmarks (x, y)-coordinates
    A = np.linalg.norm(mouth[13] - mouth[19])
    B = np.linalg.norm(mouth[14] - mouth[18])
    C = np.linalg.norm(mouth[15] - mouth[17])

    # Compute the euclidean distance between the horizontal
    # mouth landmarks (x, y)-coordinates
    D = np.linalg.norm(mouth[12] - mouth[16])

    # Compute the mouth aspect ratio
    mar = (A + B + C) / (2 * D)

    # Return the mouth aspect ratio
    return mar

def jaw_open_ratio(lbrow, rbrow, jaw):
    #compute euc distance of brows to jaw and then divide it with distance btween edge of brows
    A = np.linalg.norm(lbrow[2]-jaw[8])
    B = np.linalg.norm(rbrow[2]-jaw[8])
    C = np.linalg.norm(lbrow[0]-rbrow[4])

    jor = (A + B)/ (2 * C)

    return jor


# Return direction given the nose and anchor points.
def direction(nose_point, anchor_point, w, h, multiple=1):
    nx, ny = nose_point
    x, y = anchor_point

    if nx > x + multiple * w:
        return 'right'
    elif nx < x - multiple * w:
        return 'left'

    if ny > y + multiple * h:
        return 'down'
    elif ny < y - multiple * h:
        return 'up'

    return '-'

def direction2(nose_point, anchor_point, w, h, multiple=1):
    nx, ny = nose_point
    x, y = anchor_point

    relx = nx-x
    rely = ny-y
    a=[relx, rely]
    return a


 #get dimensions of the face
def getDims(jaw, lbrow, rbrow):
    A = np.linalg.norm(jaw[1] - jaw[15])
    B = np.linalg.norm(jaw[8] - lbrow[2])
    C = np.linalg.norm(lbrow[2] - rbrow[2])
    B = B*B
    C = (C*C)/4
    D = math.sqrt(B-C)

    res = [A, D]
    return res
