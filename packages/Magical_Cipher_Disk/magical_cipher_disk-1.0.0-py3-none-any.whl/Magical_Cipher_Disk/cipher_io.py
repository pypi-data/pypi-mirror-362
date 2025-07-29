from pathlib import Path
from datetime import datetime

from .disk import Disk
from .stones_holder import StoneHolder

class CipherIO:
    def __init__(self,base_path:str = "./Messages",debug:bool = False):
        """
        Maneja la creacion del archivo donde se guardan las configuraciones y demas del Cipher.

        Args:
            base_path (str, optional): Path Base de donde se quieren guardar los archivos. Default en "./Messages".
            debug (bool, optional): Esta en modo debug o no. Default en False.
        """
        self._isDebug = debug
        self._base_path:Path = Path(base_path).resolve()
        self._base_path.mkdir(parents=True, exist_ok=True)

        self._encrypted_dir = self._base_path / "Encrypted"
        self._decrypted_dir = self._base_path / "Decrypted"

        _paths = [self._encrypted_dir, self._decrypted_dir]
        for d in _paths:
            d.mkdir(parents=True, exist_ok=True)

    def _unique_path(self, name: str,timestamp:str, is_encrypted_suffix: str, ext: str = "txt") -> Path:
        """
        Creacion del path del archivo para que sea unico.

        Args:
            name (str): Nombre del archivo.
            timestamp (str): Fecha.
            is_encrypted_suffix (str): Esta encriptado o no esta encriptado.
            ext (str, optional): Extension del archivo. Default en "txt".

        Returns:
            Path: Path completo del archivo
        """
        filename = f"{timestamp}_{is_encrypted_suffix.upper()}_{name}.{ext}"
        _is_encrypted_suffix = is_encrypted_suffix.lower() 

        if _is_encrypted_suffix == "encrypted":
            return self._encrypted_dir / filename
        elif _is_encrypted_suffix == "decrypted":
            return self._decrypted_dir / filename
        else:
            return self._base_path / filename
    
    def log_cipher(self,
                original_text:str,result_text:str,isEncrypted:bool,
                disk:Disk,disk_order:list[str],disk_index:tuple[str,str],stone_holder:StoneHolder,
                name:str, source_alphabet:str, target_alphabet:str, cipher_seed:int
            ) -> None:
        """
        Guarda la configuracion, el texto de entrada y salida, y las piedras usadas.

        Ademas, si existen, se guardaran los 'steps' / 'pasos' de la transformacion del texto.

        Args:
            original_text (str): Texto original.
            result_text (str): Texto como resultado, ya sea encriptado o desencriptado.
            isEncrypted (bool): El texto original esta encriptado o desencriptado.
            disk (Disk): Disk usado en el cifrado.
            disk_order (list[str]): Orden de las partes del Disk
            disk_index (tuple[str,str]): Index de los alfabetos.
            stone_holder (StoneHolder): StoneHolder.
            name (str): Nombre para el archivo como extra.
            source_alphabet (str): Alfabeto original.
            target_alphabet (str): Alfabeto del Disk.
        """

        is_encrypted_suffix = "DECRYPTED" if isEncrypted else "ENCRYPTED"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        _name = name if name else ""

        required = {
                "original_text": original_text,
                "result_text": result_text,
                "disk": disk,
                "disk_order": disk_order,
                "disk_index": disk_index,
                "stone_holder": stone_holder,
                "source_alphabet": source_alphabet,
                "target_alphabet": target_alphabet
            }

        for key, value in required.items():
            if value is None or value == "":
                raise ValueError(f"Missing required: '{key}'")
            
        path = self._unique_path(_name,timestamp,is_encrypted_suffix)

        data = ""

        data += f"###### {is_encrypted_suffix} ######\n"
        data += f"Date: {timestamp}\n\n"

        data += f"###### TEXT ######\n"
        data += f"{original_text}\n\n"
        data += f"###### RESULT {is_encrypted_suffix} ######\n"
        data += f"{result_text}\n\n"

        data += f"###### ALPHABETS ######\n"
        data += f"Source Alphabet: {source_alphabet}\n"
        data += f"Target Alphabet: {target_alphabet}\n\n"

        data += f"###### Disk ######\n"
        data += f"Seed: {disk.seed}\n"
        data += f"Splits: {disk.splits}'\n"
        data += f"Ids: {disk.ids}\n"
        data += f"Parts. {disk.parts_list}\n"
        data += f"Order: {disk_order}\n"
        data += f"Index: {disk_index}\n\n"


        data += f"###### Stones ######\n"
        data += f"[STONE] -- [VALUE]\n"

        stones = stone_holder.stones
        for stone in stones:
            _stone = stones.get(stone)
            data += f"{_stone.name} -- {_stone.value}\n"
        
        data += f"\n###### Cipher ######\n"
        data += f"Seed: {cipher_seed}\n"

        _traces = stone_holder.steps
        if _traces:
            data += f"\n###### TRACES ######\n"
            data += f"{_traces}"

        path.write_text(data,encoding="utf-8")