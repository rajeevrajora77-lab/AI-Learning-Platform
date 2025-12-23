# Mobile App Deployment Guide

Complete guide for deploying AI Learning Platform to Google Play Store and Apple App Store.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Play Store Deployment](#play-store-deployment)
- [iOS App Store Deployment](#ios-app-store-deployment)
- [Store Listing Requirements](#store-listing-requirements)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Tools
```bash
# Install Flutter
sudo apt-get install flutter

# Or macOS
brew install flutter

# Verify installation
flutter doctor

# Install Android Studio
# Download from: https://developer.android.com/studio

# Install Xcode (macOS only)
sudo xcode-select --install
```

### Development Setup
```bash
# Clone repository
git clone https://github.com/rajeevrajora77-lab/AI-Learning-Platform.git
cd AI-Learning-Platform/mobile/flutter

# Install dependencies
flutter pub get

# Run on emulator/device
flutter run
```

## Play Store Deployment

### Step 1: Register Google Play Developer Account
1. Visit https://play.google.com/console
2. Pay $25 one-time registration fee
3. Complete your developer profile
4. Accept Play Developer Distribution Agreement

### Step 2: Create App on Play Console
1. Click "Create app"
2. Enter app name: "AI Learning Platform"
3. Select "Apps" as category
4. Choose default language: English
5. Accept declarations and continue

### Step 3: Generate Release APK/App Bundle

```bash
# Navigate to flutter directory
cd mobile/flutter

# Create keystore for signing (run once)
keytool -genkey -v -keystore ~/ai_learning_key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias ai_learning_key

# Create key.properties file
cat > android/key.properties << 'EOF'
storePassword=YOUR_STORE_PASSWORD
keyPassword=YOUR_KEY_PASSWORD
keyAlias=ai_learning_key
storeFile=~/ai_learning_key.jks
EOF

# Build release App Bundle (Recommended)
flutter build appbundle --release

# Or build APK
flutter build apk --release
```

### Step 4: Upload to Play Console
1. Go to Release > Production
2. Click "Create new release"
3. Upload `build/app/outputs/bundle/release/app-release.aab`
4. Review app details
5. Save and submit for review

### Step 5: Complete Store Listing
1. App title: "AI Learning Platform"
2. Short description: "Generate educational videos from topics"
3. Full description: (See Store Listing Requirements)
4. Category: "Education"
5. Content rating: Complete questionnaire
6. Target audience: "All"
7. Add screenshots (minimum 2, recommended 5)
8. Add app icon (512x512 PNG)
9. Add feature graphic (1024x500 PNG)
10. Add video preview (optional)

## iOS App Store Deployment

### Step 1: Register Apple Developer Account
1. Visit https://developer.apple.com/account
2. Pay $99 annual membership fee
3. Complete your developer profile
4. Accept Apple Developer Agreement

### Step 2: Create App on App Store Connect
1. Go to https://appstoreconnect.apple.com
2. Click "My Apps"
3. Click "+" > "New App"
4. Select:
   - Platform: "iOS"
   - App Name: "AI Learning Platform"
   - Bundle ID: "com.rajeevrajora.ailearning"
   - SKU: (any unique identifier)
5. Select "Free" pricing
6. Fill required information

### Step 3: Configure Signing & Capabilities
```bash
# Open Xcode project
open ios/Runner.xcworkspace

# Or via command line
flutter build ios --release
```

1. In Xcode:
   - Select Runner > General tab
   - Team: Select your development team
   - Bundle Identifier: com.rajeevrajora.ailearning
   - Version: 1.0.0
   - Build: 1

### Step 4: Build Release Archive
```bash
# Build for iOS
flutter build ios --release

# Open Xcode
open ios/Runner.xcworkspace

# In Xcode:
# 1. Select Generic iOS Device
# 2. Product > Archive
# 3. Wait for completion
# 4. Click "Distribute App"
# 5. Select "App Store Connect"
```

### Step 5: Submit via App Store Connect
1. Go to TestFlight tab
2. Click "+" to add beta version
3. Select your build
4. Add internal tester group
5. Test on TestFlight
6. Go to App Information tab
7. Complete all required fields
8. Submit for review

## Store Listing Requirements

### App Title
"AI Learning Platform" (max 30 characters)

### Short Description (80 characters)
"Generate educational content and creative videos from topics automatically"

### Full Description
```
AI Learning Platform revolutionizes education by automatically generating
comprehensive educational content and creating engaging experimental videos.

Key Features:
✨ Intelligent Content Generation
- Automatic topic research and information gathering
- AI-powered content synthesis using advanced LLMs
- Multi-language support
- Structured text generation

🎬 Creative Video Generation  
- Automated video creation from text
- Text-to-speech voice narration
- Dynamic visual scene generation
- Experimental creative styles

📚 Learning Management
- Topic-based course creation
- Progress tracking
- Content library organization

How It Works:
1. Enter a topic you want to learn about
2. AI gathers comprehensive information
3. Platform generates structured educational content
4. Creative video is automatically produced
5. Watch, learn, and save to your library

Perfect for:
- Students wanting quick learning
- Teachers creating lesson materials
- Content creators and educators
- Anyone interested in AI-powered learning

Requirements:
- Internet connection (for content generation)
- Backend API access
- Storage space for videos

Note: This app requires an active backend server connection.
```

### Screenshots Requirements

#### Android Screenshots
- Size: 1080x1920 pixels
- Format: PNG or JPG
- Required: Minimum 2 screenshots
- Recommended: 5 screenshots showcasing:
  1. Home screen with topic input
  2. Content generation in progress
  3. Generated content view
  4. Video playback
  5. Library/saved content

#### iOS Screenshots  
- Size: 1242x2208 pixels (iPhone 6.5")
- Format: PNG or JPG
- Required: Minimum 2 screenshots
- Same content as Android

### Privacy Policy
```
Privacy Policy

Effective Date: [Current Date]

We respect your privacy. This app:
- Does NOT collect personal data
- Does NOT track user activity
- Uses HTTPS for all communications
- Stores data locally on your device
- Does not share data with third parties

Data Usage:
- Topics are sent to backend for processing
- Generated content is cached locally
- Video files stored in app storage

Third-party Services:
- OpenAI API for content generation
- Google APIs for information gathering

Contact: rajeevrajora77@gmail.com
```

### Terms of Service
```
Terms of Service

Acceptance of Terms:
By using this app, you agree to these terms.

License:
You may use this app for personal, non-commercial purposes.

Limitations:
- No redistribution of content
- No reverse engineering
- No commercial use without permission

Disclaimer:
- App provided "as-is"
- No warranties, express or implied
- User responsible for content accuracy

Liability:
We are not liable for:
- Any damages from app use
- Generated content accuracy
- Data loss
- Third-party API issues

Termination:
We may terminate access for:
- Terms violation
- Abuse or misuse
- Illegal activity

Changes:
We may update these terms anytime.
```

## App Icons & Assets

### Android Icon Requirements
- Base size: 192x192 pixels
- Format: PNG with transparency
- No rounded corners (OS will add)
- Safe area: 66x66 pixels center
- File location: `android/app/src/main/res/`

### iOS Icon Requirements
- Size: 1024x1024 pixels
- Format: PNG without transparency
- No rounded corners or borders
- File location: `ios/Runner/Assets.xcassets/AppIcon.appiconset/`

### Feature Graphic (Android Only)
- Size: 1024x500 pixels
- Format: PNG or JPG
- Content: App name, key features visual

## Configuration Files

### Android Configuration
File: `android/app/build.gradle`
```gradle
android {
    compileSdkVersion 34
    
    defaultConfig {
        applicationId "com.rajeevrajora.ailearning"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"
    }
}
```

### iOS Configuration
File: `ios/Runner/Info.plist`
```xml
<key>CFBundleName</key>
<string>AI Learning Platform</string>
<key>CFBundleShortVersionString</key>
<string>1.0.0</string>
<key>CFBundleVersion</key>
<string>1</string>
<key>NSMinimumOSVersion</key>
<string>12.0</string>
```

## Release Checklist

### Before Building
- [ ] Update version number
- [ ] Update build number
- [ ] Test on real device
- [ ] Run `flutter analyze`
- [ ] Test all features
- [ ] Check internet connectivity handling
- [ ] Verify error messages
- [ ] Test on minimum SDK version

### Before Submission
- [ ] Complete store listing
- [ ] Add all required screenshots
- [ ] Upload privacy policy
- [ ] Upload terms of service
- [ ] Set appropriate content rating
- [ ] Review app description for typos
- [ ] Verify all links work
- [ ] Test submitted build

### After Submission
- [ ] Monitor review progress
- [ ] Respond to any review feedback
- [ ] Monitor app ratings and reviews
- [ ] Track crash reports
- [ ] Plan updates/improvements

## Troubleshooting

### Build Issues
```bash
# Clean build
flutter clean
flutter pub get

# Rebuild
flutter build apk --release

# Check for errors
flutter analyze
```

### Signing Issues
```bash
# Verify keystore
keytool -list -v -keystore ~/ai_learning_key.jks

# Check key.properties
cat android/key.properties
```

### Version Conflicts
```bash
# Update dependencies
flutter pub upgrade

# Get specific version
flutter pub get
```

## Support & Contact

- **Developer Email**: rajeevrajora77@gmail.com
- **GitHub**: https://github.com/rajeevrajora77-lab
- **Repository**: https://github.com/rajeevrajora77-lab/AI-Learning-Platform

## References

- Flutter Documentation: https://flutter.dev/docs
- Google Play Console: https://play.google.com/console
- App Store Connect: https://appstoreconnect.apple.com
- Google Play Policies: https://play.google.com/about/developer-content-policy/
- App Store Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
