# db_client.py

import os

import pandas as pd
import psycopg2
import yaml
from pandas import PeriodDtype
from psycopg2 import sql
from psycopg2.extras import execute_values

# import logging
from hmcis_packs.logger.logger_config import setup_logger

# ========== Конфигурация логирования ==========
# Папка для логов — создаём, если нет
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, 'database_client.log')

# # Настраиваем корневой логгер один раз при загрузке модуля
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s: %(message)s',
#     handlers=[
#         logging.StreamHandler(sys.stdout),  # в консоль (stdout)
#         logging.FileHandler(LOG_FILE, encoding='utf-8')  # в файл
#     ]
# )

logger = setup_logger(__name__)


# ===============================================


class DatabaseClient:
    def __init__(self, config_path=None):
        if config_path is None:
            user_home = os.path.expanduser("~")
            config_path = os.path.join(user_home, "db_config.yaml")

        with open(config_path, 'r', encoding='utf-8') as f:
            self.db_config = yaml.safe_load(f)

    def _map_dtype(self, dtype):
        """
        Маппинг pandas dtype → PostgreSQL тип.
        Поддерживает PeriodDtype, float, int, bool, datetime, object и fallback BYTEA.
        """
        # Обработка периодов. Рекомендуем использовать isinstance с PeriodDtype
        if isinstance(dtype, PeriodDtype):
            # Сохраняем период как начало/конец периода в формате TIMESTAMP
            return 'TIMESTAMP'
        if pd.api.types.is_float_dtype(dtype):
            return 'NUMERIC'
        if pd.api.types.is_integer_dtype(dtype):
            return 'INTEGER'
        if pd.api.types.is_bool_dtype(dtype):
            return 'BOOLEAN'
        if pd.api.types.is_datetime64_any_dtype(dtype):
            return 'TIMESTAMP'
        if dtype == 'object':
            return 'VARCHAR'
        return 'BYTEA'

    def save_df_to_db(self,
                      df: pd.DataFrame,
                      table_name: str,
                      schema: str = 'IFRS Reports',
                      binary_columns: list[str] = None):
        """
        Сохраняет DataFrame в PostgreSQL, создаёт схему/таблицу при необходимости,
        и производит пакетную вставку через execute_values.
        Разделено на 2 коммита: сначала схема, потом таблица + данные.
        """
        if binary_columns is None:
            binary_columns = []

        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        try:
            # 1) Создаём схему и коммитим сразу, чтобы не откатился вместе с ошибками ниже
            cursor.execute(
                sql.SQL("CREATE SCHEMA IF NOT EXISTS {}")
                .format(sql.Identifier(schema))
            )
            conn.commit()

            # 2) Готовим DDL для таблицы
            cols_ddl = []
            for col, dtype in zip(df.columns, df.dtypes):
                if col in binary_columns:
                    pg_type = 'BYTEA'
                else:
                    pg_type = self._map_dtype(dtype)
                cols_ddl.append(f"{sql.Identifier(col).as_string(conn)} {pg_type}")

            create_sql = sql.SQL(
                "CREATE TABLE IF NOT EXISTS {schema}.{table} ({fields})"
            ).format(
                schema=sql.Identifier(schema),
                table=sql.Identifier(table_name),
                fields=sql.SQL(", ").join(sql.SQL(c) for c in cols_ddl),
            )
            cursor.execute(create_sql)

            # 3) Очищаем таблицу перед вставкой
            truncate_sql = sql.SQL("TRUNCATE {schema}.{table}").format(
                schema=sql.Identifier(schema),
                table=sql.Identifier(table_name),
            )
            cursor.execute(truncate_sql)

            # 4) Готовим пакетную вставку
            insert_sql = sql.SQL(
                "INSERT INTO {schema}.{table} ({fields}) VALUES %s"
            ).format(
                schema=sql.Identifier(schema),
                table=sql.Identifier(table_name),
                fields=sql.SQL(', ').join(map(sql.Identifier, df.columns))
            )
            records = []
            for row in df.itertuples(index=False, name=None):
                rec = []
                for val, col in zip(row, df.columns):
                    if col in binary_columns:
                        rec.append(psycopg2.Binary(val))
                    else:
                        rec.append(val)
                records.append(tuple(rec))

            execute_values(cursor, insert_sql.as_string(conn), records, page_size=10000)

            # 5) Фиксируем создание таблицы и вставку данных
            conn.commit()
            logger.info(f"✅ Данные успешно загружены в '{schema}.{table_name}'")

        except Exception as e:
            conn.rollback()
            logger.error("💀 Ошибка при сохранении в БД: %s", e)
            raise
        finally:
            cursor.close()
            conn.close()
