import numpy as np

def angle(v1, v2): #v1 and v2 are lists or numpy arrays. Returns angle between the vectors.
    v1 = np.array(v1)
    v2 = np.array(v2)
    norm_v1 = np.linalg.norm(v1, ord=2)
    norm_v2 = np.linalg.norm(v2, ord=2)
    if norm_v1==0.0 or norm_v2==0.0:
        return 0.0
    else:
        return np.arccos((np.dot(v1, v2))/(norm_v1*norm_v2))

def angular_velocity(angle_val, t1, t2):
    if t2 - t1 == 0:
        return 0.0
    else:
        return angle_val/(t2 - t1)

            
    





