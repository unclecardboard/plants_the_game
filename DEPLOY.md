# Quick Deployment Guide

## Step 1: Create GitHub Repository (2 minutes)

1. Go to https://github.com/new
2. Repository name: `plants-the-game` (or any name you like)
3. Set to **Private** (recommended, since it has personal plant photos)
4. Click "Create repository"

## Step 2: Push Code to GitHub (1 minute)

Open Git Bash or Command Prompt in this folder and run:

```bash
cd "C:\Users\info.DESKTOP-EAL10AV\OneDrive\Documents\Sam_Plants"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Plants the Game app"

# Link to your GitHub repo (REPLACE 'YOUR-USERNAME' with your actual GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/plants-the-game.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Wait for Build (~30 minutes)

1. Go to your GitHub repository
2. Click the **"Actions"** tab at the top
3. You'll see a workflow running called "Build Android APK"
4. Wait for it to complete (green checkmark ✓)

## Step 4: Download the APK

1. Once the build completes, click on the completed workflow
2. Scroll down to **"Artifacts"**
3. Download **"plants-the-game-apk"**
4. Extract the ZIP file - you'll find the APK inside

## Step 5: Install on Pixel 7

**Option A: USB Transfer**
1. Connect Pixel 7 via USB
2. Copy the APK to the phone
3. On the phone, use a file manager to open the APK
4. Allow installation from unknown sources if prompted
5. Install and launch!

**Option B: Direct Download**
1. Upload the APK to Google Drive
2. On Pixel 7, download from Google Drive
3. Open the downloaded APK to install

## Troubleshooting

### Build Fails
- Check the Actions log for errors
- Common issue: buildozer.spec might need adjustments
- The workflow will show exactly where it failed

### APK Won't Install
- Enable "Install unknown apps" for your file manager
- Settings > Apps > Special app access > Install unknown apps

### Need to Rebuild
Just make any change to the code and push again:
```bash
git add .
git commit -m "Update app"
git push
```

The APK will rebuild automatically!

---

**First time using git?**
- Install Git for Windows: https://git-scm.com/download/win
- You'll be prompted for GitHub credentials when pushing
