import random
import datetime
import os
import json
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Rotate, PushMatrix, PopMatrix, RoundedRectangle
from kivy.utils import platform

# --- LUXURIOUS COLOR PALETTE ---
NAVY = (0.10, 0.14, 0.20, 1)  # #1A2332
GOLD = (0.79, 0.66, 0.38, 1)  # #C9A961
CREAM = (0.96, 0.91, 0.85, 1)  # #F4E8D8
DEEP_GREEN = (0.17, 0.37, 0.18, 1)  # #2C5F2D
LIGHT_GOLD = (0.90, 0.82, 0.63, 1)  # Lighter gold for highlights

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

    # Kitchen (6 plants)
    {"name": "Ponytail Palm", "room": "Kitchen", "img": "ponytail.png"},
    {"name": "Heartleaf Philodendron (Hanging)", "room": "Kitchen", "img": "philodendron_hang.png"},
    {"name": "Spider Plant #1 (Counter)", "room": "Kitchen", "img": "spider_1.png"},
    {"name": "Butt Plant", "room": "Kitchen", "img": "butt.png"},
    {"name": "Cactus", "room": "Kitchen", "img": "cactus.png"},
    {"name": "Little Plant We Hate", "room": "Kitchen", "img": "hate.png"}
]

# --- 2. IMPROVED PARTICLE SYSTEM ---
class ConfettiParticle:
    def __init__(self, canvas, pos):
        self.canvas = canvas
        with self.canvas:
            # Use gold/green colors for luxurious feel
            colors = [GOLD, DEEP_GREEN, LIGHT_GOLD, CREAM]
            self.color = Color(*random.choice(colors))
            PushMatrix()
            self.rot = Rotate(angle=0, origin=pos)
            # LARGER particles (40x40)
            self.rect = Rectangle(pos=pos, size=(40, 40))
            PopMatrix()
        self.vel_x = random.uniform(-20, 20)
        self.vel_y = random.uniform(10, 30)
        self.rotation_speed = random.uniform(-20, 20)

    def update(self):
        self.rect.pos = (self.rect.pos[0] + self.vel_x, self.rect.pos[1] + self.vel_y)
        self.vel_y -= 0.6  # Slower gravity
        self.rot.angle += self.rotation_speed
        # SLOWER fade-out (was 0.02, now 0.01) - particles linger longer
        self.color.a -= 0.01

