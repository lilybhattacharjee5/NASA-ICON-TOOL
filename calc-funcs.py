import math, numpy

def convert_time_format(time):
	"""Converts time stamps from the netCDF to the form for czml "2018-02-09T00:00:00+00:00"""
	time_string = time[0:10] + "T" + time[11:19] +"+00:00"
	return ('"%s"' % time_string)

def convert_time_format(time):
	"""Converts time stamps from the netCDF to the form for czml "2018-02-09T00:00:00+00:00"""
	time_string = time[0:10] + "T" + time[11:19] +"+00:00"
	return ('"%s"' % time_string) 

def positions(lat, lon, alt, time):
	"""Outputs a list with the positions of the satellite by time when given the lat, lon, alt, time variables from a netcdf file. """
	positions = []
	for i in range(len(lat)):
		positions += [convert_time_format(time[i]), lon[i], lat[i], (alt[i] * 1000)]
	return positions

def orientations(instra_x_hat,instra_y_hat,instra_z_hat,time):
	"""Generates a unit Quaternion from the xhat,yhat,zhat,and time"""
	unitQuaternions = []
	for i in range(len(instra_x_hat)):
		x = instra_x_hat[i]
		y = instra_y_hat[i]
		z = instra_z_hat[i]
		rotation_matrix = numpy.matrix([x,y,z])
		quaternion = numpy.roll(quaternion_from_matrix(rotation_matrix),3) 
		time_string = convert_time_format(time[i])
		unitQuaternions += time_string,(-1*quaternion[0]),(-1*quaternion[1]),(-1*quaternion[2]),quaternion[3]
	return unitQuaternions

def quaternion_from_matrix(matrix, isprecise=False):
    """Return quaternion from rotation matrix.

    If isprecise is True, the input matrix is assumed to be a precise rotation
    matrix and a faster algorithm is used.

 	"""
    M = numpy.array(matrix, dtype=numpy.float64, copy=False)[:4, :4]
    if isprecise:
        q = numpy.empty((4, ))
        t = numpy.trace(M)
        if t > M[3, 3]:
            q[0] = t
            q[3] = M[1, 0] - M[0, 1]
            q[2] = M[0, 2] - M[2, 0]
            q[1] = M[2, 1] - M[1, 2]
        else:
            i, j, k = 0, 1, 2
            if M[1, 1] > M[0, 0]:
                i, j, k = 1, 2, 0
            if M[2, 2] > M[i, i]:
                i, j, k = 2, 0, 1
            t = M[i, i] - (M[j, j] + M[k, k]) + M[3, 3]
            q[i] = t
            q[j] = M[i, j] + M[j, i]
            q[k] = M[k, i] + M[i, k]
            q[3] = M[k, j] - M[j, k]
            q = q[[3, 0, 1, 2]]
        q *= 0.5 / math.sqrt(t * M[3, 3])
    else:
        m00 = M[0, 0]
        m01 = M[0, 1]
        m02 = M[0, 2]
        m10 = M[1, 0]
        m11 = M[1, 1]
        m12 = M[1, 2]
        m20 = M[2, 0]
        m21 = M[2, 1]
        m22 = M[2, 2]
        # symmetric matrix K
        K = numpy.array([[m00-m11-m22, 0.0,         0.0,         0.0],
                         [m01+m10,     m11-m00-m22, 0.0,         0.0],
                         [m02+m20,     m12+m21,     m22-m00-m11, 0.0],
                         [m21-m12,     m02-m20,     m10-m01,     m00+m11+m22]])
        K /= 3.0
        # quaternion is eigenvector of K that corresponds to largest eigenvalue
        w, V = numpy.linalg.eigh(K)
        q = V[[3, 0, 1, 2], numpy.argmax(w)]
    if q[0] < 0.0:
        numpy.negative(q, q)
    return q
