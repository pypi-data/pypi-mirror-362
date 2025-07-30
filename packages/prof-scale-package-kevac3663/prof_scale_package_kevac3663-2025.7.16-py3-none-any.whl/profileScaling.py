##IMPORTS & CONSTANTS
import numpy as np
from matplotlib import pyplot as plt
from scipy import constants

plt.rcParams['figure.figsize']=(6,6)
plt.rcParams['font.weight']='normal'
plt.rcParams['axes.labelweight']='normal'
plt.rcParams['lines.linewidth']=2
plt.rcParams['lines.markeredgewidth']=0
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 16}



pi = constants.pi
e_charge = eV2J = constants.e
epsilon_0 = constants.epsilon_0
m_e = constants.m_e
m_p = constants.m_p
mu0 = constants.mu_0
Kb = 1.6022 * (10**-19)

##GIVEN PROFILES

##toroidal current density
j_tor = np.array([1503164.30181394, 1491709.15123639, 1479872.6672448,
       1467746.82293579, 1455601.48345256, 1443217.96758606,
       1430814.33461951, 1418134.32016611, 1405459.62312355,
       1392649.57620738, 1379833.74251861, 1366812.98260013,
       1353870.72316153, 1340784.24998749, 1327650.30591672,
       1314495.36993738, 1301336.34291864, 1288018.72278896,
       1274782.98807523, 1261483.63204725, 1248171.88510482,
       1234761.81869551, 1221432.9692941 , 1208051.08526808,
       1194623.84716518, 1181222.01218796, 1167792.46963731,
       1154352.93572927, 1140905.14485966, 1127437.68721006,
       1114008.69939634, 1100520.9799979 , 1087044.31623851,
       1073580.43550137, 1060097.39916528, 1046612.91954696,
       1033149.15875547, 1019651.31495462, 1006184.35817575,
        992733.37427587,  979235.34726192,  965755.26222017,
        952322.7926519 ,  938855.97496693,  925411.63974003,
        911968.86267575,  898560.12560688,  885118.35140404,
        871744.44716329,  858365.58192708,  844979.59973879,
        831662.85127022,  818350.49285462,  805070.03416917,
        791801.04554942,  778598.41039786,  765447.73807816,
        752298.8919853 ,  739250.09736962,  726247.7095755 ,
        713318.0842224 ,  700455.43803062,  687704.05949274,
        675054.53155015,  662510.65349387,  650091.83399049,
        637845.22865768,  625752.16324726,  613847.99229837,
        602166.01070378,  590742.76187664,  579575.34336721,
        568727.54586902,  558240.59600285,  548141.32642814,
        538454.45439668,  529229.94460339,  520463.2227285 ,
        512183.4888994 ,  504347.75388098,  496946.64233325,
        489956.04923063,  483312.63640229,  476991.22767723,
        470931.90780456,  465134.99392651,  459522.70760382,
        454094.99401164,  448803.12021258,  443636.73764309,
        438566.77552085,  433558.83083816,  428615.73178646,
        423707.31105392,  418817.20603535,  413930.96943408,
        409018.83487385,  404082.90684579,  399075.92939235,
        394002.39090329,  388817.08565685,  383523.43263862,
        378136.47194509,  372643.8823911 ,  367099.44357865,
        361535.40033145,  356051.81244096,  350828.99577038,
        346091.02683904,  342277.4560307 ,  339844.19970404,
        339471.87180201,  342046.61658366,  348562.06803813,
        359703.8524185 ,  376283.14565751,  398488.70623882,
        425888.40110837,  457505.59002886,  491453.90295101,
        524824.42254486,  549787.29143217,  553070.56608478,
        522910.73830391,  459720.62580965,  372081.22698777,
        274493.84976748,  183181.68996668,   87534.60668623])

