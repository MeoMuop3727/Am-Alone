def minus_tuple(__v1: tuple[int | float], __v2: tuple[int | float]) -> tuple:
    result_minused = []

    for i, value in enumerate(__v1):
        result_minused.append(value - __v2[i])
    
    return tuple(result_minused)

def plus_tuple(__v1: tuple[int | float], __v2: tuple[int | float]) -> tuple:
    result_plused = []

    for i, value in enumerate(__v1):
        result_plused.append(value + __v2[i])
    
    return tuple(result_plused)

def multi_tuple(__v1: tuple[int | float], __v2: tuple[int | float]) -> tuple:
    result_multied = []

    for i, value in enumerate(__v1):
        result_multied.append(value * __v2[i])
    
    return tuple(result_multied)


