# Product Requirements Document (PRD)

## Product Name

**Edge Light** (working name)

## Platform

* Windows 11 (primary)
* Windows 10 (secondary)

---

## 1. Product Overview

EdgeLight is a lightweight Windows background utility that improves webcam visibility in dark environments by using the laptop screen itself as a subtle, front-facing light source.

Instead of acting as a full ring-light replacement, EdgeLight provides **just enough illumination** to make the user’s face visible, identifiable, and expressive during video calls — without external hardware, camera access, or visual clutter.

**Product philosophy:**

> System-like, invisible, trustworthy, and always ready.

EdgeLight should feel closer to **Task Manager or Volume Control** than to a traditional desktop application.

---

## 2. Problem Statement

Many people use their laptops for professional meetings, casual calls with friends, or spontaneous video conversations in poorly lit environments.

Laptop webcams struggle in low light, and external lighting solutions (ring lights, desk lamps) are often:

* Inconvenient
* Bulky
* Overkill for casual or short calls

Users want a **software-only, frictionless solution** that improves webcam visibility instantly, without changing their physical setup.

---

## 3. Goals

* Make the user’s face clearly visible in low-light video calls
* Improve visibility of facial expressions and identity
* Require zero external hardware
* Avoid camera access or video manipulation
* Run quietly in the background with minimal system impact
* Be instantly configurable and dismissible

---

## 4. Non-Goals

* No webcam access or processing
* No face detection or tracking
* No AI-based enhancements
* No filters, beautification, or background effects
* No always-visible taskbar application
* No cross-platform support in v1

---

## 5. Target Users

**Primary users**

* Anyone using a laptop for:

  * Professional video calls
  * Casual calls with friends or family
  * Late-night or low-light meetings

**Usage context**

* Low ambient lighting
* Short to medium-length calls
* Desire for convenience over perfection

This product is for **broad, everyday use**, not creators or studio setups.

---

## 6. Core User Value

When EdgeLight is enabled:

* The user’s face is identifiable
* Facial expressions are visible
* The lighting feels natural and unobtrusive
* The user does not need to think about lighting equipment

---

## 7. Core Features

| Feature                      | Description                                  |
| ---------------------------- | -------------------------------------------- |
| Screen-edge glow overlay     | Soft light rendered inward from screen edges |
| Adjustable brightness        | Fine-grained control over light intensity    |
| Adjustable color temperature | Warm, neutral, cool tones                    |
| Adjustable thickness         | Control how far the glow extends inward      |
| Click-through overlay        | Never blocks mouse or keyboard input         |
| Always-on-top rendering      | Remains visible over all windows             |
| Background operation         | No taskbar presence; lives in system tray    |
| Global toggle                | Hotkey-based on/off control                  |
| Optional auto-start          | Can launch silently on system boot           |

---

## 8. User Experience & Interaction Model

### Application Presence

* No taskbar icon
* Operates as a background utility
* Accessed via:

  * System tray
  * Global hotkey

### Controls

* Tray menu provides:

  * Enable / disable EdgeLight
  * Brightness adjustment
  * Color temperature selection
  * Glow thickness adjustment
  * Quit application

### Control Philosophy

* User turns EdgeLight **on**
* User then adjusts settings **live**, seeing immediate visual feedback
* Once configured, EdgeLight can be left untouched for future use

---

## 9. Visual & Lighting Behavior

* Lighting should be **supportive**, not dominant
* The effect should not be immediately obvious as a “filter”
* The goal is not beauty enhancement, but **functional visibility**
* Default settings should favor:

  * Conservative brightness
  * Neutral color temperature
  * Moderate glow thickness

---

## 10. Trust & Safety

EdgeLight must clearly and strictly:

* Not access the camera
* Not inspect running applications
* Not capture or process screen content
* Not transmit any data

The application should behave in a way that naturally builds user trust through:

* Predictability
* Transparency
* Minimal permissions

---

## 11. Technical Constraints (Product-Level)

* CPU-only
* No admin privileges required
* Low memory footprint (<100 MB)
* Near-instant toggle response (<100ms perceived)
* No interference with:

  * Input
  * Focus
  * Screen capture
  * Video conferencing tools

---

## 12. MVP Definition

Version 1 is complete when:

* The overlay renders reliably on common Windows setups
* Brightness, color temperature, and thickness are adjustable
* Tray-based control works consistently
* Global hotkey toggles instantly
* The app runs silently in the background
* A standalone `.exe` can be distributed

---

## 13. Risks & Mitigations

**Potential risks**

* DPI scaling inconsistencies
* Multi-monitor edge cases
* Overlay conflicts with certain applications
* Users mistaking the overlay for screen dimming or filtering

**Mitigations**

* Conservative defaults
* Clear naming and behavior
* No automatic activation without user intent

---

## 14. Success Criteria

EdgeLight is successful if:

* Users feel more confident joining calls in low light
* The app does not disrupt normal workflows
* Users forget it’s running until they need it
* The lighting feels helpful but not artificial

---

## 15. Future Expansion (Post-v1)

* Per-monitor behavior
* Saved presets
* Per-app profiles
* Optional adaptive defaults
* Exploration of other desktop platforms (not in scope for v1)

---
