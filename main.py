#import cbor2
import re
import os


if __name__ == '__main__':
    # Payload 2 example - telemetry
    # Payload Type, WD UID, UNIXTIME, Global counter, Frame Counter, Tick, Latitude, Longtitude, .....
    hex_payload2 = '9402462948003988bb1a62e207541a0004f5ff1a000162241a0002a4a5fa424170f6fa418cbf2405000bfa4315666601430000ff1900a402183b43143b9d42181703'

    # Payload 3 example - event
    # Payload Type, WD UID, UNIXTIME, Global counter, Frame Counter, Tick, PAYLOAD, Source (antenna/weight), Latitude, Longtitude
    hex_payload3 = '8903462948003988bb1a62e20e631a0004f61e1a00026c644c00000000000020000301556703fa42417b8cfa418cc6e5'
    # Payload 8 example - collection
    # Payload Type, WD UID, UNIXTIME, Global counter, Frame Counter, Weight[kg], ResultCode, werror, wseqnmr, TAG NR, Antenna, button, latitude, longtitude
    hex_payload8 = '8e08462948003988bb1a62e294281a000505451a00012b741affffffff180018001a000000004c000000000000200003017760041800fa42417d73fa418ce7e5'

    foo =b'\x14;\x9d'
#    print(cbor2.loads(bytes.fromhex(hex_payload2)))
#    print(cbor2.loads(bytes.fromhex(hex_payload3))[0])
#    print(cbor2.loads(bytes.fromhex(hex_payload8)))
#    print(" ".join(hex(n) for n in foo))

    output_data = b''

    # for root, dirs, files in os.walk("C:\Sensoneo\Sledovacka 220728/DebugLog 20220728"):
    #     for file in files:
    #         with open(os.path.join(root, file), 'rb') as log_file:
    #            temp = log_file.read()
    #            output_data += bytes('\r\n#' + str(file) + '\r\n' + '########################################' + '\r\n\r\n', "cp1250")
    #            output_data += temp
    #            log_file.close()
    #
    # with open("C:\Sensoneo\Sledovacka 220728/assembled.log", 'wb') as log_file:
    #     log_file.write(output_data)

#    with open("C:\Sensoneo\Sledovacka 220728/example.log", 'r', encoding="utf-16") as log_file:
    with open("C:\Sensoneo\Sledovacka 220728/example.log", 'r') as log_file:
        log_data = log_file.read()

    rfid_tags = re.findall("[0-9]{8} ntf\.ant.+", log_data, re.MULTILINE)  # Pattern for RFID reader data

#Parse RFID events in WD log
    rfid_collection = []
    for rfid_tag in rfid_tags:
        rfid_params = {"Timestamp": None,
                       "Source": None,
                       "ID": None,
                       "RSSI": None}

        rfid_params["Timestamp"] = re.findall("[0-9]{8}", rfid_tag)[0]
        rfid_params["Source"] =re.findall("ntf.ant:[3-4]", rfid_tag)[0][8:9]
        result = re.search("EPC:\s([a-f0-9][a-f0-9]\s){6,12}",rfid_tag).group()[5:]
        rfid_params["ID"] = re.sub(" ","",result)
        rfid_params["RSSI"] = re.search("RSSI = -[0-9][0-9].[0-9][0-9]", rfid_tag).group()[7:]
        rfid_collection.append(rfid_params)

#Parse WD message with RSSI and occurence

    rfid_tags = re.findall("RSSI -[0-9]+.[0-9]+,\(.+", log_data, re.MULTILINE)  # Pattern for RFID reader data
    rfid_occurences =[]
    for rfid_tag in rfid_tags:
        rfid_params = {"Timestamp_start": None,
                       "Timestamp_stop": None,
                       "Occurences":None,
                       "Source": None,
                       "ID": None,
                       "RSSI": None}

        timestamp = re.search("T=[0-9]+-[0-9]+", rfid_tag).group()
        rfid_params["Timestamp_start"] = re.findall("[0-9]+", timestamp)[0]
        rfid_params["Timestamp_stop"] = re.findall("[0-9]+", timestamp)[1]
        rfid_params["Occurences"] = re.search("[0-9]+", re.search("\(\s+[0-9]+\)", rfid_tag).group()).group()
        rfid_params["Source"] = re.findall("ant=[3-4]", rfid_tag)[0][4:5]
        rfid_params["ID"] = re.search("[a-f0-9]{12,24}", rfid_tag).group()
        rfid_params["RSSI"] = re.search("RSSI -[0-9][0-9].[0-9][0-9]", rfid_tag).group()[5:]

        rfid_occurences.append(rfid_params)

    for rfid_entry in rfid_occurences:
        rfid_entry[ID]


#   digisense_measurements = re.findall("DigiSe = [1-4], weight=[0-9]?[0-9]?[0-9]?.+", log_data)         #Pattern for Weight data

    # 00920744 digiS 2, 34 kg, 1, 1, 6052
#    digisense_measurements = re.findall("[0-9]{8} digiS [1-4].+", log_data)  # Pattern for Weight data


#    print(digisense_measurements)
