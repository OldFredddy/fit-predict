import pandas as pd
import numpy as np
import joblib

def load_model(path):
    return joblib.load(path)

def prepare_data(filepath, feature_names):
    # Чтение данных из Excel файла
    data = pd.read_excel(filepath)

    # Сохраняем копию исходных данных
    original_data = data.copy()

    # Удаление лишних столбцов
    data = data.drop(['Центр', 'Режим', 'Протокол', 'Особ_отмет', 'Радиосеть', 'Сервер_Клиент', 'Азимут', 'Место', 'Обр', 'Угол'], axis=1)

    # Преобразование данных
    data['Дата_Время'] = pd.to_datetime(data['Дата_Время'], dayfirst=True)
    data['Дата_Время'] = data['Дата_Время'].apply(lambda x: (x - pd.Timestamp('1970-01-01')).total_seconds())
    data['Длит'] = data['Длит'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))
    data['Размер'] = data['Размер'].str.replace(' кБт', '').astype(float)

    # Преобразование категориальных переменных в dummy-переменные
    data = pd.get_dummies(data)

    # Выравнивание столбцов с обученной моделью
    data = data.reindex(columns=feature_names, fill_value=0)

    return data, original_data
def predict(model, data, original_data):
    predictions = model.predict(data)
    original_data['Predict'] = predictions  # Добавляем колонку с предсказаниями
    return original_data


