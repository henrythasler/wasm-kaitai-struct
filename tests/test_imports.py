import pytest 
from webassembly import Webassembly

def test_sections():
    module = Webassembly.from_file('tests/assets/all_imports.wasm')
    
    assert module.magic == b'\x00asm'
    assert module.version == 1
    assert len(module.sections) == 6

    expected = [
        {"id": Webassembly.SectionId["type_section"], "len": 30},
        {"id": Webassembly.SectionId["import_section"], "len": 98},
        {"id": Webassembly.SectionId["function_section"], "len": 5},
        {"id": Webassembly.SectionId["global_section"], "len": 8},
        {"id": Webassembly.SectionId["export_section"], "len": 56},
        {"id": Webassembly.SectionId["code_section"], "len": 59},
    ]

    for i, section in enumerate(module.sections):
        assert section.id == expected[i]["id"]
        assert section.len_content.value == expected[i]["len"]

def test_imports():
    module = Webassembly.from_file('tests/assets/all_imports.wasm')
    import_section = next(filter(lambda x: x.id == Webassembly.SectionId["import_section"], module.sections))
    assert import_section.id == Webassembly.SectionId["import_section"]

    assert import_section.content.num_imports.value == 7
    assert len(import_section.content.imports) == 7

    expected = [
        {"module": "env", "name": "log", "type": Webassembly.ImportTypes.func_type, "desc": 0},
        {"module": "env", "name": "add", "type": Webassembly.ImportTypes.func_type, "desc": 1},
        {"module": "env", "name": "divide", "type": Webassembly.ImportTypes.func_type, "desc": 2},
        {"module": "env", "name": "table", "type": Webassembly.ImportTypes.table_type, "elemtype": Webassembly.Types.element,"min": 10, "flags": 0},
        {"module": "env", "name": "memory", "type": Webassembly.ImportTypes.mem_type, "min": 1, "flags": 0},
        {"module": "env", "name": "globalConst", "type": Webassembly.ImportTypes.global_type},
        {"module": "env", "name": "globalMut", "type": Webassembly.ImportTypes.global_type},
    ]

    for i, item in enumerate(import_section.content.imports):
        assert item.module.value == expected[i]["module"]
        assert item.name.value == expected[i]["name"]
        assert item.import_type == expected[i]["type"]

        if item.import_type == Webassembly.ImportTypes.func_type:
            assert item.importdesc.value == expected[i]["desc"]
        elif item.import_type == Webassembly.ImportTypes.table_type:
            assert item.importdesc.elemtype == expected[i]["elemtype"]
            assert item.importdesc.limits.flags == expected[i]["flags"]
            assert item.importdesc.limits.min.value == expected[i]["min"]
        elif item.import_type == Webassembly.ImportTypes.mem_type:
            assert item.importdesc.limits.flags == expected[i]["flags"]
            assert item.importdesc.limits.min.value == expected[i]["min"]            