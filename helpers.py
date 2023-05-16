def format_table_data_to_dict(original_list:list) -> dict:
    """
    Format the data coming from the table 
    to be a Python dictionary
    """
    list_size = len(original_list)
    data_dict = dict()

    for num in range(1, list_size + 1):
        for elem in original_list:
            data_dict[str(num)] = str(elem)

    return data_dict
