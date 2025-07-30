

def lin_fit_fn(xvec, *coeff):
    a1,a2 = coeff
    return a1*xvec + a2

def quad_fit_fn(xvec, *coeff):
    a1,a2,a3 = coeff
    return a1*xvec*xvec + a2*xvec + a3