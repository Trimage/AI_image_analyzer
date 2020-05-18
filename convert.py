

#파일을 바이너리 값으로 변환
def convertToBinaryData(filepath):
    # Convert digital data to binary format
    with open(filepath, 'rb') as file:
        binaryData = file.read()

    print(binaryData)
    return binaryData