'''

This step lets you review your measurements before moving on.

'''
from   kivy.uix.gridlayout                          import   GridLayout
from   kivy.properties                              import   ObjectProperty
from   kivy.app                                     import   App

class ReviewMeasurements(GridLayout):
    readyToMoveOn   = ObjectProperty(None)
    
    
    def on_Enter(self):
        '''
        
        This function runs when the step is entered
        
        '''
        
        self.data = App.get_running_app().data
        
        tempString = "[b][color=0d72e6] LETS REVIEW THE MEASUREMENTS TO MAKE SURE EVERYTHING LOOKS GOOD. [/color][/b]\n [color=000000]You can use the back button to repeat any step.\n\n[/color] "
        tempString = tempString + "\n   [color=000000]Distance between motors: [/color][b][color=f89405]" + self.data.config.get('Maslow Settings', 'motorSpacingX') + "mm[/color][/b]"
        tempString = tempString + "\n   [color=000000]Vertical motor offset: [/color][b][color=f89405]" + self.data.config.get('Maslow Settings', 'motorOffsetY') + "mm[/color][/b]"
        tempString = tempString + "\n   [color=000000]Kinematics type: [/color][b][color=f89405]" + self.data.config.get('Advanced Settings', 'kinematicsType') + "[/color][/b]"
        tempString = tempString + "\n   [color=000000]Chain feed type: [/color][b][color=f89405]" + self.data.config.get('Advanced Settings', 'chainOverSprocket') + "[/color][/b]"
        if self.data.config.get('Advanced Settings', 'kinematicsType') == 'Triangular':
            tempString = tempString + "\n   [color=000000]Rotation radius: [/color][b][color=f89405]" + self.data.config.get('Advanced Settings', 'rotationRadius') + "mm[/color][/b]"
            tempString = tempString + "\n   [color=000000]Chain sag correction value: [/color][b][color=f89405]" + self.data.config.get('Advanced Settings', 'chainSagCorrection') + "[/color][/b]"
        else:
            tempString = tempString + "\n   Sled mount spacing: [b][color=f89405]" + self.data.config.get('Maslow Settings', 'sledWidth') + "mm[/color][/b]"
        
        self.measurementsReadout.text = tempString
    
    def loadNextStep(self):
        self.readyToMoveOn()
    
    def on_Exit(self):
        '''
        
        This function run when the step is completed
        
        '''
        pass