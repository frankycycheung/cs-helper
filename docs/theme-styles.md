# UI & CSS Style Upgrade Guidelines ("Cozy Pastel Layout")

## 1. Design Aesthetic
The application layout shifts from standard utility-heavy SaaS designs to a **"Soft Pastel, Warm Milk-Tea, and Fluffy Card"** look, minimizing harsh borders and high-contrast dark elements.

## 2. Color Palette Reference
Future components or features must align with these hexadecimal/Bootstrap utility mappings:
- **Page Background:** Warm cream/milk-tea fluid canvas (`#FFFDF9` or CSS utility style `.bg-custom-cream`).
- **Main Banner Gradient:** Soft gradient from light cherry blossom pink to soft lavender (`linear-gradient(135deg, #FFF0F5 0%, #E6E6FA 100%)`).
- **Accent Elements:** Soft coral/warm pink (`#FF9999`) as primary accent.
- **Validation Alerts / Warning Modals:** Warm Amber (`#D97706` / Bootstrap `.btn-warning`) to highlight unchecked risks gently without causing anxiety.

## 3. Global Theme CSS
Common styles are centralized in `spa/src/styles/theme.css`. This file should be imported in `index.html` and contains:
- CSS custom properties (`:root` variables)
- Reusable utility classes (`.card`, `.btn-pill`, `.form-control`, `.bg-custom-cream`, `.bg-custom-pink`)
- Base body styling

## 4. Component Styling Rules (CSS Refinement)
Apply these rules inside scoped Vue component styles or global style variables:

```css
/* Card Elements */
.card {
  border: none !important;
  border-radius: 20px !important;
  box-shadow: 0 10px 30px rgba(223, 190, 200, 0.15) !important;
  background-color: #FFFFFF;
}

/* Button Elements */
.btn-pill {
  border-radius: 50px !important;
  transition: all 0.3s ease;
}
.btn-pill:hover {
  transform: scale(1.03);
  box-shadow: 0 5px 15px rgba(255, 182, 193, 0.4);
}

/* Form Inputs */
.form-control, .form-select {
  border-radius: 12px !important;
  border: 1.5px solid #F3E5F5;
  background-color: #FFFDF9;
}
.form-control:focus, .form-select:focus {
  border-color: #FFB6C1;
  box-shadow: 0 0 0 0.25rem rgba(255, 182, 193, 0.25);
}
```

## 4. Layout Framework
- Always structure main application screens using a responsive **Three-Column Dashboard Grid** layout via Bootstrap (`.row .row-cols-1 .row-cols-lg-3 .g-4`) for modern, scannable spacing.