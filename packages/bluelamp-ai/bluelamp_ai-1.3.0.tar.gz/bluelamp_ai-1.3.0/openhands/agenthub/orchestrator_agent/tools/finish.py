from litellm import ChatCompletionToolParam, ChatCompletionToolParamFunctionChunk

from openhands.llm.tool_names import FINISH_TOOL_NAME

_FINISH_DESCRIPTION = """このツールが使用されると現在の会話とコンテクストが終了して権限委譲元のAIに戻ります。
必ずユーザーに許可をもらってから task_completed: true に切り替えてください。もし何か不具合が起きた場合は
ユーザーと相談してください。勝手にtask_completed:trueにはしないでください。
権限委譲元のAIに対しては実行したアクションとその結果の要約のメッセージを含めてください。
"""

FinishTool = ChatCompletionToolParam(
    type='function',
    function=ChatCompletionToolParamFunctionChunk(
        name=FINISH_TOOL_NAME,
        description=_FINISH_DESCRIPTION,
        parameters={
            'type': 'object',
            'required': ['message', 'task_completed'],
            'properties': {
                'message': {
                    'type': 'string',
                    'description': 'Final message to send to the user',
                },
                'task_completed': {
                    'type': 'string',
                    'enum': ['true'],
                    'description': 'Whether you have completed the task.',
                },
            },
        },
    ),
)
