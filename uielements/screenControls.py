from kivy.uix.floatlayout                      import   FloatLayout
from kivy.uix.popup                            import   Popup
from uielements.otherFeatures                  import   OtherFeatures
from datastructures.makesmithInitFuncs         import   MakesmithInitFuncs
from uielements.buttonTemplate                 import   ButtonTemplate
from uielements.buttonControls               import   ButtonControls
from kivy.app                                  import   App
from uielements.backgroundMenu                 import   BackgroundMenu


class ScreenControls(FloatLayout, MakesmithInitFuncs):
    
    
    def setButtonAppearance(self):
        '''
        
        Called on creation to set up links to button background textures
        
        '''
        self.actionsBtn.btnBackground = self.data.iconPath + 'greena.png'
        self.actionsBtn.btnBackgroundDown = self.data.iconPath + 'greendwn.png'
        self.actionsBtn.textColor = self.data.fontColor
        self.settingsBtn.btnBackground = self.data.iconPath + 'yellowa.png'
        self.settingsBtn.btnBackgroundDown = self.data.iconPath + 'yellowdwn.png'
        
        self.settingsBtn.textColor = self.data.fontColor
    
    def openSettings(self):
        '''
        
        Open the settings panel to manually change settings
        
        '''
        
        #force the settings panel to update
        App.get_running_app().destroy_settings()
        
        #open the settings panel
        App.get_running_app().open_settings()
    
    def show_actions(self):
        '''
        
        Open A Pop-up To Allow User Actions
        
        Creates a new pop-up allows the user to do things like open a file.
        
        '''
        content = OtherFeatures()
        content.setUpData(self.data)
        content.close = self.close_actions
        self._popup = Popup(title="Actions",
                            content=content,        
                            title_color=(0, 0, 0, 1),
                            size_hint=(0.4, 0.9),
                            background_color=(1, 1, 1, 0.7),
                            background='[color=cccccc]'
                            )
        self._popup.open()
    
    def close_actions(self):
        '''
        Close pop-up
        '''
        self._popup.dismiss()
    
    def open_background(self):
        '''
        Open A Pop-up To Manage the Canvas Background
        '''
        content = BackgroundMenu(self.data)
        content.setUpData(self.data)
        content.close = self.close_actions
        self._popup = Popup(title="Background Picture",
                            content=content,
                            size_hint=(0.5, 0.5)
                            )
        self._popup.open()
