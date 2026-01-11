# Plant Tinder - Gamified Plant Care App

A swipe-based mobile application for tracking plant watering with room selection, explosions, and boss levels!

## Features

- **3-Room Selection**: Choose between Kitchen (6 plants), Office (12 plants), or Bedroom (2 plants)
- **Swipe Interface**: Left swipe = Water, Right swipe = Skip
- **Explosion Celebrations**: Every water action triggers particle explosions with sound!
- **Background Music**: Looping background music during gameplay
- **Room-Specific Intros**: Each room plays its own intro sound
- **Boss Level**: Skip 3 plants in a row and face the consequences!
- **48-Hour Nag System**: Get reminded if you haven't watered in 2 days
- **Activity Log**: All actions are logged with timestamps
- **Haptic Feedback**: Vibration on swipes (Android)

## Project Structure

```
Sam_Plants/
├── main.py                 # Main application
├── buildozer.spec          # Android build configuration
├── requirements.txt        # Python dependencies
├── assets/
│   ├── images/            # 19 plant images
│   └── audio/             # 10 audio files
└── README.md              # This file
```

## Required Assets

### Plant Images (19 total)

Copy these to `assets/images/`:

**Bedroom:**
- window.png
- llama_icon.png

**Office:**
- dracaena_f.png
- dracaena_m.png
- pothos.png
- spider_2.png
- philodendron_h.png
- monstera_stand_1.png
- monstera_stand_2.png
- monstera_large.png
- monstera_shelf.png
- philodendron_hang.png
- terrarium.png

**Kitchen:**
- ponytail.png
- zz.png
- spider_1.png
- butt.png
- cactus.png
- hate.png

### Audio Files (10 total)

Copy these to `assets/audio/`:

- **watered.mp3** - Satisfying water sound
- **skipped.mp3** - Skip sound
- **llama.mp3** - Special sound for the llama plant
- **boss.mp3** - Boss level alarm
- **welcome.mp3** - Welcome screen sound
- **background.mp3** - Looping background music
- **kitchen.mp3** - Kitchen room intro
- **office.mp3** - Office room intro
- **bedroom.mp3** - Bedroom room intro
- **explosion.mp3** - Celebration explosion sound

## Setup Instructions

### 1. Copy Your Assets

```bash
# Navigate to the project folder
cd C:\Users\info.DESKTOP-EAL10AV\Documents\Sam_Plants

# Copy your 19 plant images to assets/images/
# Copy your 10 audio files to assets/audio/
```

### 2. Install Dependencies (for local testing)

```bash
pip install -r requirements.txt
```

### 3. Test Locally (Optional)

```bash
python main.py
```

This will run the app in desktop mode using Kivy. You can test:
- Room selection screen
- Plant card swiping
- Audio playback
- Particle explosions

## Android Deployment

### Prerequisites

- Linux or WSL on Windows
- Python 3.10+
- Android SDK/NDK (Buildozer will handle this)
- USB Debugging enabled on Pixel 7

### Build APK

1. Install Buildozer:
```bash
pip install buildozer
```

2. Initialize (first time only):
```bash
buildozer init
```

3. Build the APK:
```bash
buildozer -v android debug
```

This will take 20-30 minutes on first build as it downloads Android SDK/NDK.

4. Deploy to Pixel 7:
```bash
# Connect your Pixel 7 via USB with USB Debugging enabled
buildozer android deploy run
```

## Gameplay Instructions

1. **Launch App**: Welcome screen appears with room selection
2. **Choose Room**: Tap Kitchen, Office, or Bedroom
3. **Swipe Plants**:
   - **Left swipe** = Water (explosion + celebration!)
   - **Right swipe** = Skip
4. **Avoid Boss Level**: Skip 3 plants and face the Boss Level!
5. **Complete Room**: After all plants, return to room selection
6. **Repeat**: Choose another room or play again!

## Controls

- **Left Swipe**: Water plant (triggers explosion!)
- **Right Swipe**: Skip plant
- **Reset Button**: Return to room selection anytime

## Game Mechanics

### Skip Streak & Boss Level
- Skip 3 plants in a row → Boss Level triggered
- Background music stops
- Red screen appears
- Tap to revive and continue

### 48-Hour Nag
- App checks last watering time on launch
- If > 48 hours, displays warning message
- Encourages you to water your plants!

### Explosions
- **Every water action** triggers a particle explosion
- 50 colorful confetti particles
- Explosion sound plays
- Secondary sound (watered.mp3 or llama.mp3)

### Background Music
- Starts when you select a room
- Loops continuously during gameplay
- Stops during Boss Level
- Lower volume (30%) to not overpower other sounds

## Troubleshooting

### Audio Not Playing
- Verify all 10 audio files are in `assets/audio/`
- Check file names match exactly (case-sensitive)
- MP3 format recommended

### Images Not Showing
- Verify all 19 images are in `assets/images/`
- Check file names match exactly
- PNG/JPG formats supported

### Build Errors
- Run `buildozer android clean` to clean build cache
- Check buildozer.spec permissions and requirements
- Verify Android SDK/NDK paths

### App Crashes on Android
- Check `adb logcat` for error messages
- Verify all assets are included in APK
- Test locally first with `python main.py`

## File Locations (Android)

- **Log File**: `<app_user_data_dir>/plant_history.log`
- **State File**: `<app_user_data_dir>/app_state.json`

Use `adb` to access:
```bash
adb shell
cd /sdcard/Android/data/com.sampleplants.planttinder/files/
```

## Performance Notes

- **Particle Count**: Reduced to 50 (from 100) for mobile performance
- **Target**: 60 FPS on Pixel 7
- **Memory**: < 100MB
- **Cold Start**: < 2 seconds

## Future Enhancements

- Statistics dashboard
- Calendar view of watering history
- Custom plant photos
- System notifications at 48-hour mark
- Cloud sync for backup
- Dark mode support

## License

Personal use only.

## Credits

Built with Kivy for Android deployment on Pixel 7.

---

**Happy Plant Watering! 🌱💧**
# Test trigger
