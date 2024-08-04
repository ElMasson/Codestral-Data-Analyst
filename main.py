from src.describe_data import describe_data
from src.analyze_data import analyze_data

def describe_and_analyze_file(file_path, user_question):
    # Générer et exécuter le code pour l'analyse
    analysis_code = analyze_data(file_path, user_question)
    print("Analysis Code Generated!!!")
    print(analysis_code)

    # Exécuter le code d'analyse et capturer le résultat
    exec(analysis_code)
    print("Analysis Data Captured!!!")

    return analysis_code
