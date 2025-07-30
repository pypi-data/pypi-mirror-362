## NanosurfPy

# import nanosurf library. Use pip install nanosurf if you have not done before
import nanosurf
import time
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

class NanoSurf():
    def __init__(self,) -> None:
        """
        Connect or open NanoSurf CX application, and load routine applications
        """ 
        # Open or connect to nanosurf CX application:
        self.spm = nanosurf.SPM()
        # Make a shortcut to the application object:
        self.application = self.spm.application
        # Load the approach application:
        self.approach = self.application.Approach
        # Load stage application:
        self.stage = self.application.Stage
        # Load system application:
        self.system = self.application.System
        # Load scan:
        self.scan = self.application.Scan
        # Load spectroscopy application:
        self.spec = self.application.Spec
        # Load zcontroller
        self.zctrl = self.application.ZController
        # Load Operating Mode
        self.opmode = self.application.OperatingMode

    # Define a function to set stage speed
def set_stage_speed (self, stage_speed_percent):
    '''This function sets a speed for stage movement in percent between 0 and 100,
    e.g., stage_speed_percent = 30
    '''
    if stage_speed_percent>=0 and stage_speed_percent<=100:
        self.stage.SetSpeedPercent(stage_speed_percent)
        print("Stage speed is set to "+str(self.stage.GetSpeedPercent)+"%")
    else: 
        print("Set a stage speed value between 0% and 100%")
        
    return

# Withdraw and retract tip
def withdraw_retract_tip (self, withdraw_step, retract_time):
    '''
    This function first moves the tip away from the sample surface slowly with a small distance, 
    then quickly retract with a large distance. 
    withdraw_step and retract_time determine the tip lift distance at respective steps.
    '''
    #######################################################################################
    ########   First, using the StartWithdraw function to carefully move the tip --########
    ########   away from the surface with a small amount distance -----------------########
    #######################################################################################
    self.approach.WithdrawSteps = withdraw_step  # set withdraw step
    self.approach.StartWithdraw()                # start withdraw
    print ("Withdrawing...")                # wait until withdraw finish
    while self.approach.IsMoving == True:
        time.sleep(0.1)
    time.sleep(0.1)
    
    #######################################################################################
    ########   Then, using StartRetract function to move away from surface  with --########
    ########   a large distance  --------------------------------------------------########
    #######################################################################################
    self.approach.StartRetract()  # this will not stop unless you call stop
    print ("Retracting...")
    time.sleep(retract_time) # this sleep time determines how far you retract
    self.approach.Stop()          # stop retract movement
    time.sleep(0.1)
    
    return

def move_stage_nonretract (self, x_dist, y_dist, stage_speed_percent):
    '''
    This function moves motorized stage along x and y directions. Note that here we did not retract tip before moving stage,
    so largely this operation will cause cantilever damage or sample damage.
    Note this function does not unlock or lock stage
    '''
    # The stage must be refrenced for most movement actions to work properly
    if self.stage.IsReferenced == True:
        print ("Stage is referenced")
    else:
        raise RuntimeError("Stage is Not referenced")
        
    # Set stage movement speed
    set_stage_speed(stage_speed_percent = stage_speed_percent)
    
    self.stage.ClearMoveTransaction()   # clear previous move transaction
    
    # Move along x axis
    self.stage.AppendToMoveTransaction(0, x_dist, True)  # add x movement to transaction
    self.stage.CommitMoveTransaction()                   # commits all appended move commands
    print ("Moving along X direction...")   
    while self.stage.GetState == 3:  # wait when stage is moving
        time.sleep(0.1)
    time.sleep(0.2)
    # Clear trasaction after movement is done
    self.stage.ClearMoveTransaction()   # clear the move transaction of all entries    
    
    # Move along y axis  
    self.stage.AppendToMoveTransaction(1, y_dist, True)  # add y movement to transaction
    self.stage.CommitMoveTransaction()
    print ("Moving along y direction...")
        
    while self.stage.GetState == 3:  # wait when stage is moving
        time.sleep(0.1)
    time.sleep(0.2)
    # Clear trasaction after movement is done
    self.stage.ClearMoveTransaction()   # clear the move transaction of all entries
    
    # Get current stage posision
    posx=self.stage.GetAxisPosition(0)
    posy=self.stage.GetAxisPosition(1)
    print("Movement is done.\nCurrent stage position is: [" +str(posx*1E6)+" um, "+str(posy*1E6)+" um]")
    
    return posx, posy

def approach_tip (self,):
    '''
    This function approaches tip to sample surface, there are something worth adding into this function 
    such as approach speed, approach step, approach pos
    '''
    self.approach.StartApproach()
    print ("Tip approaching...")
    while self.approach.IsMoving == True:
        time.sleep(0.1)
    time.sleep(0.1)
    if self.approach.Status == 3:
        print ("Automatic approach successful finished")
        return
    else:
        print ("Approach status is " + str(self.approach.Status))
        raise RuntimeError("Approach is not correct")
        return
    
