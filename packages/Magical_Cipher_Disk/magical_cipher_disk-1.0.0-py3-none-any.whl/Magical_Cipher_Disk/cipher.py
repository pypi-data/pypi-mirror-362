from .disk import Disk
from .stones_holder import StoneHolder
from .cipher_io import CipherIO
import random
from unidecode import unidecode

class Cipher:

    def __init__(self,disk:Disk = None,stone_holder:StoneHolder = None,logger:CipherIO = CipherIO(),seed:int = None):
        """
        Maneja el Encriptado o Desencriptado, usando el 'Disk' y las 'Stones' del 'StoneHolder'.

        Usa un estado o seed para lo que requiera randomizacion, y asi poder replicarlo.

        Args:
            disk (Disk, optional): Disk que se usara para el cifrado.
            stone_holder (StoneHolder, optional): StoneHolder que guarda las Stones que se usaran para los efectos y transformaciones.
            logger (CipherIO, optional): Logger para guardar todo el proceso y configuraciones, usa la clase CipherIO.
            seed (int, optional): Seed que se usara para las partes que requieran ser randomizadas, asi podran replicarse.
        """
        self._logger = logger if logger else CipherIO()

        self._stone_holder = stone_holder
        self._disk = disk

        self._random_seed = seed if seed else random.SystemRandom().randint(0, 2**32 - 1)

        self._random = random.Random(self._random_seed)

        self.__disk_order = None
        self.__disk_index = None
        self._source_alphabet = None
        self.__target_alphabet = None

    @property
    def source_alphabet(self) -> str:
        """
        Retorna el alfabeto proporcionado en la configuracion del cifrador.
        """
        return self._source_alphabet
    
    @property
    def target_alphabet(self) -> str:
        """
        Retorna el alfabeto del 'Disk' proporcionado.
        """
        return self.__target_alphabet

    def Encrypt(self,entry_text:str = None,save_result:bool = True,context_for_log:str = "") -> str:
        """
        Encripta el texto proporcionado.        

        Args:
            entry_text (str, optional): Texto para encriptar.
            save_result (bool, optional): Se guardara el resultado en un log o no. Default en True.
            context_for_log (str, optional): Sera el nombre que se añadira al archivo generado.

        Returns:
            str: Texto Encriptado.
        """
        return self._Cipher(
            entry_text=entry_text,
            isEncrypted=False,
            save_result=save_result,
            context_for_log=context_for_log
        )
    
    def Decrypt(self,entry_text:str = None,save_result:bool = True,context_for_log:str = "") -> str:
        """
        Desencripta el texto proporcionado.        

        Args:
            entry_text (str, optional): Texto para desencriptar.
            save_result (bool, optional): Se guardara el resultado en un log o no. Default en True.
            context_for_log (str, optional): Sera el nombre que se añadira al archivo generado.

        Returns:
            str: Texto Desencriptado.
        """
        return self._Cipher(
            entry_text=entry_text,
            isEncrypted=True,
            save_result=save_result,
            context_for_log=context_for_log
        )
    
    def config_cipher(self,source_alphabet:str = None,disk_order:list[str] = None,disk_index:tuple[str,str] = None):
        """
        Configuira el cifrado que se hara, con los siguientes parametros.

        Args:
            source_alphabet (str, optional): Alfabeto que se usara como origen.
            disk_order (list[str], optional): Orden de las partes del 'Disk'
            disk_index (tuple[str,str], optional): Index con el que se juntaran los alfabetos, estos deben ser 1 letra del original y 1 del alfabeto del 'Disk'.
        """
        _source_alphabet = source_alphabet.upper() if source_alphabet else 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if not self._disk.validate_alphabets(_source_alphabet):
            raise ValueError(f"Alphabets are not the same lenght, wich will cause errors in the Encryption or Decryption\nlen of disk {self._disk.alphabet_len}\nlen of cipher {len(source_alphabet)}")

        self.__disk_order = disk_order if disk_order else self._random_disk_order()

        disk_parts = self._disk.parts_dict
        
        _temp_alphabet = ''.join(
            letter
            for disk_id in self.__disk_order
            for letter in disk_parts[disk_id]["part"]
        )

        if disk_index:
            self.__disk_index = disk_index
        else:
            _index_1 = self._random.choice(_source_alphabet)
            _index_2 = self._random.choice(_temp_alphabet)
            self.__disk_index = (_index_1,_index_2)
        
        _index_source_alphabet = _source_alphabet.index(str(self.__disk_index[0]).upper())
        _index_target_alphabet = _temp_alphabet.index(str(self.__disk_index[1]).upper())

        self._source_alphabet = _source_alphabet[_index_source_alphabet:] + _source_alphabet[:_index_source_alphabet]
        self.__target_alphabet = _temp_alphabet[_index_target_alphabet:] + _temp_alphabet[:_index_target_alphabet]

        return self

    def _Cipher(self,entry_text:str = None,isEncrypted:bool = False,save_result:bool = True,context_for_log:str = "") -> str:
        """
        Encargado de encriptar o desencriptar, maneja el paso de las letras al 'StoneHolder' o el paso de caracteres especiales
        como comas, guiones, espacios, etc.

        Args:
            entry_text (str, optional): Texto de entrada al que se le aplicaran las transformaciones.
            isEncrypted (bool, optional): Esta encriptado o no esta encriptado, asi se sabra que transformaciones hacer. Default en False.
            save_result (bool, optional): Se guardara el resultado o no se guardara. Defaults en True.
            context_for_log (str, optional): Sera el nombre que se añadira al archivo generado.

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not entry_text or entry_text == "":
            raise ValueError("There is no text")

        _entry_text = entry_text
        _isEncrypted = isEncrypted

        _normal_alphabet,_cipher_alphabet = self._get_alphabets(_isEncrypted)

        # Normalize text, for accents and spaces
        _normalized_entry_text = ''
        for _letter in _entry_text:
            if _letter not in _normal_alphabet:
                _normalized_entry_text += self._normalize_text(_letter,True)
            else:
                _normalized_entry_text += self._normalize_text(_letter)
        
        # Cipher
        _cipher_text = ""
        for i in range(len(_normalized_entry_text)):
            _temp_letter = _normalized_entry_text[i]
            
            # it expects that the _normal_alphabet doesn't containt spaces,
            # if there is space it skips it
            if _temp_letter in _normal_alphabet:
                    _cipher_text += self._stone_holder.apply_stones(_temp_letter,i,_normal_alphabet,_cipher_alphabet,_isEncrypted)
            else:
                if _temp_letter != " ":
                    self._stone_holder.add_step(f"{_temp_letter} -- PASS")
                _cipher_text += _temp_letter

        if save_result:
            self._logger.log_cipher(
                original_text=_entry_text,
                result_text=_cipher_text,
                isEncrypted=_isEncrypted,
                disk=self._disk,
                disk_order=self.__disk_order,
                disk_index=self.__disk_index,
                stone_holder=self._stone_holder,
                name=context_for_log,
                source_alphabet=self._source_alphabet,
                target_alphabet=self.__target_alphabet,
                cipher_seed=self._random_seed
            )

        self._stone_holder._clean_steps()
        return _cipher_text


    ## HELPERS ##
    def _random_disk_order(self) -> list[str]:
        """
        Randomiza el orden de las partes del 'Disk' usando las ids de las partes.

        Returns:
            list[str]: Lista del orden randomizado.
        """
        keys = self._disk.ids
        choices = []
        for i in range(len(keys)):
            random_key = self._random.choice(keys)
            choices.append(random_key)
            keys.remove(random_key)
        return choices
    
    def _get_alphabets(self,isEncrypted) -> tuple[str,str]:
        """
        Revisa si se debe encriptar o desencriptar, para devolver el alfabeto como se requiera.

        Args:
            isEncrypted (bool): El texto viene encriptado o no.

        Returns:
            tuple[str,str]: Alfabetos en orden en el que se requieren para las transformaciones.
        """
        if isEncrypted:
            return self.__target_alphabet,self._source_alphabet
        else:
            return self._source_alphabet,self.__target_alphabet
        
    def _normalize_text(self,text:str='',isUnidecode:bool=False) -> str:
        """
        Normaliza el texto para evitar acentos u otros caracteres especiales.
        Ademas de devolverlo commo mayusculas.

        Args:
            text (str, optional): Texto que se requiere normalizar.
            isUnidecode (bool, optional): Se requiere unidecode o no se requiere.

        Returns:
            str: Texto normalizado.
        """
        _text = text.upper()
        return unidecode(_text) if isUnidecode else _text