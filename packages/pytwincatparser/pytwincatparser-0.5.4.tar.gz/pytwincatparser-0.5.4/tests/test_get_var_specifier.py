from pytwincatparser.parse_declaration import get_var_specifier

def test_get_var_specifier():
    # Test case 1
    test_str1 = r"""Constant

	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
    """
    expected1 = ["Constant"]
    result1 = get_var_specifier(test_str1)
    assert result1 == expected1, f"Test case 1 failed. Expected: {expected1}, Got: {result1}"

    # Test case 2
    test_str2 = r"""PERSISTENT

	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
     """
    expected2 = ["PERSISTENT"]
    result2 = get_var_specifier(test_str2)
    assert result2 == expected2, f"Test case 2 failed. Expected: {expected2}, Got: {result2}"

    # Test case 3
    test_str3 = r"""//PERSISTENT
        // this and that
	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
     """
    expected3 = []
    result3 = get_var_specifier(test_str3)
    assert result3 == expected3, f"Test case 3 failed. Expected: {expected3}, Got: {result3}"

    # Test case 4
    test_str4 = r"""(*PERSISTENT*)
        (* this or that *)
	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
     """
    expected4  = []
    result4 = get_var_specifier(test_str4)
    assert result4 == expected4, f"Test case 4 failed. Expected: {expected4}, Got: {result4}"

    # Test case 5
    test_str5 = r"""RETAIN

	    _bLicenseOk1 							: BOOL; // this or that
	    _bLicenseOk2 							: BOOL; // this or those
    """
    expected5 = ["RETAIN"]
    result5 = get_var_specifier(test_str5)
    assert result5 == expected5, f"Test case 5 failed. Expected: {expected5}, Got: {result5}"

