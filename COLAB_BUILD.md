# Build Your APK with Google Colab (Fastest Method!)

GitHub Actions is stuck, so let's use Google Colab instead. This is actually faster and more reliable!

## Step 1: Open the Notebook in Colab (30 seconds)

Click this link to open the notebook directly in Google Colab:

🔗 **https://colab.research.google.com/github/unclecardboard/plants_the_game/blob/main/Build_APK_Colab.ipynb**

(You'll need to sign in with a Google account)

## Step 2: Run the Build (1 click)

1. In Colab, click **Runtime** → **Run all**
2. If prompted about "not authored by Google", click **Run anyway**
3. Wait ~30-35 minutes for the build to complete

## Step 3: Download Your APK

1. Look for the **Files** folder icon on the left sidebar (📁)
2. Navigate to `plants_the_game/bin/`
3. You'll see a file like `planttinder-1.0.0-arm64-v8a-debug.apk`
4. Right-click it → **Download**

## Step 4: Install on Pixel 7

1. Copy the APK to your Pixel 7 (USB cable or Google Drive)
2. On the phone, open the APK file
3. Allow "Install from unknown sources" if prompted
4. Install and launch!

---

## What the Notebook Does

The notebook automatically:
- ✅ Installs all required dependencies
- ✅ Clones your GitHub repository
- ✅ Downloads Android SDK/NDK
- ✅ Builds the APK with all 20 plant images + 10 audio files
- ✅ Creates a ready-to-install APK

---

## Troubleshooting

**Build fails?**
- Make sure you ran all cells (Runtime → Run all)
- Check the error message and let me know

**APK not appearing?**
- Refresh the Files panel
- Check the `bin` folder specifically

**Can't find Files panel?**
- Click the folder icon (📁) on the left edge of Colab

---

## Why Colab Instead of GitHub Actions?

- ✅ More reliable (no queue delays)
- ✅ Free to use
- ✅ Can see build progress in real-time
- ✅ Easy to download result

You can rebuild anytime by just clicking "Run all" again!

---

**Ready?** Click the link above to start building! 🚀
