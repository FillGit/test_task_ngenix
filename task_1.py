import os
import shutil
import string

from lxml import etree
from random import randint, choice
from zipfile import ZipFile, ZIP_DEFLATED


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(length))


def generate_xml_file(index_zip, index_file):
    _root = etree.Element('root')
    etree.SubElement(_root, 'var', name='id', value=random_string(5))
    etree.SubElement(_root, 'var', name='level', value=str(randint(1, 100)))
    _objects = etree.SubElement(_root, 'objects')
    for _ in range(1, randint(2, 11)):
        etree.SubElement(_objects, 'object', name=random_string(3))

    sheet = etree.ElementTree(_root)
    sheet.write(f'xml_files/xml_{index_file}.xml')


def zipdir(path, ziph):
    for root, _, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


if __name__ == '__main__':
    os.mkdir('xml_files/')
    if not os.path.isdir('zip_files/'):
        os.mkdir('zip_files/')
    for index_zip in range(1, 51):
        with ZipFile(f"zip_files/group_zip_{index_zip}.zip",
                     "w", ZIP_DEFLATED) as myzip:
            [generate_xml_file(index_zip, i) for i in range(1, 101)]
            zipdir('xml_files/', myzip)

    shutil.rmtree('xml_files/')
