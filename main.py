import random
import datetime
import os
import json
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Rotate, PushMatrix, PopMatrix
from kivy.utils import platform

# --- 1. PLANT DATA ---
PLANT_DECK_MASTER = [
    # Bedroom (2 plants)
    {"name": "Shitty Little Window Plant", "room": "Bedroom", "img": "window.png"},
    {"name": "The Plant in the Llama", "room": "Bedroom", "img": "llama_icon.png"},

    # Office (14 plants)
    {"name": "Dracaena Fragrans (Desk)", "room": "Office", "img": "dracaena_f.png"},
    {"name": "Dracaena Marginata (Stand)", "room": "Office", "img": "dracaena_m.png"},
    {"name": "Pothos (Stand)", "room": "Office", "img": "pothos.png"},
    {"name": "Spider Plant #2", "room": "Office", "img": "spider_2.png"},
    {"name": "Heartleaf Philodendron (Stand)", "room": "Office", "img": "philodendron_h.png"},
    {"name": "Monstera Stand #1", "room": "Office", "img": "monstera_stand_1.png"},
    {"name": "Monstera Stand #2", "room": "Office", "img": "monstera_stand_2.png"},
    {"name": "Monstera Deliciosa (Large Window)", "room": "Office", "img": "monstera_large.png"},
    {"name": "Monstera Deliciosa (Bookshelf)", "room": "Office", "img": "monstera_shelf.png"},
    {"name": "Heartleaf Philodendron (Hanging)", "room": "Office", "img": "philodendron_hang.png"},
    {"name": "Heartleaf Philodendron (Hanging) #2", "room": "Office", "img": "philodendron_hang.png"},
    {"name": "Terrarium (Desk)", "room": "Office", "img": "terrarium.png"},
    {"name": "Snake Plant #1", "room": "Office", "img": "snake_1.png"},
    {"name": "Snake Plant #2", "room": "Office", "img": "snake_2.png"},

    # Kitchen (5 plants)
    {"name": "Ponytail Palm", "room": "Kitchen", "img": "ponytail.png"},
    {"name": "Heartleaf Philodendron (Hanging)", "room": "Kitchen", "img": "philodendron_hang.png"},
    {"name": "Spider Plant #1 (Counter)", "room": "Kitchen", "img": "spider_1.png"},
    {"name": "Butt Plant", "room": "Kitchen", "img": "butt.png"},
    {"name": "Cactus", "room": "Kitchen", "img": "cactus.png"},
    {"name": "Little Plant We Hate", "room": "Kitchen", "img": "hate.png"}
]

# --- 2. PARTICLE SYSTEM (EXPLOSION) ---
class ConfettiParticle:
    def __init__(self, canvas, pos):
        self.canvas = canvas
        with self.canvas:
            self.color = Color(random.random(), random.random(), random.random(), 1)
            PushMatrix()
            self.rot = Rotate(angle=0, origin=pos)
            self.rect = Rectangle(pos=pos, size=(20, 20))
            PopMatrix()
        self.vel_x = random.uniform(-15, 15)
        self.vel_y = random.uniform(5, 25)
        self.rotation_speed = random.uniform(-15, 15)

    def update(self):
        self.rect.pos = (self.rect.pos[0] + self.vel_x, self.rect.pos[1] + self.vel_y)
        self.vel_y -= 0.8  # Gravity
        self.rot.angle += self.rotation_speed
        self.color.a -= 0.02  # Faster fade-out for better performance

