import re
import threading
import time
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

import pandas as pd
import requests
from jinja2 import Template


class SAPXMLAClient:
    """
        A client for querying SAP BW via XMLA (XML for Analysis) to execute MDX queries
        and discover metadata like dimensions and levels.
    """

    DISCOVER_TEMPLATE = Template("""
    {# Template for XMLA Discover requests to SAP BW.
       Parameters:
         - request_type: Type of discovery (e.g., MDSCHEMA_DIMENSIONS, MDSCHEMA_LEVELS).
         - restrictions: Dict of restriction keys and values (e.g., {"CUBE_NAME": "$CUBE"}).
         - catalog: Catalog name.
         - datasource: Data source name.
         - format_type: Response format (e.g., "Tabular").
         - extra_properties: Dict of additional properties (e.g., {"LocaleIdentifier": "1033"}).
    #}
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:xmla="urn:schemas-microsoft-com:xml-analysis">
      <soapenv:Header/>
      <soapenv:Body>
        <xmla:Discover>
          <xmla:RequestType>{{ request_type }}</xmla:RequestType>
          <xmla:Restrictions>
            <xmla:RestrictionList>
              {% for key, value in restrictions.items() %}
              <xmla:{{ key }}>{{ value }}</xmla:{{ key }}>
              {% endfor %}
            </xmla:RestrictionList>
          </xmla:Restrictions>
          <xmla:Properties>
            <xmla:PropertyList>
              <xmla:Catalog>{{ catalog }}</xmla:Catalog>
              <xmla:DataSourceInfo>{{ datasource }}</xmla:DataSourceInfo>
              <xmla:Format>{{ format_type }}</xmla:Format>
              {% for key, value in extra_properties.items() %}
              <xmla:{{ key }}>{{ value }}</xmla:{{ key }}>
              {% endfor %}
            </xmla:PropertyList>
          </xmla:Properties>
        </xmla:Discover>
      </soapenv:Body>
    </soapenv:Envelope>
    """)

    def __init__(self, url, username, password, catalog="$INFOCUBE", datasource="SAP_BW"):
        self.url = url
        self.auth = (username, password)
        self.catalog = catalog
        self.datasource = datasource
        self.ns = {'x': 'urn:schemas-microsoft-com:xml-analysis:rowset'}

    def _send(self, soap_body: str, soap_action: str) -> str:
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": f"urn:schemas-microsoft-com:xml-analysis:{soap_action}"
        }
        response = requests.post(
            self.url, headers=headers, data=soap_body.encode("utf-8"), auth=self.auth
        )
        response.raise_for_status()
        return response.text

    def discover_dimensions(self, cube_name: str, format_type: str = "Tabular",
                            extra_properties: dict = None) -> pd.DataFrame:
        """
        Retrieves dimensions for the specified cube.

        Args:
            cube_name (str): Technical name of the cube (e.g., "$HA01M0004").
            format_type (str, optional): Response format. Defaults to "Tabular".
            extra_properties (dict, optional): Additional XMLA properties.

        Returns:
            pd.DataFrame: DataFrame containing dimension metadata.
        """
        body = self.DISCOVER_TEMPLATE.render(
            request_type=escape("MDSCHEMA_DIMENSIONS"),
            restrictions={"CUBE_NAME": escape(cube_name)},
            catalog=escape(self.catalog),
            datasource=escape(self.datasource),
            format_type=escape(format_type),
            extra_properties=extra_properties or {}
        )
        xml = self._send(body, "Discover")
        return self._parse_rows(xml)

    def discover_dimension_members(self,
                                   cube_name: str,
                                   dimension: str,
                                   hierarchy: str = None,
                                   level: str = "LEVEL01",
                                   format_type: str = "Tabular",
                                   extra_properties: dict = None) -> pd.DataFrame:
        """
        Retrieve members of a specific dimension & level via MDSCHEMA_MEMBERS.
        """
        # Determine hierarchy and unique naming
        hierarchy = hierarchy or dimension
        # Wrap names in brackets if missing
        dim_unique = dimension if dimension.startswith('[') else f"[{dimension}]"
        hier_unique = hierarchy if hierarchy.startswith('[') else f"[{hierarchy}]"
        lvl_unique = f"{hier_unique}.[{level}]"

        restrictions = {
            "CATALOG_NAME": escape(self.catalog),
            "CUBE_NAME": escape(cube_name),
            "DIMENSION_UNIQUE_NAME": escape(dim_unique),
            "HIERARCHY_UNIQUE_NAME": escape(hier_unique),
            "LEVEL_UNIQUE_NAME": escape(lvl_unique)
        }
        body = self.DISCOVER_TEMPLATE.render(
            request_type=escape("MDSCHEMA_MEMBERS"),
            restrictions=restrictions,
            format_type=escape(format_type),
            datasource=escape(self.datasource),
            extra_properties=extra_properties or {}
        )
        xml = self._send(body, "Discover")
        return self._parse_rows(xml)

    def discover_member_properties(
            self,
            cube_name: str,
            dimension: str,
            hierarchy: str = None,
            level: str = "LEVEL01",
            member: str = None,
            format_type: str = "Tabular",
            extra_properties: dict = None
    ) -> pd.DataFrame:
        """
        Получить свойства (название/значение) для данного измерения/уровня/
        (опционально) конкретного члена.
        Возвращает DataFrame со столбцами PROPNAME, PROPVAL и т.д.
        """
        hierarchy = hierarchy or dimension
        # оборачиваем в скобки
        dim_unique = f"[{dimension}]" if not dimension.startswith('[') else dimension
        hier_unique = f"[{hierarchy}]" if not hierarchy.startswith('[') else hierarchy
        lvl_unique = f"{hier_unique}.[{level}]"

        # добавляем MEMBER_UNIQUE_NAME только если нужно отфильтровать по конкретному члену
        restrictions = {
            "CATALOG_NAME": escape(self.catalog),
            "CUBE_NAME": escape(cube_name),
            "DIMENSION_UNIQUE_NAME": escape(dim_unique),
            "HIERARCHY_UNIQUE_NAME": escape(hier_unique),
            "LEVEL_UNIQUE_NAME": escape(lvl_unique),
        }
        if member:
            m = member if member.startswith('[') else f"[{member}]"
            restrictions["MEMBER_UNIQUE_NAME"] = escape(m)

        body = self.DISCOVER_TEMPLATE.render(
            request_type=escape("MDSCHEMA_PROPERTIES"),
            restrictions=restrictions,
            catalog=escape(self.catalog),  # вот куда раньше забывали передать
            datasource=escape(self.datasource),
            format_type=escape(format_type),
            extra_properties=extra_properties or {}
        )
        xml = self._send(body, "Discover")
        return self._parse_rows(xml)

    def execute_mdx(self, mdx: str) -> pd.DataFrame:
        # Флаг для остановки счетчика
        stop_counter = threading.Event()

        def display_timer():
            """Функция для отображения интерактивного счетчика времени."""
            print("DEBUG: Счетчик запущен")  # Диагностика
            start_time = time.time()
            while not stop_counter.is_set():
                elapsed_time = time.time() - start_time
                print(f"\rВремя выполнения: {elapsed_time:.2f} секунд", end='', flush=True)
                time.sleep(0.1)  # Обновление каждые 0.1 секунды
            print("\rDEBUG: Счетчик остановлен")  # Диагностика

        # Запускаем счетчик в отдельном потоке
        print("DEBUG: Запуск потока счетчика")
        timer_thread = threading.Thread(target=display_timer)
        timer_thread.daemon = True  # Поток завершится, когда основной завершится
        timer_thread.start()

        # Выполняем запрос
        print("DEBUG: Начало выполнения запроса")
        start_query_time = time.time()  # Время начала выполнения запроса
        body = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                              xmlns:x="urn:schemas-microsoft-com:xml-analysis">
              <soapenv:Header/>
              <soapenv:Body>
                <x:Execute>
                  <x:Command>
                    <x:Statement>{mdx}</x:Statement>
                  </x:Command>
                  <x:Properties>
                    <x:PropertyList>
                      <x:Catalog>{self.catalog}</x:Catalog>
                      <x:DataSourceInfo>{self.datasource}</x:DataSourceInfo>
                      <x:Format>Tabular</x:Format>
                      <x:AxisFormat>TupleFormat</x:AxisFormat>
                    </x:PropertyList>
                  </x:Properties>
                </x:Execute>
              </soapenv:Body>
            </soapenv:Envelope>
            """
        xml = self._send(body, "Execute")
        print("DEBUG: Запрос завершен")

        # Останавливаем счетчик
        stop_counter.set()

        # Ждем завершения потока счетчика
        timer_thread.join()

        # Выводим финальное время
        final_time = time.time() - start_query_time
        print(f"\r{' ' * 50}", end='', flush=True)  # Очищаем строку
        print(f"\rЗапрос завершен за {final_time:.2f} секунд")

        return self._parse_rows(xml)

    def _parse_rows(self, xml_text: str) -> pd.DataFrame:
        try:
            root = ET.fromstring(xml_text)
            rows = root.findall('.//x:row', self.ns)
            data = [{cell.tag.split('}')[-1]: cell.text for cell in row} for row in rows]
            return pd.DataFrame(data) if data else pd.DataFrame()
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse XML response: {str(e)}")

    def validate_mdx_dimensions(self, mdx_query: str, cube_name: str) -> dict:
        """
        Сравнивает измерения из MDX с измерениями из указанного куба.

        :param mdx_query: строка MDX-запроса
        :param cube_name: имя куба (например, "$HA01M0004")
        :return: dict с ключами 'used', 'available', 'matched', 'missing'
        """

        def extract_dimensions_from_mdx(mdx: str) -> set:
            matches = re.findall(r'\[([^\[\]]+?)\]', mdx)
            ignore = {'Measures'}
            dims = set()
            for m in matches:
                dim = m.split('.')[0]
                if dim not in ignore:
                    dims.add(dim)
            return dims

        used_dims = extract_dimensions_from_mdx(mdx_query)
        df = self.discover_dimensions(cube_name)
        available_dims = set(df["DIMENSION_NAME"])

        matched = used_dims & available_dims
        missing = used_dims - available_dims

        return {
            "used": used_dims,
            "available": available_dims,
            "matched": matched,
            "missing": missing
        }

    def discover_levels(self, cube_name: str, format_type: str = "Tabular",
                        extra_properties: dict = None) -> pd.DataFrame:
        """
        Retrieves a list of all hierarchy levels for the specified cube.

        Args:
            cube_name (str): Technical name of the cube (e.g., "$HA01M0004").
            format_type (str, optional): Response format. Defaults to "Tabular".
            extra_properties (dict, optional): Additional XMLA properties (e.g., {"LocaleIdentifier": "1033"}).

        Returns:
            pd.DataFrame: DataFrame with columns like LEVEL_NAME, HIERARCHY_NAME, etc.
        """
        body = self.DISCOVER_TEMPLATE.render(
            request_type=escape("MDSCHEMA_LEVELS"),
            restrictions={"CUBE_NAME": escape(cube_name)},
            catalog=escape(self.catalog),
            datasource=escape(self.datasource),
            format_type=escape(format_type),
            extra_properties=extra_properties or {}
        )
        xml = self._send(body, "Discover")
        return self._parse_rows(xml)

    def discover_all_dimension_unique_names(self, cube_name: str, format_type: str = "Tabular",
                                            extra_properties: dict = None) -> list:
        """
        Retrieves all DIMENSION_UNIQUE_NAME values by discovering hierarchies and deduplicating.

        Returns:
            List of unique dimension unique names (e.g., ['[0ACCT_TYPE]', '[0COMP_CODE]', ...]).
        """
        # Use MDSCHEMA_HIERARCHIES to get every hierarchy row
        body = self.DISCOVER_TEMPLATE.render(
            request_type=escape("MDSCHEMA_HIERARCHIES"),
            restrictions={"CATALOG_NAME": escape(self.catalog), "CUBE_NAME": escape(cube_name)},
            catalog=escape(self.catalog),
            datasource=escape(self.datasource),
            format_type=escape(format_type),
            extra_properties=extra_properties or {}
        )
        xml = self._send(body, "Discover")
        df = self._parse_rows(xml)
        # Extract and dedupe DIMENSION_UNIQUE_NAME
        if 'DIMENSION_UNIQUE_NAME' in df.columns:
            return sorted(df['DIMENSION_UNIQUE_NAME'].dropna().unique().tolist())
        return []


    def discover_member_properties(self, cube_name: str, dimension: str, hierarchy: str = None,
                                   extra_properties: dict = None) -> pd.DataFrame:
        """
        Discover через MDSCHEMA_PROPERTIES список PROPERTY_NAME для данного измерения/иерархии.
        Если провайдер BW не поддерживает, вернёт пустой DataFrame или бросит ошибку.
        """
        hierarchy = hierarchy or dimension
        dim_unique = dimension if dimension.startswith('[') else f"[{dimension}]"
        hier_unique = hierarchy if hierarchy.startswith('[') else f"[{hierarchy}]"
        restrictions = {
            "CATALOG_NAME": escape(self.catalog),
            "CUBE_NAME": escape(cube_name),
            "DIMENSION_UNIQUE_NAME": escape(dim_unique),
            "HIERARCHY_UNIQUE_NAME": escape(hier_unique)
        }
        body = self.DISCOVER_TEMPLATE.render(
            request_type=escape("MDSCHEMA_PROPERTIES"),
            restrictions=restrictions,
            catalog=escape(self.catalog),
            datasource=escape(self.datasource),
            format_type=escape("Tabular"),
            extra_properties=extra_properties or {}
        )
        xml = self._send(body, "Discover")
        df = self._parse_rows(xml)
        return df

    def get_members_with_attributes(self, cube_name: str, dimension: str, hierarchy: str = None,
                                    attributes: list = None, extra_properties: dict = None) -> pd.DataFrame:
        """
        Получает членов указанного измерения вместе с их атрибутами через MDX.
        В MDX ставим NON EMPTY и по строкам, и по столбцам.
        Если attributes не указан, пытаемся discover_member_properties и взять PROPERTY_NAME.
        """
        hierarchy = hierarchy or dimension
        dim_unique = dimension if dimension.startswith('[') else f"[{dimension}]"
        hier_unique = hierarchy if hierarchy.startswith('[') else f"[{hierarchy}]"

        # Если не заданы атрибуты, пытаемся Discover MDSCHEMA_PROPERTIES
        if not attributes:
            try:
                df_props = self.discover_member_properties(cube_name, dimension, hierarchy,
                                                           extra_properties=extra_properties)
                if df_props.empty or "PROPERTY_NAME" not in df_props.columns:
                    raise ValueError("Discover MDSCHEMA_PROPERTIES пустой или нет колонки PROPERTY_NAME")
                props = df_props["PROPERTY_NAME"].dropna().unique().tolist()
                attributes = props
            except Exception as e:
                raise ValueError(f"Не удалось получить свойства автоматически: {e}. Укажите attributes вручную.")

        # Формируем DIMENSION PROPERTIES: базовые + пользовательские
        mdx_props = ["MEMBER_UNIQUE_NAME", "MEMBER_CAPTION"]
        for attr in attributes:
            mdx_props.append(f'{dim_unique}.{attr}')
            # if "." in attr or attr.startswith("["):
            #     mdx_props.append(attr)
            # else:
            #     mdx_props.append(f"{dim_unique}.[{attr}]")
        props_clause = ", ".join(mdx_props)

        # MDX с NON EMPTY
        mdx = f"""
            SELECT
              NON EMPTY {{}} ON COLUMNS,
              NON EMPTY {dim_unique}.{'LEVEL01'}.Members
                DIMENSION PROPERTIES {props_clause}
              ON ROWS
            FROM [{cube_name}]
            """
        df = self.execute_mdx(mdx)
        return df