## derivative of pressure
pprime = np.array([-620844.41 , -605164.368, -590721.145, -577369.417, -564980.938,
       -553442.532, -542654.324, -532528.173, -522986.299, -513960.063,
       -505388.891, -497219.331, -489404.214, -481901.915, -474675.706,
       -467693.174, -460925.723, -454348.119, -447938.1  , -441676.026,
       -435544.569, -429528.447, -423614.183, -417789.891, -412045.096,
       -406370.563, -400758.159, -395200.722, -389691.95 , -384226.303,
       -378798.916, -373405.52 , -368042.382, -362706.238, -357394.249,
       -352103.953, -346833.229, -341580.259, -336343.506, -331121.686,
       -325913.746, -320718.854, -315536.379, -310365.887, -305207.129,
       -300060.041, -294924.741, -289801.532, -284690.905, -279593.55 ,
       -274510.363, -269442.461, -264391.202, -259358.204, -254345.369,
       -249354.916, -244389.414, -239451.823, -234545.538, -229674.444,
       -224842.979, -220056.198, -215319.857, -210640.5  , -206025.564,
       -201483.492, -197023.868, -192657.566, -188396.92 , -184255.916,
       -180250.415, -176398.394, -172720.233, -169239.034, -165980.976,
       -162975.733, -160256.934, -157862.566, -155809.973, -154064.431,
       -152588.26 , -151347.995, -150313.861, -149459.308, -148760.596,
       -148196.423, -147747.593, -147396.712, -147127.92 , -146926.643,
       -146779.36 , -146673.397, -146596.726, -146537.776, -146485.256,
       -146427.973, -146354.661, -146253.802, -146113.448, -145921.033,
       -145663.176, -145325.472, -144892.268, -144346.415, -143669.003,
       -142839.064, -141833.243, -140652.774, -139657.113, -139463.467,
       -140706.942, -144045.131, -150168.398, -159810.68 , -173760.971,
       -192875.664, -218091.954, -250442.495, -291071.558, -341873.422,
       -420296.619, -549904.238, -665250.784, -679899.319, -605373.806,
       -475780.814, -324936.214, -197176.492, -108641.837])

##pressure
pres = np.array([76762.0766  , 75505.9656  , 74280.7174  , 73083.9467  ,
       71913.5482  , 70767.664   , 69644.6547  , 68543.0732  ,
       67461.6426  , 66399.2361  , 65354.859   , 64327.6337  ,
       63316.7856  , 62321.631   , 61341.5665  , 60376.0596  ,
       59424.6402  , 58486.8937  , 57562.4536  , 56650.9967  ,
       55752.2377  , 54865.9245  , 53991.8347  , 53129.7716  ,
       52279.5616  , 51441.0514  , 50614.1052  , 49798.6031  ,
       48994.4389  , 48201.5186  , 47419.7588  , 46649.0855  ,
       45889.4328  , 45140.7421  , 44402.9609  , 43676.0424  ,
       42959.9442  , 42254.6281  , 41560.0592  , 40876.2057  ,
       40203.0381  , 39540.5287  , 38888.6515  , 38247.3814  ,
       37616.6942  , 36996.5659  , 36386.9724  , 35787.8894  ,
       35199.2914  , 34621.152   , 34053.4432  , 33496.1347  ,
       32949.1938  , 32412.5847  , 31886.2682  , 31370.2005  ,
       30864.3333  , 30368.6123  , 29882.9768  , 29407.3588  ,
       28941.6816  , 28485.8588  , 28039.793   , 27603.374   ,
       27176.4775  , 26758.9629  , 26350.671   , 25951.4217  ,
       25561.0111  , 25179.2085  , 24805.7525  , 24440.3469  ,
       24082.6563  , 23732.3009  , 23388.8502  , 23051.8166  ,
       22720.6476  , 22394.7173  , 22073.3432  , 21755.8604  ,
       21441.6785  , 21130.2797  , 20821.2111  , 20514.0776  ,
       20208.5355  , 19904.2872  , 19601.0769  , 19298.6859  ,
       18996.9298  , 18695.6553  , 18394.7379  , 18094.08    ,
       17793.6092  , 17493.2774  , 17193.0598  , 16892.9546  ,
       16592.9833  , 16293.1904  , 15993.6446  , 15694.4398  ,
       15395.6963  , 15097.563   , 14800.2196  , 14503.8792  ,
       14208.7921  , 13915.2494  , 13623.5876  , 13334.1656  ,
       13046.9733  , 12760.9995  , 12473.95    , 12182.2064  ,
       11880.7691  , 11563.1791  , 11221.4172  , 10845.7785  ,
       10424.7204  ,  9944.68202 ,  9389.87215 ,  8741.38645 ,
        7960.50283 ,  6966.48059 ,  5721.48983 ,  4343.31221 ,
        3026.48173 ,  1918.78149 ,  1098.40443 ,   563.472273,
         250.145176])

