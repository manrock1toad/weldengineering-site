# Site check

Built by `.github/workflows/check.yml` from the latest `main`. Live = the WordPress site at www.weldengineering.com.

## 1. Broken links in the built site (0 of 1050 checked)
- None.

## 2. Links to a missing #anchor (0)
- None.

## 3. SEO checks (12 problems)
| Page | Title chars | H1 | Description | Canonical | Social tags | Structured data | Images missing alt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 404.html | 118 | 1 | no | 0 | no | 0 | 0 |
| calc.html | 134 | 1 | yes | 1 | yes | 0 | 0 |
| ham.html | 135 | 1 | yes | 1 | yes | 0 | 0 |
| hd.html | 152 | 1 | yes | 1 | yes | 0 | 0 |
| index.html | 101 | 1 | yes | 1 | yes | 1 | 0 |
| map.html | 112 | 1 | yes | 1 | yes | 0 | 0 |
| mission.html | 112 | 1 | yes | 1 | yes | 0 | 0 |
| new.html | 117 | 1 | yes | 1 | yes | 0 | 0 |
| pf.html | 155 | 1 | yes | 1 | yes | 0 | 0 |
| ro.html | 134 | 1 | yes | 1 | yes | 0 | 0 |
| sd.html | 155 | 1 | yes | 1 | yes | 0 | 0 |
| tb.html | 161 | 1 | yes | 1 | yes | 0 | 0 |

- 404.html: title is 118 characters (Google shows about 60)
- calc.html: title is 134 characters (Google shows about 60)
- ham.html: title is 135 characters (Google shows about 60)
- hd.html: title is 152 characters (Google shows about 60)
- index.html: title is 101 characters (Google shows about 60)
- map.html: title is 112 characters (Google shows about 60)
- mission.html: title is 112 characters (Google shows about 60)
- new.html: title is 117 characters (Google shows about 60)
- pf.html: title is 155 characters (Google shows about 60)
- ro.html: title is 134 characters (Google shows about 60)
- sd.html: title is 155 characters (Google shows about 60)
- tb.html: title is 161 characters (Google shows about 60)

## 4. Deployed site: https://we-site.pages.dev (0 problems)
Real requests to whatever Cloudflare is serving during this run. If Cloudflare's deploy hadn't finished yet, these results are for the previous version.

- OK: `/sitemap.xml` returns 200 and is valid XML (11 URLs).
- OK: All 11 sitemap pages return 200.
- OK: `robots.txt` blocks all crawlers (right for a test site).
- OK: The home page returns 200 and is marked noindex (right for a test site).
- OK: All 16 old addresses in `_redirects` return their redirect code and land on a page that returns 200.
- OK: `/no-such-page-9962995` returns a real 404.
- OK: `/wp-login.php` returns a real 404.
- OK: Literature PDFs are served as PDFs (`/catalog/PT-100-LIT.pdf`).

## 5. Live vs. built, page by page
Expected differences: the email shows as plain text instead of Cloudflare's "[email protected]", thumbnails point at `images/generated/` instead of `image.php`, and page links use clean URLs (`sd`) where live uses `sd.php`.

### index  (83% text match)
Live: https://www.weldengineering.com/
- Text only on the **live** page:
  - `Close Search Box [X]`
  - `Weld Engineering Co., Inc.`
  - `[siq_searchbox type="search-bar" placeholder="Search here" post-types="post,page" width="500" placement="left"]`
  - `The Weld Engineering Blog`
- Links/images on live but **not** in built: `#`, `ir.php`, `wp-content/plugins/easing-slider/images/indicator.gif`
- Links/images in built but not on live: `assets/easing-slider/images/indicator.gif`, `mailto:sales@weldengineering.com?subject=Product%20Information%20Request`

### new  (88% text match)
Live: https://www.weldengineering.com/new.php
- Text only on the **live** page:
  - `Close Search Box [X]`
  - `Weld Engineering Co., Inc.`
  - `[siq_searchbox type="search-bar" placeholder="Search here" post-types="post,page" width="500" placement="left"]`
  - `HPT-100-850°`
  - `150LB. (portable) or 700LB. storage capacity.`
  - `Powerful 1000 watt heating elements. (Uses specially designed elements to prevent localized overheating of flux.)`
  - `Temperature range from 200°F to 850°F (93°C to 454°C).`
  - `Accurate temperature control.`
  - `Large thermometer indicates temperature in both °F and °C for ease of use.`
  - `By a simple push of a button, the HTP-100-850 & HTS-700-850 rebake flux at an adjustable temperature for an adjustable time (3 min. to 5hrs., factory set at 2hr`
  - `150LB. (portable) or 700LB. storage capacity.`
  - `Powerful 1000 watt heating elements. (Uses specially designed elements to prevent localized overheating of flux.)`
  - `Temperature range from 175°F to 550°F (79°C to 288°C) standard. FO-700HT-AB & FO-700HT-AB range from 300°F to 700°F (148°C to 371°C).`
  - `Accurate temperature control.`
  - `Large thermometer indicates temperature in both °F and °C for ease of use.`
  - ...and 1 more
