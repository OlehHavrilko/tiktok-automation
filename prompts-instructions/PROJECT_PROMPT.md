# TikTok Project - Prompt & Instructions

## Project Overview
This project is designed for TikTok-related automation, content creation, and management tasks.

## Available Skills & Tools

### TikTok-Related Skills
- **tiktok-automation**: Automate TikTok tasks via Rube MCP (Composio) - upload/publish videos, post photos, manage content, view user profiles/stats
- **tiktok-captions**: Create TikTok video captions, scripts, optimize for TikTok (hashtags, copy, marketing)
- **tiktok-marketing**: TikTok content strategy, video creation workflows, posting optimization, and analytics
- **tiktok-scraper**: Scrape TikTok videos, profiles, hashtags, music, comments, or location-based posts
- **tiktok-ads**: Set up, optimize, or manage TikTok Ads (Pixel, Events API, Spark Ads, video ads)
- **tiktok-research**: Research TikTok trends and content

### Media & Content Skills
- **youtube-search**: Search YouTube for videos and channels, fetch transcripts
- **youtube-clipper**: Create clips from YouTube videos
- **videoagent-video-studio**: Video editing and production
- **media-downloader**: Download media content

### Marketing & Research
- **social-media-trends-research**: Programmatic social media research using pytrends, yars (Reddit), Perplexity MCP (Twitter/TikTok/Web)
- **telegram-bot-builder**: Build Telegram bots
- **telegram-mini-app**: Build Telegram Mini Apps with TON blockchain

## Configuration

### Rclone Google Drive
Remote name: `gdrive`
- Configured with OAuth credentials
- Location: `/root/.config/rclone/rclone.conf`

### Authentication Required
Run to complete Google Drive setup:
```bash
rclone authorize "drive" "<CLIENT_ID>" "<CLIENT_SECRET>"
```

## Project Structure
```
/root/tiktokproject/
├── prompts-instructions/     # Documentation and configurations
│   ├── PROJECT_PROMPT.md     # This file
│   ├── QWEN.md               # Agent memories
│   ├── output-language.md    # Language rules
│   ├── settings.json         # Qwen settings
│   └── oauth_creds.json      # OAuth credentials (sensitive)
└── ...                       # Project files
```

## Usage Examples

### TikTok Content Creation
```
1. Research trends with social-media-trends-research
2. Create captions with tiktok-captions
3. Upload/manage with tiktok-automation
```

### Video Workflow
```
1. Search content with youtube-search
2. Create clips with youtube-clipper
3. Edit with videoagent-video-studio
4. Upload to TikTok
```

### Storage
```bash
# Upload to Google Drive
rclone copy /path/to/files gdrive:/folder

# Sync directory
rclone sync /local/path gdrive:/remote/path
```

## Language Rules
- All responses MUST be in English (unless explicitly requested otherwise)
- Technical artifacts (code, paths, logs) remain unchanged
