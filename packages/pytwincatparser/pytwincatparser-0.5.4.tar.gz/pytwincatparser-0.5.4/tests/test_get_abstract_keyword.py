from pytwincatparser.parse_declaration import get_abstract_keyword

def test_get_abstract_keyword():
    assert get_abstract_keyword("""FUNCTION_BLOCK FB_Base ABSTRACT Private Extends FB_SubBase, FB_SubSubBase IMPLEMENTS I_Elementinformation, I_TestInterface, I_AnotherTestInterface""") == "ABSTRACT"
    assert get_abstract_keyword("""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase""") == "ABSTRACT"
    assert get_abstract_keyword("""extends FB_SubBase, FB_SubSubBase""") == ""
    assert get_abstract_keyword("""FUNCTION_BLOCK FB_Base ABSTRACT INTERNAL""") == "ABSTRACT"
    assert get_abstract_keyword("""FUNCTION_BLOCK FB_Base PROTECTED  EXTENDS FB_SubBase""") == ""
    assert get_abstract_keyword("""METHOD FB_Base ABSTRACT PUBLIC IMPLEMENTS I_Elementinformation, I_TestInterface EXTENDS FB_SubBase""") == "ABSTRACT"
    assert get_abstract_keyword("""FUNCTION_BLOCK FB_Base  EXTENDS FB_SubBase implements I_AnotherTestInterface""") == ""
