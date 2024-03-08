import pandas as pd
import numpy as np
from joblib import load

def load_model(path):
    return load(path)

def prepare_data(filepath, column_names):
    processed_lines = []
    with open(filepath, 'r') as file:
        for line in file:
            processed_line = line.replace('---', 'NaN').strip().split('\t')
            processed_line = [np.nan if x.strip() == '' else x for x in processed_line]
            processed_lines.append(processed_line)
    df = pd.DataFrame(processed_lines, columns=column_names)
    for col in ['Адрес', 'Объем', 'Ошибки', 'H-интервал', 'K-интервал', 'Скорость', 'Расстройка, Гц', 'Уровень, дБ']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df[['Адрес', 'H-интервал', 'K-интервал', 'Расстройка, Гц', 'Уровень, дБ']]

def predict(model, data):
    predictions = model.predict(data)
    data['Предсказание'] = predictions
    return data

def calculate_probability(data):
    count_1 = (data['Предсказание'] == 1).sum()
    count_0 = (data['Предсказание'] == 0).sum()
    total_predictions = count_1 + count_0
    probability_of_1 = (count_1 / total_predictions) * 100
    probability_of_0 = (count_0 / total_predictions) * 100
    if probability_of_1 > probability_of_0:
        return f"С вероятностью {probability_of_1:.2f}%, это воздушный УС"
    else:
        return f"С вероятностью {probability_of_0:.2f}%, это наземный УС"
# Остальной код остается без изменений

# Экспорт column_names
column_names = ['Номер', 'Время', 'Источник', 'Тип', 'Адрес', 'Объем', 'Ошибки', 'H-интервал', 'K-интервал', 'Скорость', 'Расстройка, Гц', 'Уровень, дБ']
