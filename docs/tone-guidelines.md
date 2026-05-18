# Project Voice & Tone Guidelines (CS Helper Tool)

## 1. Core Persona
This tool is built by a developer as a loving, supportive, and thoughtful gift for his girlfriend, who works as a CS (Customer Service) specialist. The app's interface must completely abandon cold, rigid corporate enterprise language.

## 2. Tone Matrix (Bilingual)
Whenever generating UI text, notifications, modals, or placeholders, strictly adhere to this tone mapping:

### Traditional Chinese (zh) - "純正廣東話、親切應援、暖心治癒"
- **Style:** Authentic Hong Kong Cantonese (口語/廣東話). It must be sweet, playful, comforting, and highly encouraging. Use cozy emojis (e.g., ✨, 💖, 🍀, 🚀, 🦸‍♀️) and natural Cantonese sentence structures.
- **Vocabulary/Phrasing Rules:**
  - Use `妳` instead of `你`.
  - Use Cantonese particles and verbs: `啦` (laa), `喎` (wo), `啊嘛` (aa maa), `咗` (zo), `嘅` (ge), `玩緊` (playing), `執嘢` (fixing stuff).
  - Replace technical terms with friendly daily words where appropriate (e.g., replace "系統錯誤" with "系統好似有啲衰咗喎").
- **Core Message:** Acknowledge her hard work, ease her stress, and remind her that her developer boyfriend is supporting her.
- **Examples:** 
  - *Bad (Corporate Written):* "請選擇欲更新之系統模組。"
  - *Good (Cozy Cantonese):* "今日辛苦啦！先揀一個今日想處理嘅模組先啦 ✨"
  - *Bad (Corporate Written):* "提醒：您尚未確認手機端測試。"
  - *Good (Cozy Cantonese):* "等陣先！妳好似未剔「手機 App 測試正常」喎，確認真係要出公告？ 💖"

### English (en) - "Warm, Supportive, Cheering"
- **Style:** Heartwarming, appreciative, and charmingly affectionate.
- **Example:**
  - *Bad:* "Select the module for the upgrade notice."
  - *Good:* "Let's pick a module to work on today, my superhero! 💝"

## 3. Hidden Content Safeguard
- **Internal Remarks Field:** The app contains an internal logging field for the user to write down Case IDs or technical notes. 
- **Rule:** AI must *never* include or leak the content of the Internal Remarks field into the public "Upgrade News Live Preview" outputs. It must strictly remain hidden from clients.