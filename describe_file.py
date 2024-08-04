from src.describe_data import describe_data


def describe_file(file_path):
    # Étape 1 : Obtient le code de description du fichier
    description_code = describe_data(file_path)
    print("I HAVE A CODE!!!")
    desc = exec(description_code)
    print("DONE DESC HERE")
    return desc



if __name__ == "__main__":
    file_path = 'data/Sample - Superstore.xls'
    describe_file(file_path)