# function for move stage
def move_stage_retract (self, x_dist, y_dist, stage_speed_percent=30, withdraw_step=300, retract_time=1):
    '''
    This function moves motorized stage along x and y directions. 
    Executing this function will performing the following actions: unlock stage, withdraw tip slowly,
    retract tip quickly, move stage, approach tip, lock stage.
    '''
    
    # Set stage movement speed
    self.set_stage_speed(stage_speed_percent = stage_speed_percent)

    # Unlock stage to move:
    self.stage.Unlock()
    print("Stage is unlocked")
    time.sleep(0.2)
        
    ##########################################################################################
    ########  The tip should be retracted to a safe position before moving the stage  ########
    ########  in order to avoid destroying the cantilever or sample ------------------########
    ##########################################################################################
    self.withdraw_retract_tip (withdraw_step=300, retract_time=1)
    
    ##########################################################################################
    ######################################  Move Stage  ######################################
    ##########################################################################################
    posx, posy = self.move_stage_nonretract (x_dist, y_dist, stage_speed_percent)
    
    ##########################################################################################
    ####################################  Approach tip  ######################################
    ##########################################################################################
    self.approach_tip()
    
    # Lock stage for measurements:
    self.stage.Lock()
    time.sleep(0.2)
    print("Stage is locked")
    
    return posx, posy  # return current stage position

def move_piezo_pos (self, piezo_pos_x, piezo_pos_y):
    '''
    This function moves tip via piezo-controller.
    '''
    #clear (piezo_x, piezo_y) position list first
    self.spec.ClearPositionList()   
    self.system.SystemStateIdleZAxisMode=1  # State 1 is to retract tip
    time.sleep(0.1)
    self.spec.AddPosition(piezo_pos_x, piezo_pos_y, 0)
    while self.spec.IsMoving == True:
        time.sleep(0.1)
    time.sleep(0.5)
    # Approach tip after movement
    self.approach_tip ()
    
    time.sleep(0.1)
    self.system.SystemStateIdleZAxisMode=0  # State 0 is engage tip
    time.sleep(0.1)
    
    current_pos = self.spec.Currentline   # current spec measurement position number
     
    return current_pos

def set_image_scan (self, scan_dict = None, startscan = False):
    '''
    This function define scan parameters including ImageWidth, ImageHeight, Points, Lines, Scantime, CenterPosX, CenterPoxY
    '''
    # default parameters
    default_image_parameters = np.asarray([10, 10, 256, 256, 0.7, 0, 0, 0])  # set default values

    # Set default values for image parameters
    image_parms_list = [default_image_parameters[0], default_image_parameters[1], default_image_parameters[2], default_image_parameters[3]]
        
    image_parms_name_list = ["ImageWidth", "ImageHeight", "Points", "Lines", "Scantime", "Rotation", "CenterPosX", "CenterPosY"]
    # if user customized some parameters, set the parameters as customized values
    if scan_dict != None:
        for i in range (len (image_parms_name_list)):
            if image_parms_name_list[i] in scan_dict:
                image_parms_list[i] = scan_dict[image_parms_name_list[i]]
    # Change the Scan settings
    self.scan.ImageWidth = (image_parms_list[0]) * 1e-6 # Set width of scan to 10 um
    self.scan.ImageHeight = (image_parms_list[1]) * 1e-6 # Set height of scan to 10 um
    self.scan.Points = (image_parms_list[2]) # Set points per line
    self.scan.Lines = (image_parms_list[3]) # Set lines per frame
    self.scan.Scantime = (image_parms_list[4])  # scan time per line
    self.scan.CenterPosX = (image_parms_list[2]) * 1e-6 # X offset = 0 um
    self.scan.CenterPosY = (image_parms_list[3]) * 1e-6 # Y offset = 0 um
    self.scan.AutoCapture = True # Turn on end-of-frame data capture  
     
    return

def start_image_scan(self, scanmode = 0):
    '''
    This function sets scan mode and start scan, scan mode includes Start, StartFrameUp, StartFrameDown
    '''
    if scanmode == 0:
        print ("Start continuous scan...")
        self.scan.Start()
    elif scanmode == 1:
        print ("Start Frame Up...")
        self.scan.StartFrameUp()
    elif scanmode == 2:
        print ("Start Frame Down...")
        self.scan.StartFrameDown()
    while self.scan.IsScanning:
        curline = self.scan.Currentline
        print("Scanning..., current line is {}".format(curline))
        time.sleep(2)
    return

def tip_voltage(self, tipvoltage = 0):
    '''
    This function sets tip voltage
    '''
    self.zctrl.TipVoltage = tipvoltage
    print("Tip Voltage is {}".format(tipvoltage))

    return

