import os
from util import get_spark_session, read, assign_orders_columns, fltr, transform, write

def core():

    appName = os.environ.get('appName')
    order_purchase_yr = os.environ.get('order_purchase_yr')
    src_file_format = os.environ.get('src_file_format')
    src_file_dir = os.environ.get('src_file_dir')
    tgt_file_format = os.environ.get('tgt_file_format')
    tgt_file_dir = os.environ.get('tgt_file_dir')
        
    spark = get_spark_session(appName)
    spark.sql('select current_date()').show()

    orders_df = read(spark, src_file_format, src_file_dir)
    
    print('*************** Original schema ***************')
    orders_df.printSchema()

    print('*************** Updated Schema ***************')
    updated_orders_df = assign_orders_columns(orders_df)
    updated_orders_df.printSchema()

    print('Number of records to be processed: ', updated_orders_df.count())
    
    print('*************** Sample record after schema update ******************')
    updated_orders_df.show(1, truncate = False)

    print('************** Filter data *****************')
    filtered_df = fltr(updated_orders_df, order_purchase_yr)
    filtered_df.show(1, truncate = False)
    print('Number of records after applying filter: ', filtered_df.count())

    print('************** Filtered and Transformed schema ******************')
    transformed_df = transform(filtered_df)
    transformed_df.printSchema()

    print('************** Sample record after applying filter and transformation ******************')
    transformed_df.show(1, truncate = False)

    try:
        write(transformed_df, tgt_file_format, tgt_file_dir)
        print('Number of records written into the target bucket is: ', transformed_df.count())
    except Exception as e:
        print('Write to target failed with exception ', e)


if __name__ == '__main__':
    core()