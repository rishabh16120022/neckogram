#!/usr/bin/env python3
"""
NickoGram Automated Patch Engine
Applies custom branding, DM Protection settings, English UI strings,
and new launcher icons onto the Telegram Android / AyuGram4A base.
"""

import os
import shutil
import re

BASE_DIR = os.path.abspath(".")
ART_DIR = os.path.join(BASE_DIR, "art")
TMESSAGES_DIR = os.path.join(BASE_DIR, "TMessagesProj")
RES_DIR = os.path.join(TMESSAGES_DIR, "src", "main", "res")
STRINGS_FILE = os.path.join(RES_DIR, "values", "strings.xml")

DM_PROTECTION_STRINGS = """
    <!-- NickoGram: DM Protection & Security Firewall -->
    <string name="NickoGramDMProtection">DM Protection</string>
    <string name="NickoGramDMProtectionSummary">Firewall incoming private messages, drop spammers, and secure calls</string>

    <string name="NickoGramStrictDMLockdown">Strict DM Lockdown (Drop Incoming DMs)</string>
    <string name="NickoGramStrictDMLockdownSummary">Completely disable direct messages from non-contacts. Senders immediately get a red 'Failed to send' error.</string>

    <string name="NickoGramInstantSpamStrike">Instant Spam Strike &amp; Auto-Report</string>
    <string name="NickoGramInstantSpamStrikeSummary">Automatically submit official spam reports with evidence to Telegram and block spammers to trigger immediate account limitations.</string>

    <string name="NickoGramQuarantineUnknown">Quarantine Unknown Senders</string>
    <string name="NickoGramQuarantineUnknownSummary">Route messages from non-contacts to a separate 'Requests' folder without notifications.</string>

    <string name="NickoGramAntiFlood">Anti-Flood &amp; Raid Protection</string>
    <string name="NickoGramAntiFloodSummary">Automatically silence spammers sending more than 5 messages within 3 seconds.</string>

    <string name="NickoGramP2PShield">Peer-to-Peer (P2P) Call Shield</string>
    <string name="NickoGramP2PShieldSummary">Disable direct P2P connections during voice and video calls to prevent IP address discovery.</string>

    <string name="NickoGramPhishingScanner">Phishing Link Scanner</string>
    <string name="NickoGramPhishingScannerSummary">Highlight suspicious domains and deceptive login links with prominent warning alerts.</string>

    <string name="NickoGramBlockUntrustedAPK">Block Untrusted APK Downloads</string>
    <string name="NickoGramBlockUntrustedAPKSummary">Prevent one-tap downloading of executable application files sent by unknown accounts.</string>

    <string name="NickoGramRestrictForwarding">Restrict Forwarding Outgoing Messages</string>
    <string name="NickoGramRestrictForwardingSummary">Disallow recipients from copying or forwarding your private messages to other chats.</string>

    <string name="NickoGramBlockScreenshots">Block Screenshots in Private Chats</string>
    <string name="NickoGramBlockScreenshotsSummary">Prohibit screenshots and screen recording inside direct conversations.</string>

    <string name="NickoGramHiddenVault">Hidden Chat Vault</string>
    <string name="NickoGramHiddenVaultSummary">Conceal selected conversations from the main chat list.</string>

    <string name="NickoGramShakeToHide">Shake Device to Hide Chats</string>
    <string name="NickoGramShakeToHideSummary">Instantly lock and hide all vaulted chats by shaking your phone.</string>

    <!-- NickoGram: Phantom Voice Chat -->
    <string name="NickoGramPhantomVoice">Phantom Voice Chat (Invisible Mode)</string>
    <string name="NickoGramPhantomVoiceSummary">Listen and speak in voice chats while completely omitted from the participant roster.</string>
"""

def patch_strings():
    if not os.path.exists(STRINGS_FILE):
        print(f"Strings file not found at {STRINGS_FILE}, skipping string patches.")
        return

    with open(STRINGS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace App Names
    content = re.sub(
        r'<string name="AppName">[^<]+</string>',
        '<string name="AppName">NickoGram</string>',
        content
    )
    content = re.sub(
        r'<string name="AppNameBeta">[^<]+</string>',
        '<string name="AppNameBeta">NickoGram</string>',
        content
    )

    # Inject DM Protection strings before </resources>
    if "NickoGramDMProtection" not in content:
        content = content.replace("</resources>", f"{DM_PROTECTION_STRINGS}\n</resources>")
        print("Injected NickoGram DM Protection English strings successfully.")

    with open(STRINGS_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("Updated AppName to NickoGram in strings.xml.")

def copy_icons():
    if not os.path.exists(ART_DIR):
        print("Art directory not found, skipping icon copy.")
        return

    for folder in os.listdir(ART_DIR):
        src_folder = os.path.join(ART_DIR, folder)
        if os.path.isdir(src_folder) and folder.startswith("mipmap-"):
            dst_folder = os.path.join(RES_DIR, folder)
            os.makedirs(dst_folder, exist_ok=True)
            for icon_name in ["ic_launcher.png", "ic_launcher_round.png"]:
                src_icon = os.path.join(src_folder, icon_name)
                if os.path.exists(src_icon):
                    shutil.copy2(src_icon, os.path.join(dst_folder, icon_name))
                    print(f"Copied {icon_name} -> {dst_folder}")

def create_api_keys():
    api_keys_file = os.path.join(BASE_DIR, "API_KEYS")
    content = '''APP_ID = 6
APP_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
MAPS_V2_API = ""
'''
    with open(api_keys_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Created API_KEYS file with official Telegram parameters.")

if __name__ == "__main__":
    print("Applying NickoGram Patches...")
    patch_strings()
    copy_icons()
    create_api_keys()
    print("All NickoGram patches applied successfully!")
