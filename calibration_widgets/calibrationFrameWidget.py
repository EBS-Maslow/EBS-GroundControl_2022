'''

This is the widget which creates a frame around the calibration process providing infrastructure like the forwards and back buttons

Each widget which it loads should be largely self contained and either gather a piece of information from the user or set the machine into a known
state regardless of the machine's state when the widget begins.

'''
from kivy.uix.gridlayout                                     import  GridLayout
from kivy.properties                                         import  ObjectProperty
from calibration_widgets.intro                               import  Intro
from calibration_widgets.chooseKinematicsType                import  ChooseKinematicsType
from calibration_widgets.chooseChainOverSprocketDirection    import  ChooseChainOverSprocketDirection
from calibration_widgets.computeCalibrationSteps             import  ComputeCalibrationSteps
from calibration_widgets.setSprocketsVertical                import  SetSprocketsVertical
from calibration_widgets.measureDistBetweenMotors            import  MeasureDistBetweenMotors
from calibration_widgets.vertDistToMotorsGuess               import  VertDistToMotorsGuess
from calibration_widgets.measureOutChains                    import  MeasureOutChains
from calibration_widgets.removeChains                        import  RemoveChains
from calibration_widgets.adjustZCalibrationDepth             import  AdjustZCalibrationDepth
from calibration_widgets.rotationRadiusGuess                 import  RotationRadiusGuess
from calibration_widgets.triangularCalibration               import  TriangularCalibration
from calibration_widgets.distBetweenChainBrackets            import  DistBetweenChainBrackets
from calibration_widgets.reviewMeasurements                  import  ReviewMeasurements
from calibration_widgets.quadTestCut                         import  QuadTestCut
from calibration_widgets.finish                              import  Finish
from calibration_widgets.finishSetChainLengths               import  FinishSetChainLengths
from calibration_widgets.manualCalibration                   import  ManualCalibration
from calibration_widgets.enterDistanceBetweenMotors          import  EnterDistanceBetweenMotors
from calibration_widgets.measureOneChain                     import  MeasureOneChain
from calibration_widgets.computeChainCorrectionFactors       import  ComputeChainCorrectionFactors
from calibration_widgets.wipeOldCorrectionValues             import  WipeOldCorrectionValues
from   kivy.app                                             import  App


