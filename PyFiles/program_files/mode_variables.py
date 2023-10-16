import numpy as np

''' Global Variables for use '''
lst_parameters = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate', 'Fixed AV Delay', 'Dynamic AV Delay', 'Sensed AV Delay Offset',
                  'Atrial Amplitude', 'Ventricular Amplitude', 'Atrial Pulse Width', 'Ventricular Pulse Width', 'Atrial Sensitivity', 'Ventricular Sensitivity',
                  'VRP', 'ARP', 'PVARP', 'PVARP Extension', 'Hysteresis', 'Rate Smoothing', 'ATR Duration', 'ATR Fallback Mode', 'ATR Fallback Time',
                  'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time']

dict_param_nom_vals = {'Lower Rate Limit' : 60, 'Upper Rate Limit' : 120, 'Maximum Sensor Rate' : 120, 'Fixed AV Delay' : 150, 'Dynamic AV Delay' : 'Off', 'Sensed AV Delay Offset' : 'Off',
                  'Atrial Amplitude' : 3.5, 'Ventricular Amplitude' : 3.5, 'Atrial Pulse Width' : 0.4, 'Ventricular Pulse Width' : 0.4, 'Atrial Sensitivity' : 0.75, 'Ventricular Sensitivity' : 2.5,
                  'VRP' : 320, 'ARP' : 250, 'PVARP' : 250, 'PVARP Extension' : 'Off', 'Hysteresis' : 'Off', 'Rate Smoothing' : 'Off', 'ATR Duration' : 20, 'ATR Fallback Mode' : 'Off', 'ATR Fallback Time' : 1,
                  'Activity Threshold' : 'Med', 'Reaction Time' : 30, 'Response Factor' : 8, 'Recovery Time' : 5}

# dicitonary of parameters and their values and units
dict_param_and_range = {
  'Lower Rate Limit' : [[i for i in range(30, 50, 5)] + [i for i in range(50, 91, 1)] + [i for i in range(95, 180, 5)], "ppm"], # [30,35,40,45,50,51,51,...]
  'Upper Rate Limit' : [[i for i in range(50, 180, 5)], "ppm"], # [50,55,60,65,...]
  'Atrial Amplitude' : [["Off"] + [round(i,1) for i in np.arange(0.5,3.3,0.1)] + [round(i,1) for i in np.arange(3.5,7.5,0.5)], "V"], # ["Off", 0.5,0.6,0.7,0.8,...]
  'Ventricular Amplitude' : [["Off"] + [round(i,1) for i in np.arange(0.5,3.3,0.1)] + [round(i,1) for i in np.arange(3.5,7.5,0.5)], "V"], # ["Off", 0.5,0.6,0.7,0.8,...]
  'Atrial Pulse Width' : [[0.05] + [round(i,1) for i in np.arange(0.1, 2.0, 0.1)], "ms"], # [[0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
  'Ventricular Pulse Width' : [[0.05] + [round(i,1) for i in np.arange(0.1, 2.0, 0.1)], "ms"],
  'VRP' : [[i for i in range(150, 510, 10)], "ms"], # [[150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 
  'ARP' : [[i for i in range(150, 510, 10)], "ms"] # [[150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 
}

dict_modes = {'AOO' : [0, 1, 6, 8], 'VOO' : [0, 1, 7, 9], 'AAI' : [0, 1, 6, 8, 13], 'VVI' : [0, 1, 7, 9, 12]} # all current modes implemented modes and their paramaters

dict_modes_enumeration = {'AOO' : 1, 'VOO' : 2, 'AAI' : 3, 'VVI' : 4}

dict_param_and_tolerance = {
  'Lower Rate Limit' : [8, "ms"],
  'Upper Rate Limit' : [8, "ms"], 
  'Atrial Amplitude' : [12, "%"], 
  'Ventricular Amplitude' : [12, "%"], 
  'Atrial Pulse Width' : [0.2, "ms"], 
  'Ventricular Pulse Width' : [0.2, "ms"],
  'VRP' : [8, "ms"], 
  'ARP' : [8, "ms"]
}