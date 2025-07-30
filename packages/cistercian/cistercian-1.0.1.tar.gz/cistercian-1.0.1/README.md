[![Cistercian](https://i.imgur.com/KCge7Lv.png)](https://github.com/teeale/Cistercian)
<h1 align="center">
  <b>Cistercian</b> - Image Generator for Cistercian Numerals
  <br>
</h1>

The medieval Cistercian numerals were developed by the Cistercian monastic order in the early thirteenth century. These numeral representations are compounded on a single stave to indicate more complex numbers. The Cistercians eventually abandoned the system in favor of the Arabic numerals, but marginal use outside the order continued until the early twentieth century.

This Python library will create an image of the relevant numeral based on the integer provided.

## Installation

Install from PyPi.

```
pip install cistercian
```

## Usage

The `create` function takes 4 arguments:
- The integer to convert.
- `background_colour`: Background colour of the image
- `line_colour`: Colour of the lines used to compose the numeral
- `height`: Image height. This uses a scale factor to ensure an appropriate image width

```py
import cistercian

>>> cistercian.create(3875, background_colour="teal", line_colour="black", height=350)
```