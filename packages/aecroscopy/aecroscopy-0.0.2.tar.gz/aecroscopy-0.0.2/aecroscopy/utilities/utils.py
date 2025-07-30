import progressbar
import numpy as np
import os
import inspect
import sidpy
import h5py
import pyNSID

# utilities functions

def logger(func):
    """Although the following wrapper should technically work 
    for all sorts of methods (static, class),
    We want to write the log to an attribute of the 'self' object.
    This creates problems for static and class methods,
    since they are not bound to self
    Since we do not have any static or class methods now, 
    we will cross that bridge when we get to it."""
    def wrapper(*args, **kwargs):
        bound_args = inspect.signature(func).bind(*args, **kwargs)
        bound_args.apply_defaults()
        all_args = bound_args.arguments
        log_fname = all_args['self']._log_file_name
        all_args.pop('self')._log.append({func.__name__: all_args})
        with open("{}.txt".format(log_fname), "a") as logsave:
            logsave.write("\n\n" + str({func.__name__: all_args}))

        return func(*args, **kwargs)
    return wrapper

def make_be_dset(file_name, pfm_imgstack, channel_imgstack, complex_spectra,
                start_x, finish_x, start_y, finish_y, freq_vector = None, coordinates = None, beps = False,
                be_parms = None, vec_dc = None, metadata = {}, beps_parms = {}):
        """
        Creates an H5 file to save band excitation data.

        Args:
            file_name (str): Customized H5 file name.
            pfm_imgstack (numpy.ndarray): Array containing all band excitation PFM image channels.
            channel_imgstack (numpy.ndarray): Array containing all images from customized channels.
            complex_spectra (numpy.ndarray): List containing the band excitation raw spectra.
            start_x (float or int): Start value of the X-axis for microscopy measurement locations.
            finish_x (float or int): Finish value of the X-axis for microscopy measurement locations.
            start_y (float or int): Start value of the Y-axis for microscopy measurement locations.
            finish_y (float or int): Finish value of the Y-axis for microscopy measurement locations.
            coordinates (numpy.ndarray, optional): Array representing where BEPS measurements were performed. Defaults to None.
            beps (bool, optional): Indicates whether the data to save is BEPS data. Defaults to False.
            metadata (dict, optional): Metadata dictionary
            beps_parms (dict, required if setting beps=True): Keys: 'Vdc'-> Vdc Vector, 'Cycles'->number of cycles

        Returns:
            sidpy datasets: If beps is False, returns sidpy datasets of BEPFM images, channel images, and BE complex spectra.
                            If beps is True, returns sidpy datasets of beps wavefrom, beps hyperimages, channel images, and BE complex spectra.
        """

        # Note: The following lines are commented out as they are under development.
        # scan_size_x = self.AR_paras[1][1]
        # scan_size_y = self.AR_paras[1][2]
        
        # TODO: check the scan sizes based on the AR metadata. Somethign like this:
        """
        if AR_scan_size_x in metadata.keys():
            scan_size_x = metadata["AR_scan_size_x"]
            scan_size_y = Ametadata["AR_scan_size_y"]
        
        """
        if beps:
            num_of_points = beps_parms['x_points']*beps_parms['y_points']
            number_beps_cycles = int(beps_parms['Cycles']*num_of_points)
            vdc_vector = beps_parms['Vdc']

        if 'ScanSize' in metadata.keys():
            scan_size_x = metadata["ScanSize"]
            scan_size_y = metadata["ScanSize"]
        else:
            scan_size_x = 10e-6
            scan_size_y = 10e-6
        len_x = np.abs(finish_x - start_x)
        len_y = np.abs(finish_y - start_y)
        
        # Quick fitting PFM images
        dset_imgs = sidpy.Dataset.from_array(pfm_imgstack, title = 'be stack')
        dset_imgs.data_type = 'image_stack'
        dset_imgs.quantity = 'quick fit pfm'

        dset_imgs.set_dimension(0, sidpy.Dimension(np.linspace(0, 1, dset_imgs.shape[0])*(scan_size_y*len_y)/2,
                                name = "y axis", units = "m", quantity = "y axis", dimension_type = "spatial"))
        dset_imgs.set_dimension(1, sidpy.Dimension(np.linspace(0, 1, dset_imgs.shape[1])*(scan_size_x*len_x)/2,
                                name = "x axis", units = "m", quantity = "x axis", dimension_type = "spatial"))
        dset_imgs.set_dimension(2, sidpy.Dimension(np.arange(dset_imgs.shape[2]), 
                                name = "BE responses", quantity = "channels", dimension_type = "frame"))
        
        # Channel images
        dset_chns = sidpy.Dataset.from_array(channel_imgstack, title = 'channel stack')
       
        dset_chns.data_type = 'image_stack'
        dset_chns.quantity = 'channels'
        print("Channels dataset is of shape {}".format(dset_chns.shape))
      
        num_channels = dset_chns.shape[0]    
        #TODO: This is all incorrect for BEPS measurements! Fix it...
        #We need an if condition - if BEPS, tehn the dataset size is (1,3,512)-> 3 channels, VDC steps. 1 is superfluous.
        #ignoring for now.

        yvector = np.linspace(0, 1, dset_chns.shape[1])*(scan_size_y*len_y)/2
        xvector = np.linspace(0, 1, dset_chns.shape[2])*(scan_size_x*len_x)/2

        dset_chns.set_dimension(0, sidpy.Dimension(np.arange(num_channels), name = 'Channels', quantity ='Channel #',
                                                dimension_type = 'frame'))                        
        dset_chns.set_dimension(1, sidpy.Dimension(yvector, name = "y axis", units = "m", quantity = "y axis", dimension_type = "spatial"))                                          
        dset_chns.set_dimension(2, sidpy.Dimension(xvector, name = "x axis", units = "m", quantity = "x axis", dimension_type = "spatial"))
        if len(dset_chns.shape)>3:
            dset_chns.set_dimension(3, sidpy.Dimension(np.arange(dset_chns.shape[-1]), name = "channels images", quantity = "other", dimension_type = "frame"))

        dset_chns.original_metadata = metadata

        # Complex spectra
        
        complex_spectra_arr = np.asarray(complex_spectra)
        print("Complex dataset is of shape {}".format(complex_spectra_arr.shape))
        dset_cs = complex_spectra_arr[...,0] + 1j*complex_spectra_arr[...,1]
        if beps:
            #if this is beps, the spectrogram gives us shape(num_vdc_points,num_freq_points).
            #we want to add the cycles axis. 
            dset_cs_nd = dset_cs.reshape((number_beps_cycles, len(vdc_vector), len(freq_vector)))
        else:
            dset_cs_nd = dset_cs.reshape((len(yvector), len(xvector), len(freq_vector)))

        dset_complex_spectra = sidpy.Dataset.from_array(dset_cs_nd, title = 'complex_spectra')
        dset_complex_spectra.quantity = 'Complex Spectra'
        dset_complex_spectra.units = 'V'

        if freq_vector is None: freq_vector = np.arange(len(dset_complex_spectra.shape[-1]))
        if beps:
            dset_complex_spectra.set_dimension(0, sidpy.Dimension(np.arange(number_beps_cycles),
                                            name = 'Cycles', quantity = 'cycle', units = 'a.u.', dimension_type = 'spectral'))

            dset_complex_spectra.set_dimension(1, sidpy.Dimension(vdc_vector,
                                            name = 'Vdc', quantity = 'Voltage', units = 'V', dimension_type = 'spectral'))
            
            dset_complex_spectra.set_dimension(2, sidpy.Dimension(freq_vector,
                                            name = 'Frequency', quantity = 'frequency', units = 'Hz', dimension_type = 'spectral'))
            
        else:

            dset_complex_spectra.set_dimension(0, sidpy.Dimension(yvector,
                                                name = 'y axis', quantity = 'y axis', units = 'm', dimension_type = 'spatial'))

            dset_complex_spectra.set_dimension(1, sidpy.Dimension(xvector,
                                            name = 'x axis', quantity = 'x axis', units = 'm', dimension_type = 'spatial'))
            
            dset_complex_spectra.set_dimension(2, sidpy.Dimension(freq_vector,
                                            name = 'Frequency', quantity = 'frequency', units = 'Hz', dimension_type = 'spectral'))
            
        dset_complex_spectra.original_metadata = metadata

        # Create H5 file to write data
        suf = 0
        save_name = "{}_{}.hf5".format(file_name, suf)
        # Update suffex if a file with the same name already exists
        while os.path.exists(save_name):
            suf += 1
            save_name = "{}_{}.hf5".format(file_name, suf)

        hf = h5py.File(save_name, 'a')

        # Save BE pulse parameters
        #beparms = self.VI.getcontrolvalue('BE_pulse_control_cluster')
        hf['BE Parameters/pulse parameters'] = np.asarray(be_parms)

        
        hf['BE Parameters/frequency'] = np.asarray(freq_vector)

        # Image size
        img_size = np.asarray([(dset_imgs.shape[0])*(scan_size_y*len_y)/2, (dset_imgs.shape[1])*(scan_size_x*len_x)/2])
        hf['BE Parameters/scan size'] = img_size

        # For BEPS data, save DC waveform as well
        if beps == True:
            hf['BEPS/vdc_waveform'] = vdc_vector
            hf['BEPS/coordinates'] = coordinates

        # Save quick fitting images
        hf.create_group("BE Quick Fitting") 
        pyNSID.hdf_io.write_nsid_dataset(dset_imgs, hf['BE Quick Fitting'], main_data_name="Quick Fitting")

        # Save channel images
        hf.create_group("BE Channels") 
        pyNSID.hdf_io.write_nsid_dataset(dset_chns, hf['BE Channels'], main_data_name="Channels_V1")
        
        # Save complex spectral
        hf.create_group("BE Complex Spectra") 
        pyNSID.hdf_io.write_nsid_dataset(dset_complex_spectra, hf['BE Complex Spectra'], main_data_name="Complex Spectra")

        hf.close()

        if beps == False:
            return dset_imgs, dset_chns, dset_complex_spectra
        elif beps == True:
            return vdc_vector, dset_imgs, dset_chns, dset_complex_spectra

