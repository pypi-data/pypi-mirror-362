import random

class Disk:
    def __init__(self,alphabet:str = None,splits:list[int] = None,seed:int = None) -> None:
        """
        Maneja la creacion de las partes del 'Disk' que se usara para Encriptar / Desencriptar.

        Args:
            alphabet (str, optional): Alfabeto que se usara para el 'Disk'.
            splits (list[int], optional): Lista de splits que se usara para dividir el disco en partes.
            seed (int, optional): Seed que se usara para las partes que requieran ser randomizadas, asi podran replicarse.
        """

        _latin_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        self._entry_alphabet = alphabet.upper() if alphabet else _latin_alphabet
 
        self._random_seed = seed if seed else random.SystemRandom().randint(0, 2**32 - 1)

        self._random = random.Random(self._random_seed)
        
        self._shuffled_alphabet = self.__create_shuffle_alphabet()
    
        self._splits_list = splits if splits else self.__create_splits_list()

        self.__parts = self.__create_split_alphabet()
        
        self._disk_parts = {}
        for part in self.__parts:
            _id = f"{part[0]}{part[-1]}"
            self._disk_parts[_id] = {
                "lenght":len(part),
                "part":part
            }

    @property
    def parts_list(self):
        """
        Retorna una lista copia de de las partes del 'Disk'.
        """
        return self.__parts.copy()
    
    @property
    def parts_dict(self):
        """
        Retorna un diccionario copia de las partes del 'Disk'.
        """
        return self._disk_parts.copy()
    
    @property
    def splits(self) -> list[int]:
        """
        Retorna la lista copia de los splits usados para dividir el alfabeto en partes.
        """
        return self._splits_list.copy()
    
    @property
    def ids(self) -> list[str]:
        """
        Retorna la lista de las ids de cada parte.
        """
        return list(self._disk_parts.keys())
    
    @property
    def seed(self):
        """
        Retorna la semilla usada para las partes Random.
        """
        return self._random_seed
    
    @property
    def alphabet_len(self):
        """
        Retorna el tamaño del alfabeto.
        """
        return len(self._entry_alphabet)
    
    def to_dict(self) -> dict:
        return {
            "alphabet":self._entry_alphabet,
            "splits":self.splits,
            "seed":self.seed
        }
    
    @classmethod
    def from_dict(cls,dictionary:dict) -> None:
        """
        Crea una instancia de la clase usando un dict o JSON.

        Args:
            dictionary (dict): Conteniendo lo siguiente:
                - alphabet (str, optional): Alfabeto que se usara para el 'Disk'.
                - splits (list[int], optional): Lista de splits que se usara para dividir el disco en partes.
                - seed (int, optional): Seed que se usara para las partes que requieran ser randomizadas, asi podran replicarse.

        Returns:
            Instancia de la Clase: Configurada con los parametros obtenidos.
        """
        return cls(
            alphabet = dictionary.get("alphabet"),
            splits = dictionary.get("splits"),
            seed = dictionary.get("seed")
        )

    def validate_alphabets(self,source_alphabet:str = None) -> bool:
        return len(source_alphabet) == len(self._entry_alphabet)

    ## HELPERS ##
    def __create_shuffle_alphabet(self) -> str:
        """
        Randomiza el orden del alfabeto.

        Returns:
            str: Alfabeto revuelto / desordenado.
        """
        _shuffled_alphabet = list(self._entry_alphabet)[:]
        self._random.shuffle(_shuffled_alphabet)

        return "".join(_shuffled_alphabet)
    
    def __create_splits_list(self) -> list[int]:
        """
        Crea splits random, entre 3 y 6 partes.

        Returns:
            list[int]: Lista de splits.
        """
        _num_parts = self._random.randint(3,6)
        _len_alphabet = len(self._shuffled_alphabet)
        
        _base = _len_alphabet // _num_parts
        _extra = _len_alphabet % _num_parts

        _splits_list = [_base + (1 if i < _extra else 0) for i in range(_num_parts)]

        return _splits_list
    
    def __create_split_alphabet(self) -> list[str]:
        """
        Crea los splits del alfabeto y los splits guardados, esto creara lo que seran las partes del 'Disk'

        Returns:
            list[str]: Lista de partes del alfabeto.
        """
        _split_alphabet = []
        _temp_alphabet = self._shuffled_alphabet
        splits = self._splits_list
        idx = 0
        while len(_temp_alphabet) > 0:
            split_size = splits[idx % len(splits)]
            _split_alphabet.append(_temp_alphabet[:split_size])
            _temp_alphabet = _temp_alphabet[split_size:]
            idx += 1
        return _split_alphabet