from db_funcs import query_events_data


def format_table_data_to_dict(original_list:list) -> dict:
    """
    Format the data coming from the table 
    to be a Python dictionary
    """
    list_size = len(original_list)
    data_dict = dict()

    for num in range(1, list_size + 1):
        for elem in original_list:
            data_dict[str(num)] = elem

    return data_dict


def format_data_for_text_message(data_list:list) -> str:
    """
    Take the data from the list and turn it into a 
    paragraph that can be sent as a message
    """
    message_text = ""
    for elem in data_list:
        message_text += f"""{elem}\n\n"""

    return message_text


def fetch_data_from_table(table, date) -> list:
    """
    fetch data from database table
    """
    data_content = list()

    data = query_events_data(table, date)

    data_dict = format_table_data_to_dict(data)

    if len(data_dict) > 0:
        for k in data_dict:
            # The (*) surrounding k are for markdown formatting when the message is sent
            data_content.append(f"""*{ k }*: { data_dict[k]["event_type"] } ({data_dict[k]["created_at"][11:19]})""")
    else:
        data_content.append("*No events data*")

    return format_data_for_text_message(data_content)
