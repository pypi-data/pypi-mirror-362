FILE_TEMPLATE = """
Using the following file data enclosed within the <<< >>> delimeters write a \
top-file level concise summary that effectively captures the overall purpose and \
functionality of the file.

file data: <<< {data} >>>

Ensure your final summary is no longer than three sentences.

{additional_prompt}
"""


ROOT_LEVEL_TEMPLATE = """
Provide a concise summary that describes the primary \
purpose of the code, utilizing all the contextual details \
available.
----------

Repository data: <<< {data} >>>

{additional_prompt}
"""

FOLDER_SHORT_DESCRIPTION_TEMPLATE = """
Generate a one-line description of the folder's purpose based on \
the summaries of the files contained in the folder enclosed within the <<< >>> delimiters

File summaries: <<< {data} >>>

{additional_prompt}
"""


SYSTEM_PROMPT = """
You are an advanced code analyzer and documenting system. \
Your job is to generate summaries from code files written in various languages, \
and then, using those summaries, create top-level summaries for folders and the full project. \
Be concise, and focus on the intent of the code, not particularities. \
Your output should be used/read by a human to understand the basic structure \
and goal of each file and folder in a software project, \
and understand what the project does at a high level view
"""
