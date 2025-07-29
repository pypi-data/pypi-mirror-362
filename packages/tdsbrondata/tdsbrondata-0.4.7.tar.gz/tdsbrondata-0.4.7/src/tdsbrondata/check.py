import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tdsbrondata
from pyspark.sql import functions as F
from pyspark.sql.types import *

def afasDebtor(dataToCheck, lakehouseName, schemaName, tableName, afasDebtors, idColumn, debtorIdColumn):
    afasTrimmed = afasDebtors.select(
        F.col("Verkooprelatie_id").alias("afas_id"),
        "Geblokkeerd_voor_levering",
        "Volledig_blokkeren"
    )

    result = dataToCheck.join(
        afasTrimmed,
        dataToCheck[debtorIdColumn] == F.col("afas_id"),
        how="left"
    ).withColumn(
        "remarks",
        F.when(F.col(debtorIdColumn).isNull(), "Debtor is empty")
         .when(F.col("afas_id").isNull(), "Debtor not found in AFAS")
         .when(
             (F.col("Geblokkeerd_voor_levering") == True) |
             (F.col("Volledig_blokkeren") == True),
             "Debtor is blocked in AFAS"
         )
    ).filter(
        F.col("remarks").isNotNull()
    ).withColumn("lakehouseName", F.lit(lakehouseName)) \
     .withColumn("schemaName", F.lit(schemaName)) \
     .withColumn("tableName", F.lit(tableName)) \
     .withColumn("idColumn", F.lit(idColumn)) \
     .withColumn("id", F.col(idColumn)) \
     .withColumn("Verkooprelatie_id", F.col(debtorIdColumn)) \
     .select("lakehouseName", "schemaName", "tableName", "idColumn", "id", "SurrogateKey", "Verkooprelatie_id", "remarks")

    return result