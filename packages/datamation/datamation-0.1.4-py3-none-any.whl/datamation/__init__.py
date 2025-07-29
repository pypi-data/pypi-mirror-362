import sys as sys
import os as _os

__version__ = "0.0.1"

sys.path.append(_os.path.split(_os.path.realpath(__file__))[0])

from datamation.db import (get_sql,
                           get_sqltab_max,
                           get_sqltab_sum,
                           get_sqltab_min,
                           get_sqltab_count,
                           get_sqltabs_count,
                           get_sqltab_cols,
                           get_sqltab_names,
                           get_sqltab_values,
                           get_sqltab_count_diff,
                           get_sqltab_description,
                           sql_execute,
                           sqltab_truncate,
                           compare_db_data1,
                           compare_db_data2,
                           get_sqldata_diff1,
                           get_sqldata_diff2,
                           get_sqldb_diff,
                           get_sqldb_ddl,
                           table_basic,
                           Dimension,
                           FactTable,
                           Change_slowly,
                           Cache_table,
                           elastic_basic,
                           source_sql,
                           source_pandas,
                           source_csv,
                           source_xlsx,
                           sqlsync,
                           dbsync,
                           dbuldr,
                           csvldr,
                           pandasldr,
                           dump_sql,
                           dump_csv,
                           sqluldr2,
                           sqlldr,
                           Cache_database,
                           Tint,
                           Tstr,
                           Tbool,
                           Tfloat,
                           Tupper,
                           Tlower,
                           Filterfalse,
                           Filtertrue,
                           Transform,
                           Tsplitchunk,
                           Tpairwise_seq,
                           Mergejoin,
                           Hashkjoin,
                           inference_dtype,
                           Filter_dict,
                           dbms_hash_mysql,
                           dbms_hash_pgsql,
                           dbms_hash_count,
                           dbcfg,
                           sqldb_structure_sync
                           )

from datamation.email.mail import to_mail,get_mail
from datamation.send import dingtalk,work_wechat
from datamation.log import get_logger,_logs

def __main():
    import logging
    logger= logging.getLogger('datamation')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s【%(levelname)s】-%(message)s',datefmt ='%Y-%m-%d %H:%M:%S ')
    streamhandler  = logging.StreamHandler()
    streamhandler.setLevel(logging.DEBUG)
    streamhandler.setFormatter(formatter)
    logger.addHandler(streamhandler )
    return logger

logger = __main()


