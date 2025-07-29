from pytwincatparser.parse_declaration import get_extend

def test_get_extend():
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase IMPLEMENTS I_Elementinformation, I_TestInterface, I_AnotherTestInterface""") == ["FB_SubBase", "FB_SubSubBase"]
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase""") == ["FB_SubBase", "FB_SubSubBase"]
    assert get_extend("""extends FB_SubBase, FB_SubSubBase""") == ["FB_SubBase", "FB_SubSubBase"]
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED""") == None
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED (* extends this and that *)""") == None
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED (* extends this and that *) EXTENDS FB_SubBase""") == ["FB_SubBase"]
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED // extends this and that """) == None
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED // extends this and that EXTENDS """) == None
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED EXTENDS FB_SubBase""") == ["FB_SubBase"]
    assert get_extend("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED IMPLEMENTS I_Elementinformation, I_TestInterface EXTENDS FB_SubBase""") == ["FB_SubBase"]
    assert get_extend("""FUNCTION_BLOCK FB_Base PROTECTED EXTENDS FB_SubBase implements I_AnotherTestInterface""") == ["FB_SubBase"]
