from litellm import ChatCompletionToolParam, ChatCompletionToolParamFunctionChunk

from openhands.llm.tool_names import FINISH_TOOL_NAME

_FINISH_DESCRIPTION = """このツールが使用されると現在の会話を終了して権限委譲元のAIに戻ります。
このツールは基本的にtaskが完了した時に権限委譲元のAIに戻すために利用しますが
現在の会話が中断されますのでtaskが完了したと思っても必ずユーザーにタスク完了確認をとり
完了の承認をもらった時にはじめてtask_completedフィールドをTrueに設定してください。

権限委譲元のAIに対しては実行したアクションとその結果の要約のメッセージを含めてください
ユーザーからの許可を取らない限りtask_completedフィールドをTrueに設定してはなりません。

task_completedフィールドは、ユーザーから完了承認を得た場合のみTrueに設定し、それ以外はFalseに設定してください。
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
                    'enum': ['true', 'false', 'partial'],
                    'description': 'Whether you have completed the task.',
                },
            },
        },
    ),
)
