# Deployment Guide for Breadsheet

This guide covers three ways to deploy and distribute Breadsheet.

## Option 1: Streamlit Cloud (Recommended for Easy Sharing)

Streamlit Cloud is the easiest way to share your app online - no downloads needed for users!

### Steps:

1. **Push code to GitHub** (you've already done this!)

2. **Sign up for Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "Sign in with GitHub"
   - Authorize Streamlit to access your repositories

3. **Deploy your app**
   - Click "New app"
   - Select your repository: `yourusername/breadsheet`
   - Select branch: `main` (or your branch name)
   - Select main file: `app.py`
   - Click "Deploy"

4. **Wait for deployment** (usually 2-3 minutes)
   - Streamlit Cloud will install dependencies
   - Build and launch your app
   - Give you a public URL like: `breadsheet-yourname.streamlit.app`

5. **Share the URL**
   - Send the URL to your friends
   - They can use it directly in their browser
   - No installation required!

### Auto-updates:
- Every time you push to GitHub, the app auto-updates
- Changes go live within a minute
- No need to redeploy manually

### Free Tier Limits:
- 1 GB storage
- Unlimited public apps
- App sleeps after 7 days of inactivity (wakes up instantly when visited)
- Plenty for a baking calculator!

---

## Option 2: GitHub Releases (For Downloadable Executables)

If your friends prefer downloading and running locally, create executables.

### Building Executables:

#### On Windows (for Windows users):
```bash
python build_executable.py
```
Or manually:
```bash
pyinstaller --onefile --windowed --add-data "breadsheet;breadsheet" --name Breadsheet app.py
```

#### On macOS (for Mac users):
```bash
python build_executable.py
```
Or manually:
```bash
pyinstaller --onefile --windowed --add-data "breadsheet:breadsheet" --name Breadsheet app.py
```

#### On Linux (for Linux users):
```bash
python build_executable.py
```
Or manually:
```bash
pyinstaller --onefile --windowed --add-data "breadsheet:breadsheet" --name Breadsheet app.py
```

### Creating a GitHub Release:

1. **Build executables on each platform**
   - Build on Windows for `.exe`
   - Build on macOS for `.app`
   - Build on Linux for Linux binary

2. **Create a release on GitHub**
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Tag version: `v1.0.0`
   - Release title: `Breadsheet v1.0.0`
   - Description: Add release notes

3. **Upload executables**
   - Click "Attach binaries"
   - Upload `Breadsheet.exe` (Windows)
   - Upload `Breadsheet.app` (macOS) - zip it first
   - Upload `Breadsheet` (Linux)
   - Add names like: `breadsheet-v1.0-windows.exe`, `breadsheet-v1.0-macos.zip`, etc.

4. **Publish release**
   - Click "Publish release"
   - Friends can now download from the Releases page

### Note on Executables:
- **Size**: Executables are large (50-150 MB) because they bundle Python
- **Platform-specific**: Must build separately for each OS
- **First-run**: May be slow to start (extracting files)
- **Antivirus**: Some antiviruses flag PyInstaller executables (false positive)

---

## Option 3: Local Installation (For Developers)

For users comfortable with Python:

### Installation:
```bash
# Clone repository
git clone https://github.com/yourusername/breadsheet.git
cd breadsheet

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

---

## Comparison of Options

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Streamlit Cloud** | ✅ No installation<br>✅ Auto-updates<br>✅ Free<br>✅ Works on all devices | ❌ Requires internet<br>❌ Public URL | Non-technical users |
| **GitHub Releases** | ✅ Works offline<br>✅ One-click run<br>✅ No Python needed | ❌ Large file size<br>❌ Platform-specific<br>❌ Manual updates | Desktop users |
| **Local Install** | ✅ Full control<br>✅ Easy development<br>✅ Small size | ❌ Requires Python<br>❌ Technical knowledge needed | Developers |

---

## Recommended Approach

**For non-technical friends**: Use **Streamlit Cloud**
- Send them a URL
- Works on phones, tablets, computers
- Always up-to-date

**For tech-savvy friends**: Provide **both options**
- Streamlit Cloud URL for quick access
- GitHub Release download for offline use

---

## Updating Your App

### Streamlit Cloud:
```bash
git add .
git commit -m "Update feature"
git push
# App updates automatically!
```

### GitHub Releases:
1. Make your changes
2. Commit and push to GitHub
3. Build new executables
4. Create new release (e.g., `v1.1.0`)
5. Upload new executables
6. Notify users to download new version

---

## Troubleshooting

### Streamlit Cloud Issues:

**App won't deploy**:
- Check requirements.txt has all dependencies
- Ensure app.py is in root directory
- Check logs in Streamlit Cloud dashboard

**App is slow**:
- Free tier has limited resources
- App sleeps after inactivity (30 sec wake-up time)

### Executable Issues:

**Antivirus blocking**:
- PyInstaller executables sometimes trigger false positives
- Whitelist the file or sign the executable

**Won't run**:
- Make sure built on correct platform
- Check if user has required system libraries

**Too large**:
- This is normal (50-150 MB)
- Can't be reduced much due to Python bundling

---

## Security Notes

- **Streamlit Cloud**: Code and data are stored on Streamlit's servers
- **Executables**: Run locally, no data sent anywhere
- **Custom conversions**: Saved locally in `custom_conversions.json`
- No telemetry or analytics in this app

---

## Support

If users have issues:
1. Check GitHub Issues page
2. Read README.md
3. Create a new Issue on GitHub

---

Happy Baking! 🍞
