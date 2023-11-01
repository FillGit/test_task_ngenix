import csv
import asyncio
import shutil

from lxml import etree
from zipfile import ZipFile


def zip_extract(index_group):
    with ZipFile(f"zip_files/group_zip_{index_group}.zip", "r") as myzip:
        myzip.extractall(path=f'group_zip_{index_group}')


def parse_xml_var(_id, _root):
    _id = _root.findall('var')[0].get('value')
    return [{'id': _id, 'level': _root.findall('var')[1].get('value')}]


def parse_xml_objects(_id, _root):
    object_names = []
    for _obj in _root.find('objects').findall('object'):
        object_names.append({'id': _id, 'object_name': _obj.get('name')})
    return object_names


async def parse_group_zip(index_group):
    zip_extract(index_group)
    group_var = []
    group_objects = []
    for index_file in range(1, 101):
        with open(f'group_zip_{index_group}/xml_files/xml_{index_file}.xml') as fobj:
            xml_file = fobj.read()
        _root = etree.fromstring(xml_file)
        _id = _root.findall('var')[0].get('value')
        group_var.extend(parse_xml_var(_id, _root))
        group_objects.extend(parse_xml_objects(_id, _root))

    shutil.rmtree(f'group_zip_{index_group}/')
    return [group_var, group_objects]


async def parse_all(list_1, list_2):
    tasks = []
    for index_group in range(1, 51):
        task = asyncio.ensure_future(parse_group_zip(index_group))
        tasks.append(task)
    await asyncio.gather(*tasks)
    for task in tasks:
        result = task.result()
        list_1.extend(result[0])
        list_2.extend(result[1])
    return


async def write_csv(name_file, _list):
    with open(name_file, 'w') as f:
        w = csv.DictWriter(f, _list[0].keys())
        w.writeheader()
        w.writerows(_list)
    return


async def load_csv(list_1, list_2):
    csv_file_1 = loop.create_task(write_csv('csv_file_1.csv', list_1))
    csv_file_2 = loop.create_task(write_csv('csv_file_2.csv', list_2))
    await asyncio.wait([csv_file_1, csv_file_2])

if __name__ == '__main__':
    list_1 = []
    list_2 = []
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(parse_all(list_1, list_2))
    loop.run_until_complete(future)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_csv(list_1, list_2))
