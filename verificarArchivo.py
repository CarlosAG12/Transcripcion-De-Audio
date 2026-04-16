def verificarArchivo(mensaje, archivo):
    #Aca verificamos que sea formato audio, que no sea un virus, etc.
    #Por ahora solo verificamos que sea un formato de audio permitido
    if not mensaje:
        return False, "El nombre no puede estar vacío."
    
    if not archivo:
        return False, "No se ha proporcionado ningún archivo."

    formatosPermitidos = ["mp3", "wav", "ogg", "flac", "m4a"]
    extension = archivo.filename.split(".")[-1].lower()
    if extension not in formatosPermitidos:
        return False, "Formato de archivo no permitido. Solo se permiten archivos de audio (mp3, wav, ogg, flac, m4a)."
    return True, "Archivo verificado correctamente."