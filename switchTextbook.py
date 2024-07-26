import dashscope
from dashscope import Generation


dashscope.api_key = 'sk-92606777cb7748e8916082663128fe09'


# noinspection PyTypeChecker
def switchTextbook(message):

    question=[{'role':'user','content':f"Does this message conveys the intention to switch to another textbook:{message}? If so, reply with the grade of textbook the user wants to switch to in this format [number-grade]. For example, if you identifies that the user wants to switch to second grade's textbook, you can reply '2nd-grade'. Reply '3rd-grade' for third grade. You must not include any other words besides the grade such as your reasoning. If no switching intention, reply nothing."}]
    assistant_response = Generation.call('qwen2-72b-instruct', messages=question,result_format='message').output.choices[0].message.content
    return assistant_response
