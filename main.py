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
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Rotate, PushMatrix, PopMatrix
from kivy.utils import platform

# --- LUXURIOUS COLOR PALETTE ---
NAVY = (0.10, 0.14, 0.20, 1)
GOLD = (0.79, 0.66, 0.38, 1)
CREAM = (0.96, 0.91, 0.85, 1)
DEEP_GREEN = (0.17, 0.37, 0.18, 1)
LIGHT_GOLD = (0.90, 0.82, 0.63, 1)

# --- PLANT DATA ---
PLANT_DECK_MASTER = [
    {"name": "Shitty Little Window Plant", "room": "Bedroom", "img": "window.png"},
    {"name": "The Plant in the Llama", "room": "Bedroom", "img": "llama_icon.png"},
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
    {"name": "Ponytail Palm", "room": "Kitchen", "img": "ponytail.png"},
    {"name": "Heartleaf Philodendron (Hanging)", "room": "Kitchen", "img": "philodendron_hang.png"},
    {"name": "Spider Plant #1 (Counter)", "room": "Kitchen", "img": "spider_1.png"},
    {"name": "Butt Plant", "room": "Kitchen", "img": "butt.png"},
    {"name": "Cactus", "room": "Kitchen", "img": "cactus.png"},
    {"name": "Little Plant We Hate", "room": "Kitchen", "img": "hate.png"}
]

# --- MASSIVE EXPLOSION OVERLAY ---
class ExplosionOverlay(Widget):
    """Full-screen explosion that appears ON TOP of everything"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        self.size = Window.size
        self.pos = (0, 0)

        # Create MASSIVE explosion - 150 particles covering entire screen
        for _ in range(150):
            self.create_particle()

        # Auto-remove after 3 seconds
        Clock.schedule_once(lambda dt: self.remove_self(), 3)
        Clock.schedule_interval(self.update_particles, 1/60)

    def create_particle(self):
        with self.canvas:
            # Luxurious colors
            colors = [GOLD, DEEP_GREEN, LIGHT_GOLD, CREAM, (1, 0.84, 0, 1)]  # Added pure gold
            color = Color(*random.choice(colors))
            PushMatrix()

            # Random starting position across entire screen
            start_x = random.uniform(0, Window.width)
            start_y = random.uniform(0, Window.height)

            rot = Rotate(angle=0, origin=(start_x, start_y))
            # MASSIVE particles - 60x60!
            rect = Rectangle(pos=(start_x, start_y), size=(60, 60))
            PopMatrix()

        self.particles.append({
            'color': color,
            'rect': rect,
            'rot': rot,
            'vel_x': random.uniform(-25, 25),
            'vel_y': random.uniform(-10, 35),
            'rotation_speed': random.uniform(-25, 25)
        })

    def update_particles(self, dt):
        for p in self.particles:
            # Move particle
            p['rect'].pos = (
                p['rect'].pos[0] + p['vel_x'],
                p['rect'].pos[1] + p['vel_y']
            )
            p['vel_y'] -= 0.5  # Gravity
            p['rot'].angle += p['rotation_speed']
            # Very slow fade
            p['color'].a -= 0.008

    def remove_self(self):
        if self.parent:
            self.parent.remove_widget(self)

# --- JAKE ICON - MASSIVE AND ON TOP ---
class JakeIcon(Image):
    """Massive Jake icon that pops up from bottom"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = os.path.join("assets", "images", "jake.png")
        self.size_hint = (None, None)
        # 5x larger: was 150x150, now 750x750
        self.size = (750, 750)
        self.pos = (Window.width/2 - 375, -800)  # Start way below screen
        self.allow_stretch = True
        self.keep_ratio = True

    def animate_in_and_out(self):
        # Pop up to center
        anim1 = Animation(y=Window.height/2 - 375, duration=0.6, t='out_elastic')
        # Wait a moment
        anim2 = Animation(y=Window.height/2 - 375, duration=0.4)
        # Shoot to top
        anim3 = Animation(y=Window.height + 800, duration=0.5, t='in_back')

        anim1.bind(on_complete=lambda *args: anim2.start(self))
        anim2.bind(on_complete=lambda *args: anim3.start(self))
        anim3.bind(on_complete=lambda *args: self.parent.remove_widget(self) if self.parent else None)
        anim1.start(self)

