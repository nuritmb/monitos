def print_sections(section_list, sep_lenght=30, sep_char='-') -> None:
    separator = sep_char*sep_lenght
    print(separator)
    for section in section_list:
        if callable(section):
            section()
        else:
            print(section)
        print(separator)