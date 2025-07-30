
'''
class Processing():
    def __init__(self,) -> None:      
       print('in process')

    def do_fit(k, cs_arr, qf_arr, wvec):
        lines, pix = cs_arr.shape[0], cs_arr.shape[1]
        i,j = int(k//pix), int(k%pix)  #CHECK
        Amp, w_0, Q, phi = qf_arr[i, j, :4]
        wmin = np.min(wvec)
        wmax = np.max(wvec)
        w_0 = (w_0-wmin)/(wmax-wmin) #scaling for resonant freq.
        Amp = 1E3 * Amp #scaling for amplitude
        phi = (phi+2*np.pi)/(4*np.pi) #Scaling for phase
        Q = Q/350 #Scaling for Q

        prior_norm = [Amp, w_0, Q, phi]

        prior_norm = np.clip([Amp, w_0, Q, phi], 0.001, 0.999)

        raw_dat_a = cs_arr[i,j,:]
        y = np.hstack([np.real(raw_dat_a),np.imag(raw_dat_a)])
    
        try:
            fitted_parms = least_squares(fun,x0 = prior_norm, bounds = (0,1), args = (wvec, y), verbose = 0).x
        except:
            fitted_parms = prior_norm
        
        return fitted_parms
    
    def make_dsets(qf, cs, local_parms, scan_size_x = 1.5, scan_size_y = 1.5, fit = True):
    
    qf_array = np.nan_to_num(np.array(qf))
    
    lines, pix = qf_array.shape[0], qf_array.shape[1]
    
    dset_qf = sid.Dataset.from_array(qf_array, title = 'Quick_fit_stack')
    dset_qf.data_type = 'image_stack'
    dset_qf.quantity = 'fast_fit_parameters'
    
    strt_x = local_parms['in_start_x'] 
    fnsh_x = local_parms['in_finish_x']
    strt_y = local_parms['in_start_y']
    fnsh_y = local_parms['in_finish_y']

    xlen = np.abs(fnsh_x - strt_x)
    ylen = np.abs(fnsh_y - strt_y)

    dset_qf.set_dimension(0, sid.Dimension(np.linspace(0,1,dset_qf.shape[0])*((scan_size_y*ylen)/2),
                                        name = 'Y',units = 'm',
                                        quantity = 'Y',
                                        dimension_type = 'spatial'))



    dset_qf.set_dimension(1, sid.Dimension(np.linspace(0,1,dset_qf.shape[1])*((scan_size_x*xlen)/2),
                                        name = 'X',units = 'm',
                                        quantity = 'X',
                                        dimension_type = 'spatial'))

    dset_qf.set_dimension(2, sid.Dimension(np.arange(dset_qf.shape[2]),
                                        name = 'C',
                                        quantity = 'channels',
                                        dimension_type = 'frame'))
    
    
    fft_frequencies = np.asarray(VI.getcontrolvalue('BE_pulse_parm_indicator_cluster')[7])
    fft_bin_indices = np.asarray(VI.getcontrolvalue('BE_pulse_parm_indicator_cluster')[3])

    #Channel names
    cs_arr = np.zeros([np.array(qf).shape[0], np.array(qf).shape[1], len(fft_frequencies[fft_bin_indices]), 2])
    
    for ind in range(len(cs)):
        try:
            cs_arr[ind] = cs[ind]
        except:
            cs_arr[ind] = 0.0
#             print(cs_arr[ind].shape)
#             print(cs[ind].shape)
            cs_arr[ind, :, 0:(cs[ind].shape[1]), :] = cs[ind]
        
#     cs_arr = np.asarray(cs)
    dset_cs = sid.Dataset.from_array(cs_arr[...,0] + 1j*cs_arr[...,1], title = 'complex_spectra')
    dset_cs.quantity = 'pfm_response'
    dset_cs.units = 'V'

    dset_cs.set_dimension(0, sid.Dimension(np.linspace(0,1,dset_qf.shape[0])*((scan_size_y*ylen)/2),
                                        name = 'Y',units = 'm',
                                        quantity = 'Y',
                                        dimension_type = 'spatial'))


    dset_cs.set_dimension(1, sid.Dimension(np.arange(dset_cs.shape[1]),
                                        name = 'X', units = 'm',
                                        quantity = 'X',
                                        dimension_type = 'spatial'))

   
    dset_cs.set_dimension(2, sid.Dimension(fft_frequencies[fft_bin_indices],
                                        name = 'nu', units = 'Hz',
                                        quantity = 'frequncy_bins',
                                        dimension_type = 'spectral'))
    
    if fit:
        
        wv = (fft_frequencies[fft_bin_indices])
        out = Parallel(n_jobs = 16)(delayed(do_fit)(k,cs_arr,qf_array, wv) for k in range(lines*pix))

        fit_dset = (np.asarray(out).reshape([lines, pix, -1]))
        
        #Making the dataset
        dset_shofit = sid.Dataset.from_array(fit_dset, title = 'SHO_fit_parms')
        dset_shofit.data_type = 'image_stack'
        dset_shofit.quantity = 'SHO_fit_parms'
        
        dset_shofit.set_dimension(0, sid.Dimension(np.linspace(0,1,fit_dset.shape[0])*((scan_size_y*ylen)/2),
                                        name = 'Y',units = 'm',
                                        quantity = 'Y',
                                        dimension_type = 'spatial'))



        dset_shofit.set_dimension(1, sid.Dimension(np.linspace(0,1,fit_dset.shape[1])*((scan_size_x*xlen)/2),
                                            name = 'X',units = 'm',
                                            quantity = 'X',
                                            dimension_type = 'spatial'))

        dset_shofit.set_dimension(2, sid.Dimension(np.arange(fit_dset.shape[2]),
                                            name = 'C',
                                            quantity = 'channels',
                                            dimension_type = 'frame'))

        dsets = [dset_qf, dset_cs, dset_shofit]
    else:
        dsets = [dset_qf, dset_cs]

    #Setting the metadata

    for dset in dsets:
        for i, val in enumerate(igor_para):
            dset.original_metadata[i] = val

        #Setting the metadata corresponding to the parms of the scan_image function
        dset.metadata.update(local_parms)
        dset.metadata['voltage_offset'] = voltage_offset
        dset.metadata['pixels'] = pix
        dset.metadata['setpoint'] = setpoint

        #BE Parameters
        BE_parms_names = ['center_frequency_Hz', 'band_width_Hz', 'amplitude_V',
                         'phase_variation', 'repeats', 'req_pulse_duration_s', 
                         'auto_smooth_ring', 'edge_smoothing_Hz', 'window_adjustment']
        BE_parms_values = VI.getcontrolvalue('BE_pulse_control_cluster')
        dset.metadata['BE_parms'] = {}
        for i, name in enumerate(BE_parms_names):
            dset.metadata['BE_parms'][name] = BE_parms_values[i]


        #IO Parameters
        IO_indicator_cluster_names = ['IO_AFM_platform', 'IO_card', 'IO_rate', 'IA_AO_range', 'Analog_output_rating',
                                     'IO_AI range', 'analog_output_amplifier', 'IO_Channel_011_type',
                                     'IO_Channel_012_type', 'IO_Channel_013_type']
        IO_indicator_cluster_values = VI.getcontrolvalue('IO_indicator_cluster')    
        dset.metadata['IO_indicator_parms'] = {}
        for i, name in enumerate(IO_indicator_cluster_names):
            dset.metadata['IO_indicator_parms'][name] = IO_indicator_cluster_values[i]

        dset.metadata['VS_wave_duration'] = VI.getcontrolvalue('Initialize_BE_line_scan_indicator_cluster')[0]

        dset.metadata['Bias_Parms'] = {}
        Bias_Parms_names = ['pulse_amp_V', 'pulse_on_duration_s', 'pulse_off_duration_s',
                                             'rise_time_s', 'pulse_repeats']
        Bias_Parms_values = VI.getcontrolvalue('voltage_pulse_control_cluster')
        
        for i, name in enumerate(Bias_Parms_names):
            dset.metadata['Bias_Parms'][name] = Bias_Parms_names[i]
        
    
    if fit:
        return [dset_qf, dset_cs, dset_shofit]
    else:
        return [dset_qf, dset_cs]

'''