##normalized radial coordinate, psi ψ_norm
psi_norm = np.array([0.       , 0.0078125, 0.015625 , 0.0234375, 0.03125  , 0.0390625,
       0.046875 , 0.0546875, 0.0625   , 0.0703125, 0.078125 , 0.0859375,
       0.09375  , 0.1015625, 0.109375 , 0.1171875, 0.125    , 0.1328125,
       0.140625 , 0.1484375, 0.15625  , 0.1640625, 0.171875 , 0.1796875,
       0.1875   , 0.1953125, 0.203125 , 0.2109375, 0.21875  , 0.2265625,
       0.234375 , 0.2421875, 0.25     , 0.2578125, 0.265625 , 0.2734375,
       0.28125  , 0.2890625, 0.296875 , 0.3046875, 0.3125   , 0.3203125,
       0.328125 , 0.3359375, 0.34375  , 0.3515625, 0.359375 , 0.3671875,
       0.375    , 0.3828125, 0.390625 , 0.3984375, 0.40625  , 0.4140625,
       0.421875 , 0.4296875, 0.4375   , 0.4453125, 0.453125 , 0.4609375,
       0.46875  , 0.4765625, 0.484375 , 0.4921875, 0.5      , 0.5078125,
       0.515625 , 0.5234375, 0.53125  , 0.5390625, 0.546875 , 0.5546875,
       0.5625   , 0.5703125, 0.578125 , 0.5859375, 0.59375  , 0.6015625,
       0.609375 , 0.6171875, 0.625    , 0.6328125, 0.640625 , 0.6484375,
       0.65625  , 0.6640625, 0.671875 , 0.6796875, 0.6875   , 0.6953125,
       0.703125 , 0.7109375, 0.71875  , 0.7265625, 0.734375 , 0.7421875,
       0.75     , 0.7578125, 0.765625 , 0.7734375, 0.78125  , 0.7890625,
       0.796875 , 0.8046875, 0.8125   , 0.8203125, 0.828125 , 0.8359375,
       0.84375  , 0.8515625, 0.859375 , 0.8671875, 0.875    , 0.8828125,
       0.890625 , 0.8984375, 0.90625  , 0.9140625, 0.921875 , 0.9296875,
       0.9375   , 0.9453125, 0.953125 , 0.9609375, 0.96875  , 0.9765625,
       0.984375 , 0.9921875, 1.       ])

##radial coordinate, psi ψ
psi = np.array([-0.2995913 , -0.29754219, -0.29549308, -0.29344398, -0.29139487,
       -0.28934577, -0.28729666, -0.28524755, -0.28319845, -0.28114934,
       -0.27910024, -0.27705113, -0.27500202, -0.27295292, -0.27090381,
       -0.2688547 , -0.2668056 , -0.26475649, -0.26270739, -0.26065828,
       -0.25860917, -0.25656007, -0.25451096, -0.25246186, -0.25041275,
       -0.24836364, -0.24631454, -0.24426543, -0.24221633, -0.24016722,
       -0.23811811, -0.23606901, -0.2340199 , -0.2319708 , -0.22992169,
       -0.22787258, -0.22582348, -0.22377437, -0.22172527, -0.21967616,
       -0.21762705, -0.21557795, -0.21352884, -0.21147974, -0.20943063,
       -0.20738152, -0.20533242, -0.20328331, -0.2012342 , -0.1991851 ,
       -0.19713599, -0.19508689, -0.19303778, -0.19098867, -0.18893957,
       -0.18689046, -0.18484136, -0.18279225, -0.18074314, -0.17869404,
       -0.17664493, -0.17459583, -0.17254672, -0.17049761, -0.16844851,
       -0.1663994 , -0.1643503 , -0.16230119, -0.16025208, -0.15820298,
       -0.15615387, -0.15410477, -0.15205566, -0.15000655, -0.14795745,
       -0.14590834, -0.14385923, -0.14181013, -0.13976102, -0.13771192,
       -0.13566281, -0.1336137 , -0.1315646 , -0.12951549, -0.12746639,
       -0.12541728, -0.12336817, -0.12131907, -0.11926996, -0.11722086,
       -0.11517175, -0.11312264, -0.11107354, -0.10902443, -0.10697533,
       -0.10492622, -0.10287711, -0.10082801, -0.0987789 , -0.0967298 ,
       -0.09468069, -0.09263158, -0.09058248, -0.08853337, -0.08648427,
       -0.08443516, -0.08238605, -0.08033695, -0.07828784, -0.07623873,
       -0.07418963, -0.07214052, -0.07009142, -0.06804231, -0.0659932 ,
       -0.0639441 , -0.06189499, -0.05984589, -0.05779678, -0.05574767,
       -0.05369857, -0.05164946, -0.04960036, -0.04755125, -0.04550214,
       -0.04345304, -0.04140393, -0.03935483, -0.03730572])

##PROFILE PARAMETRIZATIONS

