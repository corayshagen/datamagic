import os
import azure.storage.blob

def get_container():
    url = os.environ['CONTAINER_URL']
    return azure.storage.blob.ContainerClient.from_container_url(url)

def print_directory(container):
    for blob in container.list_blobs():
        print(f'{blob.size:>20} {blob.name}')

def read_lasfile(container, filename):
    blob_client = container.get_blob_client(filename)
    data = blob_client.download_blob().content_as_bytes()
    lines = []
    for line in data.splitlines():
        lines.append(line.decode("ascii", errors='ignore'))
    return lines

def find_section_index(lines, prefix):
    idx = 0
    for line in lines:
        if line.startswith(prefix):
            break
        idx += 1
    return idx

def get_header_section(lines):
    return lines[:find_section_index(lines, '~A')]

def get_data_section(lines):
    return lines[find_section_index(lines, '~A')+1:]

def print_header_section(lines):
    for line in get_header_section(lines):
        print(line)

def print_data_section(lines):
    for line in get_data_section(lines):
        print(line)

def main():
    container = get_container()
    #print_directory(container)

    lasfile = '31_5-7 Eos/07.Borehole_Seismic/TZV_TIME_SYNSEIS_2020-01-17_2.LAS'
    lines = read_lasfile(container, lasfile)
    print(len(get_header_section(lines)))
    print(len(get_data_section(lines)))

if __name__ == '__main__':
    main()
