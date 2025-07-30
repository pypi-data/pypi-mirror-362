from w2n_converter import convert

def test_to_convert():
    assert convert("Apple") == [1, 16, 16, 12, 5]
    assert convert("Python123") == [16, 25, 20, 8, 15, 14]
    assert convert("HELLO") == [8, 5, 12, 12, 15]
