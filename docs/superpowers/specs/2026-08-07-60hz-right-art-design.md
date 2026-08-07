# 60Hz Right-Side Artwork Design

## Goal

Bring the right side of the 60Hz Energias closure landing page closer to the approved reference image by replacing the current synthetic hero artwork with the supplied painterly background and the supplied farewell character. Preserve the existing page copy, support card, footer, email actions, and overall static-site architecture.

## Scope

### In scope

- Replace only the hero artwork composition on the right side.
- Use the supplied painterly blue/yellow background as the visual base.
- Extract the character from the supplied character image and place it in the foreground.
- Preserve the existing 60Hz wordmark contained in the painterly background.
- Keep the current left-side text, header, support card, footer, and support interactions unchanged.
- Keep the page dependency-free and compatible with GitHub Pages.
- Preserve responsive behavior from 320 px upward.

### Out of scope

- Rewriting the page copy or changing the support email.
- Changing support button behavior.
- Adding a custom domain or CNAME file.
- Introducing a framework, build step, or third-party runtime dependency.
- Redesigning the header, support card, or footer.

## Visual composition

On desktop, `.hero-art` remains the right-side artwork layer of the existing hero. Its painterly background fills the panel with a cover-style crop, while a transparent character cutout is positioned above it, aligned toward the bottom so the face, raised hand, coat, and scarf remain visible.

### Reference-background revision

The painterly background occupies only the right side of the desktop hero, beginning at roughly 42% of the viewport like the supplied model. The image is slightly wider than its panel and anchored to the right so the yellow sun and full 60Hz wordmark stay visible beside the unchanged character.

### Approved transition: curve of wind

Replace the left-edge fade with a solid, broad elliptical curve inspired by the movement of the character's scarf. The curved seam receives a subtle yellow painted line so the boundary looks intentional and connects to the brand palette. Do not add opacity gradients, blur, particles, or new image assets. On viewports up to 980 px, reset the curve and yellow line so the existing full-width rectangular artwork block remains space-efficient.

The existing CSS-only orbit, energy lines, embedded raster data, and duplicated overlaid logo are removed from the active composition. The logo and yellow sun remain supplied by the painterly background image itself.

On narrow viewports, the artwork becomes a full-width block below the hero copy. The background remains cropped with the face and scarf prioritized, and the character stays within the visible block without covering the page copy or support card.

## Asset strategy

Add repository-local raster assets under `assets/`:

- `60hz-painterly-background.png`: the painterly background based on the supplied 21_22_04 image.
- `60hz-character-cutout.png`: a transparent-background extraction based on the supplied 21_20_42 image.

The source files are copied into the repository so GitHub Pages can serve them without external URLs. The character extraction will preserve natural edges and the original colors; no new character or text will be generated.

The existing SVG assets remain available as general brand assets. The hero will not depend on the large embedded data URI currently used by `sun-orbit`.

## HTML/CSS boundaries

Keep the current semantic HTML and support interactions. Update only the hero-art markup as needed to expose separate background and character layers, with meaningful empty alt text because the artwork is decorative and the same communication is already present in the page text.

Use the existing CSS files and variables. Prefer a small, explicit set of hero-art rules over a new framework or runtime script. Ensure all image paths are relative so the site works at `/60hz-site/` on GitHub Pages.

## Validation

- Run the existing pytest suite.
- Run an asset/path check to confirm both new images exist and are referenced from the page or stylesheet.
- Serve the repository locally and inspect a desktop viewport plus a narrow mobile viewport.
- Confirm the character remains visible and the left-side text/support card are not modified.
- Confirm the live GitHub Pages URL loads the new artwork after publication.

## Acceptance criteria

1. The right side visually uses the supplied painterly background and the supplied character, with the character in front and no visible dark rectangular backdrop.
2. The left-side copy and support card remain functionally and textually unchanged.
3. Desktop layout resembles the approved reference: the blue/yellow painterly field remains on the right, meets the white copy area through the approved solid curve-of-wind seam, and keeps the large farewell character in front.
4. Mobile layout remains readable and keeps the character/artwork visible below the copy.
5. Existing tests pass, no `CNAME` is added, and the site remains deployable as a dependency-free GitHub Pages root site.