class CalibrationFrameWidget(GridLayout):
    done   = ObjectProperty(None)
    listOfCalibrationSteps = []
    currentStepNumber = 0
    
    def on_Enter(self):
        '''
        
        Called the first time the widget is created
        
        '''
        
        App.get_running_app().data.calibrationInProcess = True
        
        
        self.loadStep(0)
    
    def on_Exit(self):
        '''
        
        This function run when the process is completed or quit is pressed
        
        '''
        App.get_running_app().data.calibrationInProcess = False
        App.get_running_app().data.message_queue.put("Message: Notice: Exiting the calibration process early may result in incorrect calibration.")
        
        #remove the old widget
        try:
            self.cFrameWidgetSpace.remove_widget(self.currentWidget)
        except:
            pass #there was no widget to remove
        
        self.done()
    
    def setupFullCalibration(self):
        
        #ensure that there are no widgets in the deck when we start
        self.listOfCalibrationSteps = []
        
        #load the first steps in the calibration process because they are always the same
        #intro =  Intro()
        #self.listOfCalibrationSteps.append(intro)
      
        setTo12 = SetSprocketsVertical()
        self.listOfCalibrationSteps.append(setTo12)
        
        enterDistanceBetweenMotors = EnterDistanceBetweenMotors()
        self.listOfCalibrationSteps.append(enterDistanceBetweenMotors)
    
        #add extend chains
        measureOutChains = MeasureOutChains()
        self.listOfCalibrationSteps.append(measureOutChains)
            
        #add set z
        adjustZCalibrationDepth = AdjustZCalibrationDepth()
        self.listOfCalibrationSteps.append(adjustZCalibrationDepth)
            
        #add triangular kinematics
        triangularCalibration = TriangularCalibration()
        self.listOfCalibrationSteps.append(triangularCalibration)

        reviewMeasurements = ReviewMeasurements()
        self.listOfCalibrationSteps.append(reviewMeasurements)
        
        computeCalibrationSteps = ComputeCalibrationSteps()
        finish              = Finish()
        finish.done         = self.done
        self.listOfCalibrationSteps.append(finish)
        self.listOfCalibrationSteps.append(computeCalibrationSteps)
        
    
    def setupJustChainsCalibration(self):
        '''
        
        Calling this function sets up the calibration process to show just the steps to calibrate the chain lengths
        
        '''
        
        #ensure that there are no widgets in the deck when we start
        self.listOfCalibrationSteps = []
        
        #load steps
        setSprocketsVertical =  SetSprocketsVertical()
        self.listOfCalibrationSteps.append(setSprocketsVertical)
        
        measureOutChains =  MeasureOutChains()
        self.listOfCalibrationSteps.append(measureOutChains)
        
        finishSetChainLengths =  FinishSetChainLengths()
        finishSetChainLengths.done         = self.done
        self.listOfCalibrationSteps.append(finishSetChainLengths)
    
    def setupJustTriangularTestCuts(self):
        '''
         
        Calling this function sets up the calibration process to show just the steps cut the triangular test pattern
        
        '''
        
        #ensure that there are no widgets in the deck when we start
        self.listOfCalibrationSteps = []
        
        #add triangular kinematics
        triangularCalibration                       = TriangularCalibration()
        self.listOfCalibrationSteps.append(triangularCalibration)
        
        #one last review
        reviewMeasurements                          = ReviewMeasurements()
        self.listOfCalibrationSteps.append(reviewMeasurements)
        
        #add finish step
        finish              = Finish()
        finish.done         = self.done
        self.listOfCalibrationSteps.append(finish)
    
    def setupManualCalibration(self):
        '''
        
        Calling this function sets up the calibration process to show an option to enter manual machine dimensions
        
        '''
        
        #ensure that there are no widgets in the deck when we start
        self.listOfCalibrationSteps = []
        
        #add manual calibation card
        manualCalibration                       = ManualCalibration()
        self.listOfCalibrationSteps.append(manualCalibration)
        
        #one last review
        reviewMeasurements                          = ReviewMeasurements()
        self.listOfCalibrationSteps.append(reviewMeasurements)
        
        #add finish step
        finish              = Finish()
        finish.done         = self.done
        self.listOfCalibrationSteps.append(finish)
    
    def setupMeasureChainTolerances(self):
        '''
        
        Calling this function sets up the process with the cards to measure the chain tolerances
        
        '''
        
        #ensure that there are no widgets in the deck when we start
        self.listOfCalibrationSteps = []
        
        #enter manual measurement of distance between motors
        enterDistanceBetweenMotors                       = EnterDistanceBetweenMotors()
        self.listOfCalibrationSteps.append(enterDistanceBetweenMotors)
        
        #enter manual measurement of distance between motors
        wipeOldCorrectionValues                       = WipeOldCorrectionValues()
        self.listOfCalibrationSteps.append(wipeOldCorrectionValues)
        
        #set to 12
        setTo12                                          = SetSprocketsVertical()
        self.listOfCalibrationSteps.append(setTo12)
        
        #extend left chain and pull tight to measure
        measureOneChain                                  = MeasureOneChain()
        measureOneChain.setDirection('L')
        self.listOfCalibrationSteps.append(measureOneChain)
        
        #set to 12
        setTo12                                          = SetSprocketsVertical()
        self.listOfCalibrationSteps.append(setTo12)
        
        #extend right chain and pull tight to measure
        measureOneChain                                  = MeasureOneChain()
        measureOneChain.setDirection('R')
        self.listOfCalibrationSteps.append(measureOneChain)
        
        #compute values
        computeChainCorrectionFactors                    = ComputeChainCorrectionFactors()
        self.listOfCalibrationSteps.append(computeChainCorrectionFactors)
        
        #finish
        finish              = Finish()
        finish.done         = self.done
        self.listOfCalibrationSteps.append(finish)
    
    
    
    def loadNextStep(self):
        '''
        Called to trigger a loading of the next slide
        '''
        
        self.currentStepNumber = self.currentStepNumber + 1
        self.loadStep(self.currentStepNumber)
    
    def back(self):
        '''
        Re-load the previous step
        
        '''
        if  self.currentStepNumber == 0:
            self.currentStepNumber = self.currentStepNumber
            self.loadStep(self.currentStepNumber)
        else:    
            self.currentStepNumber = self.currentStepNumber - 1
            self.loadStep(self.currentStepNumber)
        
    def loadStep(self, stepNumber):
        
        #remove the old widget
        try:
            self.currentWidget.on_Exit()
            self.cFrameWidgetSpace.remove_widget(self.currentWidget)
        except:
            pass #there was no widget to remove
        
        try:
            #load the new widget
            self.currentWidget = self.listOfCalibrationSteps[self.currentStepNumber]
            
            #initialize the new widget
            self.currentWidget.readyToMoveOn = self.loadNextStep
            self.currentWidget.on_Enter()
            self.cFrameWidgetSpace.add_widget(self.currentWidget)
        except IndexError:
            #the calibration has run out of steps
            pass