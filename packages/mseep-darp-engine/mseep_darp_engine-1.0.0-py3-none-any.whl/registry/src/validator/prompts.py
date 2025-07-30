from jinja2 import Template

SENS_TOPIC_CHECK_SYSTEM_PROMPT: Template = Template(
    """
Analyze the description of an MCP server and its tools.

Your task is to determine whether the server likely works with sensitive data.

Consider the following rules:
1.	Sensitive data indicators:
•	Mentions of emails, phone numbers, SSNs, credit card numbers, access tokens, passwords, or other personal identifiable information (PII).
•	Tools or functionality related to authentication, authorization, payments, identity verification, document uploads, etc.
2.	Sensitive domains:
•	Banking
•	Finance
•	Government services
•	Or any tool that may require sending sensitive user data
"""
)

SENS_TOPIC_CHECK_USER_PROMPT: Template = Template(
    """
    '''
    Server's data: {{ server_data.model_dump_json() }}
    --------------
    Server's tools: {{ tools_data.model_dump_json() }}
    '''
    """
)
