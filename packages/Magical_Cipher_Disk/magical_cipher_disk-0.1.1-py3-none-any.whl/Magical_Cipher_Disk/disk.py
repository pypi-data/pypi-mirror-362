import random

class Disk:
    def __init__(self,alphabet:str=None,split_list:list=None,disk_serie:str=None,random_state:int=None) -> None:
        
        self.__alphabet = alphabet.upper()
        
        self.__disk_serie = disk_serie
        self.__random_state = random_state
        
        if self.__disk_serie != None:
            __disk_serie_split = self.__disk_serie.split("SCDFK")
            
            if self.__random_state != None:
                print("-------------------------------------------------------------------")
                print(f"Se esta usando la serie '{disk_serie}' para la creacion del Disk")
                print(f"Esto sustituira el random state {self.__random_state}")
                print("-------------------------------------------------------------------")
            
            self.__random_state=int(__disk_serie_split[0])
            
        else:
            __disk_serie_split = None
            self.__random_state = random_state
            
            
        self.__created_alphabet = self.__create_alphabet__(self.__alphabet,self.__random_state)
        self.__comp_disk_serie = f"{self.__created_alphabet[0]}{self.__created_alphabet[-1]}{self.__created_alphabet[1]}{self.__created_alphabet[-2]}"
        
        if __disk_serie_split != None:
            if  self.__comp_disk_serie != __disk_serie_split[1]:
               print("La serie de Disk introducida no es valida\nSi aun no ha creado algun disco no introduzca una serie")
               exit(-1)
        
            
        if split_list != None:
            self.__split_list = split_list
        else:
            self.__split_list = [6,7]

        
        self.__disk = {
            "serie":None,
            "splits":self.__split_list,
            "disk":{},
            
        }
        
    
    def Create_Disk(self):
        _cd_split_alphabet=self.__split_alphabet__(self.__created_alphabet,self.__split_list)
        
        for _d in _cd_split_alphabet:
            _cd_len_splits=len(_d)
            _cd_id = str(_d[0]) + str(_d[-1])
            self.__disk["disk"][_cd_id] = {
                "lenght":_cd_len_splits,
                "disk":_d
            }
            
        self.__disk["alphabet"] = self.__created_alphabet
        self.__disk["serie"] = f"{self.__random_state}SCDFK{self.__comp_disk_serie}"
        
        return self
    
    
    def __create_alphabet__(self,alphabet:str=None,random_state:int=None) -> str:
        
        """Crea un alfabeto desordenado, puedes introducir cualquier alfabeto o caracteres que quieras.
        Por ejemplo como una variable tipo str: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 

        Returns:
            str: Alfabeto desordenado
        """
        
        if alphabet != None:
            _ca_alphabet = list(alphabet)
        else:
            _ca_alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')  
                    
        if random_state != None:
            random.seed(random_state)
        else:
            self.__random_state=random.randint(0,9999999)
            random.seed(self.__random_state)
            
        
        #creation of the new alphabet, randomly selected
        _ca_created_alphabet = ''
        
        for i in range(len(_ca_alphabet)):
                
            _l = random.choice(_ca_alphabet)
            _ca_alphabet.remove(_l)
            _ca_created_alphabet += _l
            
        #reset de la seed
        random.seed()
        
        return _ca_created_alphabet
            

    def __split_alphabet__(self,alphabet:str=None,split_list:list=None) -> list:
        
        """ Introduce cualquier alfabeto o caracteres que funcionaran como tu alfabeto, este se dividira en una cantidad
        de veces.
        Por ejemplo como una variable tipo str: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 

        Returns:
            List: regresa una lista de los caracteres dividos y juntos en grupos.
        """
        
        if split_list != None:
            _split_list = split_list
        else:
            #Splits general para un alfabeto regular
            self.__split_list
            _split_list = [6,7]
        
        
        if alphabet != None:
            _sa_alphabet = list(alphabet)
        else:
            _sa_alphabet = list(self.Create_Alphabet())
        
        
        _split_alphabet = []
        _temp_alphabet = _sa_alphabet
        still_more = True
        
        #division de alfabeto, para la creacion de los Disk
        while still_more:
            for _s in _split_list:
                if len(_temp_alphabet) > 0:
                    _split_alphabet.append(_temp_alphabet[:_s])
                    _temp_alphabet=_temp_alphabet[_s:]
                else:
                    still_more = False
            
        return _split_alphabet
    
    ### Get Methods ### 
    
    def get_disk(self):
        return self.__disk
    
    def get_serie(self):
        if self.__disk["serie"] != None:
            return self.__disk["serie"]
        else:
            return self.__disk_serie
        
    def get_id(self):
        return list(self.__disk["disk"].keys())
    
    
    
    ### Special ###
    
    def __str__(self) -> str:
        _d = self.get_disk()

        _temp = '################ Configuración de Disco ################\n'
        _temp += f"Serie de Disco: '{_d["serie"]}'\n"
        _temp += f"Alfabeto usado:  '{self.__alphabet}'\n"
        _temp += f"Alfabeto creado: '{_d["alphabet"]}'\n"
        _temp += f"Splits alfabeto: '{self.__split_list}'\n"
        
        for i in self.get_id():
            
            _temp += f"Parte {i}: {_d["disk"][i]["disk"]}\n"
            
        return _temp
    