from src.analyze_data import analyze_data


def analyze_file(file_path, user_question):
    # Charger la description sauvegardée
    with open('description.txt', 'r') as f:
        description = f.read()

    # Utilise les données de description pour analyser les données
    analysis_code = analyze_data(file_path, description, user_question)
    exec(analysis_code)


if __name__ == "__main__":
    file_path = 'data/Sample - Superstore.xls'
    user_question = "plot the monthly trend of sales and profit"
    analyze_file(file_path, user_question)
