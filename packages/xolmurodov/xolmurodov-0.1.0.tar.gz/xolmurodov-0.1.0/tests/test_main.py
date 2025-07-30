from xolmurodov import resume

def test_about_contains_name():
    content = resume.about()
    assert "XOLMURODOV DIYORBEK" in content
