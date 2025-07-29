import re


def get_return(decl):
    """
    Extract return type from METHOD, FUNCTION, or PROPERTY declarations.
    
    Args:
        decl: The declaration string
        
    Returns:
        The return type as a string, or an empty string if no return type is found
    """
    # First, remove line comments to avoid false matches
    decl_no_line_comments = re.sub(r'//.*?$', '', decl, flags=re.MULTILINE)
    
    # Define the pattern to match METHOD, FUNCTION, or PROPERTY declarations with return types
    # This pattern looks for these keywords followed by a name and then a colon and return type
    # It stops at semicolon, newline, or end of string
    pattern = r'^\s*(?:METHOD|FUNCTION|PROPERTY)\s+\w+\s*:\s*(.+?)(?:;|\n|$)'
    
    # Search for the pattern in the declaration string (case-insensitive)
    match = re.search(pattern, decl_no_line_comments, re.IGNORECASE | re.MULTILINE)
    
    if match:
        # Extract the return type
        return_type = match.group(1).strip()
        
        # Remove comments in parentheses like ("some comment")
        return_type = re.sub(r'\s*\([^)]*\)\s*', ' ', return_type)
        
        # Clean up extra whitespace
        return_type = re.sub(r'\s+', ' ', return_type).strip()
        
        return return_type
    
    # Return empty string if no return type is found
    return None


def get_var_specifier(decl):
    """
    Extract variable specifiers from a declaration string.
    
    Args:
        decl: The declaration string
        
    Returns:
        A list of variable specifiers (CONSTANT, PERSISTENT, RETAIN, etc.) found at the beginning of the string
    """
    # First, remove comments to avoid false matches
    # Remove block comments (* ... *)
    decl_no_comments = re.sub(r'\(\*.*?\*\)', '', decl, flags=re.DOTALL)
    
    # Remove line comments // ...
    decl_no_comments = re.sub(r'//.*?$', '', decl_no_comments, flags=re.MULTILINE)
    
    # Define the pattern to match variable specifiers at the beginning of the string
    # This pattern looks for common variable specifiers like CONSTANT, PERSISTENT, RETAIN, etc.
    # It ensures these are standalone words by checking for word boundaries
    pattern = r'^\s*(CONSTANT|PERSISTENT|RETAIN)\b'
    
    # Search for the pattern in the declaration string (case-insensitive)
    match = re.search(pattern, decl_no_comments, re.IGNORECASE)
    
    if match:
        # Return the matched specifier with its original case in a list
        return [match.group(1)]
    
    # Return empty list if no specifier is found
    return []

def get_comments(decl):
    """
    Extract comments from a declaration string.

    Args:
        decl: The declaration string

    Returns:
        A dictionary with a 'comments' key containing a list of comment strings
    """
    comments = []

    # Find all comments with their positions to maintain order
    comment_matches = []

    # Find block comments (* ... *) including multiline and nested comments
    # We need to handle nested comments properly, so we'll use a custom parser
    def find_block_comments(text):
        block_comments = []
        i = 0
        while i < len(text):
            if i < len(text) - 1 and text[i : i + 2] == "(*":
                # Found start of block comment
                start_pos = i
                i += 2
                depth = 1
                comment_start = start_pos

                while i < len(text) - 1 and depth > 0:
                    if text[i : i + 2] == "(*":
                        depth += 1
                        i += 2
                    elif text[i : i + 2] == "*)":
                        depth -= 1
                        i += 2
                    else:
                        i += 1

                if depth == 0:
                    # Found complete block comment
                    comment_text = text[comment_start:i]
                    block_comments.append((comment_start, comment_text))
                else:
                    # Unclosed comment, treat as regular text
                    i = start_pos + 1
            else:
                i += 1
        return block_comments

    # Find all block comments
    block_comments = find_block_comments(decl)
    for pos, comment in block_comments:
        comment_matches.append((pos, comment))

    # Find line comments // ... but only those NOT inside block comments
    # We'll do this by checking each line comment to see if it's inside a block comment
    line_comment_pattern = r"//.*?(?=\n|$)"
    for match in re.finditer(line_comment_pattern, decl, re.MULTILINE):
        # Check if this line comment is inside any block comment
        inside_block = False
        for block_pos, block_comment in block_comments:
            block_end = block_pos + len(block_comment)
            if block_pos <= match.start() <= block_end:
                inside_block = True
                break

        if not inside_block:
            comment_matches.append((match.start(), match.group()))

    # Sort by position to maintain order
    comment_matches.sort(key=lambda x: x[0])

    # Extract just the comment text
    comments = [comment for pos, comment in comment_matches]

    return {"comments": comments}


