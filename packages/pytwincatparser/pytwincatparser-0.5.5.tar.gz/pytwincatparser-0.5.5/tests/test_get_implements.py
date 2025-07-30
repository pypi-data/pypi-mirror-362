from pytwincatparser.parse_declaration import get_implements

def test_get_implements():
    assert get_implements("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase IMPLEMENTS I_Elementinformation, I_TestInterface, I_AnotherTestInterface""") == ["I_Elementinformation", "I_TestInterface", "I_AnotherTestInterface"]
    assert get_implements("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase""") == None
    assert get_implements("""extends FB_SubBase, FB_SubSubBase""") == None
    assert get_implements("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED""") == None
    assert get_implements("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED IMPLEMENTS FB_SubBase""") == ["FB_SubBase"]
    assert get_implements("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED IMPLEMENTS I_Elementinformation, I_TestInterface EXTENDS FB_SubBase""") == ["I_Elementinformation", "I_TestInterface"]
    assert get_implements("""FUNCTION_BLOCK FB_Base PROTECTED EXTENDS FB_SubBase implements I_AnotherTestInterface""") == ["I_AnotherTestInterface"]
