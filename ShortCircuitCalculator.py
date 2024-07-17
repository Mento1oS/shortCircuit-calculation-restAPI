s_base = 100


def get_power_system_reactance(system, u_base):
    s_kz = float(system.getElementsByTagName('skz')[0].firstChild.data)

    u = float(system.getElementsByTagName('u')[0].firstChild.data)

    return (s_base / s_kz) * (u / u_base) ** 2


def get_power_transformer_reactance(transformer, u_base):
    u_kz = float(transformer.getElementsByTagName('ukz')[0].firstChild.data)

    s = float(transformer.getElementsByTagName('s')[0].firstChild.data)

    u = float(transformer.getElementsByTagName('u')[0].firstChild.data)

    return u_kz / 100 * (s_base / s) * (u / u_base) ** 2


def get_transmission_line_reactance(line, u_base):
    length = float(line.getElementsByTagName('length')[0].firstChild.data)
    x0 = float(line.getElementsByTagName('x0')[0].firstChild.data)
    conductors = float(line.getElementsByTagName('conductors')[0].firstChild.data)

    return x0 * length * s_base / ((u_base ** 2) * conductors)


def get_current(xml):
    power_systems = xml.getElementsByTagName('power_system')

    transformers = xml.getElementsByTagName('transformer')

    transmission_lines = xml.getElementsByTagName('transmission_line')

    elements = []

    elements.append(power_systems[0])
    for i in range(len(transformers) + len(transmission_lines)):
        for j in range(len(transformers)):
            if elements[i].attributes['next'].value == transformers[j].attributes['name'].value:
                elements.append(transformers[j])

        for j in range(len(transmission_lines)):
            if elements[i].attributes['next'].value == transmission_lines[j].attributes['name'].value:
                elements.append(transmission_lines[j])

    u_base = []

    u_base.append(int(power_systems[0].getElementsByTagName('u')[0].firstChild.data))
    for transformer in transformers:
        kt = float(transformer.getElementsByTagName('kt')[0].firstChild.data)
        u = float(transformer.getElementsByTagName('u')[0].firstChild.data)
        u_base.append((u / kt))

    i_base = []
    for i in range(len(u_base)):
        i_base.append(s_base / ((3 ** 0.5) * u_base[i]))

    emf_1 = 1
    x_sum = 0
    base_index = 0
    current_i_base = i_base[base_index]
    current_u_base = u_base[base_index]
    prev_u_base = 0
    sc_array = []

    for i in range(len(elements)):
        if elements[i] in transformers:
            base_index += 1
            current_i_base = i_base[base_index]
            prev_u_base = current_u_base
            current_u_base = u_base[base_index]

        if elements[i] in power_systems:
            x_sum += (get_power_system_reactance(elements[i], current_u_base))
        elif elements[i] in transformers:
            x_sum += (get_power_transformer_reactance(elements[i], prev_u_base))
        elif elements[i] in transmission_lines:
            x_sum += (get_transmission_line_reactance(elements[i], current_u_base))
        sc_array.append(round(emf_1 / x_sum * current_i_base, 3))

    return sc_array
