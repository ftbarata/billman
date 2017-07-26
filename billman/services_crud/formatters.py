def decimal_to_brz(value=None):
    if value is None:
        return float('0.00')
    else:
        str_value = str(value)
        final_value = ''
        first_separator = False
        for char in str_value:
            if len(final_value) == 0:
                if char == ',' or char == '.':
                    final_value += '0.'
                    first_separator = True
                else:
                    final_value += char
            else:
                if char == ',' or char == '.':
                    if not first_separator:
                        final_value += '.'
                        first_separator = True
                    else:
                        pass
                else:
                    final_value += char


        decimal_count = 0
        start_count = False
        for i in final_value:
            if i == '.':
                start_count = True
            if i != '.' and start_count:
                decimal_count += 1

        if decimal_count > 2:
            slice = decimal_count - 2
            return float(final_value[0:-slice])
        else:
            return float(final_value)

