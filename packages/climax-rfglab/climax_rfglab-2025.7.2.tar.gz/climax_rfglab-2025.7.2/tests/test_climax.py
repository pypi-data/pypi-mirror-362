# slider widget tests.
# for coverage, run:
# coverage run -m pytest -s
# or if you want to include branches:
# coverage run --branch -m pytest
# followed by:
# coverage report -i

import numpy
import pytest
import textual

from climax.climax import climax

@pytest.mark.usefixtures("climax_gray_fixture")
@pytest.mark.usefixtures("climax_gray_path_fixture")
def test_climax_initialization(climax_gray_fixture, climax_gray_path_fixture):
    a_climax_instance = climax(climax_gray_path_fixture)
    assert isinstance(a_climax_instance, climax)
    assert numpy.array_equal(a_climax_instance.volume, climax_gray_fixture.volume)
    assert numpy.array_equal(a_climax_instance.color, climax_gray_fixture.color)
    assert numpy.array_equal(a_climax_instance.slices, climax_gray_fixture.slices)

    for anelement, adtype in zip(climax_gray_fixture.compose(), [textual.widgets.Header, textual.containers.Vertical, textual.widgets.Footer]):
        assert isinstance(anelement, adtype)

    a_climax_instance = climax([climax_gray_path_fixture, climax_gray_path_fixture])
    assert isinstance(a_climax_instance, climax)
    assert a_climax_instance.volume.shape[-1] == climax_gray_fixture.volume.shape[-1] * 2
    assert numpy.array_equal(a_climax_instance.image_data[0, :, :a_climax_instance.image_data.shape[2]//2], climax_gray_fixture.image_data[0, :, :])

@pytest.mark.usefixtures("climax_gray_fixture")
def test_climax_basic(climax_gray_fixture):
    assert climax_gray_fixture is not None
    assert climax_gray_fixture.volume.ndim == 5
    assert climax_gray_fixture.color.shape == climax_gray_fixture.volume.shape[1:]
    assert climax_gray_fixture.slices.shape == climax_gray_fixture.volume.shape[2:]

@pytest.mark.usefixtures("climax_gray_fixture")
def test_climax_actions(climax_gray_fixture):
    climax_gray_fixture.action_next_slice()
    assert climax_gray_fixture.curslice == 1
    climax_gray_fixture.action_prev_slice()
    assert climax_gray_fixture.curslice == 0
    climax_gray_fixture.action_zoom()
    assert climax_gray_fixture.zoom_index == 1
    climax_gray_fixture.action_toggle_dark()
    assert climax_gray_fixture.theme == "textual-light"
    assert not climax_gray_fixture.action_toggle_dark()

@pytest.mark.usefixtures("climax_gray_fixture")
def test_climax_tui(climax_gray_fixture):
    # Test the TUI functionality
    climax_gray_fixture.Z_slider.value = 1
    climax_gray_fixture._Z_slider_change()
    assert climax_gray_fixture.curslice == 1
    climax_gray_fixture.Z_slider.value = 0
    climax_gray_fixture._Z_slider_change()    
    assert climax_gray_fixture.curslice == 0
    climax_gray_fixture.Z_slider.value = 1
    climax_gray_fixture._Z_slider_key()    
    assert climax_gray_fixture.curslice == 1
    climax_gray_fixture.Z_slider.value = 0
    climax_gray_fixture.continuous_update = False
    climax_gray_fixture._Z_slider_click()
    assert climax_gray_fixture.curslice == 0
    climax_gray_fixture.continuous_update = True
    climax_gray_fixture.vmax_slider.value = 10
    climax_gray_fixture.vmin_slider.value = climax_gray_fixture.vmax_slider.value + 1
    climax_gray_fixture._vmin_slider_change()
    assert climax_gray_fixture.vmin_slider.value == climax_gray_fixture.vmax_slider.value
    climax_gray_fixture.vmin_slider.value = 1
    climax_gray_fixture._update_switch_change()
    assert not climax_gray_fixture.continuous_update
    assert not climax_gray_fixture._vmin_slider_click()
    assert not climax_gray_fixture._vmax_slider_click()
    climax_gray_fixture._update_switch_change()
    assert climax_gray_fixture.continuous_update
    
    climax_gray_fixture.vmax_slider.value = climax_gray_fixture.vmin_slider.value - 1
    climax_gray_fixture._vmax_slider_change()
    assert climax_gray_fixture.vmin_slider.value == climax_gray_fixture.vmax_slider.value
    climax_gray_fixture.vmin_slider.value = climax_gray_fixture.vmax_slider.value + 1
    climax_gray_fixture._vmin_slider_key()
    assert climax_gray_fixture.vmin_slider.value == climax_gray_fixture.vmax_slider.value
    climax_gray_fixture.vmax_slider.value = climax_gray_fixture.vmin_slider.value - 1
    climax_gray_fixture._vmax_slider_key()
    assert climax_gray_fixture.vmax_slider.value == climax_gray_fixture.vmin_slider.value
    climax_gray_fixture.colormap_select.value = "gray"
    assert not climax_gray_fixture._cmap_changed()
    original_volume = climax_gray_fixture.volume.copy()
    climax_gray_fixture._rotate_button_press()
    assert not numpy.array_equal(climax_gray_fixture.volume, original_volume)

    climax_gray_fixture.volume = original_volume  # Reset volume
    climax_gray_fixture._flip_horizontal_button_press()
    assert not numpy.array_equal(climax_gray_fixture.volume, original_volume)
    climax_gray_fixture.volume = original_volume
    climax_gray_fixture._flip_vertical_button_press()
    assert not numpy.array_equal(climax_gray_fixture.volume, original_volume)
    climax_gray_fixture.volume = original_volume
    climax_gray_fixture._invert_switch_change()
    assert numpy.array_equal(climax_gray_fixture.volume, original_volume)
    climax_gray_fixture._invert_switch_change()
    assert numpy.array_equal(climax_gray_fixture.volume, original_volume)
    climax_gray_fixture._auto_contrast_pressed()
    assert climax_gray_fixture.vmin_slider.value == climax.mode(climax_gray_fixture.image_data[climax_gray_fixture.curslice,:,:].ravel())[0]
    assert climax_gray_fixture.vmax_slider.value == int(numpy.percentile(climax_gray_fixture.image_data[climax_gray_fixture.curslice,:,:], 99))
    
    climax_gray_fixture.volume = numpy.concatenate((climax_gray_fixture.volume, climax_gray_fixture.volume, climax_gray_fixture.volume), axis=1)
    climax_gray_fixture.volume = numpy.concatenate((climax_gray_fixture.volume, climax_gray_fixture.volume), axis=0)
    assert climax_gray_fixture.volume.shape == (2, 3, 5, 150, 30)
    climax_gray_fixture.color = climax_gray_fixture.volume[0]
    climax_gray_fixture.slices = climax_gray_fixture.color[0]
    climax_gray_fixture.pix_val_min_max = [numpy.min(climax_gray_fixture.color), numpy.max(climax_gray_fixture.color)]
    climax_gray_fixture.image_data = numpy.transpose(climax_gray_fixture.slices, climax.orientations[climax_gray_fixture.view_plane])
    climax_gray_fixture.display_slice(True, 0)
    climax_gray_fixture.time_slider.value = 1
    assert not climax_gray_fixture._time_slider_change()
    climax_gray_fixture.time_slider.value = 0
    assert not climax_gray_fixture._time_slider_key()
    climax_gray_fixture.time_slider.value = 1
    climax_gray_fixture.continuous_update = False
    assert not climax_gray_fixture._time_slider_click()
    climax_gray_fixture.channel_slider.value = 1
    climax_gray_fixture.continuous_update = True
    assert not climax_gray_fixture._channel_slider_change()
    climax_gray_fixture.channel_slider.value = 0
    assert not climax_gray_fixture._channel_slider_key()
    climax_gray_fixture.channel_slider.value = 1
    climax_gray_fixture.continuous_update = False
    assert not climax_gray_fixture._channel_slider_click()
    climax_gray_fixture.continuous_update = True