- Text only on the **built** page:
  - `HTP-100-850°`
  - `100LB. (portable) or 700LB. storage capacity.`
  - `Powerful 1500 watt (HTP-100-850) or 4500 watt (HTS-700-850) heating elements. (Uses specially designed elements to prevent localized overheating of flux.)`
  - `Total and uniform heating of flux. (Heating elements extend through the flux, insuring total heat transfer. Most flux particles are no more than 3″ from a heati`
  - `Temperature range up to 850°F (454°C).`
  - `Accurate digital temperature control.`
  - `Digital control shows temperature in highly visible, bright numbers for ease of use.`
  - `By a simple push of a button, the HTP-100-850 & HTS-700-850 rebake flux at an adjustable temperature for an adjustable time (1 min. to 999 hrs., factory set at `
  - `100LB. (portable) or 700LB. storage capacity.`
  - `Powerful 1000 watt (PFO-100 series) or 4500 watt (FO-700HT series) heating elements. (Uses specially designed elements to prevent localized overheating of flux.`
  - `Temperature range up to 550°F (288°C) standard. FO-700HT-AB & FO-700HT range up to 700°F (371°C).`
  - `Accurate digital temperature control.`
  - `Large digital display indicates temperature in both °F and °C for ease of use.`
  - `By a simple push of a button, the PFO-100-AB and FO-700HT-AB rebake flux at an adjustable temperature for an adjustable time (1 min. to 999 hrs., factory set at`
- Links/images on live but **not** in built: `cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js`

### sd  (99% text match)
Live: https://www.weldengineering.com/sd.php
- Text only on the **live** page:
  - `Close Search Box [X]`
  - `Weld Engineering Co., Inc.`
  - `[siq_searchbox type="search-bar" placeholder="Search here" post-types="post,page" width="500" placement="left"]`
- Links/images on live but **not** in built: `cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js`

### hd  (99% text match)
Live: https://www.weldengineering.com/hd.php
- Text only on the **live** page:
  - `Close Search Box [X]`
  - `Weld Engineering Co., Inc.`
  - `[siq_searchbox type="search-bar" placeholder="Search here" post-types="post,page" width="500" placement="left"]`
- Text only on the **built** page:
  - `MM-7500X/P dust filter chamber has a hopper bottom instead of a dust drawer. This enables continuous dumping of dust to a much larger dust container below the M`
- Links/images on live but **not** in built: `cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js`

### pf  (95% text match)
Live: https://www.weldengineering.com/pf.php
- Text only on the **live** page:
  - `Close Search Box [X]`
  - `Weld Engineering Co., Inc.`
  - `[siq_searchbox type="search-bar" placeholder="Search here" post-types="post,page" width="500" placement="left"]`
  - `The PT-“x”00 is a flux pressure feed tank system for pressure feeding flux to a flux hopper or weldinf torch.`
  - `HLPFR-3000 is the same as the LPFR-3000 except it is heated under continuous control upto 250°F (122°C).`
  - `HPFR-3000 is the same as the PFR-3000 except it is heated under continuous control upto 250°F (122°C). Either or both the hopper and tank may be heated.`
- Text only on the **built** page:
  - `The PT-“x”00 is a flux pressure feed tank system for pressure feeding flux to a flux hopper or welding torch.`
  - `HLPFR-3000 is the same as the LPFR-3000 except it is heated under continuous control upto 250°F (121°C).`
  - `HPFR-3000 is the same as the PFR-3000 except it is heated under continuous control upto 250°F (121°C). Either or both the hopper and tank may be heated.`
- Links/images on live but **not** in built: `catalog/Prod_Sel_Pgs_w_Index/#p=30#MagSep`, `catalog/Prod_Sel_Pgs_w_Index/#p=57#TankOptions`, `catalog/Prod_Sel_Pgs_w_Index/#p=57#TankSensor`, `catalog/Prod_Sel_Pgs_w_Index/#p=57#magsep100`, `cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js`
- Links/images in built but not on live: `catalog/Prod_Sel_Pgs_w_Index/#p=30`, `catalog/Prod_Sel_Pgs_w_Index/#p=57`

### ham  (95% text match)
Live: https://www.weldengineering.com/ham.php
- Text only on the **live** page:
  - `Close Search Box [X]`
  - `Weld Engineering Co., Inc.`
  - `[siq_searchbox type="search-bar" placeholder="Search here" post-types="post,page" width="500" placement="left"]`
- Text only on the **built** page:
  - `Top hopper has two 50 pound capacity sections, one for recovered flux and one for new flux.`
- Links/images on live but **not** in built: `catalog/Prod_Sel_Pgs_w_Index/#p=30#MagSep`, `catalog/Prod_Sel_Pgs_w_Index/#p=30#tank_nozzles`, `catalog/Prod_Sel_Pgs_w_Index/#p=57#Electronic_sensor`, `catalog/Prod_Sel_Pgs_w_Index/#p=57#magsep100`, `cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js`
- Links/images in built but not on live: `catalog/Prod_Sel_Pgs_w_Index/#p=30`, `catalog/Prod_Sel_Pgs_w_Index/#p=57`

