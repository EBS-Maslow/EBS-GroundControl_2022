from kivy.uix.floatlayout             import    FloatLayout
from kivy.properties                  import    ObjectProperty
from kivy.properties                  import    StringProperty
from uielements.scrollableLabel       import    ScrollableLabel


class NotificationPopup(FloatLayout):
    '''
    
    A Pop-up Dialog To Display Text
    
    If the text does not all fit on the display, the user can scroll it
    
    '''
    continueOn = ObjectProperty(None)
    text = StringProperty("")