# --- 3. ROOM SELECTION SCREEN ---
class RoomSelectScreen(FloatLayout):
    def __init__(self, on_room_selected, **kwargs):
        super().__init__(**kwargs)
        self.on_room_selected = on_room_selected

        # Background color
        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.bg_rect = Rectangle(size=Window.size, pos=(0, 0))

        # Play welcome music
        try:
            welcome = SoundLoader.load(os.path.join("assets", "audio", "welcome.mp3"))
            if welcome:
                welcome.play()
        except Exception as e:
            print(f"Could not load welcome.mp3: {e}")

        # Title
        self.add_widget(Label(text="Choose a Room", font_size='36sp',
                              pos_hint={'center_x': 0.5, 'center_y': 0.8}))

        # Kitchen Button
        kitchen_btn = Button(text="Kitchen", font_size='28sp', size_hint=(0.7, 0.12),
                            pos_hint={'center_x': 0.5, 'center_y': 0.6},
                            background_color=(0.2, 0.8, 0.2, 1))
        kitchen_btn.bind(on_release=lambda x: self.select_room("Kitchen"))
        self.add_widget(kitchen_btn)

        # Office Button
        office_btn = Button(text="Office", font_size='28sp', size_hint=(0.7, 0.12),
                           pos_hint={'center_x': 0.5, 'center_y': 0.45},
                           background_color=(0.2, 0.5, 0.8, 1))
        office_btn.bind(on_release=lambda x: self.select_room("Office"))
        self.add_widget(office_btn)

        # Bedroom Button
        bedroom_btn = Button(text="Bedroom", font_size='28sp', size_hint=(0.7, 0.12),
                            pos_hint={'center_x': 0.5, 'center_y': 0.3},
                            background_color=(0.8, 0.2, 0.8, 1))
        bedroom_btn.bind(on_release=lambda x: self.select_room("Bedroom"))
        self.add_widget(bedroom_btn)

    def select_room(self, room):
        # Play room-specific intro sound
        sound_file = f"{room.lower()}.mp3"
        try:
            sound = SoundLoader.load(os.path.join("assets", "audio", sound_file))
            if sound:
                sound.play()
        except Exception as e:
            print(f"Could not load {sound_file}: {e}")

        # Wait a moment for sound to start, then transition
        Clock.schedule_once(lambda dt: self.on_room_selected(room), 0.5)

# --- 4. SWIPE CARD UI ---
class PlantCard(FloatLayout):
    def __init__(self, plant_info, on_swipe_callback, **kwargs):
        super().__init__(**kwargs)
        self.plant_info = plant_info
        self.on_swipe_callback = on_swipe_callback
        self.start_x = 0

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=(Window.width * 0.85, Window.height * 0.7),
                                  pos=(Window.width * 0.075, Window.height * 0.15))

        # Load plant image
        try:
            img_path = os.path.join("assets", "images", plant_info['img'])
            self.add_widget(Image(source=img_path, size_hint=(0.8, 0.5),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.6}))
        except Exception as e:
            print(f"Could not load image {plant_info['img']}: {e}")
            # Fallback: colored rectangle
            with self.canvas:
                Color(0.5, 0.5, 0.5, 1)
                Rectangle(size=(Window.width * 0.6, Window.height * 0.4),
                         pos=(Window.width * 0.2, Window.height * 0.3))

        # Plant name
        self.add_widget(Label(text=plant_info['name'], font_size='24sp', bold=True,
                             pos_hint={'center_x': 0.5, 'center_y': 0.35}))

        # Room label
        self.add_widget(Label(text=f"Room: {plant_info['room']}", font_size='18sp',
                             pos_hint={'center_x': 0.5, 'center_y': 0.25}))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.start_x = self.x
            return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.x += touch.dx
            return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            if abs(self.x - self.start_x) > Window.width * 0.3:
                direction = "left" if (self.x - self.start_x) < 0 else "right"
                self.swipe_end(direction)
            else:
                Animation(x=self.start_x, duration=0.2, t='out_back').start(self)
            return True

    def swipe_end(self, direction):
        target_x = -Window.width if direction == "left" else Window.width * 2
        anim = Animation(x=target_x, opacity=0, duration=0.3)
        anim.bind(on_complete=lambda *args: self.on_swipe_callback(self.plant_info, direction))
        anim.start(self)