def Hmode_profiles(edge=0.08, ped=0.4, core=2.5, rgrid=201, expin=1.5, expout=1.5, widthp=0.04, xphalf=None):
    """
     This function generates H-mode  density and temperature profiles evenly
     spaced in your favorite radial coordinate

    :param edge: (float) separatrix height

    :param ped: (float) pedestal height

    :param core: (float) on-axis profile height

    :param rgrid: (int) number of radial grid pointsx

    :param expin: (float) inner core exponent for H-mode pedestal profile

    :param expout (float) outer core exponent for H-mode pedestal profile

    :param width: (float) width of pedestal

    :param xphalf: (float) position of tanh
    """

    w_E1 = 0.5 * widthp  # width as defined in eped
    if xphalf is None:
        xphalf = 1.0 - w_E1

    xped = xphalf - w_E1

    pconst = 1.0 - np.tanh((1.0 - xphalf) / w_E1)
    a_t = 2.0 * (ped - edge) / (1.0 + np.tanh(1.0) - pconst)

    coretanh = 0.5 * a_t * (1.0 - np.tanh(-xphalf / w_E1) - pconst) + edge

    xpsi = np.linspace(0, 1, rgrid)
    ones = np.ones(rgrid)

    val = 0.5 * a_t * (1.0 - np.tanh((xpsi - xphalf) / w_E1) - pconst) + edge * ones

    xtoped = xpsi / xped
    for i in range(0, rgrid):
        if xtoped[i] ** expin < 1.0:
            val[i] = val[i] + (core - coretanh) * (1.0 - xtoped[i] ** expin) ** expout

    return val

def my_Hmode_profiles(xdata, edge=0.08, ped=0.4, core=2.5, expin=1.5, expout=1.5, widthp=0.04, xphalf=0.95, y0=0., c=0.):
    """
    This function generates H-mode  density and temperature profiles evenly
    spaced in your favorite radial coordinate

    :param xdata: (array) x-coordinate

    :param edge: (float) separatrix height

    :param ped: (float) pedestal height

    :param core: (float) on-axis profile height

    :param expin: (float) inner core exponent for H-mode pedestal profile

    :param expout (float) outer core exponent for H-mode pedestal profile

    :param width: (float) width of pedestal

    :param xphalf: (float) position of tanh

    :param y0: (float) profile scaling coefficient

    :param c0: (float) profile scaling constant/y-intercept
    """
    w_E1 = 0.5 * widthp  # width as defined in eped
    if xphalf is None:
            xphalf = 1.0 - w_E1

    xped = xphalf - w_E1

    pconst = 1.0 - np.tanh((1.0 - xphalf) / w_E1)
    a_t = 2.0 * (ped - edge) / (1.0 + np.tanh(1.0) - pconst)

    coretanh = 0.5 * a_t * (1.0 - np.tanh(-xphalf / w_E1) - pconst) + edge

    xpsi = xdata
    ones = np.ones(len(xpsi))

    val = 0.5 * a_t * (1.0 - np.tanh((xpsi - xphalf) / w_E1) - pconst) + edge * ones

    xtoped = xpsi / xped
    for i in range(0, len(xpsi)):
            if xtoped[i] ** expin < 1.0:
                    val[i] = val[i] + (core - coretanh) * (1.0 - xtoped[i] ** expin) ** expout

    return val * y0 + c

psi_n = np.linspace(0.,1.,257)
xphalf = 0.98
widthp = 0.05

ne = Hmode_profiles(edge=0.1, ped=1.9, core=4., rgrid=257, expin=1.6, expout=1.6, widthp=widthp, xphalf=xphalf) * 1e19
Te = Hmode_profiles(edge=0.001, ped=0.5, core=4., rgrid=257, expin=1.3, expout=1.7, widthp=widthp, xphalf=xphalf) * 1e3
ni = Hmode_profiles(edge=0.1, ped=1.9, core=3.9, rgrid=257, expin=1.6, expout=1.6, widthp=widthp, xphalf=xphalf) * 1e19
Ti = Hmode_profiles(edge=0.001, ped=0.5, core=3.9, rgrid=257, expin=1.3, expout=1.7, widthp=widthp, xphalf=xphalf) * 1e3

pres = (1.6022e-19 * ne * Te) + (1.6022e-19 * ni * Ti)

Zeff = np.ones_like(psi_n)*2.

##CURRENT SCALING METHODS

def profLocalMin(prof, lowerBound = None, upperBound = None):
    if upperBound != None & lowerBound != None:
        profileSection = prof[lowerBound:upperBound]
    elif upperBound == None & lowerBound != None:
        profileSection = prof[lowerBound:]
    elif upperBound != None & lowerBound == None:
        profileSection = prof[:upperBound]
    elif upperBound == None & lowerBound == None:
        profileSection = prof

    minimumValue = np.min(profileSection)
    minValIndex = np.where(profileSection == minimumValue) + lowerBound
    return minimumValue, minValIndex

