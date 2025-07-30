from pytwincatparser.parse_declaration import get_return

def test_get_return():
    # Test case 1
    test_str1 = r"""METHOD Method1 : BOOL

	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
    """
    expected1 = "BOOL"
    result1 = get_return(test_str1)
    assert result1 == expected1, f"Test case 1 failed. Expected: {expected1}, Got: {result1}"

    # Test case 2
    test_str2 = r"""METHOD Method1 : ST_RETURN

	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
     """
    expected2 = "ST_RETURN"
    result2 = get_return(test_str2)
    assert result2 == expected2, f"Test case 2 failed. Expected: {expected2}, Got: {result2}"

    # Test case 3
    test_str3 = r"""FUNCTION FunDoFun : LREAL
        // this and that
	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
     """
    expected3 = "LREAL"
    result3 = get_return(test_str3)
    assert result3 == expected3, f"Test case 3 failed. Expected: {expected3}, Got: {result3}"

    # Test case 4
    test_str4 = r"""FUNCTION FunDoFun : ARRAY[1..5] OF LREAL
        (* this or that *)
	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
     """
    expected4  = "ARRAY[1..5] OF LREAL"
    result4 = get_return(test_str4)
    assert result4 == expected4, f"Test case 4 failed. Expected: {expected4}, Got: {result4}"

    # Test case 5
    test_str5 = r"""PROPERTY MyProp : REFERENCE TO ST_Sample

	    _bLicenseOk1 							: BOOL; // this or that
	    _bLicenseOk2 							: BOOL; // this or those
    """
    expected5 = "REFERENCE TO ST_Sample"
    result5 = get_return(test_str5)
    assert result5 == expected5, f"Test case 5 failed. Expected: {expected5}, Got: {result5}"

    # Test case 6
    test_str6 = r"""PROPERTY MyProp : REFERENCE TO ST_Sample // some comment

	    _bLicenseOk1 							: BOOL; // this or that
	    _bLicenseOk2 							: BOOL; // this or those
    """
    expected6 = "REFERENCE TO ST_Sample"
    result6 = get_return(test_str6)
    assert result6 == expected6, f"Test case 6 failed. Expected: {expected6}, Got: {result6}"

    # Test case 7
    test_str7 = r"""PROPERTY MyProp : REFERENCE TO ST_Sample ("some comment") 

	    _bLicenseOk1 							: BOOL; // this or that
	    _bLicenseOk2 							: BOOL; // this or those
    """
    expected7 = "REFERENCE TO ST_Sample"
    result7 = get_return(test_str7)
    assert result7 == expected7, f"Test case 7 failed. Expected: {expected7}, Got: {result7}"

        # Test case 8
    test_str8 = r"""PROPERTY MyProp : ("some comment")  REFERENCE ("some comment")  TO ST_Sample ("some comment") 

	    _bLicenseOk1 							: BOOL; // this or that
	    _bLicenseOk2 							: BOOL; // this or those
    """
    expected8 = "REFERENCE TO ST_Sample"
    result8 = get_return(test_str8)
    assert result8 == expected8, f"Test case 8 failed. Expected: {expected8}, Got: {result8}"

        # Test case 9
    test_str9 = r"""METHOD Method1 : BOOL;

	    _bLicenseOk1 							: BOOL;
	    _bLicenseOk2 							: BOOL;
    """
    expected9 = "BOOL"
    result9 = get_return(test_str9)
    assert result9 == expected9, f"Test case 9 failed. Expected: {expected9}, Got: {result9}"
