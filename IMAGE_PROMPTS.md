# Nano Banana 2 — Background Image Prompts

12 portrait backgrounds for the Tosca slide feed. Each image goes into `img/`
as `01-hero.jpg` … `12-signoff.jpg`.

## Target specs

- **Aspect ratio:** 9:16 vertical (1080×1920 or similar)
- **Format:** JPEG, quality ~80, target file size 300–600 KB each
- **Safe zones:** top ~140 px reserved for the story-header (avatar + label),
  bottom ~45 % of frame reserved for text overlay — keep these regions
  compositionally quiet (shadow, sky, wall, negative space)
- **No text, no logos, no visible human faces** in any image — style over
  subject; faces should be turned away, silhouetted, or absent
- **Consistent palette:** deep burgundy, antique gold, cream highlights,
  charcoal shadows — matches the site palette `#7A2332 / #C8A55C / #FDF6EC`

## Shared style block (append to every prompt)

```
Cinematic painterly aesthetic blending Renaissance chiaroscuro with modern
moody film photography. Deep burgundy, antique gold and warm cream color
palette with charcoal shadows. Dramatic low-key lighting, single directional
light source, soft atmospheric haze. Shallow depth of field. Rich texture,
subtle film grain. Romantic, operatic, melancholic atmosphere. 9:16 vertical
composition with compositional negative space in the lower two-thirds for
text overlay. No text, no logos, no visible human faces. Ultra-detailed, 4K.
```

## The 12 prompts

### 01 — Hero · `01-hero.jpg`
> A vast empty stage of a historic European opera house seen from the
> darkened auditorium, heavy burgundy velvet curtain slightly drawn, a
> single warm spotlight cone cutting through theatrical haze onto the stage
> floor, ornate gilded proscenium arch blurred in the foreground, crystal
> chandelier glinting softly overhead, romantic anticipation before the
> overture begins.

### 02 — Dinner · `02-dinner.jpg`
> An intimate candlelit table for two in a dimly lit Bavarian fine-dining
> restaurant, two crystal glasses of deep red wine catching the flame,
> small bouquet of dark garden roses in a silver vase, linen tablecloth,
> warm tungsten bokeh from distant candles, burgundy velvet banquette in
> blurred background, evening romance, no people visible.

### 03 — Intro · `03-intro.jpg`
> Rain-slicked cobblestones of a narrow Roman alley at twilight in June
> 1800, weathered oil lamps glowing warmly on iron brackets, distant
> silhouette of a Baroque church dome against a stormy indigo sky, torn
> political proclamations and papal flags on a wet stone wall, atmosphere
> of political tension and secrets, completely deserted.

### 04 — Characters · `04-characters.jpg`
> Three symbolic objects arranged in a triangular composition on an aged
> marble floor: a gilded royal opera glove, a wooden artist's palette
> streaked with oil paint, and a polished silver dagger lying across a
> sealed letter. Single shaft of warm light cutting across them from a
> tall window, deep shadows, theatrical still life, cinematic.

### 05 — Act I · `05-act1.jpg`
> Interior of a grand Baroque Roman church at late golden hour, Sant'Andrea
> della Valle, sunlight streaming through high stained-glass windows onto
> ornate frescoes and a gilded altar, wooden painter's scaffolding and an
> easel with a cloth-covered canvas in a side chapel, candles flickering,
> wisps of incense smoke rising, sacred yet secretive mood.

### 06 — Recondita armonia · `06-recondita.jpg`
> Close-up still life of a Baroque painter's wooden palette covered in
> rich oil colors of rose, cream and burgundy, a fine sable brush resting
> on it, an open golden locket beside it revealing an indistinct romantic
> portrait miniature, warm afternoon sunlight falling from a high church
> window, reverent painterly mood, dust motes in light beam.

### 07 — Act II · `07-act2.jpg`
> An opulent Roman palazzo study at night by candlelight, heavy burgundy
> damask walls, a large polished mahogany writing desk with a flickering
> silver candelabra, an overturned silver goblet of red wine spilling
> across an unfinished letter with wax seal, a sheathed dagger partially
> visible in shadow at the desk's edge, dread and menace, strong
> chiaroscuro, completely deserted.

### 08 — Vissi d'arte · `08-vissi.jpg`
> An empty ornate Baroque prie-dieu (prayer kneeler) in an opulent palazzo
> chamber at night, a forgotten silk shawl and a pearl rosary draped over
> it, a single tall candle nearly burnt down to its holder, moonlight
> filtering through heavy velvet curtains, tears of wax pooling on silver,
> heartbreak and devotion, sacred stillness, deep chiaroscuro.

### 09 — Act III · `09-act3.jpg`
> Panoramic view from the ancient stone ramparts of Castel Sant'Angelo in
> Rome during the cold blue hour just before sunrise, mist rising from the
> Tiber river below, distant silhouette of St Peter's basilica dome on the
> horizon, weathered stone battlements in the foreground, a solitary raven
> perched on a crenellation, tragic dawn atmosphere.

### 10 — E lucevan le stelle · `10-lucevan.jpg`
> The night sky above Rome seen from a high stone terrace, countless stars
> blazing across deep indigo and violet, the Milky Way faintly visible, a
> distant constellation fading toward the first hint of dawn on the
> horizon, silhouettes of Baroque rooftops and a far cupola below,
> melancholy and longing, wide cinematic composition, subtle film grain.

### 11 — Epilog · `11-epilog.jpg`
> A scattered bouquet of dark crimson roses fallen on ancient stone steps
> at dawn, petals drifting in soft mist, a single pearl-white silk glove
> left behind on a step, faint cold morning light, deep burgundy and slate
> palette, theatrical tragic stillness after the drama has ended,
> completely still, no people.

### 12 — Sign-off · `12-signoff.jpg`
> A single candle burning warmly in an antique brass holder resting on an
> aged parchment love letter, a wax seal with a heart impression, a
> delicate dried rose petal beside it, soft golden glow filling the frame,
> intimate handwritten romance, warm cream and deep burgundy tones,
> subtle film grain, tender closure.

## Workflow

1. Generate each image with the shared style block appended.
2. If the first pass is inconsistent in style, feed image 01 as a style
   reference image to Nano Banana for 02–12 (Gemini Flash Image supports
   style reference via attached images).
3. Resize/crop to 1080×1920 if needed.
4. Save to `img/` with the exact filenames listed above.
5. `git add img/ && git commit && git push` — GitHub Pages redeploys in
   ~1 minute and the slides pick up the new backgrounds automatically.
