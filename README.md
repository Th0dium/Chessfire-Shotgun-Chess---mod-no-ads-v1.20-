# Chessfire: Shotgun Chess — No Ads Mod (v1.20)

![Platform](https://img.shields.io/badge/Platform-Android-green.svg)
![Type](https://img.shields.io/badge/Patch-ARM64%20Binary-red.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)

A binary-level patch for **Chessfire: Shotgun Chess** (Unity IL2CPP, ARM64) that removes ads and unlocks ad-gated rewards. No mod menu, no APK mod tools — just direct hex editing of `libil2cpp.so`.

---

## What this does

- Removes mandatory video ads and interstitial pop-ups.
- Unlocks all "Watch Ad to claim" rewards instantly (Gems, Chests, Revives).

No god mode, no unlimited gems — just making the game playable without sitting through ads.

---

## How it works

The game uses Unity's IL2CPP backend, which compiles C# into native ARM64 machine code. There's no bytecode to edit — you work directly with the binary. (I didn't know any of this going in — most of the technical understanding here came from working with an AI agent throughout the process.)

The mod patches three methods in `libil2cpp.so` that handle purchase validation:

| Method | Offset | What we do |
| :--- | :--- | :--- |
| `GooglePurchase.IsPurchased` | `0x5070B6C` | Force return `true` |
| `Product.get_hasReceipt` | `0x5023700` | Force return `true` |
| `NonConsumableInAppPurchase.get_SaveIsPurchasedLocally` | `0x42D8B4C` | Force return `true` |

Each patch is just 8 bytes: `MOV X0, #1` + `RET`. The game's higher-level systems then see every IAP as already-purchased and stop gating ad rewards behind real transactions.

---

## The process

Worth noting upfront: I didn't have the source code. The starting point was just the APK pulled from my own phone via adb, a compiled binary and Il2CppDumper to get method signatures and offsets from the metadata.

Everything here was reverse engineered from scratch.

This took longer than expected. The first obvious approach was to find the "grant item" functions and call them directly, patch `OnPurchaseFailed` to redirect to `OnPurchaseSuccessful`, hook the `Restore Purchases` flow, etc. Every attempt resulted in the game crashing on start or hanging at 50% of the loading bar.

The root cause: Chessfire initializes its UI and Shop components early in the loading sequence, before the Inventory system is ready. Any patch touching item-granting logic during that window caused a silent deadlock - tricky to diagnose without source code.

The working approach was to go *lower* in the stack - patch the receipt validation layer instead of the granting layer. The game never gets a chance to dispute whether you paid; it just sees valid receipts everywhere and moves on.

I also attempted to unlock premium in-app purchases like the Archer Hero, but it's not as simple as patching receipt validation. The no-ads purchase is a simple boolean flag, which is why it's straightforward to patch. The Archer Hero, on the other hand, requires not only a boolean flag but also actual data in the Inventory system - without it, the game crashes when trying to access the character.

Bypassing premium purchases like the Archer Hero is probably doable, but the inventory data requirement makes it a harder problem for me to fully solve.

---

## Installation

The mod ships as a Split APK (the game uses an app bundle, so you need both the base APK and the split library APK).

1. Download `Chessfire_v1.20_Modded.zip` from the [**Releases**](../../releases/latest) page (no need to extract it).
2. Install **SAI — Split APKs Installer** on your Android device via app store.
3. Open SAI → "Install APKs" → select the zip file → Install.

> The APK is signed with an Android debug key (the original signing key is not available). You'll need to enable "Install from unknown sources" in your device settings.

---

## Tools used

- **Il2CppDumper** — to get method offsets from `global-metadata.dat`
- **Python** — for the actual byte patching ([`scripts/rebuild_v2.py`](scripts/rebuild_v2.py))
- **jar** — for repacking the APK without compression (critical for Split APKs)
- **uber-apk-signer** — for re-signing
- **SAI** — for installation
- **AI agent (Gemini/Claude)** — for the actual binary analysis, offset calculation, and ARM64 assembly. I directed the process; the AI did the heavy lifting.

---

## Disclaimer

This is a personal research project. I don't encourage piracy — if you like the game, support the original developers.