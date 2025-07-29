import re

def parse_markdown(text):
    """Parses markdown style text to a structured format for later usage.

    Args:
        text (str): The markdown formatted text.

    Returns:
        tuple: A tuple containing:
            - list: List of formatting information (type, offset, length)
            - str: Text without markdown formatting.
    """
    result = []
    
    def process_match(match, md_type):
        actual_offset = match.start() - sum(len(m.group(0)) - len(m.group(1)) for m in re.finditer(r'\[(.*?)\]\((.*?)\)|\*(.*?)\*|/(.*?)/|~(.*?)~', text[:match.start()]))
        
        format = {
            "type": md_type,
            "offset": actual_offset,
            "length": len(match.group(1)),
        }
        if md_type == 'url':
            format['url'] = match.group(2)

        result.append(format)

        return match.group(1)
    
    text = re.sub(r'\[(.*?)\]\((?P<url>.*?)\)', lambda m: process_match(m, "url"), text)
    text = re.sub(r'\*(.*?)\*', lambda m: process_match(m, "bold"), text)
    text = re.sub(r'/(.*?)/', lambda m: process_match(m, "italic"), text)
    text = re.sub(r'~(.*?)~', lambda m: process_match(m, "underline"), text)
    
    return result, text.strip()