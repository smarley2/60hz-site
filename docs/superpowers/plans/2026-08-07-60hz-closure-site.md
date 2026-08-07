# 60Hz Closure Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a lightweight, responsive closure landing page for 60Hz Energias on GitHub Pages, preserving the current blue/yellow visual identity and keeping customer support available by email.

**Architecture:** A dependency-free static site served from the repository root by GitHub Pages. `index.html` contains semantic page content and inline SVG iconography; `styles.css` contains the responsive layout and brand styling. The custom-domain `CNAME` file is intentionally deferred until the default GitHub Pages URL has been reviewed.

**Tech Stack:** HTML5, CSS3, GitHub Pages, pytest-based static checks.

## Global Constraints

- Primary brand colors: blue and yellow matching the current 60Hz site.
- Support email: `atendimento@60hz.com.br`.
- Sales and commercial operations are fully closed.
- Responsive from 320 px upward.
- No JavaScript or third-party runtime dependencies.
- Do not add `CNAME` until the GitHub Pages preview has been approved.

---

### Task 1: Static page and responsive styling

**Files:**
- Create: `index.html`
- Create: `styles.css`
- Create: `tests/test_site.py`

**Interfaces:**
- Produces: a GitHub Pages-compatible site from repository root.

- [x] Write static checks for required content, email link, viewport metadata, brand palette, responsive breakpoint, and absence of `CNAME`.
- [x] Run tests and verify they fail before the site files exist.
- [x] Implement the semantic HTML and responsive CSS.
- [x] Run tests and verify they pass.

### Task 2: Preview workflow documentation

**Files:**
- Modify: `README.md`

**Interfaces:**
- Produces: instructions for enabling GitHub Pages and previewing at the default `github.io` URL before DNS changes.

- [x] Document Pages deployment from `main` / root.
- [x] Document the preview URL.
- [x] State that DNS and `CNAME` are deferred until approval.