def get_var_blocks(decl):
    """
    Extract variable blocks from a declaration string.

    Args:
        decl: The declaration string

    Returns:
        A list of dictionaries, each with 'name' and 'content' keys representing a variable block
    """
    # First, we need to handle comments to avoid matching VAR blocks inside comments
    # We'll create a version of the string with comments removed for pattern matching

    # Create a copy of the original string for processing
    processed_decl = decl

    # Remove block comments (* ... *) for pattern matching
    # But we'll keep track of their positions to preserve them in the content
    block_comments = []

    def replace_block_comment(match):
        block_comments.append((match.start(), match.end(), match.group(0)))
        return " " * len(
            match.group(0)
        )  # Replace with spaces to preserve string length

    processed_decl = re.sub(
        r"\(\*.*?\*\)", replace_block_comment, processed_decl, flags=re.DOTALL
    )

    # Handle line comments
    # We'll replace lines that start with // with spaces
    processed_decl = re.sub(
        r"^\s*//.*$",
        lambda m: " " * len(m.group(0)),
        processed_decl,
        flags=re.MULTILINE,
    )

    # Define the pattern to match variable blocks and struct blocks
    # This pattern captures the block type (VAR, VAR_INPUT, STRUCT, etc.),
    # and everything up to the corresponding END block
    pattern = r"\s*((?:VAR(?:_[A-Za-z_]+)?|STRUCT))(.*?)END_(?:VAR|STRUCT)"

    # Find all matches in the processed declaration string
    matches = list(re.finditer(pattern, processed_decl, re.DOTALL))

    # Convert matches to a list of dictionaries
    blocks = []
    for match in matches:
        var_type = match.group(1).strip()  # VAR, VAR_INPUT, etc.
        content = match.group(2)  # Content between VAR and END_VAR

        # Check if this match is inside a block comment
        is_in_comment = False
        for start, end, _ in block_comments:
            if start <= match.start() and match.end() <= end:
                is_in_comment = True
                break

        if is_in_comment:
            continue  # Skip this match as it's inside a comment

        # Get the actual content from the original string
        start_pos = match.start(2)
        end_pos = match.end(2)
        original_content = decl[start_pos:end_pos]

        # Create the block dictionary
        block = {"name": var_type, "content": original_content}

        blocks.append(block)

    # Always return a list of dictionaries
    return blocks


def get_extend(decl):
    """
    Extract the class names that a function block extends from a declaration string.

    Args:
        decl: The declaration string

    Returns:
        A list of class names that the function block extends
    """
    # First, remove comments to avoid false matches
    # Remove block comments (* ... *)
    decl_no_comments = re.sub(r"\(\*.*?\*\)", "", decl, flags=re.DOTALL)

    # Remove line comments // ...
    decl_no_comments = re.sub(r"//.*?$", "", decl_no_comments, flags=re.MULTILINE)

    # Define the pattern to match "Extends" followed by class names
    # This pattern looks for "Extends" followed by one or more class names separated by commas
    # It stops at "IMPLEMENTS" keyword or end of string
    pattern = r"EXTENDS\s+([\w,\s]+?)(?:\s+IMPLEMENTS\s+|$)"

    # Search for the pattern in the declaration string (case-insensitive)
    match = re.search(pattern, decl_no_comments, re.IGNORECASE)

    if match:
        # Extract the matched group (the class names)
        extends_str = match.group(1)

        # Split by comma and strip whitespace to get individual class names
        extends_list = [name.strip() for name in extends_str.split(",") if name.strip()]

        return extends_list

    # Return empty list if no "Extends" found
    return None


def get_implements(decl):
    """
    Extract the interface names that a function block implements from a declaration string.

    Args:
        decl: The declaration string

    Returns:
        A list of interface names that the function block implements
    """
    # First, remove comments to avoid false matches
    # Remove block comments (* ... *)
    decl_no_comments = re.sub(r"\(\*.*?\*\)", "", decl, flags=re.DOTALL)

    # Remove line comments // ...
    decl_no_comments = re.sub(r"//.*?$", "", decl_no_comments, flags=re.MULTILINE)

    # Define the pattern to match "Implements" followed by interface names
    # This pattern looks for "Implements" followed by one or more interface names separated by commas
    # It stops at "EXTENDS" keyword or end of string
    pattern = r"IMPLEMENTS\s+([\w,\s]+?)(?:\s+EXTENDS\s+|$)"

    # Search for the pattern in the declaration string (case-insensitive)
    match = re.search(pattern, decl_no_comments, re.IGNORECASE)

    if match:
        # Extract the matched group (the interface names)
        implements_str = match.group(1)

        # Split by comma and strip whitespace to get individual interface names
        implements_list = [
            name.strip() for name in implements_str.split(",") if name.strip()
        ]

        return implements_list

    # Return empty list if no "Implements" found
    return None


