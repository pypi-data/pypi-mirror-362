from pytwincatparser.parse_declaration import get_var_blocks

def test_get_var_blocks():
    # Test case 1
    test_str1 = r"""
    VAR_STAT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected1 = [{"name":"VAR_STAT",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result1 = get_var_blocks(test_str1)
    assert result1 == expected1, f"Test case 1 failed. Expected: {expected1}, Got: {result1}"

    # Test case 2
    test_str2 = r"""
    VAR
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected2 = [{"name":"VAR",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result2 = get_var_blocks(test_str2)
    assert result2 == expected2, f"Test case 2 failed. Expected: {expected2}, Got: {result2}"

    # Test case 3
    test_str3 = r"""
    VAR_INPUT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected3 = [{"name":"VAR_INPUT",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result3 = get_var_blocks(test_str3)
    assert result3 == expected3, f"Test case 3 failed. Expected: {expected3}, Got: {result3}"

    # Test case 4
    test_str4 = r"""
    VAR_IN_OUT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected4 = [{"name":"VAR_IN_OUT",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result4 = get_var_blocks(test_str4)
    assert result4 == expected4, f"Test case 4 failed. Expected: {expected4}, Got: {result4}"

    # Test case 5
    test_str5 = r"""
    VAR_OUTPUT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected5 = [{"name":"VAR_OUTPUT","content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result5 = get_var_blocks(test_str5)
    assert result5 == expected5, f"Test case 5 failed. Expected: {expected5}, Got: {result5}"

    # Test case 6
    test_str6 = r"""
    VAR_TEMP
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected6 = [{"name":"VAR_TEMP",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result6 = get_var_blocks(test_str6)
    assert result6 == expected6, f"Test case 6 failed. Expected: {expected6}, Got: {result6}"

    # Test case 7
    test_str7 = r"""
    VAR_INST
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected7 = [{"name":"VAR_INST",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result7 = get_var_blocks(test_str7)
    assert result7 == expected7, f"Test case 7 failed. Expected: {expected7}, Got: {result7}"

    # Test case 8
    test_str8 = r"""
    VAR_OUtput
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected8 = [{"name":"VAR_OUtput",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result8 = get_var_blocks(test_str8)
    assert result8 == expected8, f"Test case 8 failed. Expected: {expected8}, Got: {result8}"

    # Test case 9
    test_str9 = r"""
    VAR PERSISTENT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected9 = [{"name":"VAR",  "content":r""" PERSISTENT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result9 = get_var_blocks(test_str9)
    assert result9 == expected9, f"Test case 9 failed. Expected: {expected9}, Got: {result9}"

    # Test case 10
    test_str10 = r"""
    VAR CONSTANT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected10 = [{"name":"VAR",  "content":r""" CONSTANT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result10 = get_var_blocks(test_str10)
    assert result10 == expected10, f"Test case 10 failed. Expected: {expected10}, Got: {result10}"

    # Test case 11
    test_str11 = r"""
    VAR CONSTANT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR
    VAR
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected11 = [{"name":"VAR",  "content":r""" CONSTANT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """},
        {"name":"VAR",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result11 = get_var_blocks(test_str11)
    assert result11 == expected11, f"Test case 11 failed. Expected: {expected11}, Got: {result11}"

    # Test case 12
    test_str12 = r"""
    VAR_INPUT
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR
    VAR
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected12 = [{"name":"VAR_INPUT",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """},
        {"name":"VAR",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result12 = get_var_blocks(test_str12)
    assert result12 == expected12, f"Test case 12 failed. Expected: {expected12}, Got: {result12}"

    # Test case 13
    test_str13 = r"""
    VAR
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR
    VAR
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected13 = [{"name":"VAR",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """},
        {"name":"VAR",  "content":r"""
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result13 = get_var_blocks(test_str13)
    assert result13 == expected13, f"Test case 13 failed. Expected: {expected13}, Got: {result13}"

    # Test case 14
    test_str14 = r"""
    VAR       persistent
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR
    VAR (* constant *)
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected14 = [{"name":"VAR", "content":r"""       persistent
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """},
        {"name":"VAR", "content":r""" (* constant *)
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result14 = get_var_blocks(test_str14)
    assert result14 == expected14, f"Test case 14 failed. Expected: {expected14}, Got: {result14}"

    # Test case 15
    test_str15 = r"""
    (* VAR 
    bTest : BOOL;
    END_VAR*)
    VAR       
        // persistent
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR
    VAR (* constant *)
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected15 = [{"name":"VAR",  "content":r"""       
        // persistent
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """},
        {"name":"VAR",  "content":r""" (* constant *)
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result15 = get_var_blocks(test_str15)
    assert result15 == expected15, f"Test case 15 failed. Expected: {expected15}, Got: {result15}"

    # Test case 16
    test_str16 = r"""
    //VAR 
    //bTest : BOOL;
    //END_VAR
    VAR       
        // persistent
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR
    VAR (* constant *)
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_VAR"""
    expected16 = [{"name":"VAR",  "content":r"""       
        // persistent
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """},
        {"name":"VAR",  "content":r""" (* constant *)
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result16 = get_var_blocks(test_str16)
    assert result16 == expected16, f"Test case 16 failed. Expected: {expected16}, Got: {result16}"

    # Test case 17
    test_str17 = r"""
    STRUCT      
        // persistent
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    END_STRUCT"""
    expected17 = [{"name":"STRUCT",  "content":r"""      
        // persistent
	    {attribute 'hide'}
	    _bLicenseOk 							: BOOL := TRUE; // static class variable, access to all fb
    """}]
    result17 = get_var_blocks(test_str17)
    assert result17 == expected17, f"Test case 17 failed. Expected: {expected17}, Got: {result17}"