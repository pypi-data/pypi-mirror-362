# image renderer widget tests.
# for coverage, run:
# coverage run -m pytest -s
# or if you want to include branches:
# coverage run --branch -m pytest
# followed by:
# coverage report -i or coverage html

import os.path

import numpy
import pytest
import skimage.io as skio

import climax


FIXTURE_DIR: str = os.path.join(os.path.split(os.path.split(climax.__file__)[0])[0], "tests", "fixtures")
GRAY_STACK_FIXTURE: str = "gray_stack.tif"
COLOUR_STACK_FIXTURE: str = "colour_stack.tif"


@pytest.fixture
def climax_gray_fixture() -> climax.climax.climax:
    return climax.climax.climax(os.path.join(FIXTURE_DIR, GRAY_STACK_FIXTURE))  

@pytest.fixture
def climax_colour_fixture() -> climax.climax.climax:
    return climax.climax.climax(os.path.join(FIXTURE_DIR, COLOUR_STACK_FIXTURE))

@pytest.fixture
def gray_stack_fixture() -> numpy.ndarray:
    return skio.imread(os.path.join(FIXTURE_DIR, GRAY_STACK_FIXTURE))

@pytest.fixture
def colour_stack_fixture() -> numpy.ndarray:
    return skio.imread(os.path.join(FIXTURE_DIR, COLOUR_STACK_FIXTURE))

@pytest.fixture
def climax_gray_path_fixture() -> str:
    return os.path.join(FIXTURE_DIR, GRAY_STACK_FIXTURE)  
