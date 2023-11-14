import re
import yaml

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

def extract_yaml_and_body(file_content):
    """ Extracts a YAML header delimited by lines consisting of '---' from the rest of a markdown document
    >>> extract_yaml_and_body("---\\nTest: Data\\nPart: Deux\\n---\\nSeparate this body part\\n")
    ({'Test': 'Data', 'Part': 'Deux'}, 'Separate this body part\\n')
    """
    assert has_yaml_header(file_content)
    in_yaml_header = False
    in_body = False
    yaml_content = []
    body_content = []
    for line in file_content.split("\n"):
        if not in_yaml_header and not in_body and line == "---":
            in_yaml_header = True
        elif in_yaml_header and line == "---":
            in_yaml_header = False
            in_body = True
        elif in_yaml_header:
            yaml_content.append(line)
        elif in_body:
            body_content.append(line)

    yaml_content = yaml.safe_load('\n'.join(yaml_content))
    body = '\n'.join(body_content)
    return yaml_content, body
