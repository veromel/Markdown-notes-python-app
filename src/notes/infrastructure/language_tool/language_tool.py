import language_tool_python

tool = None


def get_language_tool():
    global tool
    if tool is None:
        tool = language_tool_python.LanguageTool("es")
    return tool
