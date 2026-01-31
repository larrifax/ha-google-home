# Quick Start Guide

Get up and running with the Google Home API integration in 5 minutes!

## Prerequisites

- Home Assistant installed and running
- Google Cloud Platform account
- Google Home devices set up
- HACS installed (optional but recommended)

## Quick Setup (5 Steps)

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

### 5. Install and Configure Integration

In Home Assistant:

#### Via HACS (Recommended):
1. Open HACS
2. Go to "Integrations"
3. Click menu (⋮) → "Custom repositories"
4. Add: `https://github.com/larrifax/ha-google-home`
5. Category: "Integration"
6. Search for "Google Home API" and install
7. Restart Home Assistant

#### Manual Installation:
1. Download the latest release
2. Copy `custom_components/google_home/` to your HA config directory
3. Restart Home Assistant

#### Configure:
1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Google Home API"
4. Enter your credentials:
   - Project ID
   - Client ID
   - Client Secret
   - Refresh Token
5. Click "Submit"

## Verify Installation

Check the integration status:
1. Go to Settings → Devices & Services
2. Find "Google Home API" in the list
3. You should see your devices listed

You can also check Home Assistant logs for:
```
[INFO] google_home: Google Home API integration setup complete
[INFO] google_home: Discovered X device(s)
```

## Common Issues

### "Authentication failed"
- ✅ Check your Client ID and Secret
- ✅ Verify refresh token is valid
- ✅ Ensure Home Graph API is enabled

### "No devices found"
- ✅ Verify devices are set up in Google Home app
- ✅ Check your Google account has access
- ✅ Ensure correct Project ID
- ✅ Try reloading the integration

### "Integration won't load"
- ✅ Review Home Assistant logs
- ✅ Check all required fields are filled
- ✅ Verify credentials are correct
- ✅ Restart Home Assistant

## Next Steps

- Read the [full documentation](google_home/DOCS.md)
- Configure additional settings if needed
- Add automations using your devices
- Check for updates via HACS

## Need Help?

- 📚 [Complete Documentation](google_home/DOCS.md)
- 🐛 [Report Issues](https://github.com/larrifax/ha-google-home/issues)
- 💬 [Discussions](https://github.com/larrifax/ha-google-home/discussions)

---

**Time to complete**: ~5 minutes  
**Difficulty**: Intermediate  
**Prerequisites**: Google Cloud account
