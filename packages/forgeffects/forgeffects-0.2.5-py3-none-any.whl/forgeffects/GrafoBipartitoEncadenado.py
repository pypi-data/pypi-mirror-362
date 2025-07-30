import tensorflow as tf

def GrafoBipartitoEncadenado(CC, CE, EE):

    if CC is None:
        CC = tf.zeros((CE.shape[0], CE.shape[1], CE.shape[1]))
    else:
        if CC.shape[1] != CE.shape[1] or CC.shape[2] != CE.shape[1]:
            raise ValueError("The rows and columns of CC must match the rows of CE.")

    if EE is None:
        EE = tf.zeros((CE.shape[0], CE.shape[2], CE.shape[2]))
    else:
        if EE.shape[1] != CE.shape[2] or EE.shape[2] != CE.shape[2]:
            raise ValueError("The rows and columns of EE must match the columns of CE.")

    # Zeros tiene (num de rep, num de filas de EE, num de columnas de CC) *da igual como se tomen las filas y columnas de EE Y CC*
    zeros = tf.zeros((CE.shape[0], EE.shape[1], CC.shape[2]))

    # Concatenar la parte superior (CC y CE) en el eje 2
    top_row = tf.concat([CC, CE], axis=2)

    # Concatenar la parte inferior (ceros y EE) en el eje 2
    bottom_row = tf.concat([zeros, EE], axis=2)

    # Concatenar la parte superior e inferior en el eje 1
    final_tensor = tf.concat([top_row, bottom_row], axis=1)

    return final_tensor