# --- 5. MAIN APP LOGIC ---
class PlantTinderApp(App):
    def build(self):
        self.main_ui = FloatLayout()
        self.deck = []
        self.current_room = None
        self.skip_streak = 0
        self.particles = []
        self.card = None

        # Set up data directories
        self.data_dir = self.user_data_dir
        self.log_file = os.path.join(self.data_dir, "plant_history.log")
        self.state_file = os.path.join(self.data_dir, "app_state.json")

        # Load background music (but don't play yet)
        try:
            self.bg_music = SoundLoader.load(os.path.join("assets", "audio", "background.mp3"))
            if self.bg_music:
                self.bg_music.loop = True
                self.bg_music.volume = 0.3  # Lower volume for background
        except Exception as e:
            print(f"Could not load background.mp3: {e}")
            self.bg_music = None

        # Start particle update loop
        Clock.schedule_interval(self.update_particles, 1/60)

        # Check for nag status
        self.check_nag_status()

        # Show room selection screen
        self.show_room_selection()

        # Manual reset button
        reset_btn = Button(text="Reset", size_hint=(0.2, 0.05),
                          pos_hint={'right': 1, 'y': 0}, opacity=0.5)
        reset_btn.bind(on_release=self.reset_to_room_selection)
        self.main_ui.add_widget(reset_btn)

        return self.main_ui

    def show_room_selection(self):
        """Display the room selection screen"""
        self.main_ui.clear_widgets()
        room_screen = RoomSelectScreen(self.start_gameplay)
        self.main_ui.add_widget(room_screen)

        # Re-add reset button
        reset_btn = Button(text="Reset", size_hint=(0.2, 0.05),
                          pos_hint={'right': 1, 'y': 0}, opacity=0.5)
        reset_btn.bind(on_release=self.reset_to_room_selection)
        self.main_ui.add_widget(reset_btn)

    def start_gameplay(self, room):
        """Start gameplay for the selected room"""
        self.current_room = room

        # Start background music
        if self.bg_music and self.bg_music.state != 'play':
            self.bg_music.play()

        # Filter deck by selected room
        self.deck = [p for p in PLANT_DECK_MASTER if p['room'] == room]

        # Clear UI and load first card
        self.main_ui.clear_widgets()

        # Re-add reset button
        reset_btn = Button(text="Reset", size_hint=(0.2, 0.05),
                          pos_hint={'right': 1, 'y': 0}, opacity=0.5)
        reset_btn.bind(on_release=self.reset_to_room_selection)
        self.main_ui.add_widget(reset_btn)

        self.load_next_card()

    def vibrate(self, duration=0.1):
        """Vibrate the device (Android only)"""
        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                vibrator = PythonActivity.mActivity.getSystemService(Context.VIBRATOR_SERVICE)
                vibrator.vibrate(int(duration * 1000))
            except Exception as e:
                print(f"Vibration failed: {e}")

    def check_nag_status(self):
        """Check if user hasn't watered plants in 48 hours"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r") as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1]
                        last_time_str = last_line.split(']')[0][1:]
                        last_time = datetime.datetime.strptime(last_time_str, "%Y-%m-%d %H:%M")
                        if datetime.datetime.now() - last_time > datetime.timedelta(hours=48):
                            self.trigger_nag()
            except Exception as e:
                print(f"Error checking nag status: {e}")

    def trigger_nag(self):
        """Show 48-hour nag warning"""
        nag = Label(text="WARNING: 48HRS SINCE LAST WATER!\nYour plants need you!",
                   color=(1, 0, 0, 1), font_size='24sp',
                   pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.main_ui.add_widget(nag)
        Animation(opacity=0, duration=5).start(nag)

    def handle_swipe(self, plant_info, direction):
        """Handle plant card swipe"""
        if self.card:
            self.main_ui.remove_widget(self.card)

        action = "WATERED" if direction == "left" else "SKIPPED"

        # Haptics & Sound
        if action == "WATERED":
            # EXPLOSION ON EVERY WATER!
            self.explode()

            # Play explosion sound
            try:
                explosion = SoundLoader.load(os.path.join("assets", "audio", "explosion.mp3"))
                if explosion:
                    explosion.play()
            except Exception as e:
                print(f"Could not load explosion.mp3: {e}")

            self.vibrate(0.05)
            self.skip_streak = 0

            # Play secondary sound (after explosion sound)
            if 'llama' in plant_info['name'].lower():
                s_file = 'llama.mp3'
            else:
                s_file = 'watered.mp3'

            Clock.schedule_once(lambda dt: self.play_sound(s_file), 0.3)
        else:
            self.vibrate(0.2)
            self.skip_streak += 1
            self.play_sound('skipped.mp3')

        # Logging
        try:
            with open(self.log_file, "a") as f:
                t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                f.write(f"[{t}] {plant_info['name']}: {action}\n")
        except Exception as e:
            print(f"Error writing to log: {e}")

        # Check for boss level
        if self.skip_streak >= 3:
            self.trigger_boss_level()
        else:
            self.load_next_card()

    def play_sound(self, filename):
        """Play a sound file"""
        try:
            sound = SoundLoader.load(os.path.join("assets", "audio", filename))
            if sound:
                sound.play()
        except Exception as e:
            print(f"Could not load {filename}: {e}")

    def trigger_boss_level(self):
        """Trigger boss level after 3 skips"""
        # Stop background music
        if self.bg_music:
            self.bg_music.stop()

        # Red overlay with "Sad Plant" message
        self.boss = Button(text="BOSS LEVEL!\n\nYou skipped 3 plants!\nTap to revive and continue!",
                          background_color=(1, 0, 0, 0.9), font_size='30sp')
        self.boss.bind(on_release=self.clear_boss)
        self.main_ui.add_widget(self.boss)

        # Play boss sound
        self.play_sound('boss.mp3')

    def clear_boss(self, *args):
        """Clear boss level and resume gameplay"""
        self.main_ui.remove_widget(self.boss)
        self.skip_streak = 0

        # Resume background music
        if self.bg_music and self.bg_music.state != 'play':
            self.bg_music.play()

        self.load_next_card()

    def load_next_card(self):
        """Load the next plant card"""
        if self.deck:
            plant = self.deck.pop(0)
            self.card = PlantCard(plant, self.handle_swipe)
            self.main_ui.add_widget(self.card)
        else:
            # Room complete!
            self.explode()

            # Show completion message
            completion_msg = Label(
                text=f"{self.current_room} Complete!\n\nReturning to room selection...",
                font_size='32sp',
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.main_ui.add_widget(completion_msg)

            # Return to room selection after 3 seconds
            Clock.schedule_once(lambda dt: self.show_room_selection(), 3)

    def reset_to_room_selection(self, *args):
        """Reset and return to room selection"""
        self.main_ui.clear_widgets()
        self.skip_streak = 0
        self.show_room_selection()

    def explode(self):
        """Trigger particle explosion (reduced to 50 particles for performance)"""
        for _ in range(50):
            self.particles.append(
                ConfettiParticle(self.main_ui.canvas.after,
                               (Window.width / 2, Window.height / 2))
            )

    def update_particles(self, dt):
        """Update particle animation"""
        for p in self.particles[:]:
            p.update()
            if p.color.a <= 0:
                try:
                    self.main_ui.canvas.after.remove(p.color)
                    self.main_ui.canvas.after.remove(p.rect)
                except:
                    pass
                self.particles.remove(p)

    def on_pause(self):
        """Handle app pause (Android lifecycle)"""
        if self.bg_music:
            self.bg_music.stop()
        return True

    def on_resume(self):
        """Handle app resume (Android lifecycle)"""
        if self.bg_music and self.current_room:
            self.bg_music.play()

if __name__ == '__main__':
    PlantTinderApp().run()
