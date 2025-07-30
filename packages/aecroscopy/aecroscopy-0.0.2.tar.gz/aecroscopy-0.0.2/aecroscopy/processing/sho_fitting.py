#Here we will put some SHO fitting stuff
import numpy as np
import sidpy

def SHO_fit_flattened(wvec,*p):
    Amp, w_0, Q, phi=p[0],p[1],p[2],p[3]
    func = Amp * np.exp(1.j * phi) * w_0 ** 2 / (wvec ** 2 - 1j * wvec * w_0 / Q - w_0 ** 2)
    return np.hstack([np.real(func),np.imag(func)])

def sho_guess_fn(freq_vec,ydata):
    amp_guess = np.abs(ydata)[np.argmax(np.abs(ydata))]
    Q_guess = 50
    phi_guess = np.angle(ydata)[np.argmax(np.abs(ydata))]
    w_guess = freq_vec[np.argmax(np.abs(ydata))]
    p0 = [amp_guess, w_guess, Q_guess, phi_guess]
    return p0

def better_sho_guess_fn(freq_vec,ydata):
    ydata = np.array(ydata)
    amp_guess = np.abs(ydata)[np.argmax(np.abs(ydata))]
    Q_guess = 50
    max_min_ratio = np.max(abs(ydata)) / np.min(abs(ydata))
    phi_guess = np.angle(ydata)[np.argmax(np.abs(ydata))]
    w_guess = freq_vec[np.argmax(np.abs(ydata))]

    #Let's just run some Q values to find the closest one
    Q_values = [5,10,20,50,100,200,500]
    err_vals = []
    for q_val in Q_values:
        p_test = [amp_guess/q_val, w_guess, q_val, phi_guess]
        func_out = SHO_fit_flattened(freq_vec,*p_test)
        complex_output = func_out[:len(func_out)//2] + 1j*func_out[(len(func_out)//2):]
        amp_output = np.abs(complex_output)
        err = np.mean((amp_output - np.abs(ydata))**2)
        err_vals.append(err)
    Q_guess = Q_values[np.argmin(err_vals)]
    p0 = [amp_guess/Q_guess, w_guess, Q_guess, phi_guess]
    return p0

def perform_SHO_fitting(sid_dset, process_args):
    """
    This function takes as input a sidpy dataset and processing arguments to perform SHO Fitting
    Used in conjunction with the process server (server.py)
    """
    print('---Performing SHO Fit----')
    #get some defaults out of the way
    chosen_parms = {'ind_dims': [0,1], 'num_workers':4, 'return_cov':False, 'return_fit': False,
                    'return_std': False, 'km_guess':False, 'num_fit_parms':None,
                    'threads':1}
    
    process_details = sid_dset.metadata['sid_process']
    process_parms = process_details['arguments']

    for key in process_args.keys():
        chosen_parms[key] = process_args[key]
    
    fitter = sidpy.proc.fitter.SidFitter(sid_dset, SHO_fit_flattened,
                        num_workers=chosen_parms['num_workers'],
                        guess_fn = better_sho_guess_fn,ind_dims=chosen_parms['ind_dims'],
                    threads=chosen_parms['threads'], return_cov=chosen_parms['return_cov'], 
                    return_fit=chosen_parms['return_fit'], return_std=chosen_parms['return_std'],
                    km_guess=chosen_parms['km_guess'],num_fit_parms = chosen_parms['num_fit_parms'],
                    n_clus=5)
    
    #Let's see if the progressbar works
    #from dask.diagnostics import ProgressBar
    #ProgressBar().register()
    freq_vec = sid_dset._axes[2].values
    lb = [0, freq_vec.min(), 5, -2*np.pi]
    ub = [1000, freq_vec.max(), 5000, 2*np.pi]
    fitter.do_guess()
    fit_parameters = fitter.do_fit(bounds=(lb,ub), maxfev=30)
    fit_parameters= fitter.do_fit() #Fit the SHO

    print(fit_parameters)

    return fit_parameters, fitter


'''
We can use the above to do SHO fits to any sidpy dataset, consider for example
a sidpy dataset of size [50,50,44,64,3]
where the dimensions are [X,Y,frequency,voltage_steps,cycle]

The advantage is we can also use Kmeans for the priors (need latest version of sidpy from main though)

The code to run is
#Instantiate the SidFitter class
fitter = sidpy.proc.fitter.SidFitter(beps_raw, SHO_fit_flattened,num_workers=4,guess_fn = guess_fn,ind_dims=[0,1,3,4],
                           threads=2, return_cov=False, return_fit=False, return_std=False,
                           km_guess=True,num_fit_parms = 2)

fit_parameters= fitter.do_fit() #Fit the SHO

'''