try:
    import win32com.client
except:
    pass

import os
import sys
import time
import numpy as np

class AECypher():
    def __init__(self, exe_path = r"C:\AsylumResearch\v18\Igor Pro Folder\Igor.exe", 
                 client = "IgorPro.Application") -> None:
        """
        Initializes the AE_Cypher class.

        Args:
            exe_path (str): Path to the Igor.exe executable file.
            client (str): Name of the IgorPro client.
        """ 

        # Set igor
        self.igor = win32com.client.Dispatch(client)
    
    def Set_MasterPanel(self, imaging_mode = "PFM Mode", scan_mode = "One Frame Mode", masterpanel_parameters = None, do_scan = None):
        """
        Operate Master Panel.

        Args:
            imaging_mode (str): imaging mode, such as 'Contact", 'PFM Mode'.
            scan_mode (str): scan mode, such as 'One Frame Mode', 'Continuous Mode'.
            masterpanel_parameters (dic): operating parameters, e.g., masterpanel_parameters = {"ScanSize": 7e-6, "PointsLines": 256}
        """ 
        # Set Imaging Mode and Scan Mode
        self.igor.Execute('print ARExecuteControl("ImagingModePopup_0", "MasterPanel", 0, {})'.format("\"" + imaging_mode + "\""))
        self.igor.Execute('print ARExecuteControl("LastScanPopup_0", "MasterPanel", 0, {})'.format("\"" + scan_mode + "\""))
        print ("Imaging Mode: {}".format(imaging_mode))
        print ("Scan Mode: {}".format(scan_mode))

        # Set parameters
        parms_list = ['ScanSize', 'PointsLines', 'ScanRate', 'Setpoint', 'DriveAmplitude', 'DriveFrequency',
        'IntergralGain', 'ScanSpeed', 'ScanAngle', 'XOffset', 'YOffset', 'ScanPoints', 'ScanLines', 'FastRatio',
        'SlowRatio','ProportionalGain', 'FBFilterBW']
        for i in range(len(parms_list)):
            if parms_list[i] in masterpanel_parameters:
                self.igor.Execute('print PV({}, {})'.format("\""+ parms_list[i] + "\"", masterpanel_parameters[parms_list[i]]))
                print ("{}: {}".format(parms_list[i], masterpanel_parameters[parms_list[i]]))

        time.sleep(1)
        # Start Scan
        if do_scan != None:
            if do_scan == "Frame Up":
                self.igor.Execute('print ARExecuteControl("UpScan_0", "MasterPanel", 0,"")')
            elif do_scan == "Frame Down":
                self.igor.Execute('print ARExecuteControl("DownScan_0", "MasterPanel", 0,"")')
            elif do_scan == "Stop":
                self.igor.Execute('print ARExecuteControl("StopScan_0", "MasterPanel", 0,"")')
        
        return

    def Set_CrosspointPanel(self, lockin = 'ARC', crosspoint_channels_settings = None, lock = True):
        """
        Setup CrosspointPanel

        Args:
            lockin (str): lockin in use, e.g., "ARC", "CypherA".
            crosspoint_channels_settings (dict): crosspoint channels, e.g., crosspoint_channels_settings = {"BNCOut0": "OutA", "Chip": "OutB"}.
            lock (booleans): lock settings or not.
        """ 
        # Set crosspoint channels
        display_channel_names = ['InA', 'InB', 'InFast', 'InAOffset', 'InBOffset', 'InFastOffset', 
        'OutXMod', 'OutYMod', 'OutZMod', 'FilterIn', 'BNCOut0', 'BNCOut1', 'BNCOut2', 
        'PogoOut', 'Chip', 'Shake']
        hide_channel_names = ['InAPopup', 'InBPopup', 'InFastPopup', 'InAOffsetPopup', 'InBOffsetPopup', 'InFastOffsetPopup', 
        'OutXModPopup', 'OutYModPopup', 'OutZModPopup', 'FilterInPopup', 'BNCOut0Popup', 'BNCOut1Popup', 'BNCOut2Popup', 
        'PogoOutPopup', 'ChipPopup', 'ShakePopup']
        for i in range(len(display_channel_names)):
            if display_channel_names[i] in crosspoint_channels_settings:
                # Set channels
                self.igor.Execute('print ARExecuteControl({}, "CrosspointPanel", 0, {})'.format("\""+ hide_channel_names[i] + "\"", "\""+ crosspoint_channels_settings[display_channel_names[i]]+ "\""))
                print ("{}: {}".format(display_channel_names[i], crosspoint_channels_settings[display_channel_names[i]]))
                # Lock channels
                if lock==True:
                    self.igor.Execute('print ARExecuteControl("XPTLock{}Box_0", "CrosspointPanel", True, "")'.format(i))
        
        # Write Crosspoint
        self.igor.Execute('print ARExecuteControl("WriteXPT", "CrosspointPanel", True, "")')
        print("Crosspoint panel setting has been written")
    
        return
    
    def Get_MasterVariables(self,):
        """
        Return a comprehensive dict with various experimental parameters
        """ 
        # Read data from MasterVariablesTable
        # Find the folder: Programming > Global Variables > Master > Right Click a Variable > Browser MasterVariablesWave > Data Folder
        mvs = self.igor.DataFolder(r'root:packages:MFP3D:main:variables')
        mvw = mvs.Wave('MasterVariablesWave')
    
        # Get the total number of variables
        dims = mvw.GetDimensions()
        variable_list_length = dims[1]
    
    
        # Set a dictionary to add variables and description
        mvs_dict = {}
        for i in range (variable_list_length):
            # MVs_dict[mvw.DimensionLabel(0,i,0)] = mvw.MDGetNumericWavePointValue(i, 0, 0, 0)[0]
            mvs_dict[mvw.DimensionLabel(0,i,0)] = mvw.GetNumericWavePointValue(i)
    
        return mvs_dict

    def Go_There (self, xy_coordinates = np.array([0, 0]), transit_time = 0.3):
        """
        Move Tip to a Specific Locations

        Args:
            xy_coordinates (arr): coordinates of target location, e.g., xy_coordinates = np.array([0.3, 0]).
        """
        # Enable Go There and Show Tip Location
        self.igor.Execute('ARExecuteControl("GoForce_1","MasterPanel",1,"")')
        self.igor.Execute('ARExecuteControl("ShowXYSpotCheck_1", "MasterPanel", 1, "")')

        # Get MasterVariables
        mvs = self.Get_MasterVariables()

        # Convert xy_coordinates to internal values
        XLoc = (mvs["ScanSize"]*xy_coordinates[0])/(2*mvs["FastRatio"]) 
        YLoc = (mvs["ScanSize"]*xy_coordinates[1])/(2*mvs["SlowRatio"]) 

        scan_theta = - mvs["ScanAngle"]*np.pi/180

        RLoc1 = np.array([XLoc, YLoc])
        RLoc2 = np.array([[np.cos(scan_theta), np.sin(scan_theta)], [-np.sin(scan_theta), np.cos(scan_theta)]])
        XLocR, YLocR = np.dot(RLoc1, RLoc2)

        XLocV = ((XLocR + mvs["XOffset"])/mvs["XLVDTSens"])+mvs["XLVDTOffset"] 
        YLocV = ((YLocR + mvs["YOffset"])/mvs["YLVDTSens"])+mvs["YLVDTOffset"]

        # command = (f'td_SetRamp({transit_time:.6f},"$outputXloop.Setpoint",0,{XLocVMat:.6f},"$outputYloop.Setpoint",0,{YLocVMat:.6f},"",0,0,"")')
        self.igor.Execute(f'td_SetRamp({transit_time:.6f},"$outputXloop.Setpoint",0,{XLocV:.6f},"$outputYloop.Setpoint",0,{YLocV:.6f},"",0,0,"")')
    
        time.sleep(transit_time)
        return XLocV, YLocV