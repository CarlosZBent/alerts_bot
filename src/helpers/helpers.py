def format_data_for_text_message(data_list:list) -> str:
    """
    Take the data from the list and turn it into a 
    formatted paragraph that can be sent as a message
    """
    message_text = str()
    if len(data_list) > 0:
        for elem in data_list:
            message_text += f"""\n*{data_list.index(elem)+1}:* {elem["event_type"]} ({elem["created_at"][11:19]})\n"""
    else:
        message_text = "*No data matched the specified parameters*"

    return message_text
