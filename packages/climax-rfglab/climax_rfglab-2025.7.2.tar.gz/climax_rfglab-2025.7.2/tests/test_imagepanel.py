# slider widget tests.
# for coverage, run:
# coverage run -m pytest -s
# or if you want to include branches:
# coverage run --branch -m pytest
# followed by:
# coverage report -i

import numpy

from climax._imagepanel import ImagePanel

def test_imagepanel_basic():
    # Test basic initialization of ImagePanel
    image = numpy.random.randint(0, 256, (100, 100), dtype=numpy.uint8)  # Create a random grayscale image
    panel = ImagePanel(image)
    assert panel is not None
    assert panel.image is not None  # No image loaded initially
    assert panel.zoom_factor == 1.0  # Default zoom level

def test_imagepanel_rendering():
    # Test rendering functionality of ImagePanel
    image = numpy.random.randint(0, 256, (100, 100), dtype=numpy.uint8)  # Create a random grayscale image
    panel = ImagePanel(image)
    
    rendered_output = panel.render()  # Call the render method
    assert rendered_output is not None  # Should produce some output

