from shipping6DOF.rotationclasses import *
import numpy as np
from warnings import deprecated

def change_basis_application(e0: vector, e1: vector, e2: vector, rot : rotation) -> (rotation, rotation):
    """
        A change of basis for a transformation T: Rn -> Rn is performed as follows:
            B = (U^-1) T U
        where U = [u1, u2,...,un] and where the transformation B: Rn -> Rn i similar 
        to that of T, but with a basis {u1,u2,...,un} of Rn.

        Note: a basis ALWAYS has an inverse :)
    """
    basis = rotation(np.c_[e0.coeffs(),e1.coeffs(),e2.coeffs()])
    inv_basis = rotation(np.linalg.inv(basis.coeffs()))

    newRot = basis*(rot*inv_basis)

    return basis, newRot

def create_rot_matrix_from_theta_axis(theta: float, axis: vector) ->  rotation:
    crossp = axis.cpmf()
    out = (axis & axis)
    cos = np.cos(theta)
    sin = np.sin(theta)
    I = np.identity(3)
    return rotation((cos*I)) + (sin * crossp) + ((1.0-cos)*out)

def is_rotation_matrix(rot) :
    R = rot.coeffs()
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6
                               
def rotation_matrix_to_euler_angles(rot) :
 
    assert is_rotation_matrix(rot)

    R = rot.coeffs()
 
    sy = np.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
 
    singular = sy < 1e-6
 
    if  not singular :
        x = np.atan2(R[2,1] , R[2,2])
        y = np.atan2(-R[2,0], sy)
        z = np.atan2(R[1,0], R[0,0])
    else :
        x = np.atan2(-R[1,2], R[1,1])
        y = np.atan2(-R[2,0], sy)
        z = 0
 
    return x, y, z    


def create_plane_from_npoints(pointlist: np.ndarray):
    
    assert pointlist.shape[0] == 3 
    assert pointlist.shape[1] > 3

    origin = np.mean(pointlist, axis=1,keepdims=True)

    svd = np.linalg.svd(pointlist - origin)
    left = svd[0]
    axis = left[:,-1]

    return originAndAxis(origin,axis)

def create_plane_from_3points(p0: vector, p1: vector, p2: vector):
    
    u = p1 - p0
    v = p2 - p0
    axis = (u ^ v) ##  u x v
    axis = (1./axis.norm())*axis
    origin = (1./3.)*(p0 + p1 + p2)

    return originAndAxis(origin,axis)

def create_plane_from_2points(p0: vector, p1: vector):

    axis = p1 - p0
    axis = (1./axis.norm())*axis

    return originAndAxis(p0,axis)

def rotation_displacement_2planes(plane1: originAndAxis, plane2: originAndAxis):

    disp  = plane2.origin() - plane1.origin()
    angle = np.acos(plane1.axis() * plane2.axis())
    axis  = plane1.axis() ^ plane2.axis()
    axis = axis/axis.norm()

    rot = create_rot_matrix_from_theta_axis(float(angle),axis)

    return rot, disp

@deprecated("use 'create_rot_matrix_from_theta_axis' instead")
def create_rotation_matrix(axis,angle):
    
    a12 = axis[0]*axis[1]*(1-np.cos(angle)) - axis[2]*np.sin(angle)
    a21 = axis[0]*axis[1]*(1-np.cos(angle)) + axis[2]*np.sin(angle)
    
    a13 = axis[0]*axis[2]*(1-np.cos(angle)) + axis[1]*np.sin(angle)
    a31 = axis[0]*axis[2]*(1-np.cos(angle)) - axis[1]*np.sin(angle)
    
    a23 = axis[1]*axis[2]*(1-np.cos(angle)) - axis[0]*np.sin(angle)
    a32 = axis[1]*axis[2]*(1-np.cos(angle)) + axis[0]*np.sin(angle)
    
    a11 = np.cos(angle) + axis[0]**2*(1-np.cos(angle))
    a22 = np.cos(angle) + axis[1]**2*(1-np.cos(angle))
    a33 = np.cos(angle) + axis[2]**2*(1-np.cos(angle))
    
    return np.array([[a11,a12,a13],[a21,a22,a23],[a31,a32,a33]],dtype=np.float64)

@deprecated("use 'rotation_matrix_to_euler_angles' for consistency with API")
def calculate_rotations(rot):
    assert rot.shape == (3,3)
    
    yaw = None
    pitch = None
    roll = None
    
    if not abs(rot[2,0]) > 0.999:
        pitch = -np.asin(rot[2,0])
        pitch = (pitch, np.pi-pitch)
        
        roll = (np.atan2(rot[2,1]/np.cos(pitch[0]),rot[2,2]/np.cos(pitch[0])), \
                np.atan2(rot[2,1]/np.cos(pitch[1]),rot[2,2]/np.cos(pitch[1])))
        
        yaw =(np.atan2(rot[1,0]/np.cos(pitch[0]),rot[0,0]/np.cos(pitch[0])), \
                np.atan2(rot[1,0]/np.cos(pitch[1]),rot[0,0]/np.cos(pitch[1])))
    else:
        yaw = (0,0)
        if rot[2,0] > 0.999:
            pitch = (np.pi/2.,np.pi/2.)
            roll = yaw[0] + np.atan2(rot[0,1],rot[0,2])
            roll = (roll,roll)
        else:
            pitch = (-np.pi/2.,-np.pi/2.)
            roll = -yaw[0] + np.atan2(-rot[0,1],-rot[0,2])
            roll = (roll,roll)
            
    return roll, pitch, yaw
