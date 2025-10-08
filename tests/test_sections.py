import pytest 
from webassembly import Webassembly

def test_empty_module():
    module = Webassembly.from_file('tests/assets/empty.wasm')
    
    assert module.magic == b'\x00asm'
    assert module.version == 1
    assert len(module.sections) == 0


def test_complex_module():
    module = Webassembly.from_file('tests/assets/memtest.wasm')
    
    assert module.magic == b'\x00asm'
    assert module.version == 1
    assert len(module.sections) == 7

    expected = [
        {"id": Webassembly.SectionId["type_section"], "len": 19},
        {"id": Webassembly.SectionId["function_section"], "len": 13},
        {"id": Webassembly.SectionId["memory_section"], "len": 3},
        {"id": Webassembly.SectionId["export_section"], "len": 161},
        {"id": Webassembly.SectionId["code_section"], "len": 287},
        {"id": Webassembly.SectionId["data_section"], "len": 20},
        {"id": Webassembly.SectionId["custom_section"], "len": 62},
    ]

    for i, section in enumerate(module.sections):
        assert section.id == expected[i]["id"]
        assert section.len_content.value == expected[i]["len"]

def test_bad_magic():
    corrupted_data = b'\x00asn\x01\x00\x00\x00'
    
    with pytest.raises(Exception):
        Webassembly.from_bytes(corrupted_data)
