from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config

# Set fullscreen mode
Config.set('graphics', 'fullscreen', 'auto')

class LifeTrackerApp(App):
    def build(self):
        # Main layout: 2x2 grid
        main_layout = GridLayout(cols=2, rows=2, spacing=10, padding=10)

        # Add player trackers to the grid
        main_layout.add_widget(self.create_player_tracker(1, invert=True))  # Top-left (inverted)
        main_layout.add_widget(self.create_player_tracker(2, invert=True))  # Top-right (inverted)
        main_layout.add_widget(self.create_player_tracker(3, invert=False))  # Bottom-left
        main_layout.add_widget(self.create_player_tracker(4, invert=False))  # Bottom-right

        return main_layout

    def create_player_tracker(self, player, invert=False):
        # Container for player tracker
        player_box = BoxLayout(orientation='vertical' if not invert else 'vertical', spacing=10)

        # Life total label
        life_label = Label(text="40", font_size=50, bold=True)

        # Adjust buttons layout
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)

        # Minus button
        minus_button = Button(text="-", font_size=40, size_hint=(0.4, 1))
        minus_button.bind(on_press=lambda instance: self.change_life(life_label, -1))

        # Plus button
        plus_button = Button(text="+", font_size=40, size_hint=(0.4, 1))
        plus_button.bind(on_press=lambda instance: self.change_life(life_label, 1))

        if invert:
            # Add elements in inverted order
            player_box.add_widget(button_layout)
            button_layout.add_widget(plus_button)
            button_layout.add_widget(minus_button)
            player_box.add_widget(life_label)
        else:
            # Add elements in normal order
            player_box.add_widget(life_label)
            button_layout.add_widget(minus_button)
            button_layout.add_widget(plus_button)
            player_box.add_widget(button_layout)

        # Anchor the box to center
        anchored_box = AnchorLayout(anchor_x='center', anchor_y='center')
        anchored_box.add_widget(player_box)

        return anchored_box

    def change_life(self, label, amount):
        # Update the life total
        current_life = int(label.text)
        new_life = current_life + amount
        label.text = str(new_life)

# Run the app
if __name__ == "__main__":
    LifeTrackerApp().run()
