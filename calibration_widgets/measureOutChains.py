from kivy.uix.gridlayout                import   GridLayout
from kivy.properties                    import   ObjectProperty
from kivy.properties                    import   StringProperty
from kivy.clock                         import   Clock
from kivy.app                           import   App

class MeasureOutChains(GridLayout):
    '''
    
    Provides a standard interface for measuring out a known length of both chains
    
    '''
    data              =  ObjectProperty(None) #set externally
    text              =  StringProperty("")
    countDownTime     =  0
    
    def on_Enter(self):
        '''
        
        This function runs when the step is entered
        
        '''
        self.data = App.get_running_app().data
        self.text =  "[b][color=0d72e6]WE ARE GOING TO ADJUST THE CHAINS TO A KNOWN LENGHT[/color][/b]\n\n[color=000000]1 - Place the first link from the left chain over the top tooth on the left sprocket and click [Adjust Left Chain]\n     [b][color=f89405]Be sure to keep an eye on the chains during this process to ensure that they do not become tangled around the sprocket.[/color][/b]\n2 - Do the same for the right chain and click [Adjust Right Chain]\n3 - Once both chains are finished, attach the chains to the sled using the cotter pins\n4 - Complete the top assembly, then click on [Move to Center] and [Next]"
        
        #select the right image for a given setup
        print ("measure out chains on enter")
        if App.get_running_app().data.config.get('Advanced Settings', 'chainOverSprocket') == 'Top':
            print ("top feeding detected")
            self.leftImg.source = "./images/cal_3.png"
        else :
            print ("bottom feeding detected")
            self.leftImg.source = "./images/cal_3.png"
    
    def stop(self):
        self.data.quick_queue.put("!") 
        with self.data.gcode_queue.mutex:
            self.data.gcode_queue.queue.clear()
    
    def moveToCenter(self):
        '''
        
        Adjusts the chains to the lengths to put the sled in the center of the sheet
        
        '''
        self.data.gcode_queue.put("B15 ")
    
    def next(self):
        
        self.readyToMoveOn()
    
    '''
    Left Chain
    '''
    def startCountDownL(self):
        self.countDownTime  = 5
        
        Clock.schedule_once(self.countingDownL, 1)
        self.leftChainBtn.text = '   Extend\nLeft Chain (' + str(self.countDownTime) + ")"
    
    def countingDownL(self, *args):
        self.countDownTime = self.countDownTime - 1
        
        self.leftChainBtn.text = '   Extend\nLeft Chain (' + str(self.countDownTime) + ")"
        
        if self.countDownTime > 0:
            Clock.schedule_once(self.countingDownL, 1)
        else:
            self.leftChainBtn.text = '   Extend\nLeft Chain'
            self.data.gcode_queue.put("B02 L1 R0 ")
    
    '''
    Right Chain
    '''
    
    def startCountDownR(self):
        self.countDownTime  = 5
        
        Clock.schedule_once(self.countingDownR, 1)
        self.rightChainBtn.text = '   Extend\nRight Chain (' + str(self.countDownTime) + ")"
    
    def countingDownR(self, *args):
        self.countDownTime = self.countDownTime - 1
        
        self.rightChainBtn.text = '   Extend\nRight Chain (' + str(self.countDownTime) + ")"
        
        if self.countDownTime > 0:
            Clock.schedule_once(self.countingDownR, 1)
        else:
            self.rightChainBtn.text = '   Extend\nRight Chain'
            self.data.gcode_queue.put("B02 L0 R1 ")
    
    def on_Exit(self):
        '''
        
        This function runs when the step is completed
        
        '''
        
        pass