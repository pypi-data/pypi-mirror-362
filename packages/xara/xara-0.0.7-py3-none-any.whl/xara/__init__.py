# try:
#     from opensees.openseespy import Model
# except:
#     Model = None

successful = 0

def __getattr__(name):
    global successful
    if name == "Model":
        try:
            from opensees.openseespy import Model
        except:
            Model = None
        if Model is None:
            raise ImportError("openseespy is not installed or not available.")
        return Model

    elif name == "successful":
        return successful
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")