import numpy as np
import math
import matplotlib.pyplot as plt


def z_DAK(Ppr, Tpr):
    '''
    To check if input data is scalar or array to return properly
    :param Ppr:
    :param Tpr:
    :return:
    '''
    if np.isscalar(Ppr) == False or np.isscalar(Tpr) == False:
        # if input as a list - output as a nested list z[Tpr[Ppr]]
        z_array = []
        z_array_Ppr = []
        for i in Tpr:
            for j in Ppr:
                z_array_Ppr.append(z_DAK_alpha(j,i))
            z_array.append(z_array_Ppr)
            z_array_Ppr = []
        return z_array
    else:
        return z_DAK_alpha(Ppr, Tpr)


def z_plot(Ppr, Tpr, z):
    for i in range(len(Tpr)):
        plt.plot(Ppr, z[i])

def calculateDensity(Ppr, Tpr, z_new):
    '''
    :param Ppr:
    :param Tpr:
    :param z_new:
    :return:
    '''
    return 0.27 * Ppr / (z_new * Tpr)

def z_DAK_alpha(Ppr, Tpr):
    '''
    To compute z factor using DAK correlation
    :param Ppr:
    :param Tpr:
    :return:
    '''
    Ppr = np.asanyarray(Ppr)
    Tpr = np.asanyarray(Tpr)
    '''
    :param Ppr:
    :param Tpr:
    :return:
    '''
    A1 = 0.3265
    A2 = -1.07
    A3 = -0.5339
    A4 = 0.01569
    A5 = -0.05165
    A6 = 0.5475
    A7 = -0.7361
    A8 = 0.1844
    A9 = 0.1056
    A10 = 0.6134
    A11 = 0.721

    R1 = A1 + A2 / Tpr + A3 / Tpr**3 + A4 / Tpr**4 + A5 / Tpr**5
    R2 = 0.27*Ppr / Tpr
    R3 = A6 + A7 / Tpr + A8 / Tpr**2
    R4 = A9 * (A7 / Tpr + A8 / Tpr**2)
    R5 = A10 / Tpr**3

    tolerance = 10e-5
    max_iteration = 1000
    z_old = 1
    rho = calculateDensity(Ppr, Tpr, z_old)

    while True:

        z_new = R1 * rho - R2 / rho + R3 * rho**2 - R4 * rho**5 + R5 * rho**2 * (1 + A11 * rho**2) * math.exp(-A11 * rho**2) + 1

        z_new_prime = R1 + R2 / rho**2 + 2 * R3 * rho - 5*R4 * rho**4 + 2*R5 * rho * math.exp(-A11 * rho**2)*((1 + 2*A11 * rho**3)- A11*rho**2*(1 + A11*rho**2))

        if abs(z_new) < tolerance:
            break
        rho1 = rho - z_new / z_new_prime

        if abs(rho1 - rho) < tolerance:
            break
        else:
            rho = rho1

    z_DAK = 0.27 * Ppr / (rho * Tpr)

    return z_DAK

def z_ANN_10(Ppr, Tpr):
    '''
    To check if input data is scalar or array to return properly
    :param Ppr:
    :param Tpr:
    :return:
    '''
    if np.isscalar(Ppr) == False or np.isscalar(Tpr) == False:
        # if input as a list - output as a nested list z[Tpr[Ppr]]
        z_array = []
        z_array_Ppr = []
        for i in Tpr:
            for j in Ppr:
                z_array_Ppr.append(z_ANN_10_alpha(j,i))
            z_array.append(z_array_Ppr)
            z_array_Ppr = []
        return z_array
    else:
        return z_ANN_10_alpha(Ppr, Tpr)