def progress_bar(max_value):
    """
    Creates a progress bar to track the progress of long experiments.

    Args:
        max_value (int): The maximum number of iterations.

    Returns:
        progressbar.ProgressBar: The progress bar object.
    """
    widgets = [' [',
                progressbar.Timer(format= 'progress: %(elapsed)s'),
                '] ', progressbar.Bar('*'),' (',progressbar.ETA(), ') ',]
    bar = progressbar.ProgressBar(max_value=max_value, widgets=widgets).start()
    return bar

def convert_coordinates(original_coordinates=None, num_pix_x = 128, num_pix_y = 128, start_x = -1, finish_x = 1, start_y = -1, finish_y = 1):
    """
    Converts 2D space coordinates to the parameters of microscopy probe location.

    Args:
        original_coordinates (numpy.ndarray): Array representing the original coordinates in a 2D space.
        start_x (float or int): Start value of the X-axis in the target coordinate space. Default is -1.
        finish_x (float or int): Finish value of the X-axis in the target coordinate space. Default is 1.
        start_y (float or int): Start value of the Y-axis in the target coordinate space. Default is -1.
        finish_y (float or int): Finish value of the Y-axis in the target coordinate space. Default is 1.

    Returns:
        numpy.ndarray: Array representing the converted parameters of probe location.

    Notes:
        - The original_coordinates should be a numpy array of shape [2] with the first element representing Y-coordinate
            and the second element representing X-coordinate.
    """

    original_coordinates = np.asarray(original_coordinates, dtype = np.float64()) # convert to int to float first

    coor_x = original_coordinates [1]
    coor_y = original_coordinates [0]
    # rescale the data to be symmetric around 0
    convert_x = (coor_x - (num_pix_x/2)) / (num_pix_x)
    convert_y = (coor_y - (num_pix_y/2)) / (num_pix_y)

    # shift and scale it to the scan range
    convert_x = convert_x * (finish_x - start_x) + (finish_x + start_x) / 2
    convert_y = convert_y * (finish_y - start_y) + (finish_y + start_y) / 2
    
    # write converted locations
    converted_locations = np.copy(original_coordinates)
    converted_locations[1] = convert_x
    converted_locations[0] = convert_y

    return converted_locations