from pytwincatparser.parse_declaration import get_var_content

def test_get_var_content():
    # Test case 1
    test_str1 = r"""_bLicenseOk1 							: BOOL;"""
    expected1 = [{"name":"_bLicenseOk1","type":"BOOL", "init":"","attributes":[],r"comments":""}]
    result1 = get_var_content(test_str1)
    assert result1 == expected1, f"Test case 1 failed. Expected: {expected1}, Got: {result1}"

    # Test case 2
    test_str2 = r"""_bLicenseOk1 							: BOOL; // comment"""
    expected2 = [{"name":"_bLicenseOk1","type":"BOOL", "init":"","attributes":[],"comments":r"// comment"}]
    result2 = get_var_content(test_str2)
    assert result2 == expected2, f"Test case 2 failed. Expected: {expected2}, Got: {result2}"

    # Test case 3
    test_str3 = r"""_bLicenseOk1 							: BOOL := TRUE; // comment"""
    expected3 = [{"name":"_bLicenseOk1","type":"BOOL", "init":"TRUE","attributes":[],"comments":r"// comment"}]
    result3 = get_var_content(test_str3)
    assert result3 == expected3, f"Test case 3 failed. Expected: {expected3}, Got: {result3}"

    # Test case 4
    test_str4 = r"""_bLicenseOk1 							: BOOL := (bValue := FALSE); // comment"""
    expected4 = [{"name":"_bLicenseOk1","type":"BOOL", "init":"(bValue := FALSE)","attributes":[],"comments":r"// comment"}]
    result4 = get_var_content(test_str4)
    assert result4 == expected4, f"Test case 4 failed. Expected: {expected4}, Got: {result4}"

    # Test case 5
    test_str5 = r"""_bLicenseOk1 							: BOOL; (* multiline comment *)"""
    expected5 = [{"name":"_bLicenseOk1","type":"BOOL", "init":"","attributes":[],"comments":r"(* multiline comment *)"}]
    result5 = get_var_content(test_str5)
    assert result5 == expected5, f"Test case 5 failed. Expected: {expected5}, Got: {result5}"

    # Test case 6
    test_str6 = r"""_bLicenseOk1 							: BOOL; (* multiline 
    true comment *)"""
    expected6 = [{"name":"_bLicenseOk1","type":"BOOL", "init":"","attributes":[],"comments":r"""(* multiline 
    true comment *)"""}]
    result6 = get_var_content(test_str6)
    assert result6 == expected6, f"Test case 6 failed. Expected: {expected6}, Got: {result6}"

    # Test case 7
    test_str7 = r"""{attribute : hide}
	    _bLicenseOk1 							: BOOL; // this or that"""
    expected7 = [{"name":"_bLicenseOk1","type":"BOOL", "init":"","attributes":["{attribute : hide}"],"comments":r"// this or that"}]
    result7 = get_var_content(test_str7)
    assert result7 == expected7, f"Test case 7 failed. Expected: {expected7}, Got: {result7}"

    # Test case 8
    test_str8 = r"""_bLicenseOk1, multipleVar, multipleVar2							: BOOL; // this or that"""
    expected8 = [{"name":"_bLicenseOk1","type":"BOOL", "init":"","attributes":[],"comments":r"// this or that"},{"name":"multipleVar","type":"BOOL", "init":"","attributes":[],"comments":r"// this or that"},{"name":"multipleVar2","type":"BOOL", "init":"","attributes":[],"comments":r"// this or that"}]
    result8 = get_var_content(test_str8)
    assert result8 == expected8, f"Test case 8 failed. Expected: {expected8}, Got: {result8}"

    # Test case 9
    test_str9 = r"""{attribute : hide}
        _bLicenseOk1, multipleVar, multipleVar2							: BOOL; // this or that"""
    expected9 = [{"name":"_bLicenseOk1","type":"BOOL", "init":"","attributes":["{attribute : hide}"],"comments":r"// this or that"},{"name":"multipleVar","type":"BOOL", "init":"","attributes":["{attribute : hide}"],"comments":r"// this or that"},{"name":"multipleVar2","type":"BOOL", "init":"","attributes":["{attribute : hide}"],"comments":r"// this or that"}]
    result9 = get_var_content(test_str9)
    assert result9 == expected9, f"Test case 9 failed. Expected: {expected9}, Got: {result9}"

    # Test case 10
    test_str10 = r"""_bLicenseOk1 							: BOOL; (* multiline 
    true comment *)(* another comment*)"""
    expected10 = [{"name":"_bLicenseOk1","type":"BOOL", "init":"","attributes":[],"comments":r"""(* multiline 
    true comment *)(* another comment*)"""}]
    result10 = get_var_content(test_str10)
    assert result10 == expected10, f"Test case 10 failed. Expected: {expected10}, Got: {result10}"

