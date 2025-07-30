import numpy as np
import pandas as pd
import tensorflow as tf

def process_data(tensor, values, CC=None, CE=None, EE=None, causes=None, effects=None):
    # Asegurarnos de que 'tensor' y 'values' sean arreglos de NumPy
    if isinstance(tensor, tf.Tensor):
        tensor = tensor.numpy()
    if isinstance(values, tf.Tensor):
        values = values.numpy()
    
    # Eliminar la primera columna de 'tensor'
    tensor = tensor[:, 1:]

    # Obtener el número de columnas en 'tensor'
    n_cols = tensor.shape[1]

    # Construir los nombres de las columnas
    col_names = ['From'] + [f'Through{i+1}' for i in range(n_cols - 2)] + ['To']

    # 'tensor' y 'values' ya son arreglos de NumPy
    tensor_np = tensor
    values_np = values

    # Crear un diccionario para almacenar las filas y sus posiciones
    row_dict = {}
    for idx, row in enumerate(tensor_np):
        row_key = tuple(row.tolist())
        if row_key in row_dict:
            row_dict[row_key].append(idx)
        else:
            row_dict[row_key] = [idx]

    # Preparar datos para construir el DataFrame
    data = []
    for row_key, positions in row_dict.items():
        positions_np = np.array(positions)
        values_at_positions = values_np[positions_np]
        count = len(positions)
        mean_value = values_at_positions.mean()
        std_value = values_at_positions.std(ddof=0)  # Desviación estándar
        data_row = list(row_key) + [count, mean_value, std_value]
        data.append(data_row)

    # Construir los nombres de las columnas
    df_columns = col_names + ['Count', 'Mean', 'SD']

    # Crear el DataFrame
    df = pd.DataFrame(data, columns=df_columns)

    # Ordenar el DataFrame por 'Count' de mayor a menor
    df = df.sort_values(by='Count', ascending=False).reset_index(drop=True)

    # Mapear números a etiquetas según las condiciones
    mapping = {}

    if causes is not None and effects is None:
        # Caso: Solo 'causes' es proporcionado
        labels = causes
        mapping = dict(zip(range(len(labels)), labels))

    elif effects is not None and causes is None:
        # Caso: Solo 'effects' es proporcionado
        labels = effects
        mapping = dict(zip(range(len(labels)), labels))

    elif causes is not None and effects is not None:
        # Caso: Ambos 'causes' y 'effects' son proporcionados
        labels_causes = causes
        labels_effects = effects
        labels = labels_causes + labels_effects
        mapping = dict(zip(range(len(labels)), labels))

    else:
        # Cuando 'causes' y 'effects' son None
        # Asegurarnos de que 'CC', 'CE' y 'EE' sean arreglos de NumPy si son tensores
        if CC is not None and isinstance(CC, tf.Tensor):
            CC = CC.numpy()
        if CE is not None and isinstance(CE, tf.Tensor):
            CE = CE.numpy()
        if EE is not None and isinstance(EE, tf.Tensor):
            EE = EE.numpy()

        if CC is not None and CE is not None and EE is not None:
            # Caso: CC, CE y EE existen
            M = CE.shape[1]
            N = CE.shape[2]
            labels_causes = [f'a{i+1}' for i in range(M)]
            labels_effects = [f'b{i+1}' for i in range(N)]
            labels = labels_causes + labels_effects
            mapping = dict(zip(range(M + N), labels))
        elif CC is not None and CE is not None and EE is None:
            # Caso: CC y CE existen
            M = CE.shape[1]
            N = CE.shape[2]
            labels_causes = [f'a{i+1}' for i in range(M)]
            labels_effects = [f'b{i+1}' for i in range(N)]
            labels = labels_causes + labels_effects
            mapping = dict(zip(range(M + N), labels))
        elif CC is None and CE is not None and EE is not None:
            # Caso: CE y EE existen
            M = CE.shape[1]
            N = CE.shape[2]
            labels_causes = [f'a{i+1}' for i in range(M)]
            labels_effects = [f'b{i+1}' for i in range(N)]
            labels = labels_causes + labels_effects
            mapping = dict(zip(range(M + N), labels))
        elif CC is not None and CE is None and EE is None:
            # Caso: Solo CC existe
            N = CC.shape[1]
            labels = [f'a{i+1}' for i in range(N)]
            mapping = dict(zip(range(N), labels))
        elif CC is None and CE is None and EE is not None:
            # Caso: Solo EE existe
            N = EE.shape[1]
            labels = [f'b{i+1}' for i in range(N)]
            mapping = dict(zip(range(N), labels))
        else:
            raise ValueError("The provided combination of tensors is not valid.")

    # Aplicar el mapeo al DataFrame
    for col in col_names:
        df[col] = df[col].map(mapping)

    return df

