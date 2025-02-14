from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.slider import MDSlider
from kivymd.uix.label import MDLabel


class SliderWidget(MDBoxLayout):
    def __init__(self, text, min, max, id,**kwargs):
        super(SliderWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.slider = MDSlider(min=min, max=max, value=min)
        self.slider.orientation = 'horizontal'
        self.slider.value_track = True
        self.slider.value_track_color = [1, 0, 0, 1]
        self.slider.text = text
        self.slider.min = min
        self.slider.max = max
        self.slider.id = id

        self.value_label = MDLabel(text=f"{text}", size_hint=(1, 0.2), font_size='40sp')
        self.slider.bind(value=self.on_value_change)

        self.add_widget(self.value_label)
        self.add_widget(self.slider)

    def on_value_change(self, instance, value):
        rounded_value = round(value, 2)
        message = f"{self.slider.id},{rounded_value}"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))
        self.value_label.text = f"{self.slider.text}: {rounded_value}"
