# 📱 Mobile Privacy & Security Configuration Guide

> **Last Updated: December 2025**  
> **Compatible Systems: iOS 18+, Android 14+, HarmonyOS 5, MagicOS 8, HyperOS 2**  
> **Setup Time: 5-10 minutes**  
> **No Jailbreak/Root Required**

---

## 📋 Table of Contents

- [I. Configuration Goals](#i-configuration-goals)
- [II. iOS Configuration Guide](#ii-ios-configuration-guide)
- [III. Android Stock/AOSP Configuration Guide](#iii-android-stockaosp-configuration-guide)
- [IV. Huawei/HarmonyOS Configuration Guide](#iv-huaweiharmonyos-configuration-guide)
- [V. Honor/MagicOS Configuration Guide](#v-honormagicos-configuration-guide)
- [VI. Xiaomi/HyperOS Configuration Guide](#vi-xiaomihyperos-configuration-guide)
- [VII. General Security Recommendations](#vii-general-security-recommendations)
- [VIII. Frequently Asked Questions](#viii-frequently-asked-questions)

---

## I. Configuration Goals

This guide uses native system settings (no third-party tools required) to achieve three main objectives:

### 🔒 **Goal 1: Set Strong Lock Screen**
- Use PIN (≥6 digits) as the first line of defense
- Avoid weak passwords like birthdays or phone numbers

### 🚫 **Goal 2: Disable Sensitive Data Collection**
- Disable system analytics, telemetry, and crash log uploads
- Turn off advertising identifiers
- Stop personalized ad tracking

### 🔐 **Goal 3: Encrypt Network Functions**
- Use encrypted DNS (DoH) to prevent hijacking and tracking
- Keep keyboard clipboard data local (no cloud sync)
- Use open-source/encrypted communication tools

---

## II. iOS Configuration Guide

### Compatible Devices
iPhone 12 and above (iOS 17+)

### Configuration Checklist

| # | Item | Path | Steps | Verification |
|---|------|------|-------|--------------|
| 1 | **Set PIN Lock** | Settings → Face ID & Passcode → Change Passcode | 1. Tap "Passcode Options"<br>2. Choose "Custom Numeric Code"<br>3. Enter ≥6 digits (avoid sequential numbers) | Lock screen shows only numeric keypad |
| 2 | **Disable Analytics** | Settings → Privacy & Security → Analytics & Improvements | Turn off all options:<br>- Share iPhone Analytics<br>- Share iCloud Analytics<br>- Improve Siri & Dictation<br>- Share Routing & Network Analytics | Enter "Analytics Data" - no new logs |
| 3 | **Disable Ad Tracking** | Settings → Privacy & Security → Tracking | Turn off "Allow Apps to Request to Track" | Toggle grayed out, apps no longer show tracking prompts |
| 4 | **Configure Encrypted DNS** | Settings → General → VPN & Device Management | **Option 1: Profile (Recommended)**<br>1. Visit in Safari: https://adguard-dns.io/kb/en/ios/solving-problems/configuration-profile/<br>2. Download "Default" profile<br>3. Install in Settings<br><br>**Option 2: 18bit DNS (China-based, Ad Blocking)**<br>1. Visit in Safari: https://go.18bit.cn/help-docs/help-docs-ios.html<br>2. Download 18bit DNS profile<br>3. Install in Settings<br>4. Auto-enabled after installation<br><br>**Option 3: App Method**<br>Download "AdGuard" or "DNSCloak" | **AdGuard Verification:**<br>Visit https://dns.adguard.com/info<br>Shows "DNS Protection: Yes"<br><br>**18bit Verification:**<br>Visit https://dtest.18bit.cn/<br>Red screen shows "18bit Blocked" |
| 5 | **Localize Keyboard** | Settings → General → Keyboard → Keyboards | 1. Keep only "Simplified Chinese - Pinyin" or use Gboard<br>2. If using Gboard, disable in settings:<br>- Cloud clipboard<br>- Input predictions<br>- Auto-learning | Copy sensitive content, paste after 5 min<br>Should show "Clipboard cleared" |
| 6 | **Limit Location Tracking** | Settings → Privacy & Security → Location Services | 1. Review app permissions individually<br>2. Change to "While Using" or "Never"<br>3. Disable "Precise Location" | Location icon no longer appears frequently in status bar |
| 7 | **Disable Background Refresh** | Settings → General → Background App Refresh | Disable background refresh for rarely-used apps | Battery life improves |

### ⚠️ iOS Special Notes

- **iCloud Backup**: Backs up all app data. Disable iCloud backup for sensitive apps (banking, messaging)
- **Siri Suggestions**: Settings → Siri & Search, disable "Learn from this App" for sensitive apps individually
- **Photo Privacy**: Use "Hidden Album" and disable "Show Hidden Album" in Photos settings

---

## III. Android Stock/AOSP Configuration Guide

### Compatible Devices
Pixel, Stock Android, OnePlus OxygenOS, Nothing OS, etc.

### Configuration Checklist

| # | Item | Path | Steps | Verification |
|---|------|------|-------|--------------|
| 1 | **Set PIN Lock** | Settings → Security → Screen Lock → PIN | Enter ≥6 digits (avoid sequential numbers) | Lock screen shows only numeric keypad |
| 2 | **Disable Telemetry** | Settings → Google → Usage & Diagnostics | Turn off "Send usage and diagnostics data" | Search "usage" in settings shows "Disabled" |
| 3 | **Delete Ad ID** | Settings → Google → Ads | Tap "Delete advertising ID"<br>(Android 12+)<br>or disable "Personalized ads" | Shows "Advertising ID deleted" |
| 4 | **Configure Private DNS** | Settings → Network & Internet → Private DNS | Select "Private DNS provider hostname"<br><br>**Recommended Options:**<br>- **18bit DNS** (China, ad blocking): `dns.18bit.cn`<br>- **AdGuard DNS** (International, ad blocking): `dns.adguard-dns.com`<br>- **Alibaba DNS** (China, no blocking): `dns.alidns.com`<br>- **Cloudflare** (International, no blocking): `1dot1dot1dot1.cloudflare-dns.com` | Status shows "Connected"<br><br>**18bit Verification:**<br>Visit https://dtest.18bit.cn/<br>Red screen shows success<br><br>**AdGuard Verification:**<br>Visit https://dns.adguard.com<br>Shows "DNS Protection: Yes" |
| 5 | **Localize Keyboard** | Settings → System → Languages & Input → Gboard | Enter Gboard settings:<br>- Disable "Clipboard cloud sync"<br>- Disable "Personal dictionary cloud sync"<br>- Disable "Share usage statistics" | Copy password, switch apps<br>Long press paste shows no history |
| 6 | **Review Permissions** | Settings → Privacy → Permission Manager | Check individually:<br>- Location (change to "Only while using")<br>- Camera/Microphone (disable unnecessary apps)<br>- Contacts (keep only necessary apps) | Permission icons no longer appear frequently in status bar |
| 7 | **Limit Background Activity** | Settings → Apps → Special App Access → Unrestricted Data Usage | Keep only necessary communication apps | Data usage decreases |

---

## IV. Huawei/HarmonyOS Configuration Guide

### Compatible Devices
Mate 60 series, Pura 70 series, Mate X5, nova series, etc. (HarmonyOS 4.0+)

### Configuration Checklist

| # | Item | Path | Steps | Verification |
|---|------|------|-------|--------------|
| 1 | **Set PIN Lock** | Settings → Biometrics & Password → Lock Screen Password | Choose "PIN"<br>Enter ≥6 digits (disable "Simple password") | Lock screen shows only numeric keypad |
| 2 | **Disable Experience Program** | Settings → Huawei Account → Privacy Center → Experience Improvement | Turn off all options:<br>- User Experience Improvement Program<br>- Crash log upload<br>- Diagnostic data | Page shows "Disabled" |
| 3 | **Delete Ad Identifier** | Settings → Huawei Account → Privacy Center → Ads & Privacy | Tap "Delete advertising identifier" | Shows "Advertising identifier disabled" |
| 4 | **Disable System Telemetry** | Settings → System & Updates → User Experience Improvement Program | Turn off "Join User Experience Improvement Program" | Search "experience improvement" shows disabled |
| 5 | **Configure Encrypted DNS** | Settings → More Connections → Encrypted DNS | Select "Manual"<br><br>**Recommended:**<br>- `dns.18bit.cn` (China, ad blocking)<br>- `dns.adguard-dns.com` (International, ad blocking)<br>- `dns.alidns.com` (China, no blocking) | Status shows "Connected"<br><br>Verify: Visit https://dtest.18bit.cn/<br>Red screen shows success |
| 6 | **App Lock + Background Blur** | Phone Manager → Privacy Center → App Lock | 1. Lock sensitive apps like WeChat, email<br>2. Enable "Background blur preview" | Recent tasks show blurred content |
| 7 | **PrivateSpace (Optional)** | Settings → Privacy → PrivateSpace | Create independent fingerprint/password | File Manager shows "PrivateSpace" entry at bottom |
| 8 | **Pure Mode** | Settings → System & Updates → Pure Mode | Keep enabled (default) | Can only install apps from AppGallery and official channels |

### 🔍 Huawei Quick Checklist

Use Settings search bar, search these keywords to ensure all are disabled:
- ✅ "Experience improvement" → All toggles off
- ✅ "Ads" → Advertising identifier deleted
- ✅ "Diagnostic" → All diagnostic toggles off
- ✅ "Cloud" → Check if sensitive data cloud sync is disabled

---

## V. Honor/MagicOS Configuration Guide

### Compatible Devices
Magic V3/V5, Magic6 series, Magic7 series, etc. (MagicOS 8.0+)

### Configuration Checklist

| # | Item | Path | Steps | Verification |
|---|------|------|-------|--------------|
| 1 | **Set PIN Lock** | Settings → Biometrics & Password → Lock Screen Password | Choose "PIN"<br>Enter ≥6 digits (disable "Simple password") | Lock screen shows only numeric keypad |
| 2 | **Disable Experience Program** | Settings → Honor Account → Privacy Center → Experience Improvement | Turn off "Join Experience Improvement Program" | Page shows "Disabled" |
| 3 | **Delete Ad ID** | Settings → Honor Account → Privacy Center → Ads | Tap "Delete advertising identifier" | Shows "Advertising ID disabled" |
| 4 | **Disable Remote Diagnostics** | Settings → System & Updates → Honor Remote Diagnostics | Turn off "Allow remote log collection" | Search "remote diagnostics" shows disabled |
| 5 | **Configure Encrypted DNS** | Settings → More Connections → Encrypted DNS | Select "Manual"<br><br>**Recommended:**<br>- `dns.18bit.cn` (China, ad blocking)<br>- `dns.adguard-dns.com` (International, ad blocking)<br>- `dns.alidns.com` (China, no blocking) | Status shows "Connected"<br><br>Verify: Visit https://dtest.18bit.cn/<br>Red screen shows success |
| 6 | **App Lock** | Phone Manager → App Lock | 1. Lock sensitive apps<br>2. Enable "Background blur" | Recent tasks show blurred content |
| 7 | **On-Device AI (Magic V3/V5)** | Settings → Privacy → On-Device AI | Choose "Local processing only"<br>Turn off "Cloud enhancement" | Knowledge base page shows "Pure on-device mode" |

### 🔍 Honor Quick Checklist

Settings search bar, search sequentially:
- ✅ "Experience improvement" → Disabled
- ✅ "Ads" → ID deleted
- ✅ "Remote diagnostics" → Disabled
- ✅ "Cloud" → Check sync items

---

## VI. Xiaomi/HyperOS Configuration Guide

### Compatible Devices
Xiaomi 14 series, Redmi K70 series, Xiaomi 15 series, etc. (HyperOS 1.0+)

### Configuration Checklist

| # | Item | Path | Steps | Verification |
|---|------|------|-------|--------------|
| 1 | **Set PIN Lock** | Settings → Password & Security → Lock Screen Password | Choose "PIN"<br>Enter ≥6 digits (disable "Simple password") | Lock screen shows only numeric keypad |
| 2 | **Disable Experience Program** | Settings → Password & Security → System Security → User Experience Program | Turn off "Join User Experience Program" | Toggle grayed out |
| 3 | **Delete Ad ID** | Settings → Password & Security → System Security → Ad Services | Tap "Delete advertising ID" | Shows "Advertising identifier disabled" |
| 4 | **Disable Diagnostic Data** | Settings → Password & Security → System Security → Diagnostic Data | Turn off "Send diagnostic data" | Search "diagnostic data" shows disabled |
| 5 | **Disable Personalized Ads** | Settings → Accounts & Sync → Mi Account → Privacy → Ad Preferences | Turn off "Personalized ads" | Page shows "Disabled" |
| 6 | **Configure Private DNS** | Settings → Connection & Sharing → Private DNS | Select "Manual"<br><br>**Recommended:**<br>- `dns.18bit.cn` (China, ad blocking)<br>- `dns.adguard-dns.com` (International, ad blocking)<br>- `dns.alidns.com` (China, no blocking) | Status shows "Connected"<br><br>Verify: Visit https://dtest.18bit.cn/<br>Red screen shows success |
| 7 | **App Lock + Blur Snapshot** | Settings → App Settings → App Lock | 1. Lock sensitive apps<br>2. Enable "Blur snapshot" | Recent tasks show blurred content |
| 8 | **Disable MIUI Recommendations** | Settings → Search "recommendations" | Turn off all "Content recommendations" options | Negative screen no longer shows ads |

### 🔍 Xiaomi Quick Checklist

Settings search bar, search sequentially:
- ✅ "Experience program" → Disabled
- ✅ "Ads" → ID deleted + personalized disabled
- ✅ "Diagnostic data" → Disabled
- ✅ "Recommendations" → All content recommendations disabled

---

## VII. General Security Recommendations

### 🔄 Regular Maintenance (Quarterly)

1. **Recheck Toggle Status**  
   Search in Settings for these keywords to ensure they haven't been silently re-enabled:
   - "Experience improvement"
   - "Diagnostic data" / "usage"
   - "Advertising ID" / "ads"

2. **Clear Cache & Logs**  
   - Android: Settings → Storage → Cached Data → Clear
   - iOS: Settings → General → iPhone Storage → Clear "Other"

3. **Check Permission Changes**  
   Review new permission requests in "Permission Manager"

### 📶 Public Wi-Fi Protection

1. **Ensure Encrypted DNS is Enabled** (Steps 4/5 above)
2. **Avoid Sensitive Operations**: No banking, password changes, etc.
3. **Use HTTPS**: Check URL prefix is `https://`
4. **Optional: Use VPN**  
   Recommended open-source solutions:
   - iOS: WireGuard, Shadowrocket
   - Android: WireGuard, v2rayNG
   - ⚠️ Avoid free Chinese accelerators (may log data)

### 🔍 DNS Tools Recommended

| Tool | Function | Link |
|------|----------|------|
| **18bit DNS Test** | Check if 18bit DNS is active | https://dtest.18bit.cn/ |
| **AdGuard DNS Test** | Check if AdGuard DNS is active | https://dns.adguard.com/info |
| **DNS Leak Test** | Check if DNS leaks real IP | https://www.dnsleaktest.com/ |
| **18bit Service Status** | View 18bit DNS real-time status | https://status.18bit.cn/ |

### 📱 Keyboard & Clipboard

| Platform | Recommended Solution | Configuration |
|----------|---------------------|---------------|
| iOS | System default / Gboard | Gboard needs "Cloud clipboard" disabled |
| Android | Gboard / System default | Disable "Cloud sync" and "Statistics" |
| Chinese ROMs | System default | Avoid third-party input methods |

**Security Tips:**
- After copying passwords/codes, system auto-clears in 5 minutes
- Don't use Sogou, Baidu, or other internet-connected third-party keyboards

### 🔒 App Security Recommendations

| App Type | Recommendation |
|----------|---------------|
| Messaging (WeChat/QQ) | Enable app lock + hide notification content |
| Financial (Banking/Payment) | Enable app lock + disable cloud backup |
| Notes | Use local notes (Apple Notes/Google Keep)<br>or E2E encrypted notes (Notion/Obsidian) |
| Email | Disable auto-load images (prevent tracking pixels) |
| Browser | Use Safari (iOS)/Chrome (Android)<br>Enable "Prevent cross-site tracking" |

### 🛡️ System Updates

| Platform | Update Recommendation | Notes |
|----------|----------------------|-------|
| iOS | Keep auto-update enabled | Apple responds quickly to security issues, safe to upgrade |
| Android Stock | Keep auto-update enabled | Google pushes security patches first week of each month |
| Huawei/Honor/Xiaomi | Only install "Security patches" | Wait 1-2 weeks before major version updates to avoid issues |

**⚠️ Important:** System security patches won't re-enable privacy toggles, safe to upgrade

---

## VIII. Frequently Asked Questions

### ❓ Some Apps Don't Work After DNS Configuration?

**Cause:** DNS with ad blocking (18bit, AdGuard) blocks some ads and tracking domains. Some apps require ads to function.

**Solutions:**
1. **Temporary:** Disable encrypted DNS, re-enable after using the app
2. **Permanent:** Switch to non-blocking DNS
   - Alibaba DNS (China, no blocking): `dns.alidns.com`
   - Cloudflare (International, malware blocking only): `1dot1dot1dot1.cloudflare-dns.com`

### ❓ 18bit DNS vs AdGuard DNS - Which to Choose?

| Comparison | 18bit DNS | AdGuard DNS |
|------------|-----------|-------------|
| **Server Location** | 🇨🇳 China Mainland | 🌍 Overseas (Singapore, USA, etc.) |
| **China Speed** | ✅ Fast (latency <20ms) | ⚠️ Average (latency 50-100ms) |
| **Ad Blocking** | ✅ Optimized for Chinese ads | ✅ Optimized for international ads |
| **Privacy Policy** | 🔍 Check official website | ✅ Open source, has audit reports |
| **Stability** | ⚠️ Occasional attacks | ✅ High |
| **Use Case** | Chinese users daily use | Privacy-focused or frequent international app users |

**Recommended Choice:**
- 🏠 China users priority: `dns.18bit.cn` (fast, blocks Chinese ads)
- 🌏 Privacy priority/overseas apps: `dns.adguard-dns.com` (open source transparent)
- ⚡ Stability priority (no ad blocking): `dns.alidns.com` (Alibaba Public DNS)

### ❓ Forgot PIN Password?

| Platform | Solution |
|----------|----------|
| iOS | Need to restore device via iTunes/Finder (data will be lost)<br>If "Find My iPhone" is enabled, can remotely erase |
| Android | After multiple wrong attempts, can unlock with Google account<br>or restore factory settings via Recovery (data loss) |
| Chinese ROMs | Most can recover via brand account<br>or use "Forgot password" (need pre-bind) |

**💡 Suggestion:** Use password manager (1Password/Bitwarden) to backup PIN

### ❓ Will I Still See Ads After Disabling Ad ID?

**Yes, but ads won't be personalized.**

- Before: Apps push targeted ads based on browsing history, location, purchase records
- After: Apps can only push generic ads (all users see same ads)

**Key Difference:** Protects privacy, doesn't completely remove ads (ad removal requires encrypted DNS)

### ❓ Should I Enable "Pure Mode" on Huawei/Honor/Xiaomi?

| Mode | Pros | Cons | Recommendation |
|------|------|------|----------------|
| Pure Mode | Only install apps from official channels<br>Blocks malware | Can't install third-party APKs<br>(e.g., GitHub open-source apps) | ✅ Regular users keep enabled<br>❌ Developers/geeks can disable |

### ❓ Android 9 and Below - How to Use Encrypted DNS?

Android 9 and below don't natively support Private DNS, need third-party app:

**Recommended App: Intra (Google developed)**

1. **Download & Install:** Search "Intra" on Google Play or APKMirror
2. **Configure 18bit DNS:**
   - Open Intra → Settings → Choose "Custom server URL"
   - Enter: `https://doh.18bit.cn/dns-query`
   - Return to home, enable protection
3. **Verify:** Visit https://dtest.18bit.cn/ shows red

**Note:** Intra uses VPN channel for DoH, may conflict with other VPNs

### ❓ Will Phone Slow Down After Configuration?

**No, may actually be smoother.**

- Disabling telemetry and ad tracking reduces background network requests
- Disabling background refresh lowers power consumption
- Encrypted DNS doesn't affect speed (latency difference <10ms)

---

## 📚 Further Reading

### Official Privacy Documentation
- [Apple Privacy Whitepaper](https://www.apple.com/privacy/docs/iOS_Privacy_Overview.pdf)
- [Google Android Privacy Center](https://safety.google/android/)
- [Huawei Privacy Protection Whitepaper](https://consumer.huawei.com/cn/privacy/)

### DNS Related Resources
- [18bit DNS Official Website](https://18bit.cn/)
- [AdGuard DNS Knowledge Base](https://adguard-dns.io/kb/en/)
- [Cloudflare 1.1.1.1](https://1.1.1.1/)
- [Alibaba Public DNS](https://www.alidns.com/)

### Recommended Tools
- **Password Managers:** 1Password, Bitwarden, KeePassXC
- **Open-Source Browsers:** Firefox, Brave (built-in ad blocking)
- **Encrypted Messaging:** Signal (end-to-end encrypted SMS)

### Related Projects
- [DNSCrypt Protocol](https://dnscrypt.info/)
- [Privacy Guides](https://www.privacyguides.org/)

---

## 📝 Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2025-12 | v1.0 | Initial release, supports iOS 18, Android 14, HarmonyOS 5, MagicOS 8, HyperOS 2 |

---

## 📧 Feedback & Suggestions

If you encounter any of the following, feel free to submit an Issue or Pull Request:

- ✅ System updates causing menu path changes
- ✅ New privacy leak points discovered
- ✅ Better configuration solutions

---

**⚠️ Disclaimer**  
This guide is for educational reference only. The author is not responsible for any issues arising from configuration. Please backup important data before configuration.

**📌 Final Reminder**  
Privacy protection is an ongoing process, not a one-time setup. Recommend quarterly reviews and stay informed about system update notes.

---

<div align="center">

**If this guide helps you, please give it a ⭐ Star!**

[中文版本](手机隐私安全配置指南.md) | English

</div>

