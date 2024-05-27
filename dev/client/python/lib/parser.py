import json
import re
import enum


class Parser:
    """
    A class that provides methods for parsing messages to JSON and vice versa.
    """

    class RegexPattern(enum.Enum):
        PATTERN_1 = r'^[A-Za-z]+$'
        PATTERN_2 = r'^\d+$'
        PATTERN_3 = r'^[A-Za-z0-9]+$'
        
        
    def message_to_json(self, message):
        """
        Converts the given message to JSON format.

        Args:
            message (str): The message to be converted.

        Returns:
            str: The JSON representation of the message.
        """
        return #processing du message ici pour l'envoyer au gestionnaire du modèle derrière
    
    def json_to_message(self, json_message):
        """
        Converts the given JSON message to a regular message.

        Args:
            json_message (str): The JSON message to be converted.

        Returns:
            str: The regular message.
        """
        return #processing du message ici pour l'envoyer au serveur depuis le modèle
