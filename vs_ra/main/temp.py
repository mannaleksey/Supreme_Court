import ftplib
import os
import time
import xml.etree.ElementTree as ET
import gzip
import shutil

from .all_keys import keys, keys_texts
from .models import DataCase, TextsCase


def get_file_ftp(court):
    host = f'search.vs-ra.org'
    ftp_user = 'radpay2_search'
    ftp_password = 'fk^5gYan5hdu'

    ftp = ftplib.FTP(host, ftp_user, ftp_password)
    folder_list = ftp.nlst()
    for folder in folder_list:
        if folder == court:
            ftp.cwd(court)
            file_list = ftp.nlst()
            file_list.remove('..')
            file_list.remove('.')
            for file in file_list:
                with open(file, 'wb') as fp:  # Создаем локальный файл в режиме двоичной записи
                    ftp.retrbinary('retr ' + file, fp.write)
            break
    ftp.close()


def unpack_rar():
    list_rar_file = os.listdir()
    for rar_file in list_rar_file:
        if rar_file.find('.xml.gz') != -1:
            with gzip.open(f'{rar_file}', 'rb') as f_in:
                with open(f'{rar_file.split(".")[0]}.xml', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)


def read_xml(court):
    all_data = []
    all_data_texts = []
    list_file = os.listdir()
    for file in list_file:
        if file.split('.')[-1] == 'xml':
            tree = ET.parse(f'{file}')
            root = tree.getroot()
            root = root[0][2]
            for row in root:
                data = {'Court': court, 'type_of_legal_proceeding': file.split('.')[0]}
                for column in row:
                    if column.tag == 'Column':
                        attrs = column.attrib
                        attrs_name = attrs['Name']
                        if attrs_name == 'pubattach':
                            attrs_name = 'PubAttach'
                        if file.split('.')[0].find('Texts') == -1:
                            keys_xml = keys
                        else:
                            keys_xml = keys_texts
                        if attrs_name in keys_xml:
                            data[attrs_name] = attrs['Value']
                if file.split('.')[0].find('Texts') == -1:
                    all_data.append(DataCase(**data))
                else:
                    all_data_texts.append(TextsCase(**data))
    while True:
        try:
            if all_data:
                DataCase.objects.bulk_create(all_data)
            if all_data_texts:
                TextsCase.objects.bulk_create(all_data_texts)
            break
        except:
            pass


def del_xml_files():
    list_rar_file = os.listdir()
    for rar_file in list_rar_file:
        if rar_file.find('.xml') != -1:
            os.remove(rar_file)


def main():
    del_xml_files()
    list_courts = ['ais', 'sgs', 'gagr', 'gud', 'srs', 'gul', 'och', 'tku', 'gal', 'voin']
    for court in list_courts:
        while True:
            try:
                get_file_ftp(court)
                break
            except:
                del_xml_files()
                time.sleep(1)
                print('bad connection ftp')
        unpack_rar()
        read_xml(court)
        del_xml_files()
