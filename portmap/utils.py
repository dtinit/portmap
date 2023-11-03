import re

def has_yaml_header(file_content):
    """ Detects if a string (usually the contents of a .md file) has a YAML header
    >>> has_yaml_header("---\\nTest: Yes\\n---")
    True
    >>> has_yaml_header("Test: No")
    False
    >>> has_yaml_header("---\\nProblem: about to be too many dashes\\n----")
    False
    """
    p = re.compile(r"^---$", re.MULTILINE)
    results = p.findall(file_content)
    return len(results) > 1

def extract_yaml(file_content):
    """ Extracts a YAML header delimited by lines consisting of '---' from the rest of a markdown document
    >>> extract_yaml("---\\nTest: Data\\nPart: Deux\\n---\\nDo not return this\\n")
    'Test: Data\\nPart: Deux'
    """
    assert has_yaml_header(file_content)
    #p = re.compile("^---$(.*?)^---$", re.MULTILINE)
    #yaml = p.findall(file_content)
    #return yaml
    in_yaml_header = False
    yaml_content = []
    for line in file_content.split("\n"):
        if not in_yaml_header and line == "---":
            in_yaml_header=True
        elif in_yaml_header and line == "---":
            break
        elif in_yaml_header:
            yaml_content.append(line)

    return '\n'.join(yaml_content)
