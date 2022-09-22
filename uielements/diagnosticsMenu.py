from kivy.uix.floatlayout                           import    FloatLayout
from datastructures.makesmithInitFuncs              import    MakesmithInitFuncs
from uielements.scrollableTextPopup                 import    ScrollableTextPopup
from kivy.uix.popup                                 import    Popup
from calibration_widgets.calibrationFrameWidget     import    CalibrationFrameWidget
from simulation.simulationCanvas                    import    simulationCanvas
from kivy.clock                                     import    Clock
from kivy.app                                       import    App
import sys
import os
import time

class Diagnostics(FloatLayout, MakesmithInitFuncs):
    
    def about(self):
        popupText = 'Ground Control 2022 allows you to control the Maslow machine. ' + \
                    'From within Ground Control, you can move the machine to where you want to begin a cut, calibrate the machine, ' + \
                    'open and run a g-code file, or monitor the progress of an ongoing cut. For more details about the current version see our website ' + \
                    'at https://www.eastbaysource.com/. The source code can be downloaded at https://github.com/EBS-Maslow/GroundControl. ' + \
                    '\n\n' + \
                    'GroundControl is part of the of the Maslow cnc Control Software initially made by Bar Smith and later modified/updated by EastBaySource. ' + \
                    'This program is free software: you can redistribute it and/or modify ' + \
                    'it under the terms of the GNU General Public License as published by ' + \
                    'the Free Software Foundation, either version 3 of the License, or ' + \
                    '(at your option) any later version. ' + \
                    '\n\n' + \
                    'This program is distributed in the hope that it will be useful, ' + \
                    'but WITHOUT ANY WARRANTY; without even the implied warranty of ' + \
                    'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the ' + \
                    'GNU General Public License for more details. ' + \
                    '\n\n' + \
                    'You should have received a copy of the GNU General Public License ' + \
                    'along with the Maslow Control Software. If not, see <http://www.gnu.org/licenses/>.'

        content = ScrollableTextPopup(text=popupText)
        if sys.platform.startswith('darwin'):
            self._popup = Popup(title='About GroundControl', content=content, size=(520,480), background_color=(0,0,0,.9), size_hint=(.6, .6), background='[color=cccccc]')
        else:
            self._popup = Popup(title='About GroundControl', content=content, size=(520,480), background_color=(0,0,0,.9), size_hint=(None, None), background='[color=cccccc]')
        self._popup.open()
    
    def dismiss_popup(self):
        '''
        
        Close The Pop-up
        
        '''
        self._popup.dismiss()
        
    def calibrateChainLengths(self):
        '''
        
        This function is called when the "Calibrate Chain Lengths Automatic" button is pressed under the Actions window
        
        '''
        
        self.popupContent       = CalibrationFrameWidget(done=self.dismissCalibrationPopup)
        self.popupContent.setupJustChainsCalibration()
        self.popupContent.on_Enter()
        
        self._popup = Popup(title="Calibrate Chain Lengths",
                            title_color=(0,0,0,1),
                            background_color=(0,0,0,.7),
                            background='[color=cccccc]',
                            content=self.popupContent,
                            size_hint=(0.85, 0.95),
                            auto_dismiss = False
                            )
        self._popup.open()
    
    def runJustTriangularCuts(self):
        '''
        
        This function is called when the "Run Triangular Test Cuts" button under advanced options is pressed
        
        '''
        
        self.popupContent       = CalibrationFrameWidget(done=self.dismissCalibrationPopup)
        self.popupContent.setupJustTriangularTestCuts()
        self.popupContent.on_Enter()
        
        self._popup = Popup(title="Calibrate Chain Lengths",
                            title_color=(0,0,0,1),
                            background_color=(0,0,0,.7),
                            background='[color=cccccc]',
                            content=self.popupContent,
                            size_hint=(0.85, 0.95),
                            auto_dismiss = False
                             )
        self._popup.open()
    
    def manualCalibration(self):
        '''
        
        This function is called when the "Run Triangular Test Cuts" button under advanced options is pressed
        
        '''
        
        self.popupContent = CalibrationFrameWidget(done=self.dismissCalibrationPopup)
        self.popupContent.setupManualCalibration()
        self.popupContent.on_Enter()
        
        self._popup = Popup(title="Lengths",
                            title_color=(0,0,0,1),
                            background_color=(0,0,0,.7),
                            background='[color=cccccc]',
                            content=self.popupContent,
                            size_hint=(0.85, 0.95),
                            auto_dismiss = False
                            )
        self._popup.open()
    
    def manualCalibrateChainLengths(self):
        self.data.gcode_queue.put("B08 ")
        self.parentWidget.close()
    
    def testMotors(self):
        self.data.gcode_queue.put("B04 ")
        self.parentWidget.close()
    
    def wipeEEPROM(self):
        self.data.gcode_queue.put("$RST=* ")
        Clock.schedule_once(self.data.pushSettings, 6)
        self.parentWidget.close()
    
    def calibrateMachine(self):
        '''
        
        Spawns a walk through that helps the user measure the machine's dimensions
        
        '''
        self.popupContent       = CalibrationFrameWidget(done=self.dismissCalibrationPopup)
        self.popupContent.setupFullCalibration()
        self.popupContent.on_Enter()
        self._popup = Popup(title="Calibration",
                            content=self.popupContent,
                            size_hint=(0.85, 0.95),
                            background_color=(0, 0, 0, 0.1),
                            background='[color=cccccc]',
                            auto_dismiss = False
                            )
        self._popup.open()
    
    def dismissCalibrationPopup(self):
        '''
        
        Close The calibration Pop-up
        
        '''
        self.data.calibrationInProcess = False
        self._popup.dismiss()
    
    def launchsimulation(self):
        print ("launch simulation")
        self.popupContent      = simulationCanvas()
        self.popupContent.data = self.data
        self.popupContent.initialize()
        self._popup = Popup(title="Maslow Calibration simulation",
                            title_color=(0,0,0,1),
                            content=self.popupContent,
                            size_hint=(0.85, 0.95),
                            background_color=(0,0,0,.7),
                            background='[color=cccccc]',
                            auto_dismiss = True
                            )
        self._popup.open()
        self.parentWidget.close()
    
    def loadCalibrationBenchmarkTest(self):
        '''
        
        Loads the Calibration Benchmark Test file
        
        '''
        self.data.gcodeFile = "./gcodefortesting/Calibration Benchmark Test.nc"
        self.parentWidget.close()
    
    def resetAllSettings(self):
        '''
        
        Renames the groundcontrol.ini file which resets all the settings to the default values
        
        '''
        
        currentSettingsFile = App.get_running_app().get_application_config()
        newSettingsFile = currentSettingsFile.replace("groundcontrol","groundcontrolbackup" + time.strftime("%Y%m%d-%H%M%S"))
        
        os.rename(currentSettingsFile, newSettingsFile)
        
        #close ground control
        app = App.get_running_app()
        app.stop()
        
    def measureChainTolerances(self):
        '''
        
        Chains can stretch over time and with use. This process computes the true length of your chains.
        
        '''
        
        self.popupContent = CalibrationFrameWidget(done=self.dismissCalibrationPopup)
        self.popupContent.setupMeasureChainTolerances()
        self.popupContent.on_Enter()
        
        self._popup = Popup(title="Measure Chain Tolerances",
                            title_color=(0,0,0,1),
                            background_color=(0,0,0,.8),
                            background='[color=cccccc]',
                            content=self.popupContent,
                            size_hint=(0.85, 0.95),
                            auto_dismiss = False
                            )
        self._popup.open()
    
    def advancedOptionsFunctions(self, text):
        
        if  text == "Set Chain Length - Manual":
            self.manualCalibrateChainLengths()
        elif text == "Wipe EEPROM":
            self.wipeEEPROM()
        elif text == "Simulation":
            self.launchsimulation()
        elif text == "Load Calibration Benchmark Test":
            self.loadCalibrationBenchmarkTest()
        elif text == "Run Triangular Test Cut Pattern":
            self.runJustTriangularCuts()
        elif text == "Factory Reset":
            self.wipeEEPROM()
            self.resetAllSettings()
        #elif text == "Compute chain calibration factors":
            #self.measureChainTolerances()
        elif text == "Manual Calibration":
            self.manualCalibration()
