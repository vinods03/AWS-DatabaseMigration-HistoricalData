# AWS-DatabaseMigration-HistoricalData

Here, data is moved from an OLTP system into an OLAP system. Data enrichment is done during the data movement.
Please refer the Architecture Diagram first so as to get an idea of what we are trying to build.
I have included the important notes on each and every service used in the pipeline and also all the code snippets.
The notes are numbered in the order in which the services were built in the pipeline.

Note the usage of batch writing into dynamoDB in the lambda functions. This is an important concept that helps to achive higher throughput and increased parallelism without us having to manage the multiple threads. Another important feature is the usage of pagination when using the s3 list_objects_v2. Without the usage of pagination, only 1000 records were getting processed and it took me some time to figure out this concept of pagination. The usage of State Machines / Step functions and the way in which EMR cluster is provisioned, used and then terminated immediately after the completion of processing is demonstrated here.

This pipeline is built for "historical" data migration. 
Working on a similar pipeline for "ongoing / current" data migration. 
Minor tweaks will be needed in the architecture and also planning to use different AWS services (compared to the historical data pipeline) whereever possible.
One important change i will be doing to replace the Glue job that loads Redshift tables with lambda, because we are not doing any processing in the Glue job other than connecting to Redshift and executing Redshift commands. However, if there is a huge number of files to be processed and we expect the redshift load to take more than 15 minutes, better to stick with the Glue job. Also, i will be replacing the Step function / State Machine using EMR cluster with a Glue job.
