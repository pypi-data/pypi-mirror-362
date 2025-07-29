class Stones:
    def __init__(self,stones:list=None) -> None:
        
        self.__stones = stones
        
        #dar cada valor a una sola variable
        
        self.__yellow_value = sum(_y[1] for _y in self.__stones if str(_y[0]).upper() == "YELLOW")
        
        self.__red_green_value = sum(_rg[1] for _rg in self.__stones if str(_rg[0]).upper() == "RED-GREEN")
        
        self.__blue_value = sum(_b[1] for _b in self.__stones if str(_b[0]).upper() == "BLUE")
        
        self.__purple_value = sum(_p[1] for _p in self.__stones if str(_p[0]).upper() == "PURPLE")
        
        
    def apply_stones(self,txt:str='',normal_alphabet:str='',disk_alphabet:str='',isEncrypted:bool=False,position:int=0):
        _tempo_blue = 0
        
        _t = self.apply_stone_red_green(txt,normal_alphabet,disk_alphabet,isEncrypted)
        
        if self.__blue_value > 0:
            if _tempo_blue % self.__blue_value == 0:
                _t = self.apply_stone_blue(_t,disk_alphabet)
                _tempo_blue += 1
    
        return _t
        
        
    def apply_stone_red_green(self,txt:str='',normal_alphabet:str='',disk_alphabet:str='',isEncrypted:bool=False):
        
        if isEncrypted:
            _orden = -self.__red_green_value
        else:
            _orden = self.__red_green_value
        
        _id = (normal_alphabet.index(str.upper(txt))+_orden)%len(disk_alphabet)
        _t = str.upper(disk_alphabet[_id])
        
        return _t
    

    def apply_stone_blue(self,txt:str='',alphabet:str=''):
        
        _alphabet = alphabet
        _id = (_alphabet.index(str.upper(txt))+13)%len(_alphabet)
        _t = str.upper(_alphabet[_id])
        return _t

    #getters
    
    def get_stone_yellow(self):
        if self.__yellow_value > 0:
            return self.__yellow_value % 4
        else:
            return 0
        
    def get_stone_red_green(self):
        if self.__red_green_value > 0:
            return self.__red_green_value
        else:
            return 0
        
    def get_stone_blue(self):
        if self.__blue_value > 0:
            return self.__blue_value
        else:
            return 0
        
    def get_stone_purple(self):
        if self.__purple_value > 0:
            return self.__purple_value
        else:
            return 0
        
        
        
    #### special ####
    
    def __str__(self) -> str:
        _temp = '################ Configuración de Piedras Mágicas ################\n'
        
        _temp += f'Piedra    |  Valor Total\n'
        _temp += f'YELLOW    |  {self.get_stone_yellow()}\n'
        _temp += f'RED-GREEN |  {self.get_stone_red_green()}\n'
        _temp += f'BLUE      |  {self.get_stone_blue()}\n'
        _temp += f'PURPLE    |  {self.get_stone_purple()}\n'
        
        return _temp
        
        