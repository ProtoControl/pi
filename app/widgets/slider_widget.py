from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.slider import MDSlider, MDSliderHandle, MDSliderValueLabel
from kivymd.uix.label import MDLabel

class SliderWidget(MDBoxLayout):
    def __init__(self, text, min, max, id, **kwargs):
        super(SliderWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.value_label = MDLabel(
            text=f"{text}: {min}",  # Initial value
            size_hint=(1, None),
            height='40dp',  # Set a fixed height for the label
            halign="center"  # Center-align the text
        )
        # Create the slider with a value label
        self.slider = MDSlider(
            MDSliderHandle(),
            MDSliderValueLabel(
                text=f"{text}: {min}",  # Initial value label text
                font_size="16sp",  # Customize font size
                halign="center"  # Center-align the text
            ),
            min=min,
            max=max,
            value=min
        )
        self.slider.orientation = 'horizontal'
        self.slider.value_track = True
        self.slider.value_track_color = [1, 0, 0, 1]
        self.slider.min = min
        self.slider.max = max
        self.slider.id = id
        self.slider.text = text

        # Bind the slider's value to update the value label
        self.slider.bind(value=self.on_value_change)

        # Add the slider to the layout
        self.add_widget(self.slider)
        self.add_widget(self.value_label)

    def on_value_change(self, instance, value):
        # Round the value to 2 decimal places
        rounded_value = round(value, 2)

        # Update the value label text
        self.value_label.text = f"{self.slider.text}: {rounded_value}"

        # Print the message (for debugging or sending data)
        message = f"{self.slider.id},{rounded_value}"
        print(message)
        # if not debug_mode:
        #     ser.write(message.encode('utf-8'))