def profLocalMax(prof, lowerBound, upperBound = None):
    if upperBound != None & lowerBound != None:
        profileSection = prof[lowerBound:upperBound]
    elif upperBound == None & lowerBound != None:
        profileSection = prof[lowerBound:]
    elif upperBound != None & lowerBound == None:
        profileSection = prof[:upperBound]
    elif upperBound == None & lowerBound == None:
        profileSection = prof

    maxValue = np.max(profileSection)
    maxValIndex = np.where(profileSection == maxValue) + lowerBound
    return maxValue, maxValIndex

def pedStartAndMax(prof, x_coord = None):
    
    """
    Find the pedestal minimum (start) and maximum (top) in profile.

    Parameters:
    -----------
    profile : array-like
        Profile data (j_tor, pressure, etc.)
    x_coord : array-like, optional
        Corresponding radial coordinates. If None, returns indices.

    Returns:
    --------
    ped_min_index, ped_max_index : indices of pedestal foot and top
    """
    # Calculate second derivative to find inflection points
    prof_double_prime = np.diff(np.sign(np.diff(prof)))

    # Focus on outer half of profile where pedestal is typically located
    half_idx = len(prof_double_prime) // 2

    # Find all local maxima (where second derivative is -2)
    maxima_idx = np.where(prof_double_prime == -2)[0] + 1

    # Find all local minima (where second derivative is 2)
    minima_idx = np.where(prof_double_prime == 2)[0] + 1

    # Filter to the edge region
    edge_maxima = maxima_idx[maxima_idx > half_idx]
    edge_minima = minima_idx[minima_idx > half_idx]

    # Select the most prominent extrema in the edge region
    ped_max_index = edge_maxima[np.argmax(prof[edge_maxima])] if len(edge_maxima) > 0 else None
    ped_min_index = edge_minima[np.argmin(prof[edge_minima])] if len(edge_minima) > 0 else None

    # Return coordinates if provided, otherwise indices
    if x_coord is not None and ped_min_index is not None and ped_max_index is not None:
        return x_coord[ped_min_index], x_coord[ped_max_index]
    else:
        return ped_min_index, ped_max_index

def isolatePedestal(prof, x_coord):
    """
    Returns a new profile consisting of inputs pedestal

    Parameters:
    -----------
    prof : array-like
        Profile data (j_tor, pressure, etc.)
    x_coord : array-like, optional
        X-coordinate associated with profile
    Returns:
    --------
    pedestal, ped_x_coords : arrays with only the pedestal and the x_coords of the pedestal
    """

    pedStart, pedPeak = pedStartAndMax(prof, x_coord)

    pedestal = prof[pedStart:]
    
    ped_x_coords = x_coord[pedStart:]
    
    return pedestal, ped_x_coords

def FWHM(x_coord, prof):

    pedestal, ped_x_coords = isolatePedestal(x_coord, prof)

    pedStartIndex, pedMaxIndex = pedStartAndMax(prof, x_coord)
    
    baseline = pedestal[0] 

    half_max = (pedMaxIndex - baseline) / 2 + baseline

    left_indices = np.where(pedestal[:pedMaxIndex] <= half_max)[0]
    left_idx = left_indices[-1] if len(left_indices) > 0 else 0

    right_indices = np.where(pedestal[pedMaxIndex:] <= half_max)[0]
    right_idx = right_indices[0] + pedMaxIndex if len(right_indices) > 0 else len(prof)-1

    fwhm = x_coord[right_idx] - x_coord[left_idx]

    return fwhm


def currentScaleFunc(x, c1, c2, s, w):
    return c1 + c2/np.cosh( 2*(x - s )/w )**2


##COLLISIONALITY CALCULATION METHODS

def ln_lambda(tempProf, densityProf):
    return 24 + 3*np.log(10) - 0.5*np.log(densityProf) + np.log(tempProf)

def nu_e(te, ne):
    ##collision frequency
    zeff = 1.6
    fac = 4 * np.sqrt(2 * pi) * e_charge**4 / (4 * pi * epsilon_0) ** 2 / 3.0 / m_e**0.5 * eV2J**-1.5 * 17
    return fac * zeff * ne * ln_lambda(te, ne) / 17.0 / te**1.5

def nu_star(te, ne):
    ##collisionality
    Zeff = 1.6
    eps_nz = 1/2.5
    q = 1
    R = 2.5
    return 6.921e-18 * abs(q) * R * ne * Zeff * ln_lambda(te, ne) / (te**2 * eps_nz**1.5)

