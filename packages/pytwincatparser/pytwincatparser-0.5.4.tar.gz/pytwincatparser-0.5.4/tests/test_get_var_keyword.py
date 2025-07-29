from pytwincatparser.parse_declaration import get_var_keyword

def test_get_var_keyword():
    # Test case 1
    test_str1 = r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """
    expected1 = None
    result1 = get_var_keyword(test_str1)
    assert result1 == expected1, f"Test case 1 failed. Expected: {expected1}, Got: {result1}"

    # Test case 2
    test_str2 = r""" PERSISTENT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """
    expected2 = ["PERSISTENT"]
    result2 = get_var_keyword(test_str2)
    assert result2 == expected2, f"Test case 2 failed. Expected: {expected2}, Got: {result2}"

    # Test case 3
    test_str3 = r""" PERSIstent
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """
    expected3 = ["PERSIstent"]
    result3 = get_var_keyword(test_str3)
    assert result3 == expected3, f"Test case 3 failed. Expected: {expected3}, Got: {result3}"

    # Test case 4
    test_str4 = r""" CONSTANT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """
    expected4 = ["CONSTANT"]
    result4 = get_var_keyword(test_str4)
    assert result4 == expected4, f"Test case 4 failed. Expected: {expected4}, Got: {result4}"

    # Test case 5
    test_str5 = r"""                            CONSTANT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """
    expected5 = ["CONSTANT"]
    result5 = get_var_keyword(test_str5)
    assert result5 == expected5, f"Test case 5 failed. Expected: {expected5}, Got: {result5}"

    # Test case 6
    test_str6 = r""" (* constant *)
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """
    expected6 = None
    result6 = get_var_keyword(test_str6)
    assert result6 == expected6, f"Test case 6 failed. Expected: {expected6}, Got: {result6}"

    # Test case 7
    test_str7 = r"""       
        // persistent
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """
    expected7 = None
    result7 = get_var_keyword(test_str7)
    assert result7 == expected7, f"Test case 7 failed. Expected: {expected7}, Got: {result7}"
