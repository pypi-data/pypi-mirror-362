from pytwincatparser.parse_declaration import get_comments

def test_get_comments():
    # Test case 1
    test_str1 = r"""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase IMPLEMENTS I_Elementinformation, I_TestInterface, I_AnotherTestInterface
                (*details This is a detail*)
                (*usage 
                this describes how to use this
                # It can have markdown

                ```
                someCode.someMethod();
                ```
                *)"""
    expected1 = {"comments":["(*details This is a detail*)","""(*usage 
                this describes how to use this
                # It can have markdown

                ```
                someCode.someMethod();
                ```
                *)"""]}
    result1 = get_comments(test_str1)
    assert result1 == expected1, f"Test case 1 failed. Expected: {expected1}, Got: {result1}"

    # Test case 2
    test_str2 = r"""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase IMPLEMENTS I_Elementinformation, I_TestInterface, I_AnotherTestInterface
                // this is a comment // this is not a comment
                (* here is a comment, // and here is a comment inside one *)"""
            
    expected2 = {"comments":["// this is a comment // this is not a comment","(* here is a comment, // and here is a comment inside one *)"]}
    result2 = get_comments(test_str2)
    assert result2 == expected2, f"Test case 2 failed. Expected: {expected2}, Got: {result2}"

    # Test case 3
    test_str3 = r"""FUNCTION_BLOCK FB_Base (* noice *) ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase IMPLEMENTS I_Elementinformation, I_TestInterface, I_AnotherTestInterface
                //////////// this a comment aswell
                (** this is a brurap comment *)"""
    expected3 = {"comments":["(* noice *)","//////////// this a comment aswell","(** this is a brurap comment *)"]}
    result3 = get_comments(test_str3)
    assert result3 == expected3, f"Test case 3 failed. Expected: {expected3}, Got: {result3}"

    # Test case 4
    test_str4 = r"""FUNCTION_BLOCK FB_Base ABSTRACT PROTECTED Extends FB_SubBase, FB_SubSubBase IMPLEMENTS I_Elementinformation, I_TestInterface, I_AnotherTestInterface
                // this is a comment // this is not a comment
                (* here is a comment, (* here is a comment inside a comment*) *)"""
            
    expected4 = {"comments":["// this is a comment // this is not a comment","(* here is a comment, (* here is a comment inside a comment*) *)"]}
    result4 = get_comments(test_str4)
    assert result4 == expected4, f"Test case 4 failed. Expected: {expected4}, Got: {result4}"