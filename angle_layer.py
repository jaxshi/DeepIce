from keras.engine.topology import Layer
from keras import backend as K
from keras.layers import Concatenate, Dot

""" Layer that converts catersian coordinates into spherical coordinates 
    
    Input is the xyz coordinates of the 10 nearest neighbours
    Returns the spherical coordinate of the 10 nearest neighbours in the form of 
    the angles theta and phi and the squared distance (r2)

    # Example
    angles = Layer_Angles(input_shape=(30,))(inputTensor)

"""

class Layer_Angles(Layer):

    def __init__(self, nearest_neigbours, **kwargs):
        self.nearest_neigbours = nearest_neigbours
        self.output_dim = nearest_neigbours *3
        super(Layer_Angles, self).__init__(**kwargs)

    def call(self, inputTensor):
        Cat_angles = []
        for i in range(1, self.nearest_neigbours+1):
            id_start = (i - 1) * 3 #9
            id_end = id_start + 3

            coord = inputTensor[:, id_start:id_end]

            r2 = Dot(axes=-1, normalize=False)([coord, coord])

            z = coord[:, 2:3]
            y = coord[:, 1:2]
            x = coord[:, 0:1]

            z_square = K.square(z)

            theta = K.tf.acos(K.tf.divide(z_square, r2))
            Phi = K.tf.atan(K.tf.divide(y, x))

            Cat_angles.append(Concatenate()([r2, theta, Phi]))

        ConcatSpherical = Concatenate()(Cat_angles)
        return ConcatSpherical

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)