def get_access_modifier(decl):
    """
    Extract the access modifier from a function block declaration string.

    Args:
        decl: The declaration string

    Returns:
        The access modifier as a string, or an empty string if no access modifier is found
    """
    # First, remove comments to avoid false matches
    # Remove block comments (* ... *)
    decl_no_comments = re.sub(r"\(\*.*?\*\)", "", decl, flags=re.DOTALL)

    # Remove line comments // ...
    decl_no_comments = re.sub(r"//.*?$", "", decl_no_comments, flags=re.MULTILINE)

    # Define the pattern to match access modifiers
    # This pattern looks for PRIVATE, PROTECTED, PUBLIC, or INTERNAL keywords
    # It ensures these are standalone words by checking for word boundaries
    pattern = r"\b(PRIVATE|PROTECTED|PUBLIC|INTERNAL)\b"

    # Search for the pattern in the declaration string (case-insensitive)
    match = re.search(pattern, decl_no_comments, re.IGNORECASE)

    if match:
        # Return the matched access modifier with its original case
        return match.group(1)

    # Return empty string if no access modifier is found
    return None


def get_abstract_keyword(decl):
    """
    Extract the ABSTRACT keyword from a function block declaration string.

    Args:
        decl: The declaration string

    Returns:
        The string "ABSTRACT" if the keyword is present, or an empty string if it's not found
    """
    # First, remove comments to avoid false matches
    # Remove block comments (* ... *)
    decl_no_comments = re.sub(r"\(\*.*?\*\)", "", decl, flags=re.DOTALL)

    # Remove line comments // ...
    decl_no_comments = re.sub(r"//.*?$", "", decl_no_comments, flags=re.MULTILINE)

    # Define the pattern to match the ABSTRACT keyword
    # This pattern looks for the ABSTRACT keyword as a standalone word
    pattern = r"\b(ABSTRACT)\b"

    # Search for the pattern in the declaration string (case-insensitive)
    match = re.search(pattern, decl_no_comments, re.IGNORECASE)

    if match:
        # Return the matched keyword with its original case
        return match.group(1)

    # Return empty string if ABSTRACT keyword is not found
    return ""


def get_var_keyword(content):
    """
    Extract keywords like PERSISTENT or CONSTANT from a variable block content.

    Args:
        content: The content string from a variable block

    Returns:
        A list containing the keyword if found, or a list with an empty string if no keyword is found
    """
    # First, remove comments to avoid false matches
    # Remove block comments (* ... *)
    content_no_comments = re.sub(r"\(\*.*?\*\)", "", content, flags=re.DOTALL)

    # Remove line comments // ...
    content_no_comments = re.sub(r"//.*?$", "", content_no_comments, flags=re.MULTILINE)

    # Define the pattern to match keywords like PERSISTENT or CONSTANT
    # This pattern looks for these keywords at the beginning of the content (after whitespace)
    pattern = r"^\s*(PERSISTENT|CONSTANT)\b"

    # Search for the pattern in the content string (case-insensitive)
    match = re.search(pattern, content_no_comments, re.IGNORECASE)

    if match:
        # Return the matched keyword with its original case in a list
        return [match.group(1)]

    # Return a list with an empty string if no keyword is found
    return None


