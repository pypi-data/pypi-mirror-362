# slider widget tests.
# for coverage, run:
# coverage run -m pytest -s
# or if you want to include branches:
# coverage run --branch -m pytest
# followed by:
# coverage report -i


import pytest
from textual import events
from textual.geometry import Offset

from climax._slider import Slider


pytest_plugins = ('pytest_asyncio',)


def test_slider_value_clamping():
    slider = Slider(min=0, max=10, step=1)
    slider.value = 15
    assert slider.value == 10
    assert int(slider._slider_position) == 90
    slider.value = -5
    assert slider.value == 0
    assert int(slider._slider_position) == 0

def test_slider_step():
    slider = Slider(min=0, max=10, step=2)
    slider.value = 4
    assert slider.value == 4
    slider.action_slide_right()
    assert slider.value == 6
    slider.action_slide_left()
    assert slider.value == 4

@pytest.mark.asyncio
async def test_key_press():
    slider = Slider(min=0, max=10, step=1)
    slider.value = 5
    await slider._on_key(events.Key("right", None))
    assert slider.value == 6
    await slider._on_key(events.Key("left", None))
    assert slider.value == 5


@pytest.mark.asyncio
async def test_mouse_click():
    slider = Slider(min=0, max=10, step=1)
    slider.value = 5
    assert slider._grabbed is None
    slider._on_mouse_capture(events.MouseCapture(Offset(0, 0)))
    assert slider._grabbed is not None
    await slider._on_mouse_move(events.MouseMove(0, 0, 0, 0, 0, False, False, False, 0, 0, None))
    assert slider.value == 5  # No change since mouse didn't move
    await slider._on_click(events.Click(0, 0, 0, 0, 0, False, False, False, 0, 0, None))
    assert slider.value == 5