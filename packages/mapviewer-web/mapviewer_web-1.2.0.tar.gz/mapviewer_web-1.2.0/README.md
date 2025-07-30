
# MapViewer-Web: Visualizing galaxy properties from the GIST pipeline products

[![pypi](https://img.shields.io/badge/python-pypi-blue.svg)](https://pypi.org/project/mapviewer-web/)
[![LICENSE](https://img.shields.io/badge/lisence-MIT-blue.svg)](https://github.com/purmortal/mapviewer-web/blob/master/LICENSE)

Mapviewer-web is a web-based tool for visualizing galaxy properties analyzed by the [GIST Pipeline](https://gitlab.com/abittner/gist-development).
It is an enhanced adaptation of the original PyQt-based [Mapviewer](https://gitlab.com/abittner/gist-development/-/blob/master/gistPipeline/Mapviewer.py?ref_type=heads) widget, 
offering improved interactivity and easier access through web browsers. 
This web version also significantly reduces response times compared to its PyQt version.
![Alt text](example.jpg)

## Installation

### Using pip

```
pip install mapviewer-web
```

### From the git repo

```
git clone https://github.com/purmortal/mapviewer-web.git
cd mapviewer-web
pip install .
```

## Run Mapviewer-Web

In the terminal, just type:
```
Mapviewer-Web
```
The terminal will return an address (by default ``http://127.0.0.1:9928``) which can be opened by a browser.
Next, input the hardcoded path of GIST products, and click ``Load Database``.
Then you can inspect galaxy properties and spectra fitting for each Voaonoi bin as you wish.

To use a different port (e.g., 5800), type:
```
Mapviewer-Web --port 5800
```

To also allow remote access (your internet should have a static ip address), type:
```
Mapviewer-Web --port 5800 --mode remote
```

## Example

Follow the command below to inspect an example galaxy properties:

Download GIST products example
```
wget https://github.com/purmortal/mapviewer-web/archive/refs/heads/gistProducts.zip
unzip gistProducts.zip
```
Then, run ``Mapviewer-Web`` and open the browser. 
Input ``/your-download-path/mapviewer-web-gistProducts/NGC0000Example``,
and now you can explore this tool.

## License
This software is governed by the MIT License. In brief, you can use, distribute, and change this package as you want.


## Contact 
- Zixian Wang (University of Utah, wang.zixian.astro@gmail.com)