def get_var(content):
    """
    Extract variable declarations from a string.

    Args:
        content: The content string containing variable declarations

    Returns:
        A list of variable declarations, each as a string
    """

    def is_standalone_line_comment(line):
        """Check if a line is a standalone line comment."""
        return line.startswith("//")

    def is_standalone_block_comment(line):
        """Check if a line is the start of a standalone block comment."""
        return line.startswith("(*")

    def is_attribute_declaration(line):
        """Check if a line is an attribute declaration."""
        return line.startswith("{")

    def is_variable_declaration(line):
        """Check if a line is a variable declaration."""
        # Match patterns for variable declarations
        return (
            re.match(r"^[_A-Za-z][_A-Za-z0-9]*\s+.*?;", line)
            or re.match(r"^[_A-Za-z][_A-Za-z0-9]*,.*?;", line)
            or re.match(r"^\s*[_A-Za-z][_A-Za-z0-9]*,.*?;", line)
        )

    def is_start_of_new_declaration(line):
        """Check if a line is the start of a new declaration."""
        stripped_line = line.strip()
        return (
            not stripped_line
            or is_standalone_line_comment(stripped_line)
            or is_standalone_block_comment(stripped_line)
            or is_attribute_declaration(stripped_line)
            or is_variable_declaration(stripped_line)
        )

    def skip_block_comment(lines, start_index):
        """Skip a block comment and return the index of the next line after the comment."""
        comment_start = start_index
        current_index = start_index

        # Find the end of the block comment
        while current_index < len(lines) and "*" + ")" not in lines[current_index]:
            current_index += 1

        if current_index < len(lines):  # Found the end of the comment
            return current_index + 1  # Move past the comment
        else:  # Reached the end without finding the end of the comment
            return comment_start + 1  # Just move past the first line

    def process_attribute_declaration(lines, start_index):
        """Process an attribute declaration and its associated variable declaration."""
        attribute_lines = [
            lines[start_index].strip()
        ]  # Use the stripped line without whitespace
        current_index = start_index + 1

        # Continue collecting lines until we find a variable declaration
        while current_index < len(lines):
            stripped_line = lines[current_index].strip()

            # Skip empty lines but keep track of them
            if not stripped_line:
                attribute_lines.append(lines[current_index])
                current_index += 1
                continue

            # If we find a variable declaration, include the attribute with it
            if is_variable_declaration(stripped_line):
                # Create the variable declaration with the attribute
                var_decl = "\n".join(attribute_lines) + "\n" + lines[current_index]

                # Check if this declaration continues to the next line
                next_index = current_index + 1
                while (
                    next_index < len(lines)
                    and not is_start_of_new_declaration(lines[next_index])
                    and lines[next_index].strip()
                ):
                    var_decl += "\n" + lines[next_index]
                    next_index += 1

                return next_index, var_decl
            else:
                # If it's not a variable declaration, it might be part of the attribute
                attribute_lines.append(lines[current_index])
                current_index += 1

        # If we didn't find a variable declaration, return the original index
        return start_index + 1, None

    def process_variable_declaration(lines, start_index):
        """Process a variable declaration and return the declaration string."""
        stripped_line = lines[start_index].strip()

        # Check if this is a multiple variable declaration with a leading space
        if re.match(r"^\s*[_A-Za-z][_A-Za-z0-9]*,.*?;", stripped_line):
            var_decl = " " + stripped_line
        else:
            var_decl = stripped_line

        # Check if this declaration continues to the next line
        current_index = start_index + 1
        while (
            current_index < len(lines)
            and not is_start_of_new_declaration(lines[current_index])
            and lines[current_index].strip()
        ):
            var_decl += "\n" + lines[current_index]
            current_index += 1

        return current_index, var_decl

    # Remove keywords like PERSISTENT or CONSTANT at the beginning
    content_without_keywords = re.sub(
        r"^\s*(PERSISTENT|CONSTANT)\b", "", content, flags=re.IGNORECASE
    )

    # Split the content by lines for processing
    lines = content_without_keywords.split("\n")

    # Process the lines to extract variable declarations
    var_declarations = []
    line_index = 0

    while line_index < len(lines):
        # Get the current line and its stripped version
        current_line = lines[line_index]
        stripped_line = current_line.strip()

        # Skip empty lines
        if not stripped_line:
            line_index += 1
            continue

        # Handle different types of lines
        if is_standalone_line_comment(stripped_line):
            # Skip standalone line comments
            line_index += 1
        elif is_standalone_block_comment(stripped_line):
            # Skip standalone block comments
            line_index = skip_block_comment(lines, line_index)
        elif is_attribute_declaration(stripped_line):
            # Process attribute declaration
            line_index, attribute_var_decl = process_attribute_declaration(
                lines, line_index
            )
            if attribute_var_decl:
                var_declarations.append(attribute_var_decl)
        elif is_variable_declaration(stripped_line):
            # Process variable declaration
            line_index, var_decl = process_variable_declaration(lines, line_index)
            var_declarations.append(var_decl)
        else:
            # Skip any other lines
            line_index += 1

    return var_declarations


