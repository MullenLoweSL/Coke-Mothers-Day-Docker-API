class StringUtils:
    @staticmethod
    def remove_first_n_characters(input_string, number_to_remove):
        return input_string[number_to_remove:]

    @staticmethod    
    def string_to_boolean(string: str):
        if string is None:
            return False
        string = string.strip()
        return True if string.lower() == 'true' else False