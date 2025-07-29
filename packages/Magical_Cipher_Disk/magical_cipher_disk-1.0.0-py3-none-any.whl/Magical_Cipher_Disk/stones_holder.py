from .stones import BaseStone

class StoneHolder:
    def __init__(self,stones:list[BaseStone]) -> None:
        """
        Guarda la coleccion de 'Stones' y maneja cuando aplicar sus efectos para las transformaciones de letras.

        Combina la lista dada de 'Stones' en un diccionario de nombre y valor para un uso mas sencillo.
        Ademas recuerda / guarda los 'steps' / 'pasos' de cada transforacion para poder hacer un log despues.

        Args:
            stones (list[BaseStone]): Lista de 'BaseStones' de la cual se tomaran los efectos para las transforaciones.
        """
        self._stones:dict[str,BaseStone] = self._merge_stones(stones)
        self._steps:list[str] = []

    @property
    def stones(self) -> dict[str,BaseStone]:
        """
        Retorna un diccionario copia de 'Stones' guardadas, por nombre y valor.
        """
        return self._stones.copy()
    
    @property
    def steps(self) -> str:
        """
        Retorna un string formateado de todos los 'steps' / 'pasos' guardados, uno por linea.
        """
        return "\n".join(self._steps)
    
    def apply_stones(self,letter:str,position:int = 0,source_alphabet:str = None,target_alphabet:str = None,isEncrypted:bool = False) -> str:
        """
        Aplica transformaciones basadas en las 'Stones' que fueron guardadas previamente usando el 'StoneHolder', estas transformaciones
        cambian la letra a otra.

        Ademas se guarda el 'step' / 'paso' por cada transformación.

        Args:
            letter (str): La letra a la que se aplicaran los cambios.
            position (int): La posicion de la letra en la frase u oracion, usada para saber cuando aplicar las piedras.
            source_alphabet (str): El alfabeto de origen del que se tomara el indice de la letra.
            target_alphabet (str): El alfabeto objetivo del que se usara la letra para sustituir.
            isEncrypted (bool, optional): El valor para conocer si se esta Encriptando o Desencriptando.

        Raises:
            ValueError: Error conel Alfabeto.

        Returns:
            str: La letra cambiada despues de todas las transformaciones. 
        """

        if not source_alphabet or not isinstance(source_alphabet,str):
            raise ValueError(f"Error with the alphabet {source_alphabet}") 
        
        if not target_alphabet or not isinstance(target_alphabet,str):
            raise ValueError(f"Error with the alphabet {target_alphabet}")

        YELLOW_STONE:BaseStone = self._stones.get("YELLOW")
        REDGREEN_STONE:BaseStone = self._stones.get("RED-GREEN")
        BLUE_STONE:BaseStone = self._stones.get("BLUE")

        if YELLOW_STONE and position > 0:
            if YELLOW_STONE.value > 0 and position % YELLOW_STONE.value == 0:
                
                _letter = letter

                if REDGREEN_STONE:
                    _letter = REDGREEN_STONE.apply(_letter, source_alphabet, target_alphabet, isEncrypted)

                    # saving trace trace
                    self.add_step(f"{letter} -> {_letter} -- Change [RED-GREEN]")
                
                if BLUE_STONE:
                    if BLUE_STONE.value > 0 and position % BLUE_STONE.value == 0:
                        _temp_blue_letter = _letter
                        _letter = BLUE_STONE.apply(_letter, source_alphabet, target_alphabet, isEncrypted)

                        # saving trace trace
                        self.add_step(f" ^ {_temp_blue_letter} -> {_letter} -- Change [BLUE]")
                
                return _letter
            
        result = self._change_letter(letter,source_alphabet,target_alphabet)

        # saving trace trace
        self.add_step(f"{letter} -> {result} -- Change [SIMPLE]")

        return result
    
    ## GETTERS ##
    def get_steps_by_stone(self, stone_name: str) -> list[str]:
        """
        Toma los 'steps' / 'pasos' para devolver solo aquellos que sean de la piedra
        requerida.

        Args:
            stone_name (str): Nombre de la piedra de la cual se quieren obtener los 'steps' / 'pasos'.

        Returns:
            list[str]: Lista de 'steps' / 'pasos' de la piedra especificada.
        """
        return [t for t in self._steps if f"[{stone_name.upper()}]" in t]
    
    ## HELPERS ##
    def _merge_stones(self,stones:list[BaseStone]) -> dict[str,BaseStone]:
        """
        Toma la lista de 'BaseStones' para combinar sus valores y guardarlos en un diccionario.

        Args:
            stones (list[BaseStone]): Lista de 'BaseStones'.

        Returns:
            dict[str,BaseStone]: Diccionario de nombre y valor de cada 'BaseStone'
        """
        merged = {}
        for stone in stones:
            key  = stone.name
            if key in merged:
                merged[key] = merged[key] + stone
            else:
                merged[key] = stone
        return merged

    def _change_letter(self,letter:str,source_alphabet:str,target_alphabet:str) -> str:
        """
        Cambia la letra a su substitucion directa del 'source alphabet' al 'target alphabet',
        usando el indice de la letra.

        Args:
            letter (str): La letra que se cambiara.
            source_alphabet (str): El alfabeto de origen del que se tomara el indice de la letra.
            target_alphabet (str): El alfabeto objetivo del que se usara la letra para sustituir.

        Returns:
            str: La letra cambiada.
        """
        _index = source_alphabet.index(str.upper(letter))
        _result = str.upper(target_alphabet[_index])
        return _result
    
    def _clean_steps(self) -> None:
        """
        Limpia / Reinicia los 'steps' / 'pasos' que se guardaron anteriormente
        """
        self._steps = []

    def add_step(self,text:str) -> None:
        """
        Añade 'steps' / 'pasos' para guardar el proceso.

        Args:
            text (str): El texto que se guardara como 'step' / 'paso'
        """
        self._steps.append(text)