# --- 3. JAKE ICON ANIMATION ---
class JakeIcon(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = os.path.join("assets", "images", "jake.png")
        self.size_hint = (None, None)
        self.size = (150, 150)
        self.pos = (Window.width/2 - 75, -200)  # Start below screen

    def animate_in_and_out(self):
        # Animate from bottom to center
        anim1 = Animation(y=Window.height/2 - 75, duration=0.5, t='out_back')
        # Then animate from center to top
        anim2 = Animation(y=Window.height + 200, duration=0.5, t='in_back')
        anim1.bind(on_complete=lambda *args: anim2.start(self))
        anim2.bind(on_complete=lambda *args: self.parent.remove_widget(self))
        anim1.start(self)

# --- 4. LOG VIEWER SCREEN ---
class LogViewer(FloatLayout):
    def __init__(self, log_file, on_close, **kwargs):
        super().__init__(**kwargs)

        # Background with navy color
        with self.canvas.before:
            Color(*NAVY)
            self.bg_rect = Rectangle(size=Window.size, pos=(0, 0))

        # Title bar with gold
        with self.canvas.before:
            Color(*GOLD)
            Rectangle(size=(Window.width, 80), pos=(0, Window.height - 80))

        # Title
        title = Label(
            text="Watering Log",
            font_size='28sp',
            bold=True,
            color=NAVY,
            pos_hint={'center_x': 0.5, 'center_y': 0.95}
        )
        self.add_widget(title)

        # Close button
        close_btn = Button(
            text="✕",
            size_hint=(None, None),
            size=(60, 60),
            pos_hint={'right': 0.98, 'top': 0.98},
            background_color=DEEP_GREEN,
            font_size='24sp',
            color=CREAM
        )
        close_btn.bind(on_release=lambda x: on_close())
        self.add_widget(close_btn)

        # Log content
        log_text = self.load_log(log_file)

        log_label = Label(
            text=log_text,
            font_size='16sp',
            color=CREAM,
            size_hint_y=None,
            text_size=(Window.width * 0.9, None),
            halign='left',
            valign='top'
        )
        log_label.bind(texture_size=log_label.setter('size'))

        scroll = ScrollView(
            size_hint=(0.95, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )
        scroll.add_widget(log_label)
        self.add_widget(scroll)

    def load_log(self, log_file):
        """Load and format the log file"""
        if not os.path.exists(log_file):
            return "No watering history yet.\n\nStart watering plants to see your log!"

        try:
            with open(log_file, "r") as f:
                lines = f.readlines()
                if not lines:
                    return "No watering history yet."

                # Show most recent first
                lines.reverse()
                return "".join(lines)
        except Exception as e:
            return f"Error loading log: {e}"

# --- 5. ROOM SELECTION SCREEN (LUXURIOUS) ---
class RoomSelectScreen(FloatLayout):
    def __init__(self, on_room_selected, **kwargs):
        super().__init__(**kwargs)
        self.on_room_selected = on_room_selected

        # Background - Navy gradient effect
        with self.canvas.before:
            Color(*NAVY)
            self.bg_rect = Rectangle(size=Window.size, pos=(0, 0))

        # Play welcome music
        try:
            welcome = SoundLoader.load(os.path.join("assets", "audio", "welcome.mp3"))
            if welcome:
                welcome.play()
        except Exception as e:
            print(f"Could not load welcome.mp3: {e}")

        # Title with gold color
        title = Label(
            text="Choose Your Room",
            font_size='42sp',
            bold=True,
            color=GOLD,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        self.add_widget(title)

        # Subtitle
        subtitle = Label(
            text="Select a room to water your plants",
            font_size='18sp',
            color=CREAM,
            pos_hint={'center_x': 0.5, 'center_y': 0.78}
        )
        self.add_widget(subtitle)

        # Kitchen Button - with rounded corners and luxurious styling
        kitchen_btn = Button(
            text="Kitchen",
            font_size='28sp',
            bold=True,
            size_hint=(0.7, 0.11),
            pos_hint={'center_x': 0.5, 'center_y': 0.62},
            background_color=DEEP_GREEN,
            color=CREAM
        )
        kitchen_btn.bind(on_release=lambda x: self.select_room("Kitchen"))
        self.add_widget(kitchen_btn)

        # Office Button
        office_btn = Button(
            text="Office",
            font_size='28sp',
            bold=True,
            size_hint=(0.7, 0.11),
            pos_hint={'center_x': 0.5, 'center_y': 0.48},
            background_color=GOLD,
            color=NAVY
        )
        office_btn.bind(on_release=lambda x: self.select_room("Office"))
        self.add_widget(office_btn)

        # Bedroom Button
        bedroom_btn = Button(
            text="Bedroom",
            font_size='28sp',
            bold=True,
            size_hint=(0.7, 0.11),
            pos_hint={'center_x': 0.5, 'center_y': 0.34},
            background_color=DEEP_GREEN,
            color=CREAM
        )
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

        Clock.schedule_once(lambda dt: self.on_room_selected(room), 0.5)

# --- 6. SWIPE CARD UI (LUXURIOUS) ---
class PlantCard(FloatLayout):
    def __init__(self, plant_info, on_swipe_callback, **kwargs):
        super().__init__(**kwargs)
        self.plant_info = plant_info
        self.on_swipe_callback = on_swipe_callback
        self.start_x = 0

        # Card background with cream color
        with self.canvas.before:
            Color(*CREAM)
            self.rect = Rectangle(
                size=(Window.width * 0.9, Window.height * 0.75),
                pos=(Window.width * 0.05, Window.height * 0.12)
            )

        # Gold accent border
        with self.canvas.before:
            Color(*GOLD)
            # Top border
            Rectangle(size=(Window.width * 0.9, 4), pos=(Window.width * 0.05, Window.height * 0.87 - 4))
            # Bottom border
            Rectangle(size=(Window.width * 0.9, 4), pos=(Window.width * 0.05, Window.height * 0.12))

        # SWIPE INSTRUCTIONS at the top
        instructions = Label(
            text="← Swipe LEFT to Water  |  Swipe RIGHT to Skip →",
            font_size='16sp',
            color=NAVY,
            bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.92}
        )
        self.add_widget(instructions)

        # Load plant image
        try:
            img_path = os.path.join("assets", "images", plant_info['img'])
            self.add_widget(Image(
                source=img_path,
                size_hint=(0.75, 0.5),
                pos_hint={'center_x': 0.5, 'center_y': 0.55}
            ))
        except Exception as e:
            print(f"Could not load image {plant_info['img']}: {e}")

        # Plant name with navy color
        self.add_widget(Label(
            text=plant_info['name'],
            font_size='26sp',
            bold=True,
            color=NAVY,
            pos_hint={'center_x': 0.5, 'center_y': 0.25}
        ))

        # Room label with gold
        self.add_widget(Label(
            text=f"📍 {plant_info['room']}",
            font_size='20sp',
            color=GOLD,
            pos_hint={'center_x': 0.5, 'center_y': 0.18}
        ))

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

# --- 7. MAIN APP LOGIC ---
class PlantTinderApp(App):
    def build(self):
        self.main_ui = FloatLayout()
        self.deck = []
        self.current_room = None
        self.skip_streak = 0
        self.particles = []
        self.card = None
        self.log_viewer = None

        # Navy background
        with self.main_ui.canvas.before:
            Color(*NAVY)
            Rectangle(size=Window.size, pos=(0, 0))

        # Set up data directories
        self.data_dir = self.user_data_dir
        self.log_file = os.path.join(self.data_dir, "plant_history.log")
        self.state_file = os.path.join(self.data_dir, "app_state.json")

        # Load background music
        try:
            self.bg_music = SoundLoader.load(os.path.join("assets", "audio", "background.mp3"))
            if self.bg_music:
                self.bg_music.loop = True
                self.bg_music.volume = 0.3
        except Exception as e:
            print(f"Could not load background.mp3: {e}")
            self.bg_music = None

        # Start particle update loop
        Clock.schedule_interval(self.update_particles, 1/60)

        # Check for nag status
        self.check_nag_status()

        # HAMBURGER MENU BUTTON
        self.menu_btn = Button(
            text="☰",
            size_hint=(None, None),
            size=(60, 60),
            pos_hint={'x': 0.02, 'top': 0.98},
            background_color=GOLD,
            color=NAVY,
            font_size='32sp'
        )
        self.menu_btn.bind(on_release=self.toggle_log_viewer)
        self.main_ui.add_widget(self.menu_btn)

        # Show room selection screen
        self.show_room_selection()

        # Manual reset button
        reset_btn = Button(
            text="Reset",
            size_hint=(0.2, 0.06),
            pos_hint={'right': 0.98, 'y': 0.02},
            background_color=DEEP_GREEN,
            color=CREAM,
            font_size='18sp'
        )
        reset_btn.bind(on_release=self.reset_to_room_selection)
        self.main_ui.add_widget(reset_btn)

        return self.main_ui

    def toggle_log_viewer(self, *args):
        """Show/hide the log viewer"""
        if self.log_viewer:
            self.main_ui.remove_widget(self.log_viewer)
            self.log_viewer = None
        else:
            self.log_viewer = LogViewer(self.log_file, self.toggle_log_viewer)
            self.main_ui.add_widget(self.log_viewer)

    def show_room_selection(self):
        """Display the room selection screen"""
        self.main_ui.clear_widgets()

        # Re-add hamburger menu
        self.main_ui.add_widget(self.menu_btn)

        room_screen = RoomSelectScreen(self.start_gameplay)
        self.main_ui.add_widget(room_screen)

        # Re-add reset button
        reset_btn = Button(
            text="Reset",
            size_hint=(0.2, 0.06),
            pos_hint={'right': 0.98, 'y': 0.02},
            background_color=DEEP_GREEN,
            color=CREAM,
            font_size='18sp'
        )
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

        # Re-add hamburger menu and reset button
        self.main_ui.add_widget(self.menu_btn)

        reset_btn = Button(
            text="Reset",
            size_hint=(0.2, 0.06),
            pos_hint={'right': 0.98, 'y': 0.02},
            background_color=DEEP_GREEN,
            color=CREAM,
            font_size='18sp'
        )
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
        nag = Label(
            text="⚠️ 48 HOURS SINCE LAST WATER!\nYour plants need you!",
            color=GOLD,
            font_size='26sp',
            bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.main_ui.add_widget(nag)
        Animation(opacity=0, duration=5).start(nag)

    def handle_swipe(self, plant_info, direction):
        """Handle plant card swipe"""
        if self.card:
            self.main_ui.remove_widget(self.card)

        action = "WATERED" if direction == "left" else "SKIPPED"

        # Haptics & Sound
        if action == "WATERED":
            # NO EXPLOSION on individual water - only play watered sound!
            self.vibrate(0.05)
            self.skip_streak = 0

            # Show JAKE ICON animation
            jake = JakeIcon()
            self.main_ui.add_widget(jake)
            jake.animate_in_and_out()

            # Play watered sound (llama special case)
            if 'llama' in plant_info['name'].lower():
                self.play_sound('llama.mp3')
            else:
                self.play_sound('watered.mp3')
        else:
            self.vibrate(0.2)
            self.skip_streak += 1
            self.play_sound('skipped.mp3')

        # Logging with timestamp
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

        # Red overlay with boss message
        self.boss = Button(
            text="💀 BOSS LEVEL! 💀\n\nYou skipped 3 plants!\nTap to revive and continue!",
            background_color=(0.8, 0.1, 0.1, 0.95),
            font_size='32sp',
            bold=True,
            color=CREAM
        )
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
            # Room complete! NOW play explosion
            self.explode()

            # Play explosion sound ONLY on room complete
            try:
                explosion = SoundLoader.load(os.path.join("assets", "audio", "explosion.mp3"))
                if explosion:
                    explosion.play()
            except Exception as e:
                print(f"Could not load explosion.mp3: {e}")

            # Show completion message
            completion_msg = Label(
                text=f"🎉 {self.current_room} Complete! 🎉\n\nReturning to room selection...",
                font_size='36sp',
                bold=True,
                color=GOLD,
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.main_ui.add_widget(completion_msg)

            # Return to room selection after 4 seconds (give time to see explosion)
            Clock.schedule_once(lambda dt: self.show_room_selection(), 4)

    def reset_to_room_selection(self, *args):
        """Reset and return to room selection"""
        self.main_ui.clear_widgets()
        self.skip_streak = 0
        self.show_room_selection()

    def explode(self):
        """Trigger particle explosion (100 particles for room complete!)"""
        for _ in range(100):  # More particles for room complete celebration
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
