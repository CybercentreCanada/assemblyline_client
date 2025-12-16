from textwrap import dedent

from assemblyline_client.v4_client.common.utils import api_path


class Assistant(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(
        self,
        user_prompt,
        language="english",
    ):
        """\
Return the AI generated response for the given query hash.

Required:
user_prompt     : The prompt to send to the assistant (string)

Optional:
language        : The language to use for the response (string)

Throws a Client exception if the query does not exist.
"""

        return self._connection.post(
            api_path("assistant", lang=language),
            json=[
                {"role": "user", "content": dedent(user_prompt)},
            ],
        )["trace"][-1]["content"]
