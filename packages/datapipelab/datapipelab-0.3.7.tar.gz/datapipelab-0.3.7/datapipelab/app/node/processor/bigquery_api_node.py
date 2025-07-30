from datapipelab.app.node.tnode import TNode
from datapipelab.logger import logger

class BigQueryAPIProcessorNode(TNode):
    def __init__(self, spark, tnode_config):
        super().__init__(spark=spark)
        self.sql_query = tnode_config['options']['query']
        self.node_name = tnode_config['name']
        self.credentials_path = tnode_config['options'].get('credentials_path', None)
        self.credentials_info_env_name = tnode_config['options'].get('credentials_info_env_name', None)
        self.return_as_spark_df = tnode_config['options']['return_as_spark_df']
        self.project_name = tnode_config['options']['project_name']
        self.return_as_python_list = tnode_config['options'].get('return_as_python_list', False)
        self.return_as_is = tnode_config['options'].get('return_as_is', False)

    def __get_gcp_credentials(self):
        from google.oauth2 import service_account
        if self.credentials_path:
            return service_account.Credentials.from_service_account_file(self.credentials_path)
        elif self.credentials_info_env_name:
            import os
            import json
            credentials_info = json.loads(os.environ[self.credentials_info_env_name])
            return service_account.Credentials.from_service_account_info(credentials_info)
        else:
            logger.warning("No credentials provided. Please provide either 'credentials_path' or 'credentials_info'.")
            return None

    def __sql_biqquery(self, sql_query):
        from google.cloud import bigquery
        credentials = self.__get_gcp_credentials()
        client = bigquery.Client(credentials=credentials, project=self.project_name)

        # run the job
        query_job = client.query(sql_query)

        results = query_job.result()
        if self.return_as_spark_df:
            rows = [dict(row) for row in results]
            self.node = self.spark.createDataFrame(rows)
        elif self.return_as_python_list:
            rows = [dict(row) for row in results]
            self.node = rows
        elif self.return_as_is:
            self.node = results
        else:
            self.node = None
        # logger.info([dict(row) for row in results])  # TODO: Remove this

    def _process(self):
        self.__sql_biqquery(self.sql_query)
        if self.return_as_spark_df:
            self._createOrReplaceTempView()
        return self.node
