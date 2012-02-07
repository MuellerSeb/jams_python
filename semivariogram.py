#!/usr/bin/env python

import time
import numpy as np

def semivariogram(x,y,v,nL,di,td,type='omnidirectional',model='exponential',
                  graph=True,lunit='m',p0=(0.5,0.5,100),runtimediag=True):

    """
    Calculates single or multiple experimental semivariogram(s) for
    spatial distributed data. X and Y coordinates and corresponding
    values are required in separate numpy arrays. Different theoretical
    semivariograms can be fitted. Results are plotted in various graphs
    and the fitted model parameters are given to the output.
    

    Requirements
    ------------    
    pylab, scipy (at least version 0.8.0), matplotlib, numpy
    

    Definition
    ----------
    def semivariogram(x,y,v,nL,di,td,type='omnidirectional',
                      model='exponential',graph=True,lunit='m',
                      p0=(0.5,0.5,100)):
                

    Input
    -----
    x    :    numpy array with longitude ('easting')
    y    :    numpy array with latitude ('northing')
    v    :    numpy array with values
    nL   :    int with number of lags to calculate
    di   :    list with angles to consider (in degree). di's > 180
              or < -180 are not allowed.
    td   :    int with one sided angle tolerance, so td=30 means
              an angular span of 60 (in degree). Choose td big
              enough, so that no "empty" angular span with no
              samples appear. Otherwise, an exeption appears.
              td > 180 is not allowed.

    
    Parameters
    ----------
    type :    type of semivariogram
    
        'omnidirectional' semivariogram is calculated for the hole
                          circle from 0 to 180 and 0 to -180. So 
                          every direction is considered. (default)
        'directional'     semivariogram is calculated only for the
                          given angles in di. Orientation is not
                          considered, so that e.g. 45 deg equals 
                          -135 deg. Due to that, negative angles
                          in di make no sense (and are not allowed)
                          here.
        'directional+orientational'
                          semivariogram is calculated only for the
                          given angles in di. Orientation is
                          considered. Every angle between 0 to 180
                          and 0 to -180 are allowed.
    
    model:    type of theoretical semivariogram model to fit to the
              experimental semivariogram.
              
        'exponential'     exponential semivariogram model (default)
        'spherical'       sperical semivariogram model
        'gaussian'        gaussian semivariogram model
        'noidea'          fitts all three models and returns the one
                          with the smallest coefficient of variation
                          (That does not mean, the returning model
                          is the best model for your data, it only
                          has the smallest parameter variation, but
                          it may help you with the decision for the
                          right model)
        'nomodel'         model fitting is disabled
    
    graph:    If True, plotting is enabled. If False, plotting is
              disabled. (default=True)
    
    lunit:    Unit of the longitude and latitude (default=meter, 
              only used for plot labeling)
    
    p0   :    Initial guess for parameter estimation of the 
              theoretical semivariogram.
              1st entry: equals approximately the nugget
              2nd entry: equals approximately nugget-sill
              3rd entry: equals approximately the range
              (default=(0.5,0.5,100))
              Sometimes you have to play around with it if no
              fitting result can be reached.
    
    runtimediag:
              If True, during run time of the function, diagnostics
              are printed to the console. If False, runtime diagnostics
              print is disabled. (default=True)
       

    Output
    ------
    nugget:   height of nugget(s) [(unit of v)**2]
    sill  :   height if sill(s) [(unit of v)**2]
    range :   distance of range [unit of x and y]
    vark  :   coefficient(s) of variation averaged over all three
              model parameter (goodness-of-fit) [-] 
    pcov  :   matrices of parameter variance and covariances
              of the model parameters
    h     :   array(s) of lags
    g     :   array(s) of variances
    c     :   array(s) of samples per lag
              

    Graphs
    ------
    Figure 1: shows a scatter plot of your original geodata
    
    Figure 2: shows the experimental and theoretical semivariogram
    
    Figure 3: shows the number of samples in each lag and angle
    
    Figure 4: visualize di and td, the angles and angle tolerances
              you have chosen.
    

    Examples
    --------
    # provide you some sample data:
    # easting
    >>> x = np.array([557509.27, 557518.11, 557526.95, 557535.79, 557544.63, 557553.47\
                    , 557544.63, 557535.79, 557526.95, 557518.11, 557526.95, 557535.79\
                    , 557544.63, 557553.47, 557562.31, 557571.15, 557562.31, 557553.47\
                    , 557544.63, 557535.79, 557544.63, 557553.47, 557562.31, 557571.15\
                    , 557579.99, 557597.66, 557579.99, 557562.31, 557544.63, 557526.7\
                    , 557509.27, 557491.60, 557473.92, 557491.6 , 557509.27, 557526.95\
                    , 557544.63, 557562.31, 557579.99, 557597.66, 557615.34, 557650.7\
                    , 557686.05, 557756.76, 557827.47, 557898.18, 557827.47, 557756.76\
                    , 557686.05, 557615.34, 557650.70, 557686.07, 557721.41, 557756.76\
                    , 557721.41, 557686.05, 557650.70, 557686.05, 557650.7,  557579.99\
                    , 557615.34, 557509.27, 557579.99, 557544.63, 557509.27, 557473.92\
                    , 557438.56, 557403.21, 557438.56, 557473.92, 557509.27, 557544.63\
                    , 557579.99, 557615.34, 557615.34, 557579.99, 557544.63, 557509.27\
                    , 557473.92, 557438.56, 557403.21, 557367.85, 557332.5,  557367.85\
                    , 557403.21, 557438.56, 557473.92, 557332.50, 557261.79, 557191.08\
                    , 557261.79, 557332.50, 557403.21, 557473.92, 557544.63, 557615.34])

    # northing
    >>> y = np.array([4332422.55, 4332413.71, 4332404.87, 4332396.03, 4332387.19, 4332396.03\
                    , 4332404.87, 4332413.71, 4332422.55, 4332431.39, 4332440.23, 4332431.39\
                    , 4332422.55, 4332413.71, 4332404.87, 4332413.71, 4332422.55, 4332431.39\
                    , 4332440.23, 4332449.07, 4332457.91, 4332449.07, 4332440.23, 4332431.39\
                    , 4332422.55, 4332404.87, 4332387.19, 4332369.52, 4332351.84, 4332369.52\
                    , 4332387.19, 4332404.87, 4332422.55, 4332440.23, 4332457.91, 4332475.58\
                    , 4332493.26, 4332475.58, 4332457.91, 4332440.23, 4332422.55, 4332316.48\
                    , 4332210.42, 4332281.13, 4332351.84, 4332422.55, 4332493.26, 4332563.97\
                    , 4332634.68, 4332563.97, 4332528.62, 4332493.25, 4332457.91, 4332422.55\
                    , 4332387.19, 4332351.84, 4332387.19, 4332422.55, 4332457.91, 4332599.33\
                    , 4332493.26, 4332599.33, 4332528.62, 4332563.97, 4332528.62, 4332493.26\
                    , 4332457.91, 4332422.55, 4332387.19, 4332351.84, 4332316.48, 4332281.13\
                    , 4332316.48, 4332351.84, 4332281.13, 4332245.77, 4332210.42, 4332245.77\
                    , 4332281.13, 4332316.48, 4332351.84, 4332387.19, 4332422.55, 4332457.91\
                    , 4332493.26, 4332528.62, 4332563.97, 4332563.97, 4332493.26, 4332422.55\
                    , 4332351.84, 4332281.13, 4332210.42, 4332139.71, 4332069.00, 4332139.71])

    # value
    >>> v = np.array([9.94691161e-01, 7.94158417e-02, 0.00000000e+00, 1.75837990e+00\
                    , 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00\
                    , 1.02915310e+00, 2.69597379e+00, 2.14552427e+00, 2.18417112e+00\
                    , 0.00000000e+00, 8.96101277e-01, 1.14034753e+00, 3.46398689e-01\
                    , 3.01418491e-01, 0.00000000e+00, 1.17920343e+00, 1.09682206e+00\
                    , 4.79485665e-01, 0.00000000e+00, 1.83183398e+00, 0.00000000e+00\
                    , 0.00000000e+00, 0.00000000e+00, 9.86233407e-02, 7.68290376e-02\
                    , 2.63911513e-01, 0.00000000e+00, 2.10013460e+00, 0.00000000e+00\
                    , 2.47535521e+00, 1.47047869e+00, 8.00371532e-01, 2.39448347e+00\
                    , 0.00000000e+00, 2.26426861e+00, 0.00000000e+00, 0.00000000e+00\
                    , 1.13769438e+00, 1.01969271e+00, 2.26036007e+00, 2.38991410e+00\
                    , 1.82558084e-03, 0.00000000e+00, 0.00000000e+00, 2.52583544e+00\
                    , 6.35195403e-01, 2.43778382e+00, 0.00000000e+00, 2.47738704e+00\
                    , 8.83280548e-01, 2.42328547e+00, 0.00000000e+00, 2.41534081e+00\
                    , 2.45629467e+00, 0.00000000e+00, 2.50770630e+00, 1.30382267e+00\
                    , 2.06891940e+00, 9.17384801e-02, 0.00000000e+00, 1.10185544e-01\
                    , 2.53460688e+00, 2.15217780e+00, 1.16908154e+00, 1.70072787e-01\
                    , 1.60603658e-01, 2.15438377e+00, 2.32464926e+00, 3.26255002e-01\
                    , 0.00000000e+00, 1.48404530e+00, 2.10439439e+00, 0.00000000e+00\
                    , 0.00000000e+00, 0.00000000e+00, 2.34663663e-01, 1.46993948e+00\
                    , 2.67691613e+00, 2.13262460e-02, 1.01551520e+00, 1.10878523e+00\
                    , 1.80374874e+00, 1.85571813e+00, 2.93929948e+00, 4.43192829e-01\
                    , 2.55962879e+00, 0.00000000e+00, 1.46545683e+00, 1.75659977e+00\
                    , 0.00000000e+00, 2.37093751e+00, 0.00000000e+00, 0.00000000e+00])
    
    # omnidirectional semivariogram with exponential model and fifty lags
    >>> td = 180
    >>> di = [0]
    >>> nL = 50
    >>> h, g, c = semivariogram(x,y,v,nL,di,td,type='omnidirectional',\
                  model='nomodel',graph=False,lunit='m',p0=(0.5,0.5,100), runtimediag=False)
    >>> print np.round(g,3)
    [[ 0.55   0.776  0.619  0.849  0.991  1.033  1.067  1.106  1.079  1.002
       1.119  1.06   0.935  0.789  1.117  1.125  1.063  1.015  1.041  0.911
       1.077  1.116  1.202  1.195  0.935  0.918  0.946  0.596  1.035  1.153
       1.205  1.635  1.384  0.806  0.006  1.409  0.748  0.31   0.977  1.95
       1.748  1.087]]
    >>> nugget, sill, range, vark, pcov, h, g, c = semivariogram(x,y,v,nL,di,td,type='omnidirectional',\
                  model='exponential',graph=False,lunit='m',p0=(0.5,0.5,100), runtimediag=False)
    >>> print round(nugget, 3)
    0.425
    >>> print round(sill, 3)
    1.056
    >>> print round(range, 0)
    93.0
    
    # directional semivariogram with spherical model and fifty lags
    >>> td = 45
    >>> di = [0,90]
    >>> nL = 50
    >>> nugget, sill, range, vark, pcov, h, g, c = semivariogram(x,y,v,nL,di,td,type='directional',\
                  model='spherical',graph=False,lunit='m',p0=(0.5,0.5,100), runtimediag=False)
    >>> print np.round(nugget, 3)
    [ 0.487  0.554]
    >>> print np.round(sill, 3)
    [ 1.071  1.034]
    >>> print np.round(range, 0)
    [  94.  112.]
    
    # directional+orientational semivariogram with gaussian model and fifty lags
    >>> td = 30
    >>> di = [0,45,90,135,180,-45,-90,-135]
    >>> nL = 50
    >>> nugget, sill, range, vark, pcov, h, g, c = semivariogram(x,y,v,nL,di,td,type='directional+orientational',\
                  model='spherical',graph=False,lunit='m',p0=(0.5,0.5,100), runtimediag=False)
    >>> print np.round(nugget, 3)
    [ 0.041  0.393  0.529  0.538 -0.127  0.651  0.504 -1.106]
    >>> print np.round(sill, 3)
    [ 1.075  1.193  1.171  1.187  1.008  1.13   1.103  1.086]
    >>> print np.round(range, 0)
    [  74.  122.  132.  130.   82.  171.  310.   35.]


    History
    -------
    Written AP, Feb 2011 - small code parts based on Alghalandis.com
    """

    if (np.shape(x)!=np.shape(y)) or (np.shape(y)!=np.shape(v)):
        raise TypeError('SemivariogramError: x, y and v must have the same dimensions!')
    
    if type == 'directional' and np.less(di,0).any():
        raise TypeError('SemivariogramError: if you choose type=directional,'
                        ' no negative directions in di are allowed')
        
    if (np.array(di).any() > 180) or (np.array(di).any() < -180):
        raise TypeError('SemivariogramError: elements of di > 180 or < -180 are not allowed.')        
        
    if td > 180:
        raise TypeError('SemivariogramError: td > 180 is not allowed.')        
    
    try:
        from scipy.optimize import curve_fit # requires at least scipy 0.8.0
    except ImportError:
        model = 'nomodel'
        print 'SemivariogramWarning: the package scipy.optimize.curve_fit can not be found. It requires at least scipy 0.8.0. No fitting of experimental semivariogram(s) is possible.'

    start = tic()
    
    #---------------------------------------
    #compute all distances and angles between vectors x and y
    r,t,xr,n = distang(x,y)
    
    t = np.where(t==-180, 180, t)
    
    if type == 'omnidirectional':
        headtitle = 'Omnidirectional Semivariogram'
        di = [0]
        td = 180
    elif type == 'directional':
        headtitle = 'Directional Semivariograms'
    elif type == 'directional+orientational':
        headtitle = 'Directional and Orientational Semivariograms'
    else:
        raise NameError('SemivariogramError: wrong semivariogram type! '
         'Choose omnidirectional, directional or directional+orientational')
    
    #---------------------------------------
    # compute semivariogram
    h = []
    g = []
    c = []
    for i in di:
        hi,gi,ci = semivario(r,t,xr,n,v,nL,i,td,type=type)
        h.append(hi)
        g.append(gi)
        c.append(ci)
    
    if runtimediag:
        stop1 = tic()
        print 'Experimental semivariogram took %0.3f seconds' %(stop1-start)
    
    if model == 'exponential':
        func  = [expvar]
        range = [exprange]
    elif model == 'spherical':
        func  = [sphvar]
        range = [sphrange]
    elif model == 'gaussian':
        func  = [gauvar]
        range = [gaurange]
    elif model == 'noidea':
        func  = [expvar, sphvar, gauvar]
        range = [exprange,sphrange,gaurange]
    elif model == 'nomodel':
        pass
    else:
        raise NameError('SemivariogramError: wrong semivariogram model! '
         'Choose exponential, spherical or gaussian')
    
    #---------------------------------------
    # fit semivariogram model
    if model != 'nomodel':
        subtitles = ['Exponential Semivariogram Model', 'Spherical Semivariogram Model', 'Gaussian Semivariogram Model' ]
        popt = np.zeros((len(func),len(di),3))
        pcov = np.zeros((len(func),len(di)),dtype='object')
        vark = np.zeros((len(func),len(di)))
        for j in xrange(len(func)):
            for i in xrange(len(di)):
                try:
                    popti, pcovi = curve_fit(func[j], h[i], g[i], p0=p0)
                    popt[j,i] = popti
                    pcov[j,i] = pcovi
                    vark[j,i] = np.mean(np.sqrt(pcovi.diagonal())/popti)
                except AttributeError:
                    vark[j,i] = float('inf')
                    print 'SemivariogramWarning: %s can not be fitted to %i deg angle' %(subtitles[j], di[i])
        
        ind = np.argmin(np.mean(vark, axis=1))
        
        if runtimediag:
            stop2 = tic()
            print 'Theoretical semivariogram took %0.3f seconds' %(stop2-stop1)

        nugget = popt[ind,:,0]
        sill   = popt[ind,:,0] + popt[ind,:,1]
        range  = range[ind](sill,popt[ind,:,0], popt[ind,:,1], popt[ind,:,2])
        vark   = vark[ind]
        pcov   = pcov[ind]
        
        if runtimediag:
            print 'Model: %s'%subtitles[ind]
            print 'Nugget(s): %s'%nugget
            print 'Sill(s): %s'%sill
            print 'Range(s): %s'%range
            print 'Coefficient(s) of variation: %s'%vark
            print 'Covariance/Variance matrices: %s'%pcov
    
    #---------------------------------------
    # plot
    if graph:
        import matplotlib.cm as cm
        import matplotlib.pyplot as plt
        # scatterplot of input data
        plt.figure(1)                               
        scat=plt.scatter(x,y,s=40,c=v,cmap='BrBG')                  
        plt.xlabel('X [%s]' %lunit)
        plt.ylabel('Y [%s]' %lunit)
        plt.title('Scatter Plot')
        plt.axis('image')
        plt.colorbar(scat)
        plt.grid(True)      
        
        # semivariogram plot with/without fitted model
        plt.figure(2)                              
        for i in xrange(len(di)):                       
            plt.plot(h[i],g[i],'o-', c=cm.jet(256/len(di)*i), label='%i'%di[i])                      
            if model != 'nomodel':
                plt.plot(h[i], func[ind](h[i], popt[ind,i,0], popt[ind,i,1], popt[ind,i,2]), '-', c=cm.jet(256/len(di)*i))
        plt.xlabel('h [%s]' %lunit)
        plt.ylabel(r'$\gamma(X,Y)$')
        if model != 'nomodel':                  
            plt.title('%s \n %s' %(headtitle, subtitles[ind]))
        else:
            plt.title('%s' %(headtitle))
        plt.axis('auto')
        plt.grid('on')                            
        plt.legend()                     
    
        # plot samples per lag
        plt.figure(3)                              
        for i in xrange(len(di)):                       
            plt.plot(h[i],c[i],'o-', c=cm.jet(256/len(di)*i), label='%i'%di[i])                      
        plt.xlabel('h [%s]' %lunit)
        plt.ylabel('Samples per lag')                    
        plt.title('%s' %(headtitle))
        plt.axis('auto')
        plt.grid('on')                            
        plt.legend()
        
        # plot of directions
        fig = plt.figure(4, figsize=(6,6))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True, axisbg='black')
        if type == 'directional':
            theta = np.deg2rad(append((np.array(di)-td),(np.array(di)-td)+180))
        else:
            theta = np.deg2rad(np.array(di)-td)
        radii = np.ones_like(theta)
        radii[::2] += 0.1
        width = np.deg2rad(np.ones_like(theta)*td*2)
        xlab =[]
        for i in xrange(19):
            xlab.append(r'$\sf{%i\degree}$' %(i*10))
        for i in xrange(17):
            xlab.append(r'$\sf{%i\degree}$' %(-170+i*10))
        bars = ax.bar(theta, radii, width=width, bottom=0.0)
        
        for r,bar in zip(radii, bars):
            bar.set_facecolor('#00ff04')
            bar.set_edgecolor('yellow')
            bar.set_alpha(0.5)
            ax.set_yticklabels(radii, alpha=0)
            ax.xaxis.set_major_locator(plt.LinearLocator(numticks=37, presets=None))
            ax.set_xticklabels(xlab, fontsize=15)
            plt.grid(color='yellow')
        plt.suptitle(headtitle, fontsize=15)    
        
        plt.show()
               
    # output
    if model != 'nomodel':
        return nugget, sill, range, vark, pcov, h, g, c
    else:
        return h, g, c
    
