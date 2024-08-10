def get_element_id(element):
    last_elems = element.split("/")[-4:]
    proper_name = last_elems[-1].split(".")[0]
    random_numbers = last_elems[-1].split("=")[-1]
    del last_elems[-1]
    last_elems.append(proper_name)
    last_elems.append(random_numbers)
    final = '-'.join(last_elems)
    return final