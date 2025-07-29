from supabase import create_client, Client
from supabase.client import ClientOptions


class Connection:

    def __init__(self):
        url: str = "https://tvpehjbqxpiswkqszwwv.supabase.co"
        key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cGVoamJxeHBpc3drcXN6d3d2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTY0NTEzODksImV4cCI6MjAxMjAyNzM4OX0.LZW0i9HU81lCdyjAdqjwwF4hkuSVtsJsSDQh7blzozw"
        self.supabase: Client = create_client(
            url, key,
            options=ClientOptions(
                auto_refresh_token=False,
                postgrest_client_timeout=40,
                storage_client_timeout=40,
                schema="xerenity",
            ))

    def login(self, username, password):
        """

        Inicia sesion con el servidor de xerenity

        :param username: Usuario
        :param password: contrasena
        :return:
        """
        try:
            data = self.supabase.auth.sign_in_with_password(
                {
                    "email": username,
                    "password": password}
            )
            return data

        except Exception as er:
            return str(er)

    def get_all_series(self):
        """

        :return:
        """
        try:
            data = self.supabase.from_('search_mv').select('source_name,grupo,description,display_name,ticker').execute().data
            return data
        except Exception as er:
            return str(er)

    def read_serie(self, ticker: str):
        """

        Funcion que retorna los valores de la serie deseada, si la serie no es encontrada
        se retorna un contenedor vacio

        :param ticker: Identificador unico de la serie a leer
        :return:
        """
        try:
            data = self.supabase.rpc('search', {"ticket": ticker}).execute().data
            if 'data' in data:
                return data['data']
            return data
        except Exception as er:
            return str(er)
