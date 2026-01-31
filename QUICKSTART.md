# Quick Start Guide

Get up and running with the Google Home API add-on in 5 minutes!

## Prerequisites

- Home Assistant installed and running
- Google Cloud Platform account
- Google Home devices set up

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

### 5. Configure Add-on

In Home Assistant:

1. Add this repository: `https://github.com/larrifax/ha-google-home`
2. Install "Google Home API" add-on
3. Configure with your credentials:
   ```yaml
   project_id: "your-project-id"
   client_id: "your-client-id.apps.googleusercontent.com"
   client_secret: "your-client-secret"
   refresh_token: "your-refresh-token"
   log_level: "info"
   scan_interval: 30
   ```
4. Start the add-on

## Verify Installation

Check the add-on logs. You should see:
```
[INFO] Starting Google Home API add-on...
[INFO] Configuration validated successfully
[INFO] Google Home API client initialized successfully
[INFO] Home Assistant integration initialized successfully
[INFO] Found X device(s)
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

### "Add-on won't start"
- ✅ Review configuration syntax
- ✅ Check all required fields are filled
- ✅ View logs for specific error messages

## Next Steps

- Read the [full documentation](google_home/DOCS.md)
- Adjust scan interval for your needs
- Enable debug logging if troubleshooting

## Need Help?

- 📚 [Complete Documentation](google_home/DOCS.md)
- 🐛 [Report Issues](https://github.com/larrifax/ha-google-home/issues)
- 💬 [Discussions](https://github.com/larrifax/ha-google-home/discussions)

---

**Time to complete**: ~5 minutes  
**Difficulty**: Intermediate  
**Prerequisites**: Google Cloud account
