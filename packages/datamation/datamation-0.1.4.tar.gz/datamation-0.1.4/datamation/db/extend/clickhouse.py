
from datamation import table_basic

class clickhouse_table(table_basic):
     '''基于 clickhouse_driver驱动 '''
     def general_executemany(self,operation,seq):
        operation = operation.replace(':','')
        super().general_executemany(operation.replace(':',''),seq)
