import graphics
import pytest
import random

expected_colors = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black',
                   'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate',
                   'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod',
                   'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
                   'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray',
                   'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey',
                   'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite',
                   'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred',
                   'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue',
                   'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey',
                   'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey',
                   'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon',
                   'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen',
                   'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue',
                   'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab',
                   'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred',
                   'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown',
                   'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver',
                   'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal',
                   'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']


def test_getColorsList():
    assert graphics.getColorsList() == expected_colors


def assert_valid_color(x):
    assert type(x) == tuple and len(x) == 4
    r, g, b, a = x
    assert type(r) == int and type(g) == int and type(b) == int and type(a) == int
    assert 0 <= r < 256 and 0 <= g < 256 and 0 <= b < 256 and 0 <= a < 256


def test_lookupColor_correct():
    for color in expected_colors:
        assert_valid_color(graphics.lookupColor(color))


def test_lookupColor_missing():
    for color in expected_colors:
        with pytest.raises(ValueError) as vale:
            graphics.lookupColor(color + "a")
        assert "Unknown color name" in str(vale)


def test_lookupColor_simple():
    ran = range(1, 255)
    elems = [0, 255] + [random.choice(ran) for i in range(0, 10)]
    for r in elems:
        for g in elems:
            for b in elems:
                assert graphics.lookupColor((r, g, b)) == (r, g, b, 255)
                for a in elems:
                    assert graphics.lookupColor((r, g, b, a)) == (r, g, b, a)


def test_lookupColor_hex_6_8():
    ran = range(1, 255)
    elems = [0, 255] + [random.choice(ran) for i in range(0, 10)]
    for r in elems:
        for g in elems:
            for b in elems:
                assert graphics.lookupColor("#%.2x%.2x%.2x" % (r, g, b)) == (r, g, b, 255)
                for a in elems:
                    assert graphics.lookupColor("#%.2x%.2x%.2x%.2x" % (r, g, b, a)) == (r, g, b, a)


def test_lookupColor_hex_3_4():
    ran = range(1, 15)
    elems = [0, 15] + [random.choice(ran) for i in range(0, 4)]
    for r in elems:
        for g in elems:
            for b in elems:
                assert graphics.lookupColor("#%.1x%.1x%.1x" % (r, g, b)) == (r * 17, g * 17, b * 17, 255)
                for a in elems:
                    assert graphics.lookupColor("#%.1x%.1x%.1x%.1x" % (r, g, b, a)) == (r * 17, g * 17, b * 17, a * 17)


def test_lookupColor_hex_wrong_count():
    ran = range(1, 15)
    elems = [0, 15] + [random.choice(ran) for i in range(0, 4)]
    for i in range(0, 16):
        h = "%.1x" % i
        for n in range(0, 16):
            if n in (3, 4, 6, 8):
                continue
            with pytest.raises(ValueError) as vale:
                graphics.lookupColor("#" + h * n)
            assert "must have either 3, 4, 6, or 8 hex digits" in str(vale)


def test_lookupColor_hex_wrong_chars():
    goodfs = ["#%s00000", "#0%s0000", "#00%s000", "#000%s00", "#0000%s0", "#00000%s"]
    for i in range(0, 256):
        ic = chr(i)
        if ic in "0123456789abcdefABCDEF":
            continue
        for goodf in goodfs:
            with pytest.raises(ValueError) as vale:
                graphics.lookupColor(goodf % ic)
            assert "must only use hex digits" in str(vale)


def test_lookupColor_simple_wrong_component_number():
    for i in range(0, 256):
        for n in range(0, 10):
            if n == 3 or n == 4:
                continue
            with pytest.raises(ValueError) as vale:
                graphics.lookupColor((i,) * n)
            assert "components must have three or four elements" in str(vale)


def test_lookupColor_simple_wrong_component_type():
    for i in (0.1, False, "hello", "0"):
        for n in [3, 4]:
            with pytest.raises(ValueError) as vale:
                graphics.lookupColor((i,) * n)
            assert "specified with integer components" in str(vale)


def test_lookupColor_simple_wrong_component_range():
    for i in (-1, -255, -256, -1000, 256, 500, 1000):
        for n in [3, 4]:
            with pytest.raises(ValueError) as vale:
                graphics.lookupColor((i,) * n)
            assert "0 (minimum) to 255 (maximum)" in str(vale)


def test_lookupColor_not_str_tuple():
    for x in (0, 0.0, False, [0, 0, 0]):
        with pytest.raises(ValueError) as vale:
            graphics.lookupColor(x)
        assert "To specify a color, either use the " in str(vale)
