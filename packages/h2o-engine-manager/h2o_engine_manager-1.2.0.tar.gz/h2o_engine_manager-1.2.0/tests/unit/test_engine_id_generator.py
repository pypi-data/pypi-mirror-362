import re

import pytest

from h2o_engine_manager.clients.engine_id.generator import generate_engine_id_candidate
from h2o_engine_manager.clients.engine_id.generator import sanitize_display_name


@pytest.mark.parametrize(
    "display_name,expected",
    [
        ("Valid Name", "valid-name"),
        ("133t", "t"),
        ("  what spaces?   ", "what-spaces"),
        ("", ""),
        ("_underscore", "underscore"),
        ("-dash-", "dash"),
        ("----", ""),
        ("Some very long but very useful display name for my most beloved artificial intelligence engine.",
         "some-very-long-but-very-useful-display-name-for-my-most-be"),
    ],
)
def test_sanitize_display_name(display_name, expected):
    assert sanitize_display_name(display_name=display_name) == expected


def test_generate_engine_rand():
    id1 = generate_engine_id_candidate(display_name="a", engine_type="dai", attempt=0)
    id2 = generate_engine_id_candidate(display_name="a", engine_type="dai", attempt=1)
    id3 = generate_engine_id_candidate(display_name="a", engine_type="dai", attempt=2)
    id4 = generate_engine_id_candidate(display_name="", engine_type="dai", attempt=0)
    id5 = generate_engine_id_candidate(display_name="", engine_type="dai", attempt=1)

    assert id1 == "a"

    pattern = re.compile("^a-[0-9]{4}$")
    assert pattern.match(id2)
    assert pattern.match(id3)
    assert id2 != id3

    assert id4 == "new-dai-engine"

    pattern = re.compile("^new-dai-engine-[0-9]{4}$")
    assert pattern.match(id5)
