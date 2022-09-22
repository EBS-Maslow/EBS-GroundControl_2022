from kivy.uix.floatlayout             import    FloatLayout
from kivy.properties                  import    ObjectProperty, StringProperty
from uielements.scrollableLabel       import    ScrollableLabel


class ScrollableTextPopup(FloatLayout):

    cancel = ObjectProperty(None)
    text = StringProperty('')