from datetime import datetime

def ordenar_ficheros_por_fecha_en_nombre(patron_fecha, ficheros):
    """
    Ordena una lista de nombres de ficheros según la fecha contenida en su nombre.

    Args:
        patron_fecha (re.Pattern): Patrón regex que captura la fecha en group(1).
        ficheros (list of str): Lista de nombres de ficheros a ordenar.

    Returns:
        list of str: Lista de nombres de ficheros ordenados cronológicamente según la fecha extraída.
    """
    archivos_con_fecha = []
    for fichero in ficheros:
        fecha = extraer_fecha_desde_nombre_fichero(patron_fecha, fichero)
        archivos_con_fecha.append((fecha, fichero))

    archivos_con_fecha.sort(key=lambda x: x[0])
    return [nombre for _, nombre in archivos_con_fecha]

def extraer_fecha_desde_nombre_fichero(patron_fecha, nombre_fichero):
    """
    Extrae la fecha del nombre de un fichero usando un patrón regex.

    Args:
        patron_fecha (re.Pattern): Patrón regex que captura la fecha en group(1).
        nombre_fichero (str): Nombre del fichero del que extraer la fecha.

    Returns:
        datetime: Objeto datetime con la fecha extraída.

    Raises:
        ValueError: Si no se encuentra fecha en el nombre del fichero.
    """
    match = patron_fecha.search(nombre_fichero)
    if not match:
        raise ValueError(f"El fichero {nombre_fichero} no contiene una fecha válida")

    fecha_str = match.group(1)
    return datetime.strptime(fecha_str, "%Y_%m_%d")