def get_var_content(decl):
    """
    Extract structured information from variable declarations.

    Args:
        decl: The variable declaration string

    Returns:
        A list of dictionaries, each containing information about a variable:
        - name: The variable name
        - type: The variable type
        - init: The initialization value (if any)
        - attributes: List of attributes (if any)
        - comments: Any comments associated with the variable (if any)
    """
    # Extract attributes if present
    attributes = []
    attribute_pattern = r"^\s*(\{.*?\})"
    attribute_match = re.search(attribute_pattern, decl, re.MULTILINE)
    if attribute_match:
        attributes.append(attribute_match.group(1))
        # Remove the attribute from the declaration for easier parsing
        decl = decl.replace(attribute_match.group(0), "", 1)

    # Extract comments
    comments = ""
    # Line comments
    line_comment_pattern = r"//.*?$"
    line_comment_match = re.search(line_comment_pattern, decl, re.MULTILINE)
    if line_comment_match:
        comments = line_comment_match.group(0)
        # Remove the comment from the declaration for easier parsing
        decl = decl.replace(comments, "", 1)

    # Block comments
    block_comment_pattern = r"\(\*.*?\*\)"
    block_comment_matches = re.finditer(block_comment_pattern, decl, re.DOTALL)
    block_comments = []
    for match in block_comment_matches:
        block_comments.append(match.group(0))

    if block_comments:
        # If we have block comments, add them to the comments string
        if comments:
            comments += "".join(block_comments)
        else:
            comments = "".join(block_comments)

        # Remove the block comments from the declaration for easier parsing
        for comment in block_comments:
            decl = decl.replace(comment, "", 1)

    # Extract variable names, type, and initialization value
    # Pattern to match: variable_name(s) : type [:= init_value];
    var_pattern = r"^\s*(.*?)\s*:\s*(.*?)\s*(?::=\s*(.*?))?\s*;"
    var_match = re.search(var_pattern, decl.strip(), re.DOTALL)

    if var_match:
        var_names_str = var_match.group(1)
        var_type = var_match.group(2).strip()
        var_init = var_match.group(3) if var_match.group(3) else ""

        # Split multiple variable names if present
        var_names = [name.strip() for name in var_names_str.split(",")]

        # Create a dictionary for each variable
        result = []
        for var_name in var_names:
            var_dict = {
                "name": var_name,
                "type": var_type,
                "init": var_init,
                "attributes": attributes,
                "comments": comments,
            }
            result.append(var_dict)

        return result

    # If no match found, return an empty list
    return []


def get_comment_content(decl):
    """
    Extract and categorize comments from a declaration string.

    Args:
        decl: The declaration string containing comments

    Returns:
        A dictionary with two keys:
        - "standard": A list of standard comment contents (without comment markers)
        - "documentation": A list of dictionaries, each containing a documentation keyword and its content
    """
    # Initialize the result dictionary
    result = {"standard": [], "documentation": {}}
    documentation = {}
    standard = []

    # Extract line comments first
    # We'll look for // followed by text until the end of the line or until a block comment starts
    line_comment_pattern = r"//\s*(.*?)(?=\(\*|$)"
    line_comment_matches = re.finditer(line_comment_pattern, decl)

    for match in line_comment_matches:
        # Add the comment content (without the // marker) to the standard comments list
        # result["standard"].append(match.group(1).strip())
        standard.append(match.group(1).strip())

    # Now extract and process block comments
    block_comment_pattern = r"\(\*(.*?)\*\)"
    block_comment_matches = re.finditer(block_comment_pattern, decl, re.DOTALL)

    for match in block_comment_matches:
        full_comment = match.group(0)  # The entire comment including (* and *)
        comment_content = match.group(1)  # Just the content between (* and *)

        # Check if there's a whitespace after (*
        if full_comment.startswith("(* "):
            # This is a standard comment
            #result["standard"].append(comment_content.strip())
            standard.append(comment_content.strip())
        else:
            # This is a documentation comment
            # Extract the keyword and content
            doc_keyword_pattern = r"^(\w+)\s+(.*?)$"
            doc_match = re.match(
                doc_keyword_pattern, comment_content.strip(), re.DOTALL
            )

            if doc_match:
                keyword = doc_match.group(1)
                content = doc_match.group(2)

                # Add the documentation comment to the documentation list
                #result["documentation"].update({keyword: content})
                documentation.update({keyword: content})
            else:
                # If we can't extract a keyword, treat it as a standard comment
                #result["standard"].append(comment_content.strip())
                standard.append(comment_content.strip())

    result["documentation"] = documentation
    result["standard"] = standard
    return result
