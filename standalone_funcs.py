from db_funcs import query_present_day_data


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


def fetch_data_from_table(table, date) -> list:
    """
    fetch data from database table
    """
    data_content = list()

    data = query_present_day_data(table, date)

    data_dict = format_table_data_to_dict(data)

    for k in data_dict:
        data_content.append(f"""__{ k }__: { data_dict[k]["event_type"] } ({data_dict[k]["created_at"][11:19]})""")

    return data_content
