import ctypes

class Model:
    DLL_PATH = './model/model.dll'

    def __init__(self):
        try:
            # Chargement de la DLL
            self.dll = ctypes.CDLL(self.DLL_PATH)
            
            # Initialisation des fonctions de la DLL que vous voulez utiliser
            self._initialize_functions()

            # Appel de la fonction d'initialisation de la DLL
            self.initialize()
        except OSError as e:
            print(f"Erreur lors du chargement de la DLL: {e}")
        except AttributeError as e:
            print(f"Erreur lors de l'initialisation des fonctions: {e}")
    
    def _initialize_functions(self):
        # Initialisation des fonctions de la DLL avec leurs types d'arguments et de retour
        
        # Exemple d'initialisation d'une fonction 'initialize'
        self.initialize = self.dll.initialize
        self.initialize.argtypes = []  # Liste des types des arguments
        self.initialize.restype = ctypes.c_int  # Type de retour
        
        # Exemple d'initialisation d'une fonction 'process'
        self.process = self.dll.process
        self.process.argtypes = [ctypes.c_char_p]  # Type des arguments (chaîne de caractères en C)
        self.process.restype = ctypes.c_char_p  # Type de retour (chaîne de caractères en C)

        # Vous pouvez ajouter d'autres fonctions ici de la même manière
        # self.other_function = self.dll.other_function
        # self.other_function.argtypes = [ctypes.c_int, ctypes.c_double]
        # self.other_function.restype = ctypes.c_double
    
    def process_message(self, message):
        try:
            # Traitement du message reçu du client avec la DLL
            result = self.process(message.encode('utf-8'))  # Appel de la fonction avec encodage du message
            return result.decode('utf-8')  # Décodage du résultat pour le retour en Python
        except Exception as e:
            print(f"Erreur lors du traitement du message: {e}")
            return None

# Exemple d'utilisation
if __name__ == "__main__":
    model = Model()
    message = "Message to process"
    response = model.process_message(message)
    if response:
        print("Response from DLL:", response)
    else:
        print("Aucune réponse reçue de la DLL.")
