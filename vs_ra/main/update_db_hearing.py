import ftplib
import time
import xml.etree.ElementTree as ET
import gzip
from .all_keys import keys_hearing as keys
from .models import HearingCase
import io
# from vs_ra.main.all_keys import keys, keys_texts


def get_file_ftp(court):
    all_data = []
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
                if file.split('.')[0].find('CaseList') == -1:
                    continue
                c = 0
                while True:
                    if c == 10:
                        break
                    try:
                        sio = io.BytesIO()

                        def handle_binary(more_data):
                            # print(more_data)
                            sio.write(more_data)

                        resp = ftp.retrbinary(f"retr {file}", callback=handle_binary)

                        sio.seek(0)  # Go back to the start
                        zippy = gzip.GzipFile(fileobj=sio)

                        uncompressed = zippy.read()
                        str_xml = ET.canonicalize(uncompressed)
                        root = ET.fromstring(str_xml)
                        root = root[0][2]
                        for row in root:
                            data = {}
                            for column in row:
                                if column.tag == 'Column':
                                    attrs = column.attrib
                                    attrs_name = attrs['Name']
                                    if attrs_name in keys:
                                        data[attrs_name] = attrs['Value']
                            if data:
                                data['Court'] = court
                                data['type_of_legal_proceeding'] = file.split('.')[0]
                                all_data.append(HearingCase(**data))
                        break
                    except:
                        time.sleep(1)
                        c += 1
                        pass
            break
    while True:
        try:
            if all_data:
                HearingCase.objects.bulk_create(all_data)
            break
        except:
            pass
    ftp.close()


def update_db_hearing():
    list_courts = ['ais', 'sgs', 'gagr', 'gud', 'srs', 'gul', 'och', 'tku', 'gal', 'voin']
    for court in list_courts:
        # while True:
        #     try:
                get_file_ftp(court)
                # break
            # except:
            #     time.sleep(10)
            #     print('bad connection ftp')


if __name__ == '__main__':
    update_db_hearing()