def z_ANN_10_alpha(Ppr, Tpr):
    '''
    Reproduced from Kamyab et al., 2010. Using ANN to estimate the z-factor for natural
    hydrocarbon gases.
    ANN used 2x10x10x1
    :param Ppr: 0 < Ppr < 30
    :param Tpr: 1 < Tpr < 3
    :return: z
    '''

    # Statistics to normalize data
    Ppr_min = 0
    Ppr_max = 30
    Tpr_min = 1
    Tpr_max = 3
    Z_min = 0.25194
    Z_max = 2.66

    # Weight and biases fro the 1st neural layer:[10][2]
    wb1 = [[2.2458, -2.2493, -3.7801],[3.4663, 8.1167, -14.9512],[5.0509, -1.8244, 3.5017],
           [6.1185, -0.2045, 0.3179], [1.3366, 4.9303, 2.2153],[-2.8652, 1.1679, 1.0218],
           [-6.5716, -0.8414, -8.1646],[-6.1061, 12.7945, 7.2201],[13.0884, 7.5387, 19.2231],[70.7187, 7.6138, 74.6949]]

    # Weight and biases fro the 2ndneural layer: [10[[11]
    wb2 =[[4.674,	1.4481,		-1.5131,	0.0461,		-0.1427,	2.5454,		-6.7991,	-0.5948,	-1.6361,	0.5801,		-3.0336],
    [-6.7171,	-0.7737,	-5.6596,	2.975,	    14.6248,	2.7266,	    5.5043,	    -13.2659,	-0.7158,	3.076,	    15.9058],
    [7.0753,	-3.0128,	-1.1779,	-6.445,	    -1.1517,	7.3248,	    24.7022,	-0.373,	    4.2665,	    -7.8302,	-3.1938],
    [2.5847,	-12.1313,	21.3347,	1.2881,	    -0.2724,	-1.0393,	-19.1914,	-0.263,	    -3.2677,	-12.4085,	-10.2058],
    [-19.8404,	4.8606,	    0.3891,	    -4.5608,	-0.9258,	-7.3852,	18.6507,	0.0403,	    -6.3956,	-0.9853,	13.5862],
    [16.7482,	-3.8389,	-1.2688,	1.9843,	    -0.1401,	-8.9383,	-30.8856,	-1.5505,	-4.7172,	10.5566,	8.2966],
    [2.4256,	2.1989,	    18.8572,	-14.5366,	11.64,	    -19.3502,	26.6786,	-8.9867,	-13.9055,	5.195,	    9.7723],
    [-16.388,	12.1992,	-2.2401,	-4.0366,	-0.368,	    -6.9203,	-17.8283,	-0.0244,	9.3962,	    -1.7107,	-1.0572],
    [14.6257,	7.5518,	    12.6715,	-12.7354,	10.6586,	-43.1601,	1.3387,	    -16.3876,	8.5277,	    45.9331,	-6.6981],
    [-6.9243,	0.6229,	    1.6542,	    -0.6833,	1.3122,	    -5.588,	    -23.4508,	0.5679,	    1.7561,	    -3.1352,	5.8675]
   ]

    # Weight and biases fro the 3rd neural layer: [11]
    wb3 =[-30.1311, 2.0902, -3.5296,	18.1108, -2.528, -0.7228, 0.0186, 5.3507, -0.1476, -5.0827, 3.9767]

    # ANN Correlation:
    n1_10 = []
    n2_10 = []
    Ppr_n = 2 / (Ppr_max - Ppr_min) * (Ppr - Ppr_min) - 1
    Tpr_n = 2 / (Tpr_max - Tpr_min) * (Tpr - Tpr_min) - 1

    for i in range(10):
        n1_10.append([0, 0])
        n1_10[i][0] = Ppr_n * wb1[i][0] + Tpr_n * wb1[i][1] + wb1[i][2]
        n1_10[i][1] = logsig(n1_10[i][0])

    for i in range(10):
        n2_10.append([0, 0])
        for j in range(10):
            n2_10[i][0] += n1_10[j][1] * wb2[i][j]
        n2_10[i][0] += wb2[i][10]
        n2_10[i][1] = logsig(n2_10[i][0])

    z_n = 0
    for j in range(len(n2_10)):
        z_n += n2_10[j][1] * wb3[j]
    z_n += wb3[10]

    zANN10 = (z_n + 1) * (Z_max - Z_min) / 2 + Z_min
    return zANN10


def logsig(x): # log-sigmoid function for hidden layers
        return (1/ (1 + math.exp(-1 * x)))