#---------------------------------------
# sub functions
#---------------------------------------
# function to compute all distances and angles between vectors x and y
def distang(x,y):
    n = len(x)
    t = np.zeros(n*(n-1)/2)
    r = np.zeros(n*(n-1)/2)
    k = 0
    for o in range(n-1):
        for p in range(o+1,n):
            dx = x[p]-x[o]
            dy = y[p]-y[o]
            t[k] = np.arctan2(dy,dx)       # angle (theta)
            r[k] = np.sqrt(dx**2+dy**2)    # distance (ray)
            k += 1
    xr = max(r)
    return r,t,xr,n

#---------------------------------------
# function to compute semivariogram
def semivario(r,t,xr,n,z,nL,di,td,type='omnidirectional'):     # x and y are vectors of coordinates
    L = xr/nL                           # lag size
    g = np.zeros(nL)
    c = np.zeros(nL)
    a = np.deg2rad(di)                     # angle = direction in radian
    ta = np.deg2rad(td)                    # tolerance of angle in radians
    b = np.deg2rad(0.01)                   # buffer for numerical problems
    for s in range(nL):
        k = 0
        q = 0
        g[s] = 0
        c[s] = 0
        for o in range(n-1):
            for p in range(o+1,n):      
                if  (s*L < abs(r[k]) < (s+1)*L):
                    if type == 'omnidirectional':
                        g[s] += (z[p]-z[o])**2
                        q += 1
                    if type == 'directional':
                        if a<0:
                            m=np.deg2rad(di+180)
                        else:
                            m=np.deg2rad(di-180)
                            
                        if a+ta+b > np.deg2rad(180):
                            if ((a-ta-b)<t[k]<a) or (a<t[k]<np.deg2rad(180)+b) or (-np.deg2rad(180)-b<t[k]<(-np.deg2rad(360)+(a+ta+b))):
                                g[s] += (z[p]-z[o])**2
                                q += 1
                        elif a-ta-b < -np.deg2rad(180):
                            if ((a+ta+b)>t[k]>a) or (a>t[k]>-np.deg2rad(180)-b) or (np.deg2rad(180)+b>t[k]>(np.deg2rad(360)+(a-ta-b))):
                                g[s] += (z[p]-z[o])**2
                                q += 1
                        else:
                            if (a-ta-b)<t[k]<(a+ta+b):
                                g[s] += (z[p]-z[o])**2
                                q += 1
                                
                        if m+ta+b > np.deg2rad(180):
                            if ((m-ta-b)<t[k]<m) or (m<t[k]<np.deg2rad(180)+b) or (-np.deg2rad(180)-b<t[k]<(-np.deg2rad(360)+(m+ta+b))):
                                g[s] += (z[p]-z[o])**2
                                q += 1
                        elif m-ta-b < -np.deg2rad(180):
                            if ((m+ta+b)>t[k]>m) or (m>t[k]>-np.deg2rad(180)-b) or (np.deg2rad(180)+b>t[k]>(np.deg2rad(360)+(m-ta-b))):
                                g[s] += (z[p]-z[o])**2
                                q += 1
                        else:
                            if (m-ta-b)<t[k]<(m+ta+b):
                                g[s] += (z[p]-z[o])**2
                                q += 1        
                                
                    if type == 'directional+orientational':
                        if a+ta+b > np.deg2rad(180):
                            if ((a-ta-b)<t[k]<a) or (a<t[k]<np.deg2rad(180)+b) or (-np.deg2rad(180)-b<t[k]<(-np.deg2rad(360)+(a+ta+b))):
                                g[s] += (z[p]-z[o])**2
                                q += 1
                        elif a-ta-b < -np.deg2rad(180):
                            if ((a+ta+b)>t[k]>a) or (a>t[k]>-np.deg2rad(180)-b) or (np.deg2rad(180)+b>t[k]>(np.deg2rad(360)+(a-ta-b))):
                                g[s] += (z[p]-z[o])**2
                                q += 1
                        else:
                            if (a-ta-b)<t[k]<(a+ta+b):
                                g[s] += (z[p]-z[o])**2
                                q += 1
                k += 1
        #MC: q can becore zero ???
        if q == 0.:
            g[s] = np.nan
        else:
            g[s] /= (q*2)
        c[s] = q
    h = np.array(range(nL))*L+L/2    
    h = np.delete(h,np.where(np.isnan(g)))       # ranges 
    c = np.delete(c,np.where(np.isnan(g)))       # number of samples per range
    g = np.delete(g,np.where(np.isnan(g)))       # variance per range
    return h,g,c

#---------------------------------------
# exponential semivariogram model
def expvar(h,c0,ce,a0):
    return c0 + ce*(1.-np.exp(-abs(h)/a0))
# range of exponential model at a given sill
def exprange(sill,c0,ce,a0):
    return -np.log(-(sill*0.95-c0)/ce+1)*a0

#---------------------------------------
# spherical semivariogram model
def sphvar(h,c0,ce,a0):
    return np.where((0 <= np.abs(h)) & (np.abs(h) <= a0), c0 + ce*((3./2.)*(abs(h)/a0) - (1./2.)*(abs(h)/a0)**3), c0 + ce)
# range of spherical model at a given sill
def sphrange(sill,c0,ce,a0):
    return a0

#---------------------------------------
# gaussian semivariogram model
def gauvar(h,c0,ce,a0):
    return c0 + ce*(1. - np.exp(-h**2/a0**2))
# range of gaussian model at a given sill
def gaurange(sill,c0,ce,a0):
    return np.sqrt( -(a0)**2 * np.log(-(sill*0.95-c0)/ce+1))

#---------------------------------------
# timing
def tic():                              
    sec = time.time()
    return sec

# DOCTEST:
if __name__ == '__main__':
    import doctest
    doctest.testmod()
# END
