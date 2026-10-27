# 🎨 DESIGN.md — Master Design System, Feminine Ergonomics & UI Tokens v1.0 🌸

**Standard Identifier**: `DS-YERLY-V1.0`  
**Status**: `MANDATORY & ACTIVE`  
**Aesthetic Theme**: Sakura & Soft Orchid · Feminine-Mature Elegance · High-Polish Glassmorphism · Calm Fintech Canvas  
**Core Design Philosophy**: *"Estetika yang menenangkan menghadirkan kejernihan pikiran. Antarmuka yang anggun dan bebas distraksi membantu engineer bekerja dengan presisi tanpa kelelahan visual (*Calm Telemetry*)."*  
**Release Date**: 2026-10-27  

---

## 1. 🌈 Color System & Semantic Tokens

### 1.1 The 60-30-10 Rule
* **60% Dominan / Background**: Deep Midnight Slate Canvas (`#0a0f1d` / `#0f172a`).
* **30% Sekunder / Surface Containers**: Soft Orchid Glass Cards (`#1e293b` / `rgba(30, 41, 59, 0.7)`).
* **10% Aksen / Highlights & CTA**: Sakura Blossom Pink (`#f472b6`) & Soft Lilac Glow (`#c084fc`).

### 1.2 Color Palette Matrix

| Token Name | Hex Value | HSL Value | Tailwind Class Equivalent | Peran / Penggunaan |
|---|---|---|---|---|
| `--color-canvas` | `#0a0f1d` | `223° 48% 7%` | `bg-slate-950` | Background canvas utama (anti-pure black). |
| `--color-surface` | `#0f172a` | `222° 47% 11%` | `bg-slate-900` | Surface layer 1 (Sidebar, Navbar, Panels). |
| `--color-surface-elevated` | `#1e293b` | `217° 33% 17%` | `bg-slate-800` | Cards, Modals, Dialogs, Dropdowns. |
| `--color-surface-glass` | `rgba(30, 41, 59, 0.65)` | - | `bg-slate-800/65 backdrop-blur-md` | Glassmorphism container. |
| `--color-border-subtle` | `rgba(255, 255, 255, 0.08)`| - | `border-white/10` | Divider & card outline tipis. |
| `--color-border-focus` | `#f472b6` | `330° 81% 70%` | `border-pink-400` | Active input & focus ring. |
| `--color-primary` | `#f472b6` | `330° 81% 70%` | `text-pink-400 bg-pink-400` | Primary Brand (Sakura Blossom Pink). |
| `--color-primary-hover` | `#ec4899` | `330° 81% 60%` | `bg-pink-500` | Hover state tombol utama. |
| `--color-accent` | `#c084fc` | `271° 91% 75%` | `text-purple-400` | Secondary accent (Soft Lilac Glow). |
| `--color-success` | `#34d399` | `156° 72% 52%` | `text-emerald-400` | Test case PASS / Status hijau. |
| `--color-error` | `#f87171` | `0° 91% 71%` | `text-red-400` | Test case FAIL / Error toast. |

---

## 2. 🌸 Feminine Ergonomics (Calm Telemetry)

1. **Pola Spacing Lembut & Longgar**: Gunakan padding yang lega (`p-4` s/d `p-6`) untuk memberikan ruang bernapas pada elemen UI.
2. **Sudut Membulat yang Elegan**: Border radius menggunakan `rounded-xl` (12px) atau `rounded-2xl` (16px) untuk menghilangkan kesan tajam dan kaku.
3. **Tipografi Hirarkis**: Sans-serif modern (*Inter*, *Plus Jakarta Sans*) dengan pembobotan font yang proporsional (*Medium* untuk body, *Semibold* untuk judul modul).
4. **Micro-Interactions yang Halus**: Animasi transisi menggunakan *cubic-bezier* lembut (`duration-200 ease-out`).

---
*Design Tokens Specification — Yerly-Playground 🌸*
