from pytwincatparser.parse_declaration import get_var

def test_get_var():
    # Test case 1
    test_str1 = r"""

	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
    """
    expected1 = ["_bLicenseOk1 							: BOOL;","_bLicenseOk2 							: BOOL;"]
    result1 = get_var(test_str1)
    assert result1 == expected1, f"Test case 1 failed. Expected: {expected1}, Got: {result1}"

    # Test case 2
    test_str2 = r"""PERSISTENT

	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
     """
    expected2 = ["_bLicenseOk1 							: BOOL;","_bLicenseOk2 							: BOOL;"]
    result2 = get_var(test_str2)
    assert result2 == expected2, f"Test case 2 failed. Expected: {expected2}, Got: {result2}"

    # Test case 3
    test_str3 = r"""PERSISTENT
        // this and that
	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
     """
    expected3 = ["_bLicenseOk1 							: BOOL;","_bLicenseOk2 							: BOOL;"]
    result3 = get_var(test_str3)
    assert result3 == expected3, f"Test case 3 failed. Expected: {expected3}, Got: {result3}"

    # Test case 4
    test_str4 = r"""PERSISTENT
        (* this or that *)
	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
     """
    expected4  = ["_bLicenseOk1 							: BOOL;","_bLicenseOk2 							: BOOL;"]
    result4 = get_var(test_str4)
    assert result4 == expected4, f"Test case 4 failed. Expected: {expected4}, Got: {result4}"

    # Test case 5
    test_str5 = r"""

	    _bLicenseOk1 							: BOOL; // this or that
	    _bLicenseOk2 							: BOOL; // this or those
    """
    expected5 = ["_bLicenseOk1 							: BOOL; // this or that","_bLicenseOk2 							: BOOL; // this or those"]
    result5 = get_var(test_str5)
    assert result5 == expected5, f"Test case 5 failed. Expected: {expected5}, Got: {result5}"

    # Test case 6
    test_str6 = r"""

	    _bLicenseOk1 							: BOOL; // this or that (* multiline comment
        goes over multilines*)
	    _bLicenseOk2 							: BOOL; // this or those
    """
    expected6 = ["""_bLicenseOk1 							: BOOL; // this or that (* multiline comment
        goes over multilines*)""","""_bLicenseOk2 							: BOOL; // this or those"""]
    result6 = get_var(test_str6)
    assert result6 == expected6, f"Test case 6 failed. Expected: {expected6}, Got: {result6}"

    # Test case 7
    test_str7 = r"""

	    _bLicenseOk1 							: BOOL; // this or that
        (* multiline comment
        goes over multilines BUT NOT after var decl*)
	    _bLicenseOk2 							: BOOL; // this or those
    """
    expected7 = ["""_bLicenseOk1 							: BOOL; // this or that""","""_bLicenseOk2 							: BOOL; // this or those"""]
    result7 = get_var(test_str7)
    assert result7 == expected7, f"Test case 7 failed. Expected: {expected7}, Got: {result7}"

    # Test case 8
    test_str8 = r"""
        {attribute : hide}
	    _bLicenseOk1 							: BOOL; // this or that

	    _bLicenseOk2 							: BOOL; // this or those
    """
    expected8 = ["""{attribute : hide}
	    _bLicenseOk1 							: BOOL; // this or that""","""_bLicenseOk2 							: BOOL; // this or those"""]
    result8 = get_var(test_str8)
    assert result8 == expected8, f"Test case 8 failed. Expected: {expected8}, Got: {result8}"

    # Test case 9
    test_str9 = r"""
        {attribute : hide}
	    _bLicenseOk1 							: BOOL; // this or that
        {something other than that}
	    _bLicenseOk2 							: BOOL; // this or those
    """
    expected9 = ["""{attribute : hide}
	    _bLicenseOk1 							: BOOL; // this or that""","""{something other than that}
	    _bLicenseOk2 							: BOOL; // this or those"""]
    result9 = get_var(test_str9)
    assert result9 == expected9, f"Test case 9 failed. Expected: {expected9}, Got: {result9}"

    # Test case 10
    test_str10 = r"""

	    _bLicenseOk1, multipleVar, multipleVar2							: BOOL; // this or that
	    _bLicenseOk2 							: BOOL; // this or those
    """
    expected10 = [""" _bLicenseOk1, multipleVar, multipleVar2							: BOOL; // this or that""","""_bLicenseOk2 							: BOOL; // this or those"""]
    result10 = get_var(test_str10)
    assert result10 == expected10, f"Test case 10 failed. Expected: {expected10}, Got: {result10}"

    # Test case 11
    test_str11 = r"""

	    _bLicenseOk1, multipleVar, multipleVar2							: BOOL; // this or that
	    _bLicenseOk2 							: BOOL := FALSE; // this or those
    """
    expected11 = [""" _bLicenseOk1, multipleVar, multipleVar2							: BOOL; // this or that""","""_bLicenseOk2 							: BOOL := FALSE; // this or those"""]
    result11 = get_var(test_str11)
    assert result11 == expected11, f"Test case 11 failed. Expected: {expected11}, Got: {result11}"