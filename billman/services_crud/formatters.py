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

        return round(float(final_value), 2)

