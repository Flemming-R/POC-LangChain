import subprocess

def get_ollama_model_names(debug=False):
    """
    Ruft über den Befehl "ollama list" die Modellnamen ab und gibt sie als Liste von Strings zurück.
    
    Parameter:
      debug (bool): Falls True, wird die Rohausgabe sowie der extrahierte Modellnamen-Output ausgegeben.
      
    Rückgabe:
      Eine Liste der Modellnamen (Strings). Wenn keine Ausgabe vorliegt, wird eine leere Liste zurückgegeben.
    """
    # Führe den Befehl aus und erfasse die Ausgabe als Text
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    output = result.stdout.strip()
    
    if debug:
        print("Rohausgabe von 'ollama list':")
        print(output)
    
    # Zerlege die Ausgabe in einzelne Zeilen
    lines = output.splitlines()
    if not lines:
        if debug:
            print("Keine Ausgabe erhalten.")
        return []
    
    # Überspringe die Kopfzeile (erste Zeile) und sammle den ersten Bestandteil jeder Zeile (Modellname)
    model_names = []
    for line in lines[1:]:
        parts = line.split()
        if parts:
            model_names.append(parts[0])
    
    if debug:
        print("Model names:", model_names)
    
    return model_names

# Beispielhafter Aufruf der Funktion:
if __name__ == '__main__':
    names = get_ollama_model_names(debug=True)
    print("Abgerufene Modellnamen:", names)
