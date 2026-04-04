# Design System Specification: The Guardian Interface

## 1. Overview & Creative North Star
**Creative North Star: "The Resilient Horizon"**

For the delivery professional, the smartphone is a tool of survival, often used under the harsh glare of the midday sun or the blur of a rainy night. This design system moves beyond the "standard app" aesthetic to create a **High-End Editorial** experience that feels like a premium utility. 

We reject the "boxed-in" look of traditional insurance apps. Instead, we embrace **The Resilient Horizon**: a layout philosophy defined by intentional asymmetry, expansive breathing room, and a sophisticated layering of depth. We use high-contrast typography and "Ghost" surfaces to ensure that while the interface feels lightweight and fast, it carries the authoritative weight of a financial guardian. 

By breaking the rigid grid with overlapping elements and tonal shifts rather than lines, we create a UI that feels fluid, modern, and relentlessly reliable.

---

## 2. Colors: Tonal Depth over Borders
This system leverages a sophisticated palette of deep nautical blues (`primary`) and growth-oriented teals (`secondary`). 

### The "No-Line" Rule
**Lines are a sign of structural weakness.** To maintain a premium, lightweight feel, designers are strictly prohibited from using 1px solid borders to section content. Boundaries must be defined solely through background color shifts or subtle tonal transitions.
*   *Implementation:* Place a `surface_container_highest` card against a `surface` background. The contrast in tone creates the edge, not a stroke.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers—like stacked sheets of frosted glass.
*   **Base:** `surface` (#fcf9f8)
*   **Sectioning:** Use `surface_container_low` for large background areas.
*   **Interaction Hubs:** Use `surface_container_highest` for primary cards.
*   **The Depth Stack:** An inner element should always be "higher" in the tier than its parent container to signify importance.

### The Glass & Gradient Rule
To move beyond "flat" design, use **Glassmorphism** for floating action buttons or sticky headers.
*   **Effect:** Apply `surface` at 80% opacity with a `20px` backdrop-blur. 
*   **Signature Textures:** For high-impact CTAs, use a subtle linear gradient from `primary` (#00286d) to `primary_container` (#003d9b) at a 135-degree angle. This adds a "soul" to the UI that flat colors lack.

---

## 3. Typography: Editorial Authority
We pair the structural elegance of **Manrope** for high-level branding with the utilitarian clarity of **Inter** for data-heavy mobile interactions.

*   **Display & Headlines (Manrope):** These are your "Editorial" voices. Use `display-lg` and `headline-md` with tight letter spacing (-0.02em) to create an authoritative, bold presence.
*   **Body & Labels (Inter):** Designed for high visibility outdoors. `body-lg` is your default for legibility. 
*   **The Hierarchy Strategy:** Large headlines signal security and brand confidence, while smaller, high-contrast labels (`label-md` in `on_surface_variant`) handle the "fast" data—weather alerts, earnings, and policy numbers.

---

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows are often messy. We use **Ambient Depth** to signal hierarchy.

*   **The Layering Principle:** Avoid shadows where possible. Instead, stack `surface_container_lowest` cards on a `surface_container_high` background. This creates a "soft lift" that feels integrated.
*   **Ambient Shadows:** If an element must float (e.g., a critical "File a Claim" button), use an extra-diffused shadow:
    *   *Y: 8px, Blur: 24px, Opacity: 6%*
    *   *Color:* Use a tinted version of `on_surface` (#1c1b1b) rather than pure black.
*   **The "Ghost Border" Fallback:** In high-glare outdoor scenarios where contrast is failing, use a "Ghost Border": `outline_variant` at 15% opacity. Never use 100% opaque borders.

---

## 5. Components: Minimalist Primitives

### Buttons: The "Solid Weight"
*   **Primary:** Solid `primary` with `on_primary` text. Corners: `xl` (1.5rem) for a friendly, modern touch.
*   **Secondary:** `secondary_container` with `on_secondary_container` text. No border.
*   **Tertiary:** No background. Bold `primary` text with an underline only on hover/active states.

### Input Fields: The "Interactive Well"
*   **Styling:** Use `surface_container_highest` as the background. 
*   **Indicator:** Instead of a full border, use a 2px bottom-bar in `primary` that animates outward when focused.
*   **Error State:** Shift background to `error_container` and text to `on_error_container`.

### Cards & Lists: The "No-Divider" Mandate
*   **Rule:** Forbid the use of divider lines between list items. 
*   **Alternative:** Use 12px of vertical white space and subtle alternating tonal shifts between `surface_container_low` and `surface_container_lowest`.

### Signature Component: The "Active Shield" Status
A specialized card for this design system. A large, `secondary_fixed` container with a glassmorphic overlay that displays live "Protected" status. Use `tertiary` (#003608) for "Live" indicators to signal growth and safety.

---

## 6. Do’s and Don’ts

### Do:
*   **Do** use `display-lg` for monetary values. It should feel like a celebration of the worker's earnings.
*   **Do** embrace white space. If a screen feels "empty," it means it's "fast."
*   **Do** use `rounded-xl` for all major containers to soften the "insurance" persona into a "supportive" one.

### Don’t:
*   **Don’t** use pure black (#000) for text. Use `on_surface` (#1c1b1b) to maintain a premium, ink-like quality.
*   **Don’t** use standard Material Design "Outlined" buttons. They feel too "templated" and clinical for a supportive brand.
*   **Don’t** crowd the bottom navigation. Keep it to 3-4 high-priority icons to ensure easy thumb-reach for workers on the move.