# Quick Start Guide

Get up and running with the Google Home API integration in 5 minutes!

This guide covers both installation methods: **HACS Custom Integration (Recommended)** and **Home Assistant Add-on**.

## Prerequisites

- Home Assistant installed and running
- Google Cloud Platform account
- Google Home devices set up

## Installation Method

Choose your preferred installation method:

### Option A: HACS Integration (Recommended)
✅ Works with any Home Assistant installation  
✅ Easy UI-based configuration  
✅ Automatic updates through HACS  

[Jump to HACS Quick Setup](#hacs-quick-setup)

### Option B: Home Assistant Add-on
⚠️ Only for Home Assistant OS/Supervised  
⚠️ Requires YAML configuration  

[Jump to Add-on Quick Setup](#add-on-quick-setup)

---

## Google Cloud Setup (Required for Both Methods)

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Note your Project ID

### 2. Enable Home Graph API

1. In your project, go to "APIs & Services" > "Library"
2. Search for "Home Graph API"
3. Click "Enable"

### 3. Create OAuth2 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client ID"
3. Choose "Web application"
4. Add redirect URI: `http://localhost:8080/callback`
5. Save the Client ID and Client Secret

### 4. Get Refresh Token

Run this Python script to get your refresh token:

```python
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": "YOUR_CLIENT_ID",
            "client_secret": "YOUR_CLIENT_SECRET",
            "redirect_uris": ["http://localhost:8080/callback"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    },
    scopes=['https://www.googleapis.com/auth/homegraph']
)

credentials = flow.run_local_server(port=8080)
print(f"Refresh token: {credentials.refresh_token}")
```

---

## HACS Quick Setup

### 5A. Install via HACS

1. Ensure [HACS](https://hacs.xyz/) is installed
2. Go to **HACS** → **Integrations**
3. Click the three dots (⋮) → **Custom repositories**
4. Add: `https://github.com/larrifax/ha-google-home`
5. Category: **Integration**
6. Click **Add**, then find "Google Home API"
7. Click **Download**
8. **Restart Home Assistant**

### 6A. Configure Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Google Home API"
4. Enter your credentials in the dialog:
   - Google Cloud Project ID
   - OAuth2 Client ID
   - OAuth2 Client Secret
   - OAuth2 Refresh Token
5. Click **Submit**

### 7A. Verify Installation

Check **Settings** → **Devices & Services** → **Google Home API**:
- You should see discovered devices
- Sensor entities should be created for each device

---

## Add-on Quick Setup

### 5B. Install Add-on

1. Go to **Settings** → **Add-ons**
2. Click **Add-on Store** → **⋮** → **Repositories**
3. Add: `https://github.com/larrifax/ha-google-home`
4. Find "Google Home API" and click **Install**

### 6B. Configure Add-on

In the add-on configuration tab:

```yaml
project_id: "your-project-id"
client_id: "your-client-id.apps.googleusercontent.com"
client_secret: "your-client-secret"
refresh_token: "your-refresh-token"
log_level: "info"
scan_interval: 30
```

### 7B. Start Add-on

1. Click **Start**
2. Check logs for success messages

### 8B. Verify Installation

Check the add-on logs. You should see:
```
[INFO] Starting Google Home API add-on...
[INFO] Configuration validated successfully
[INFO] Google Home API client initialized successfully
[INFO] Home Assistant integration initialized successfully
[INFO] Found X device(s)
```

---

## Common Issues

### "Authentication failed" or "Cannot connect"
- ✅ Check your Client ID and Secret
- ✅ Verify refresh token is valid
- ✅ Ensure Home Graph API is enabled
- ✅ Try regenerating the refresh token

### "No devices found"
- ✅ Verify devices are set up in Google Home app
- ✅ Check your Google account has access
- ✅ Ensure correct Project ID
- ✅ Wait a few minutes for initial sync

### "Integration/Add-on won't start"
- ✅ Review configuration syntax (Add-on)
- ✅ Check all required fields are filled
- ✅ View logs for specific error messages
- ✅ Verify Home Graph API is enabled

### "Already configured" error (HACS)
- ✅ Check Settings → Devices & Services
- ✅ Remove existing configuration if needed
- ✅ Try a different Project ID

## Next Steps

- Read the [full documentation](google_home/DOCS.md)
- Configure scan interval in options (HACS) or config (Add-on)
- Set up automations with your devices
- Enable debug logging if troubleshooting

## Need Help?

- 📚 [Complete Documentation](google_home/DOCS.md)
- 🐛 [Report Issues](https://github.com/larrifax/ha-google-home/issues)
- 💬 [Discussions](https://github.com/larrifax/ha-google-home/discussions)

---

**Time to complete**: ~5 minutes  
**Difficulty**: Intermediate  
**Prerequisites**: Google Cloud account
