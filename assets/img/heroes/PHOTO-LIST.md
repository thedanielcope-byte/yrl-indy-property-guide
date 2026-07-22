# Hero Photos — what to send, and what to shoot

The hero system is built and live. Any page **without** a photo keeps the navy
gradient, so photos can be added one at a time, in any order, with nothing
breaking. Send photos whenever you have them.

To add one:

```bash
python3 set-hero.py ~/Photos/carmel-arts-district.jpg cities/hamilton-county/carmel-indiana-real-estate
```

That resizes, strips EXIF (removes GPS/camera data), writes an optimised WebP +
JPEG, wires the page, and adds a preload hint. To remove one:
`python3 set-hero.py --remove <page>`. To see what's set: `python3 set-hero.py --list`.

---

## Specs

| | |
|---|---|
| **Minimum width** | 1600px (2400px+ preferred — I downscale, never upscale) |
| **Orientation** | Landscape. Roughly 3:2 or wider. Never portrait. |
| **Format to send** | Original JPEG/PNG/HEIC straight off the camera or phone is fine |
| **File size to send** | Don't pre-compress — send the biggest you have, I handle optimisation |
| **What I output** | ~1600px WebP + JPEG, typically 200–300KB |

**Composition matters more than resolution.** A dark navy scrim sits over the
photo so the white headline stays readable, and it's heaviest on the **left**
(desktop). So:

- Keep the **left third relatively simple** — sky, lawn, water, open road. Busy
  detail there fights the headline.
- Put the **subject on the right side** of the frame.
- **Shoot wide.** The hero is a short, wide band; tall subjects get cropped.
- **Golden hour** (early morning / just before sunset) makes almost any exterior
  look premium. Overcast midday is the enemy.
- Avoid: recognisable faces, readable license plates, real-estate signs from
  other brokerages, anything with a visible date/season mismatch.

---

## What to actually photograph

**Strong preference: real, recognisable Central Indiana.** A photo of the actual
Carmel Arts & Design District on the Carmel page is worth ten stock photos of an
anonymous suburban house — and it's the single biggest thing that will stop the
site looking like every other agent template. Generic stock houses are exactly
what we're trying to get away from.

⚠️ **Do not reuse MLS listing photos** unless you own the rights. Listing
photography is normally the photographer's or listing brokerage's copyright, and
MLS rules restrict reuse. Your own listings shot by your own photographer, with
rights assigned, are fine.

---

## TIER 1 — the 12 that cover most of your traffic

Start here. These are the highest-traffic pages on the site.

| # | Page | File to send | Ideal subject |
|---|---|---|---|
| 1 | Homepage | `home.jpg` | Indianapolis skyline at golden hour, or a signature Central Indiana streetscape *(currently a stock house — replace when you can)* |
| 2 | Carmel | `carmel.jpg` | Arts & Design District, the Palladium, or a Monon Trail roundabout |
| 3 | Fishers | `fishers.jpg` | Nickel Plate District, Fishers Amphitheater, or Geist waterfront |
| 4 | Greenwood | `greenwood.jpg` | Old Town Greenwood / Madison Ave streetscape |
| 5 | Noblesville | `noblesville.jpg` | Hamilton County Courthouse square or Federal Hill Commons |
| 6 | Westfield | `westfield.jpg` | Grand Park Sports Campus |
| 7 | Zionsville | `zionsville.jpg` | The brick-paved Main Street Village — your most photogenic asset |
| 8 | Indianapolis hub | `indianapolis.jpg` | Downtown skyline, Monument Circle, or Mass Ave |
| 9 | Buying guide | `guide-buying.jpg` | Keys handed over, a front door, a couple on a porch |
| 10 | Selling guide | `guide-selling.jpg` | A well-staged living room or attractive curb appeal |
| 11 | Avon | `avon.jpg` | Washington Township Park or the US-36 corridor |
| 12 | Brownsburg | `brownsburg.jpg` | Main Street downtown or Lucas Oil Raceway |

## TIER 2 — remaining Phase-1 cities & top neighborhoods

| Page | File | Ideal subject |
|---|---|---|
| Plainfield | `plainfield.jpg` | Downtown or Hummel Park |
| Franklin | `franklin.jpg` | Courthouse square / Franklin College |
| McCordsville | `mccordsville.jpg` | New construction streetscape |
| Shelbyville | `shelbyville.jpg` | Public square / courthouse |
| Lawrence | `lawrence.jpg` | Fort Harrison State Park |
| Speedway | `speedway.jpg` | Main Street / IMS pagoda area |
| Beech Grove | `beech-grove.jpg` | Main Street |
| Southport | `southport.jpg` | Residential streetscape |
| Broad Ripple | `broad-ripple.jpg` | The Village, canal, or Monon |
| Irvington | `irvington.jpg` | Historic homes / Irving Circle |
| Geist Reservoir | `geist.jpg` | Water at sunset, docks, boats |
| Meridian-Kessler | `meridian-kessler.jpg` | Tree-lined historic street |
| Fountain Square | `fountain-square.jpg` | The fountain / arts district murals |

## TIER 3 — counties (shared fallback for their smaller towns)

One photo per county covers every small town in it. Landscape/rural or the
county seat's courthouse both work well.

`hamilton.jpg` · `marion.jpg` · `johnson.jpg` · `hendricks.jpg` · `boone.jpg` ·
`hancock.jpg` · `madison.jpg` · `shelby.jpg` · `morgan.jpg` · `montgomery.jpg` ·
`decatur.jpg` · `brown.jpg` *(Brown County State Park in fall is spectacular)* ·
`putnam.jpg` · `parke.jpg` *(covered bridges)* · `bartholomew.jpg`
*(Columbus architecture)* · `jackson.jpg` · `jennings.jpg`

## TIER 4 — service & comparison pages (optional)

Mostly fine on the gradient. If you want a few: `sell-my-home.jpg`,
`first-time-buyers.jpg`, `luxury-homes.jpg`, `new-construction.jpg`,
`investment.jpg`.

---

## The realistic minimum

**If you only send 5:** homepage, Carmel, Fishers, Greenwood, and the downtown
Indianapolis skyline. That covers your highest-traffic pages and the site will
already feel transformed. Everything else keeps the gradient until you get to it.
