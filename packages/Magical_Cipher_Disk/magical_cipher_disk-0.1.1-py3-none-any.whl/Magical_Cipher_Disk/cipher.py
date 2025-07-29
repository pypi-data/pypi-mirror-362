from .disk import Disk
from .stones import Stones
import random
from unidecode import unidecode
from pathlib import Path

class Cipher:
    def __init__(self,disk:Disk=None,stones:Stones=None) -> None:
        
        self.__disk = disk
        self.__disk_keys = self.__disk.get_id()
        
        self.__stones = stones
        
        self.__alphabet_disk = ''
        self.__comparative_alphabet = ''
        self.__encrypted_text = ''
        self.__entered_text = ''
        
    def save_encrypted(self,path:str='.',context:str=''):
        
        if path != None:
            
            _isEncrypted = self.__isEncrypted
            
            if _isEncrypted:
                path += '/Decrypted_Messages'
                _isEncrypted_txt = 'Desencriptado'
            else:
                path += '/Encrypted_Messages'
                _isEncrypted_txt = 'Encriptado'
                
            
            if context != None:
                _context = context
            else:
                _context = ''
        
        
            # Llamado de las variables a guardar
            _encrypted_text = self.get_encrypted_text()
            _normal_text = self.get_entered_text()
            
            _comparative_alphabet = self.__comparative_alphabet
            
            _disk = self.__disk
            _disk_serie = _disk.get_serie()
            _disk_order = self.__disk_order
            _disk_index = self.__disk_index
            _stones = self.__stones
            
            file_name = f'{_disk_serie}_{_context}'
            
            #Creacion de directorio y archivo unico
            p = Path(path)
            p.mkdir(parents=True, exist_ok=True)
            _unique_file = Path(f"{self.__unique_path__(path,file_name)}")
            
            #Guardado de archivo
            result = ''
            
            result += f'Guardado del texto {_isEncrypted_txt}\n\n'
            result += f'Alfabeto usado para la comparación: {_comparative_alphabet}\n\n'
            result += f'######## Texto Proporcionado ########\n'
            result += f'{_normal_text}\n'
            result += f'#####################################\n\n'
            result += f'######## Texto {_isEncrypted_txt} ########\n'
            result += f'{_encrypted_text}\n'
            result += f'#####################################\n\n'
            
            result += f'{_disk}'
            result += f'Orden: {_disk_order}\n'
            result += f'Index: {_disk_index}\n\n'
            
            result += f'{_stones}\n'
            
            
            with _unique_file.open("w", encoding ="utf-8") as f:
                f.write(result)        
      
    
    def config_comparative_alphabet(self,comparative_alphabet:str=None,disk_order:list=None,disk_index:tuple=None):
        
        if comparative_alphabet != None:
            _comparative_alphabet = comparative_alphabet
        else:
            _comparative_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            
            
        if disk_order != None:
            self.__disk_order = disk_order
        else:
            #random select del disk order
            self.__disk_order=self.__random__disk__order(self.__disk)
        
        
        _temp_alphabet = ''
        for _d in self.__disk_order:
            _temp_disk = self.__disk.get_disk()["disk"][_d]["disk"]
            for _l in _temp_disk:
                _temp_alphabet += _l
                
        
        #configuracion de orden seleccionado para el disco
        if disk_index != None:
            self.__disk_index = disk_index
        else:
            #random select del disk index
            _index_choice_1 = random.choice(_comparative_alphabet)
            _index_choice_2 = random.choice(_temp_alphabet)
            self.__disk_index = [_index_choice_1,_index_choice_2]
        
                
                
        _index_alphabet_comparative = _comparative_alphabet.index(str(self.__disk_index[0]).upper())     
        _index_alphabet_disk = _temp_alphabet.index(str(self.__disk_index[1]).upper())
        
        self.__comparative_alphabet = _comparative_alphabet[_index_alphabet_comparative:] + _comparative_alphabet[:_index_alphabet_comparative]
        self.__alphabet_disk = _temp_alphabet[_index_alphabet_disk:] + _temp_alphabet[:_index_alphabet_disk]
        
        return self
    
    def Encrypt(self,txt:str='',isEncrypted:bool=False):
        
        self.__entered_text = txt
        self.__isEncrypted = isEncrypted
        
        if not self.__isEncrypted:
            _normal_alphabet = self.__comparative_alphabet
            _encrypt_alphabet = self.__alphabet_disk
        else:
            _normal_alphabet = self.__alphabet_disk
            _encrypt_alphabet = self.__comparative_alphabet
        
        
        #normalizacion del texto, espacios y acentos
        _entry_text = ''
    
        for _txt in self.__entered_text:
            if _txt not in _normal_alphabet:
                _entry_text += self.__normalize_text__(_txt,True)
            else:
                _entry_text += self.__normalize_text__(_txt)
                
        
        # guardar espacios entre palabras, para asi reconstruirlo al final
        _entry_text_spaces = [len(_s) for _s in txt.split()]
        
        
        #Encriptador
        _new_text = ''
        for _t in range(len(_entry_text)):
            
            _temp_t = _entry_text[_t] #letra a letra
            _range_yellow = self.__stones.get_stone_yellow()
            
            if _temp_t in _normal_alphabet and _range_yellow > 0:  #si esta en el alfabeto normal continua, sino lo toma como un caracter especial
                
                if (_t % _range_yellow == 0) and (_t > 0): 
                    # si el numero de letra coincide con el valor de la piedra amarilla, se ejecutara el cambio
                    _new_text += self.__stones.apply_stones(_temp_t,_normal_alphabet,_encrypt_alphabet,self.__isEncrypted,_t)
                
                else:
                    _new_text += self.__change_letter__(_temp_t,_normal_alphabet,_encrypt_alphabet)
            
            else:
                #Pasarlo como especial, acentos interrogantes o numeros, osea sin cambios
                _new_text += _temp_t
        
        
        
        # Reconstruccion de texto con espacios
        _text_return = ''
        for _sp in _entry_text_spaces:
            _text_return += f"{_new_text[:_sp]} "
            _new_text = _new_text[_sp:]
            
            
        self.__encrypted_text = _text_return
        
        return self
    
    
    #### Getters ####
    
    def get_encrypted_text(self):
        return self.__encrypted_text
  
    def get_entered_text(self):
        return self.__entered_text
    
    def get_comparative_alphabet(self):
        return self.__comparative_alphabet
    
    def get_disk_alphabet(self):
        return self.__alphabet_disk
    
    
    
    
    
    
    def __change_letter__(self,txt,n_alphabet:str='',d_alphabet:str=''):
        
        _id = n_alphabet.index(str.upper(txt))
        _t = str.upper(d_alphabet[_id])
        return _t
    
    
    def __unique_path__(self,directory:str, file_name:str):
        counter = 0
        while True:
            counter += 1
            path = Path(f"{directory}\\{file_name}__{counter}.txt")
            if not path.is_file():
                return path
            
    
    
    #### Random AutoConfig ####
    def __random__disk__order(self,disk:Disk):
        
        _keys = disk.get_id()
        _choice = []
        for _k in range(len(_keys)):
            _temp = random.choice(_keys)
            _choice.append(_temp)
            _keys.remove(_temp)
            
        return _choice

    
    def __normalize_text__(self,txt:str='',isUnidecode:bool=False):
        # regresa texto sin espacios
        if isUnidecode:
            return unidecode(txt.upper().replace(" ",""))
        else:
            return txt.upper().replace(" ","")