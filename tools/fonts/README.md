`embed.css` is the base64 woff2 payload inlined into `deck/index.html`, so the
deck needs no network at the podium. The matching TTFs for the PowerPoint file
live in `deck/fonts/`.

Regenerate with the Google Fonts CSS API (Cormorant Garamond 400/500/600/700 +
italic, Montserrat 300–700, latin subset), de-duplicating the variable-font
files and declaring each face with a weight range.
