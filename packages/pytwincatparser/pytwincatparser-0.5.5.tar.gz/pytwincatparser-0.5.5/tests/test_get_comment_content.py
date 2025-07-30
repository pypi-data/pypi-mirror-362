from pytwincatparser.parse_declaration import get_comment_content

def test_get_comment_content():
    # Test case 1
    test_str1 = r"""// comment"""
    expected1 = {"standard":["comment"],"documentation":{}}
    result1 = get_comment_content(test_str1)
    assert result1 == expected1, f"Test case 1 failed. Expected: {expected1}, Got: {result1}"

    # Test case 2
    test_str2 = r"""//      comment khjsdkfh 234230849"""
    expected2 =  {"standard":["comment khjsdkfh 234230849"],"documentation":{}}
    result2 = get_comment_content(test_str2)
    assert result2 == expected2, f"Test case 2 failed. Expected: {expected2}, Got: {result2}"

    # Test case 3
    test_str3 = r"""(* hkjhkjfdsuziuzsdfkjh sdfsdf *)"""
    expected3 =  {"standard":["hkjhkjfdsuziuzsdfkjh sdfsdf"],"documentation":{}}
    result3 = get_comment_content(test_str3)
    assert result3 == expected3, f"Test case 3 failed. Expected: {expected3}, Got: {result3}"

    # Test case 4
    test_str4 = r"""(* hkjhkjfdsuziuzsdfkjh
    this is a multiline comment sdfsdf *)"""
    expected4 =  {"standard":[r"""hkjhkjfdsuziuzsdfkjh
    this is a multiline comment sdfsdf"""],"documentation":{}}
    result4 = get_comment_content(test_str4)
    assert result4 == expected4, f"Test case 4 failed. Expected: {expected4}, Got: {result4}"

    # Test case 5
    test_str5 = r"""(* hkjhkjfdsuziuzsdfkjh
    this is a multiline comment sdfsdf *)(* antoher comment *)"""
    expected5 =  {"standard":[r"""hkjhkjfdsuziuzsdfkjh
    this is a multiline comment sdfsdf""", "antoher comment" ],"documentation":{}}
    result5 = get_comment_content(test_str5)
    assert result5 == expected5, f"Test case 5 failed. Expected: {expected5}, Got: {result5}"

    # Test case 6
    test_str6 = r"""(*details hkjhkjfdsuziuzsdfkjh sdfsdf *)"""
    expected6 =  {"standard":[],"documentation":{"details": "hkjhkjfdsuziuzsdfkjh sdfsdf"}}
    result6 = get_comment_content(test_str6)
    assert result6 == expected6, f"Test case 6 failed. Expected: {expected6}, Got: {result6}"

    # Test case 7
    test_str7 = r"""(*details hkjhkjfdsuziuzsdfkjh sdfsdf *)(*usage this works like that
    even a newline is possible*)"""
    expected7 =  {"standard":[],"documentation":{"details": "hkjhkjfdsuziuzsdfkjh sdfsdf", "usage":r"""this works like that
    even a newline is possible"""}}
    result7 = get_comment_content(test_str7)
    assert result7 == expected7, f"Test case 7 failed. Expected: {expected7}, Got: {result7}"

    # Test case 8
    test_str8 = r"""// this or that(*details hkjhkjfdsuziuzsdfkjh sdfsdf *)(*anotherkeyword this works like that
    even a newline is possible*)"""
    expected8 =  {"standard":["this or that"],"documentation":{"details": "hkjhkjfdsuziuzsdfkjh sdfsdf", "anotherkeyword":r"""this works like that
    even a newline is possible"""}}
    result8 = get_comment_content(test_str8)
    assert result8 == expected8, f"Test case 8 failed. Expected: {expected8}, Got: {result8}"
