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
        # Main layout: 3x3 grid
        main_layout = GridLayout(cols=3, rows=3, spacing=10, padding=10)

        # Fill in players and center area
        main_layout.add_widget(self.create_player_tracker(1))  # Top-left
        main_layout.add_widget(Label())  # Top-center (empty)
        main_layout.add_widget(self.create_player_tracker(2))  # Top-right

        main_layout.add_widget(Label())  # Middle-left (empty)
        main_layout.add_widget(self.create_center_area())  # Center area
        main_layout.add_widget(Label())  # Middle-right (empty)

        main_layout.add_widget(self.create_player_tracker(3))  # Bottom-left
        main_layout.add_widget(Label())  # Bottom-center (empty)
        main_layout.add_widget(self.create_player_tracker(4))  # Bottom-right

        return main_layout

    def create_player_tracker(self, player):
        # Container for player tracker
        player_box = BoxLayout(orientation='vertical', spacing=10)

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

        # Add buttons to the layout
        button_layout.add_widget(minus_button)
        button_layout.add_widget(plus_button)

        # Add elements to the player box
        player_box.add_widget(life_label)
        player_box.add_widget(button_layout)

        # Anchor the box to center
        anchored_box = AnchorLayout(anchor_x='center', anchor_y='center')
        anchored_box.add_widget(player_box)

        return anchored_box

    def create_center_area(self):
        # Center area can be used for additional features (e.g., reset button)
        center_label = Label(text="Commander Life Tracker", font_size=30, bold=True)
        anchored_box = AnchorLayout(anchor_x='center', anchor_y='center')
        anchored_box.add_widget(center_label)
        return anchored_box

    def change_life(self, label, amount):
        # Update the life total
        current_life = int(label.text)
        new_life = current_life + amount
        label.text = str(new_life)

# Run the app
if __name__ == "__main__":
    LifeTrackerApp().run()