# --- LOG VIEWER ---
class LogViewer(FloatLayout):
    def __init__(self, log_file, on_close, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*NAVY)
            Rectangle(size=Window.size, pos=(0, 0))

        with self.canvas.before:
            Color(*GOLD)
            Rectangle(size=(Window.width, 100), pos=(0, Window.height - 100))

        title = Label(
            text="Watering Log",
            font_size='30sp',
            bold=True,
            color=NAVY,
            size_hint=(0.9, None),
            height=80,
            text_size=(Window.width * 0.9, None),
            halign='center',
            valign='middle',
            pos_hint={'center_x': 0.5, 'top': 0.98}
        )
        self.add_widget(title)

        close_btn = Button(
            text="X Close",
            size_hint=(0.3, 0.08),
            pos_hint={'center_x': 0.5, 'y': 0.02},
            background_color=DEEP_GREEN,
            font_size='22sp',
            bold=True,
            color=CREAM
        )
        close_btn.bind(on_release=lambda x: on_close())
        self.add_widget(close_btn)

        log_text = self.load_log(log_file)

        log_label = Label(
            text=log_text,
            font_size='18sp',
            color=CREAM,
            size_hint_y=None,
            text_size=(Window.width * 0.9, None),
            halign='left',
            valign='top',
            markup=True
        )
        log_label.bind(texture_size=log_label.setter('size'))

        scroll = ScrollView(
            size_hint=(0.95, 0.75),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        scroll.add_widget(log_label)
        self.add_widget(scroll)

    def load_log(self, log_file):
        if not os.path.exists(log_file):
            return "[color=FFD700][b]No watering history yet[/b][/color]\n\nStart watering plants to see your log!"

        try:
            with open(log_file, "r") as f:
                lines = f.readlines()
                if not lines:
                    return "[color=FFD700][b]No watering history yet[/b][/color]"

                lines.reverse()  # Most recent first
                formatted = []
                for line in lines:
                    if "WATERED" in line:
                        formatted.append(f"[color=90EE90]{line.strip()}[/color]")
                    elif "SKIPPED" in line:
                        formatted.append(f"[color=FFA07A]{line.strip()}[/color]")
                    else:
                        formatted.append(line.strip())

                return "\n".join(formatted)
        except Exception as e:
            return f"[color=FF6B6B]Error loading log: {e}[/color]"

# --- SKIPPED PLANTS LOG VIEWER ---
class SkippedPlantsLogViewer(FloatLayout):
    def __init__(self, log_file, on_close, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*NAVY)
            Rectangle(size=Window.size, pos=(0, 0))

        with self.canvas.before:
            Color(*GOLD)
            Rectangle(size=(Window.width, 100), pos=(0, Window.height - 100))

        title = Label(
            text="Skipped Plants (Last 7 Days)",
            font_size='28sp',
            bold=True,
            color=NAVY,
            size_hint=(0.9, None),
            height=80,
            text_size=(Window.width * 0.9, None),
            halign='center',
            valign='middle',
            pos_hint={'center_x': 0.5, 'top': 0.98}
        )
        self.add_widget(title)

        close_btn = Button(
            text="X Close",
            size_hint=(0.3, 0.08),
            pos_hint={'center_x': 0.5, 'y': 0.02},
            background_color=DEEP_GREEN,
            font_size='22sp',
            bold=True,
            color=CREAM
        )
        close_btn.bind(on_release=lambda x: on_close())
        self.add_widget(close_btn)

        log_text = self.load_skipped_plants(log_file)

        log_label = Label(
            text=log_text,
            font_size='18sp',
            color=CREAM,
            size_hint_y=None,
            text_size=(Window.width * 0.9, None),
            halign='left',
            valign='top',
            markup=True
        )
        log_label.bind(texture_size=log_label.setter('size'))

        scroll = ScrollView(
            size_hint=(0.95, 0.75),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        scroll.add_widget(log_label)
        self.add_widget(scroll)

    def load_skipped_plants(self, log_file):
        if not os.path.exists(log_file):
            return "[color=FFD700][b]No watering history yet[/b][/color]\n\nStart watering plants to see skipped plants!"

        try:
            with open(log_file, "r") as f:
                lines = f.readlines()
                if not lines:
                    return "[color=FFD700][b]No watering history yet[/b][/color]"

                # Get current date
                now = datetime.datetime.now()
                seven_days_ago = now - datetime.timedelta(days=7)

                # Filter for skipped plants in last 7 days
                skipped_lines = []
                for line in lines:
                    if "SKIPPED" in line:
                        try:
                            # Parse date from line: [YYYY-MM-DD HH:MM]
                            date_str = line.split(']')[0].strip('[')
                            log_date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                            if log_date >= seven_days_ago:
                                skipped_lines.append(line)
                        except:
                            # If date parsing fails, include it anyway
                            skipped_lines.append(line)

                if not skipped_lines:
                    return "[color=90EE90][b]No plants skipped in the last 7 days![/b][/color]\n\nGreat job!"

                skipped_lines.reverse()  # Most recent first
                formatted = []
                for line in skipped_lines:
                    formatted.append(f"[color=FFA07A]{line.strip()}[/color]")

                return "\n".join(formatted)
        except Exception as e:
            return f"[color=FF6B6B]Error loading log: {e}[/color]"

# --- ROOM SELECTION ---
class RoomSelectScreen(FloatLayout):
    def __init__(self, on_room_selected, **kwargs):
        super().__init__(**kwargs)
        self.on_room_selected = on_room_selected

        with self.canvas.before:
            Color(*NAVY)
            Rectangle(size=Window.size, pos=(0, 0))

        # Play welcome music and DON'T interrupt it
        try:
            self.welcome_sound = SoundLoader.load(os.path.join("assets", "audio", "welcome.mp3"))
            if self.welcome_sound:
                self.welcome_sound.play()
        except Exception as e:
            print(f"Could not load welcome.mp3: {e}")
            self.welcome_sound = None

        title = Label(
            text="Choose Your Room",
            font_size='44sp',
            bold=True,
            color=GOLD,
            size_hint=(0.9, None),
            height=80,
            text_size=(Window.width * 0.9, None),
            halign='center',
            valign='middle',
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        self.add_widget(title)

        subtitle = Label(
            text="Select a room to water your plants",
            font_size='18sp',
            color=CREAM,
            size_hint=(0.9, None),
            height=40,
            text_size=(Window.width * 0.9, None),
            halign='center',
            valign='middle',
            pos_hint={'center_x': 0.5, 'center_y': 0.77}
        )
        self.add_widget(subtitle)

        kitchen_btn = Button(
            text="Kitchen",
            font_size='28sp',
            bold=True,
            size_hint=(0.75, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.60},
            background_color=DEEP_GREEN,
            color=CREAM,
            text_size=(Window.width * 0.7, None),
            halign='center',
            valign='middle'
        )
        kitchen_btn.bind(on_release=lambda x: self.select_room("Kitchen"))
        self.add_widget(kitchen_btn)

        office_btn = Button(
            text="Office",
            font_size='28sp',
            bold=True,
            size_hint=(0.75, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            background_color=GOLD,
            color=NAVY,
            text_size=(Window.width * 0.7, None),
            halign='center',
            valign='middle'
        )
        office_btn.bind(on_release=lambda x: self.select_room("Office"))
        self.add_widget(office_btn)

        bedroom_btn = Button(
            text="Bedroom",
            font_size='28sp',
            bold=True,
            size_hint=(0.75, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.30},
            background_color=DEEP_GREEN,
            color=CREAM,
            text_size=(Window.width * 0.7, None),
            halign='center',
            valign='middle'
        )
        bedroom_btn.bind(on_release=lambda x: self.select_room("Bedroom"))
        self.add_widget(bedroom_btn)

        # Skipped plants button
        skipped_btn = Button(
            text="SKIPPED PLANTS",
            font_size='20sp',
            bold=True,
            size_hint=(0.6, 0.10),
            pos_hint={'center_x': 0.5, 'center_y': 0.12},
            background_color=LIGHT_GOLD,
            color=NAVY
        )
        skipped_btn.bind(on_release=lambda x: self.on_room_selected("__SKIPPED__"))
        self.add_widget(skipped_btn)

    def select_room(self, room):
        # Stop welcome sound
        if self.welcome_sound:
            self.welcome_sound.stop()

        # Open room immediately, sound will play after room loads
        self.on_room_selected(room)

# --- PLANT CARD WITH VISIBLE INSTRUCTIONS ---
class PlantCard(FloatLayout):
    def __init__(self, plant_info, on_swipe_callback, **kwargs):
        super().__init__(**kwargs)
        self.plant_info = plant_info
        self.on_swipe_callback = on_swipe_callback
        self.start_x = 0

        # Card background
        with self.canvas.before:
            Color(*CREAM)
            Rectangle(
                size=(Window.width * 0.92, Window.height * 0.78),
                pos=(Window.width * 0.04, Window.height * 0.11)
            )

        # Gold borders
        with self.canvas.before:
            Color(*GOLD)
            Rectangle(size=(Window.width * 0.92, 5), pos=(Window.width * 0.04, Window.height * 0.89 - 5))
            Rectangle(size=(Window.width * 0.92, 5), pos=(Window.width * 0.04, Window.height * 0.11))

        # Plant image
        try:
            img_path = os.path.join("assets", "images", plant_info['img'])
            self.add_widget(Image(
                source=img_path,
                size_hint=(0.8, 0.55),
                pos_hint={'center_x': 0.5, 'center_y': 0.52},
                allow_stretch=True,
                keep_ratio=True
            ))
        except Exception as e:
            print(f"Could not load image {plant_info['img']}: {e}")

        # Plant name - with text wrapping
        plant_name = Label(
            text=plant_info['name'],
            font_size='24sp',
            bold=True,
            color=NAVY,
            size_hint=(0.9, None),
            height=70,
            text_size=(Window.width * 0.85, None),
            halign='center',
            valign='middle',
            pos_hint={'center_x': 0.5, 'center_y': 0.22}
        )
        self.add_widget(plant_name)

        # Room label
        self.add_widget(Label(
            text=f"Room: {plant_info['room']}",
            font_size='20sp',
            color=GOLD,
            bold=True,
            size_hint=(0.9, None),
            height=30,
            text_size=(Window.width * 0.85, None),
            halign='center',
            valign='middle',
            pos_hint={'center_x': 0.5, 'center_y': 0.15}
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

# --- MAIN APP ---
class PlantsTheGameApp(App):
    def build(self):
        self.root = FloatLayout()
        self.deck = []
        self.current_room = None
        self.skip_streak = 0
        self.card = None
        self.log_viewer = None
        self.skipped_viewer = None
        self.menu_btn = None
        self.reset_btn = None
        self.instruction_label = None

        with self.root.canvas.before:
            Color(*NAVY)
            Rectangle(size=Window.size, pos=(0, 0))

        self.data_dir = self.user_data_dir
        self.log_file = os.path.join(self.data_dir, "plant_history.log")

        try:
            self.bg_music = SoundLoader.load(os.path.join("assets", "audio", "background.mp3"))
            if self.bg_music:
                self.bg_music.loop = True
                self.bg_music.volume = 0.25
        except Exception as e:
            print(f"Could not load background.mp3: {e}")
            self.bg_music = None

        self.create_persistent_buttons()
        self.show_room_selection()

        return self.root

    def create_persistent_buttons(self):
        """Create hamburger menu and reset button that persist"""
        # Hamburger menu
        self.menu_btn = Button(
            text="MENU",
            size_hint=(None, None),
            size=(80, 70),
            pos=(10, Window.height - 80),
            background_color=GOLD,
            color=NAVY,
            font_size='18sp',
            bold=True
        )
        self.menu_btn.bind(on_release=self.toggle_log_viewer)

        # Reset button
        self.reset_btn = Button(
            text="Reset",
            size_hint=(None, None),
            size=(80, 70),
            pos=(Window.width - 90, Window.height - 80),
            background_color=DEEP_GREEN,
            color=CREAM,
            font_size='18sp',
            bold=True
        )
        self.reset_btn.bind(on_release=self.reset_to_room_selection)

    def show_room_selection(self):
        self.root.clear_widgets()
        room_screen = RoomSelectScreen(self.start_gameplay)
        self.root.add_widget(room_screen)
        # Add persistent buttons ON TOP
        self.root.add_widget(self.menu_btn)
        self.root.add_widget(self.reset_btn)

    def start_gameplay(self, room):
        # Special case: Show skipped plants log
        if room == "__SKIPPED__":
            self.show_skipped_plants()
            return

        self.current_room = room

        if self.bg_music and self.bg_music.state != 'play':
            self.bg_music.play()

        self.deck = [p for p in PLANT_DECK_MASTER if p['room'] == room]

        self.root.clear_widgets()
        self.root.add_widget(self.menu_btn)
        self.root.add_widget(self.reset_btn)

        self.load_next_card()

        # Play room intro sound AFTER room is loaded and visible
        sound_file = f"{room.lower()}.mp3"
        try:
            room_sound = SoundLoader.load(os.path.join("assets", "audio", sound_file))
            if room_sound:
                room_sound.play()
        except Exception as e:
            print(f"Could not load {sound_file}: {e}")

    def show_skipped_plants(self):
        """Show skipped plants log viewer"""
        self.root.clear_widgets()
        self.skipped_viewer = SkippedPlantsLogViewer(self.log_file, self.close_skipped_viewer)
        self.root.add_widget(self.skipped_viewer)
        # Add buttons on top
        self.root.add_widget(self.menu_btn)
        self.root.add_widget(self.reset_btn)

    def close_skipped_viewer(self):
        """Close skipped plants viewer and return to room selection"""
        if self.skipped_viewer:
            self.root.remove_widget(self.skipped_viewer)
            self.skipped_viewer = None
        self.show_room_selection()

    def toggle_log_viewer(self, *args):
        if self.log_viewer:
            self.root.remove_widget(self.log_viewer)
            self.log_viewer = None
        else:
            self.log_viewer = LogViewer(self.log_file, self.toggle_log_viewer)
            # Remove buttons temporarily
            self.root.remove_widget(self.menu_btn)
            self.root.remove_widget(self.reset_btn)
            # Add log viewer
            self.root.add_widget(self.log_viewer)
            # Re-add buttons on top
            self.root.add_widget(self.menu_btn)
            self.root.add_widget(self.reset_btn)

    def vibrate(self, duration=0.1):
        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                vibrator = PythonActivity.mActivity.getSystemService(Context.VIBRATOR_SERVICE)
                vibrator.vibrate(int(duration * 1000))
            except:
                pass

    def handle_swipe(self, plant_info, direction):
        if self.card:
            self.root.remove_widget(self.card)

        action = "WATERED" if direction == "left" else "SKIPPED"

        # Log it
        try:
            with open(self.log_file, "a") as f:
                t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                f.write(f"[{t}] {plant_info['name']}: {action}\n")
        except Exception as e:
            print(f"Error writing log: {e}")

        if action == "WATERED":
            self.vibrate(0.05)
            self.skip_streak = 0

            # Play watered sound
            if 'llama' in plant_info['name'].lower():
                self.play_sound('llama.mp3')
            else:
                self.play_sound('watered.mp3')
        else:
            self.vibrate(0.2)
            self.skip_streak += 1
            self.play_sound('skipped.mp3')

        if self.skip_streak >= 3:
            self.trigger_boss_level()
        else:
            self.load_next_card()

            # Add jake icon AFTER next card is loaded so it appears on top
            if action == "WATERED":
                jake = JakeIcon()
                self.root.add_widget(jake)
                jake.animate_in_and_out()

    def play_sound(self, filename):
        try:
            sound = SoundLoader.load(os.path.join("assets", "audio", filename))
            if sound:
                sound.play()
        except Exception as e:
            print(f"Could not load {filename}: {e}")

    def trigger_boss_level(self):
        if self.bg_music:
            self.bg_music.stop()

        self.boss = Button(
            text="BOSS LEVEL!\n\nYou skipped 3 plants!\n\nTap to continue",
            background_color=(0.85, 0.1, 0.1, 0.97),
            font_size='32sp',
            bold=True,
            color=CREAM,
            text_size=(Window.width * 0.9, None),
            halign='center',
            valign='middle'
        )
        self.boss.bind(on_release=self.clear_boss)
        self.root.add_widget(self.boss)
        # Keep buttons on top
        self.root.remove_widget(self.menu_btn)
        self.root.remove_widget(self.reset_btn)
        self.root.add_widget(self.menu_btn)
        self.root.add_widget(self.reset_btn)

        self.play_sound('boss.mp3')

    def clear_boss(self, *args):
        self.root.remove_widget(self.boss)
        self.skip_streak = 0

        if self.bg_music and self.bg_music.state != 'play':
            self.bg_music.play()

        self.load_next_card()

    def load_next_card(self):
        if self.deck:
            plant = self.deck.pop(0)
            self.card = PlantCard(plant, self.handle_swipe)
            self.root.add_widget(self.card)

            # Add instruction label above card on navy background
            if self.instruction_label:
                self.root.remove_widget(self.instruction_label)
            self.instruction_label = Label(
                text="Swipe left to water, right to wait",
                font_size='20sp',
                color=CREAM,
                bold=True,
                size_hint=(None, None),
                size=(Window.width * 0.9, 50),
                text_size=(Window.width * 0.9, None),
                halign='center',
                valign='middle',
                pos=(Window.width * 0.05, Window.height * 0.91)
            )
            self.root.add_widget(self.instruction_label)

            # Ensure buttons stay on top
            self.root.remove_widget(self.menu_btn)
            self.root.remove_widget(self.reset_btn)
            self.root.add_widget(self.menu_btn)
            self.root.add_widget(self.reset_btn)
        else:
            # Room complete - MASSIVE EXPLOSION!
            explosion = ExplosionOverlay()
            self.root.add_widget(explosion)

            # Play explosion sound
            self.play_sound('explosion.mp3')

            completion_msg = Label(
                text=f"{self.current_room}\nCOMPLETE!",
                font_size='40sp',
                bold=True,
                color=GOLD,
                size_hint=(0.9, None),
                height=150,
                text_size=(Window.width * 0.9, None),
                halign='center',
                valign='middle',
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.root.add_widget(completion_msg)

            Clock.schedule_once(lambda dt: self.show_room_selection(), 4)

    def reset_to_room_selection(self, *args):
        """Actually reset and go back to room selection"""
        print("Reset button clicked!")  # Debug
        self.skip_streak = 0
        self.deck = []
        self.current_room = None
        if self.card:
            try:
                self.root.remove_widget(self.card)
            except:
                pass
        if self.instruction_label:
            try:
                self.root.remove_widget(self.instruction_label)
                self.instruction_label = None
            except:
                pass
        if self.log_viewer:
            try:
                self.root.remove_widget(self.log_viewer)
                self.log_viewer = None
            except:
                pass
        if self.skipped_viewer:
            try:
                self.root.remove_widget(self.skipped_viewer)
                self.skipped_viewer = None
            except:
                pass
        self.show_room_selection()

    def on_pause(self):
        if self.bg_music:
            self.bg_music.stop()
        return True

    def on_resume(self):
        if self.bg_music and self.current_room:
            self.bg_music.play()

if __name__ == '__main__':
    PlantsTheGameApp().run()
