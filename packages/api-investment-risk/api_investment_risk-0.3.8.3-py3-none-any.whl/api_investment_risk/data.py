import os
import json
import requests
import pandas as pd
from dataclasses import dataclass

@dataclass
class API:
    """
    Obtiene el url y token de acceso de la API-INVESTMENT-RISK desde la variables de entorno y defince la función de conexión.
    """

    api_url : str = os.getenv('API_RISK_URL')
    api_token : str = os.getenv('API_RISK_TOKEN')

    def engine(self, url:str=None):
        """
        Función principal para hacer la consulta a la url de la API.

        Args:
            url (str): url de consulta.
        """
        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }

        # Realizar el request GET
        response = requests.get(url, headers=headers, stream=True)

        # Comprobar el estado de la respuesta
        if response.status_code == 200:
            raw = response.raw.read(decode_content=True)
            data = json.loads(raw)  # Si la respuesta es JSON, se puede mostrar así

            return pd.json_normalize(data)

        else:
            print(f"Error de Conexión: {response.status_code}")
            print(response.text)


@dataclass
class Data(API):

    # -- AFP ---
    def get_afp_vc(self, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET AFP_ValoresCuota de la API.
        """
        api_url = f'{self.api_url}/AFP_ValoresCuota/{start}_{end}'
        data = self.engine(url=api_url)
        
        return data
    
    def get_afp_patrimonio(self, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET AFP_Patrimonio de la API.
        """
        api_url = f'{self.api_url}/AFP_Patrimonio/{start}_{end}'
        data = self.engine(url=api_url)
        
        return data
    
    # --- VALORES CUOTA BURTOS & NETOS ---
    def get_lva_update(self, tipo:str) -> pd.DataFrame:
        """
        Retorna el método GET VC_Bruto de la API.
        """
        api_url = f'{self.api_url}/LVA_Update/{tipo}'
        data = self.engine(url=api_url)
        
        return data

    def get_fm_vc(self, tipo:str, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET VC_Bruto de la API.
        """
        api_url = f'{self.api_url}/FondosMutuos_ValoresCuota/{tipo}_{start}_{end}'
        data = self.engine(url=api_url)
        
        return data
    
    def get_fm_vc_categ(self, tipo:str, categoria:str,start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET VC_Bruto de la API.
        """
        api_url = f'{self.api_url}/FondosMutuos_ValoresCuota_Categ/{categoria}_{tipo}_{start}_{end}'
        data = self.engine(url=api_url)
        
        return data

    def get_fm_vc_run(self, tipo:str, run:str ,start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET VC_Bruto de la API.
        """
        api_url = f'{self.api_url}/FondosMutuos_ValoresCuota_Run/{run}_{tipo}_{start}_{end}'
        data = self.engine(url=api_url)
        
        return data

    # --- RIESGO ---
    def get_risk_metrics(self, runsura:str, metrica:str, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET Riesgo de la API.
        """
        api_url = f'{self.api_url}/Risk_Metrics/{runsura}_{metrica}_{start}_{end}'
        data = self.engine(url=api_url)
        
        return data
    
    def get_metricas(self) -> pd.DataFrame:
        """
        Retorna el método GET Metricas de la API.
        """
        api_url = f'{self.api_url}/Metricas'
        data = self.engine(url=api_url)
        
        return data
    
    def get_abs_metrics(self, run:str, id_metrica:int, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET Metricas Absoluta de la API.
        """
        api_url = f'{self.api_url}/Metricas_Absolutas/{run}_{id_metrica}_{start}_{end}'
        data = self.engine(url=api_url)
        
        return data
    
    def get_abs_metrics_categ(self, categ:str, id_metrica:int, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET Metricas Absoluta de la API.
        """
        api_url = f'{self.api_url}/Metricas_Absolutas_Categoria/{categ}_{id_metrica}_{start}_{end}'
        data = self.engine(url=api_url)
        
        return data
    
    
    def competidores(self, definicion:str) -> pd.DataFrame:
        """
        Retorna el método GET Competidores de la API.
        """
        api_url = f'{self.api_url}/Competidores/{definicion}'
        data = self.engine(url=api_url)
        
        return data
    
    def get_alertas_run(self, runsura:str, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET Alertas de la API.
        """
        api_url = f'{self.api_url}/Alertas_Run/{runsura}_{start}_{end}'
        data = self.engine(url=api_url)
        
        return data
    
    def get_alertas(self, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET Alertas de la API.
        """ 
        api_url = f'{self.api_url}/Alertas/{start}_{end}'
        data = self.engine(url=api_url)
        
        return data
    
    def get_nivel_riesgo(self, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET Alertas de la API.
        """ 
        api_url = f'{self.api_url}/Nivel_Riesgo/{start}_{end}'
        data = self.engine(url=api_url)
        
        return data
    
    # --- PERFORMANCE & ALPHA ---
    def get_alpha(self, date:str) -> pd.DataFrame:
        """
        Retorna el método GET Alpha de la API.
        """
        api_url = f'{self.api_url}/Performance_SURA/{date}'
        data = self.engine(url=api_url)
        
        return data
    
    def get_alpha_run(self, runsura:str, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET Alpha de la API.
        """
        api_url = f'{self.api_url}/Performance_SURA_Run/{runsura}_{start}_{end}'
        data = self.engine(url=api_url)
        
        return data

    def get_quartil(self, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET Quartil de la API.
        """
        api_url = f'{self.api_url}/Quartil/{start}_{end}'    
        data = self.engine(url=api_url)
        
        return data
    
    def get_quartil_run(self, runsura:str, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET Quartil de la API.
        """
        api_url = f'{self.api_url}/Quartil/{runsura}_{start}_{end}'    
        data = self.engine(url=api_url)
        
        return data
    
    def get_quartil_categ(self, categoria:str, start:str, end:str) -> pd.DataFrame:
        """
        Retorna el método GET Quartil de la API.
        """
        api_url = f'{self.api_url}/Quartil_Categoria/{categoria}_{start}_{end}'    
        data = self.engine(url=api_url)
        
        return data

