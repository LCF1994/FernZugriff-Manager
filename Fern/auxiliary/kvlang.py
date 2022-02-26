from os import listdir, path


def string_builder(kv_files_path=None) -> str:
    if kv_files_path is None:
        kv_files_path = 'Fern/kv'

    # Errors
    if type(kv_files_path) is not str:
        raise TypeError
    if not path.exists(kv_files_path):
        raise FileNotFoundError

    kv_string = ''
    kv_file_list = filter(
        lambda file: file.endswith('.kv'), listdir(kv_files_path)
    )

    for kv_file in kv_file_list:
        with open(path.join(kv_files_path, kv_file), 'r') as opend_file:
            content = ''.join(opend_file.readlines())

            kv_string = '\n'.join([kv_string, content])

    return kv_string


if __name__ == '__main__':
    print(string_builder())
