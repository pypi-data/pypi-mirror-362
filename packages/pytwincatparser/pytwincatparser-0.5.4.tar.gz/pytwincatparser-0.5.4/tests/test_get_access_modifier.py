from pytwincatparser.parse_declaration import get_access_modifier

def test_get_access_modifier():
    assert get_access_modifier("""FUNCTION_BLOCK FB_Base ABSTRACT Private Extends FB_SubBase, FB_SubSubBase IMPLEMENTS I_Elementinformation, I_TestInterface, I_AnotherTestInterface""") == "Private"
    assert get_access_modifier("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase""") == "PROTECTED"
    assert get_access_modifier("""extends FB_SubBase, FB_SubSubBase""") == None
    assert get_access_modifier("""FUNCTION_BLOCK FB_Base ABSTRACT INTERNAL""") == "INTERNAL"
    assert get_access_modifier("""FUNCTION_BLOCK FB_Base PROTECTED ABSTRACT EXTENDS FB_SubBase""") == "PROTECTED"
    assert get_access_modifier("""METHOD FB_Base ABSTRACT PUBLIC IMPLEMENTS I_Elementinformation, I_TestInterface EXTENDS FB_SubBase""") == "PUBLIC"
    assert get_access_modifier("""FUNCTION_BLOCK FB_Base ABSTRACT EXTENDS FB_SubBase implements I_AnotherTestInterface""") == None
