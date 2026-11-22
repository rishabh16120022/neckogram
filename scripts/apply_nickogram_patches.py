#!/usr/bin/env python3
"""
NickoGram Automated Patch Engine
Applies custom branding, DM Protection settings, English UI strings,
and new launcher icons onto the Telegram Android / Nekogram base.
"""

import os
import shutil
import re

BASE_DIR = os.path.abspath(".")
ART_DIR = os.path.join(BASE_DIR, "art")

# Find strings.xml and res directories across both Nekogram and AyuGram/Telegram structures
RES_DIRS = [
    os.path.join(BASE_DIR, "TMessagesProj_App", "src", "main", "res"),
    os.path.join(BASE_DIR, "TMessagesProj", "src", "main", "res"),
]

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
    patched_any = False
    for res_dir in RES_DIRS:
        strings_file = os.path.join(res_dir, "values", "strings.xml")
        if not os.path.exists(strings_file):
            continue

        with open(strings_file, "r", encoding="utf-8") as f:
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
            print(f"Injected NickoGram DM Protection English strings in {strings_file}")

        with open(strings_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Updated AppName to NickoGram in {strings_file}")
        patched_any = True

    if not patched_any:
        print("Warning: No strings.xml found in expected paths.")

def copy_icons():
    if not os.path.exists(ART_DIR):
        print("Art directory not found, skipping icon copy.")
        return

    for res_dir in RES_DIRS:
        if not os.path.exists(res_dir):
            continue

        for folder in os.listdir(ART_DIR):
            src_folder = os.path.join(ART_DIR, folder)
            if os.path.isdir(src_folder) and folder.startswith("mipmap-"):
                dst_folder = os.path.join(res_dir, folder)
                os.makedirs(dst_folder, exist_ok=True)
                for icon_name in ["ic_launcher.png", "ic_launcher_round.png"]:
                    src_icon = os.path.join(src_folder, icon_name)
                    if os.path.exists(src_icon):
                        shutil.copy2(src_icon, os.path.join(dst_folder, icon_name))
                        print(f"Copied {icon_name} -> {dst_folder}")

def create_config_files():
    # Write local.properties with API keys
    local_props = os.path.join(BASE_DIR, "local.properties")
    with open(local_props, "w", encoding="utf-8") as f:
        f.write("apiId=25806904\napiHash=514b5e04d7cf2e6a188a5e8f5310ec90\n")
    print("Created local.properties with API credentials.")

    # Write API_KEYS for Telegram/AyuGram base
    api_keys_file = os.path.join(BASE_DIR, "API_KEYS")
    with open(api_keys_file, "w", encoding="utf-8") as f:
        f.write('APP_ID = 6\nAPP_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"\nMAPS_V2_API = ""\n')
    print("Created API_KEYS file.")

if __name__ == "__main__":
    print("Applying NickoGram Patches...")
    patch_strings()
    copy_icons()
    create_config_files()
    print("All NickoGram patches applied successfully!")
