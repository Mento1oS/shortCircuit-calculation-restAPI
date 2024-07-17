from xml.dom import minidom

import ShortCircuitCalculator
from DataBase import ConfigRepository


async def get_data_from_db(sc_place, scheme_id):
    array_of_sc = await ConfigRepository.find_one(scheme_id)
    # print(array_of_sc)

    deserialized = array_of_sc.split(', ')
    deserialized[0] = deserialized[0].replace('[', '')
    deserialized[len(deserialized) - 1] = deserialized[len(deserialized) - 1].replace(']', '')

    sc_value = deserialized[int(sc_place) - 1]

    # print(scheme_id, sc_place, sc_value)
    return sc_value


async def post_data_to_db(file_name):
    doc = minidom.parseString(file_name)
    result_currents = str(ShortCircuitCalculator.get_current(doc))
    xml_file_to_save = doc.toxml()

    string_of_result_currents = str(result_currents)

    object_to_save = {'scheme': xml_file_to_save, 'sc_values': string_of_result_currents}

    scheme_id = await ConfigRepository.add_one(object_to_save)

    return scheme_id


async def put_data_to_db(file_name, scheme_id):
    doc = minidom.parseString(file_name)
    result_currents = str(ShortCircuitCalculator.get_current(doc))
    xml_file_to_save = doc.toxml()

    string_of_result_currents = str(result_currents)
    object_to_save = {'scheme': xml_file_to_save, 'sc_values': string_of_result_currents}

    # print(scheme_id)

    response = await ConfigRepository.update_one(object_to_save, scheme_id)
    if response:
        return True
    return False


async def delete_data_from_db(scheme_id):
    response = await ConfigRepository.delete_one(scheme_id)
    if response:
        return True
    return False