### ro  (55% text match)
Live: https://www.weldengineering.com/ro.php
- Text only on the **live** page:
  - `Close Search Box [X]`
  - `Weld Engineering Co., Inc.`
  - `[siq_searchbox type="search-bar" placeholder="Search here" post-types="post,page" width="500" placement="left"]`
  - `Typically holds over 700 lb. (226 Kg) of flux. (Weight will vary depending on type and density of flux.)`
  - `Powerful 4000 watt heating elements (Uses “low watt density” elements to prevent localized over heating of flux)`
  - `Total and uniform heating of flux. (Heating elements extend through the flux, insuring total heat transfer. Most flux particles are no more than 2″ from a heati`
  - `High temperature range from 200°F to 850°F (93°C to 454°C).`
  - `By a simple push of a button, the HTS-700-850 re-bakes flux at an adjustable temperature of 200°F (93°C) to 850°F (454°C) for an adjustable time (3 min. to 5hrs`
  - `Automatically resets to an adjustable storage temperature of 175°F (79°C) to 550°F (288°C) after bake cycle.`
  - `Large control knobs and push buttons make operation very easy.`
  - `Typically holds over 100 lb. (45.4 Kg) of flux. (Weight will vary depending on type and density of flux.)`
  - `Temperature range from 200°F to 850°F (93°C to 454°C)`
  - `Accurate temperature control`
  - `Large thermometer for easy reading (both °F and °C)`
  - `By a simple push of a button, the HPT-100-850 re-bakes flux at an adjustable temperature of 200°F (93°C) to 850°F (454°C) for an adjustable time (3 min. to 5hrs`
  - ...and 24 more
- Text only on the **built** page:
  - `Typically holds over 700 lb. (318 Kg) of flux. (Weight will vary depending on type and density of flux.)`
  - `Powerful 4500 watt heating elements (Uses “low watt density” elements to prevent localized over heating of flux)`
  - `Total and uniform heating of flux. (Heating elements extend through the flux, insuring total heat transfer. Most flux particles are no more than 3″ from a heati`
  - `High temperature range up to 850°F (454°C).`
  - `By a simple push of a button, the HTS-700-850 re-bakes flux at an adjustable temperature up to 850°F (454°C) for an adjustable time (1 min. to 999 hrs., factory`
  - `Automatically resets to an adjustable storage temperature up to 850°F (454°C) after bake cycle.`
  - `Digital control provides accurate temperature control and highly visible, bright numbers.`
  - `Typically holds over 100 lb. (46 Kg) of flux. (Weight will vary depending on type and density of flux.)`
  - `Powerful 1500 watt heating elements`
  - `Total uniform heating of flux. Most flux particles are no more than 3″ from a heating element.`
  - `Temperature range up to 850°F (454°C)`
  - `Accurate digital temperature control`
  - `Highly visible, bright digital numbers for easy reading`
  - `By a simple push of a button, the HTP-100-850 re-bakes flux at an adjustable temperature up to 850°F (454°C) for an adjustable time (1 min. to 999 hrs., factory`
  - `Automatically resets to an adjustable storage temperature up to 850°F (454°C) after bake cycle.`
  - ...and 25 more
- Links/images on live but **not** in built: `cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js`

### tb  (99% text match)
Live: https://www.weldengineering.com/tb.php
- Text only on the **live** page:
  - `Close Search Box [X]`
  - `Weld Engineering Co., Inc.`
  - `[siq_searchbox type="search-bar" placeholder="Search here" post-types="post,page" width="500" placement="left"]`
- Links/images on live but **not** in built: `#`, `cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js`

### calc  (96% text match)
Live: https://www.weldengineering.com/calc.php
- Text only on the **live** page:
  - `Close Search Box [X]`
  - `Weld Engineering Co., Inc.`
  - `[siq_searchbox type="search-bar" placeholder="Search here" post-types="post,page" width="500" placement="left"]`
- Links/images on live but **not** in built: `#`

### mission  (88% text match)
Live: https://www.weldengineering.com/mission.php
- Text only on the **live** page:
  - `Close Search Box [X]`
  - `Weld Engineering Co., Inc.`
  - `[siq_searchbox type="search-bar" placeholder="Search here" post-types="post,page" width="500" placement="left"]`
- Links/images on live but **not** in built: `#`

### map  (91% text match)
Live: https://www.weldengineering.com/map.php
- Text only on the **live** page:
  - `Close Search Box [X]`
  - `[siq_searchbox type="search-bar" placeholder="Search here" post-types="post,page" width="500" placement="left"]`
- Links/images on live but **not** in built: `#`, `ir.php`
- Links/images in built but not on live: `mailto:sales@weldengineering.com?subject=Product%20Information%20Request`

