import requests
import pandas as pd
import ast

class PowerBIClient():
    # Power BI Client Class
   
    # Init and get token
    def __init__(self, tenant_id, client_id, client_secret):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_token()
 
    def get_token(self):
        # Grab token
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'login.microsoftonline.com:443'
        }
 
        data = {
            'grant_type': 'client_credentials',
            'scope': 'https://analysis.windows.net/powerbi/api/.default',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
 
        result = requests.post(f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token', headers=header, data=data)
        self.access_token = result.json()['access_token']
        return self.access_token
 
    def get_header(self):
        # Define header
        header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        return header
    # Other functions
    def extract_connection_details(self, x):
        try:
            if isinstance(x, str):
                details = ast.literal_eval(x)
            elif isinstance(x, dict):
                details = x
            else:
                return pd.Series([None]*5, index=['server', 'database', 'connectionString', 'url', 'path'])
 
            return pd.Series({
                'server': details.get('server'),
                'database': details.get('database'),
                'connectionString': details.get('connectionString'),
                'url': details.get('url'),
                'path': details.get('path')
            })
        except Exception as e:
            print(f"Error parsing connectionDetails: {e}")
            return pd.Series([None]*5, index=['server', 'database', 'connectionString', 'url', 'path'])
 
    # Trigger actions
    def refresh_dataflow(self, workspace_id, dataflow_id):
        # Define URL
        url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/dataflows/{dataflow_id}/refreshes'
        # Send POST request
        result = requests.post(url, headers=self.get_header())
        # Print message
        print(f'Start refreshing dataflow {dataflow_id}')
 
    def refresh_dataset(self, workspace_id, dataset_id):
        # Define URL
        url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes'
        # Send POST request
        result = requests.post(url, headers=self.get_header())
        # Print message
        print(f'Start refreshing dataset {dataset_id}')
 
    # Get data functions
    def get_report_by_workspace(self, workspace_id):
        # Define URL endpoint
        get_report_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports'
        # Send API call to get data
        result = requests.get(url=get_report_url, headers=self.get_header())
        return result
 
    def get_dataset_by_workspace(self, workspace_id):
        # Define URL endpoint
        get_dataset_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets'
        # Send API call to get data
        result = requests.get(url=get_dataset_url, headers=self.get_header())
        return result
 
    def get_dataflow_by_workspace(self, workspace_id):
        # Define URL endpoint
        get_dataflow_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/dataflows'
        # Send API call to get data
        result = requests.get(url=get_dataflow_url, headers=self.get_header())
        return result
 
    def get_dataset_refresh_history_by_id(self, workspace_id, dataset_id, top_n = 10):
        """
        Get dataset refresh history by dataset id.
        Args:
            workspace_id (str): The ID of the Power BI workspace.
            dataset_id (str): The ID of the Power BI dataset.
            top_n (int): The number of most recent refreshes to retrieve. Default is 10.
        Returns:
            result (requests.Response): The response object containing the dataset refresh history.
        """
        # Define URL endpoint
        get_dataset_refresh_history_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes?$top={top_n}'
        # Send API to get data
        result = requests.get(url=get_dataset_refresh_history_url, headers=self.get_header())
        return result
 
    def get_dataflow_refresh_history_by_id(self, workspace_id, dataflow_id):
        """
        Get dataflow refresh history by dataflow id.
        Args:
            workspace_id (str): The ID of the Power BI workspace.
            dataflow_id (str): The ID of the Power BI dataflow.
        Returns:
            result (requests.Response): The response object containing the dataflow refresh history.
        """
        get_dataflow_refresh_history_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/dataflows/{dataflow_id}/transactions'
        # Send API to get data
        result = requests.get(url=get_dataflow_refresh_history_url, headers=self.get_header())
   
        return result
   
    def get_dataset_sources_by_id(self, workspace_id, dataset_id):
 
        """
        Get dataset sources by dataset id.
       
        Args:
            workspace_id (str): The ID of the Power BI workspace.
            dataset_id (str): The ID of the Power BI dataset.
        Returns:
            result (requests.Response): The response object containing the dataset sources.
        """
        # Define URL endpoint
        get_dataset_source_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/datasources'
        # Send API to get data
        result = requests.get(url=get_dataset_source_url, headers=self.get_header())
        return result
   
    def get_dataflow_sources_by_id(self, workspace_id, dataflow_id):
        """
        Get dataflow sources by dataflow id.
       
        Args:
            workspace_id (str): The ID of the Power BI workspace.
            dataflow_id (str): The ID of the Power BI dataflow.
        Returns:
            result (requests.Response): The response object containing the dataflow sources.
        """
        # Define URL endpoint
        get_dataflow_source_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/dataflows/{dataflow_id}/datasources'
        # Send API to get data
        result = requests.get(url=get_dataflow_source_url, headers=self.get_header())
        return result
 
    def get_dataset_users_by_id(self,workspace_id, dataset_id):
        """
        Get dataset users by dataset id.
       
        Args:
            workspace_id (str): The ID of the Power BI workspace.
            dataset_id (str): The ID of the Power BI dataset.
        Returns:
            result (requests.Response): The response object containing the dataset users.
        """
        # Define URL endpoint
        get_dataset_users_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/users'
        # Send API to get data
        result = requests.get(url=get_dataset_users_url, headers=self.get_header())
        return result
 
    # Get data in bulk
    def get_all_workspaces(self):
        """
        Get all workspaces from Power BI.
        """
        # Send API Request
        result = requests.get(url='https://api.powerbi.com/v1.0/myorg/groups', headers=self.get_header())
        # Convert to dataframe
        df_get_all_workspaces = pd.DataFrame.from_dict(result.json()['value'], orient='columns')
        return df_get_all_workspaces
 
    def get_all_datasets(self):
        """
        Get all datasets from Power BI.
        """
        # Set workspace list
        df_get_all_workspaces = self.get_all_workspaces()
        workspace_id_list = df_get_all_workspaces['id']
        # Define an empty dataframe
        df_get_all_datasets = pd.DataFrame()
        # Loop through workspace
        for workspace_id in workspace_id_list:
            try:
                workspace_name = df_get_all_workspaces.query('id == "{0}"'.format(workspace_id))["name"].iloc[0]
                # Send API call to get data
                result = self.get_dataset_by_workspace(workspace_id)
                # If result success then proceed:
                if result.status_code == 200:
                    # Create dataframe to store data
                    df = pd.DataFrame.from_dict(result.json()['value'], orient='columns')
                    # Convert all columns to string type (optional)
                    df = df.astype('str')
                    # Add workspace id column
                    df['workspaceId'] = workspace_id
                    # Add workspace name column
                    df['workspaceName'] = workspace_name
                    # Convert all columns to string type (optional)
                    df = df.astype('str')
                    # Append data
                    df_get_all_datasets = pd.concat([df_get_all_datasets, df])
            except Exception as e:
                continue
        return df_get_all_datasets
 
    def get_all_dataflows(self):
        """
        Get all dataflows from Power BI.
        """
        # Set workspace list
        df_get_all_workspaces = self.get_all_workspaces()
        workspace_id_list = df_get_all_workspaces['id']
        # Define an empty dataframe
        df_get_all_dataflows = pd.DataFrame()
        # Loop through workspace
        for workspace_id in workspace_id_list:
            try:
                workspace_name = df_get_all_workspaces.query('id == "{0}"'.format(workspace_id))["name"].iloc[0]
                # Send API call to get data
                result = self.get_dataflow_by_workspace(workspace_id)
                # If result success then proceed:
                if result.status_code == 200:
                    # Create dataframe to store data
                    df = pd.DataFrame.from_dict(result.json()['value'], orient='columns')
                    # Add column
                    df['workspaceId'] = workspace_id
                    # Add workspace name column
                    df['workspaceName'] = workspace_name
                    # Convert all columns to string type (optional)
                    df = df.astype('str')
                    # Append data
                    df_get_all_dataflows = pd.concat([df_get_all_dataflows, df])
            except Exception as e:
                continue
        return df_get_all_dataflows
 
    def get_all_reports(self):
        """
        Get all reports from Power BI.
        """
        # Set workspace list
        df_get_all_workspaces = self.get_all_workspaces()
        workspace_id_list = df_get_all_workspaces['id']
        # Define an empty dataframe
        df_get_all_reports = pd.DataFrame()
        # Loop through workspace
        for workspace_id in workspace_id_list:
            try:
                workspace_name = df_get_all_workspaces.query('id == "{0}"'.format(workspace_id))["name"].iloc[0]
                # Send API call to get data
                result = self.get_report_by_workspace(workspace_id)
                # If result success then proceed:
                if result.status_code == 200:
                    # Create dataframe to store data
                    df = pd.DataFrame.from_dict(result.json()['value'], orient='columns')
                    # Add workspace name column
                    df['workspaceName'] = workspace_name
                    # Convert all columns to string type (optional)
                    df = df.astype('str')
                    # Append data
                    df_get_all_reports = pd.concat([df_get_all_reports, df])
            except Exception as e:
                continue
        return df_get_all_reports
 
    def get_all_dataset_refresh_history(self):
        """
        Get all dataset refresh history from Power BI.
        """
        # Get all datasets
        df_get_all_datasets = self.get_all_datasets()
        # Get dataset refresh history
        df_get_all_datasets_refresh_history = pd.DataFrame()
        list_of_ds = df_get_all_datasets.query('isRefreshable == "True"')['id']
        # Loop through dataset
        for dataset_id in list_of_ds:
            try:
                # Get workspace id
                workspace_id = df_get_all_datasets.query('id == "{0}"'.format(dataset_id))["workspaceId"].iloc[0]
                # Get workspace name
                workspace_name = df_get_all_datasets.query('id == "{0}"'.format(dataset_id))["workspaceName"].iloc[0]
                # Get dataset name
                dataset_name = df_get_all_datasets.query('id == "{0}"'.format(dataset_id))["name"].iloc[0]
                # Send API to get data
                result = self.get_dataset_refresh_history_by_id(workspace_id, dataset_id)
                # If result success then proceed:
                if result.status_code == 200:
                    # Parse data from json output
                    df = pd.DataFrame.from_dict(result.json()['value'], orient='columns')
                    # Add column
                    df['datasetId'] = dataset_id
                    # Add column
                    df['datasetName'] = dataset_name
                    # Add column
                    df['workspaceId'] = workspace_id
                    # Add column
                    df['workspaceName'] = workspace_name
                    # Convert all columns to string type (optional)
                    df = df.astype('str')
                    # Append data
                    df_get_all_datasets_refresh_history = pd.concat([df_get_all_datasets_refresh_history, df])
            except Exception as e:
                continue
 
        return df_get_all_datasets_refresh_history
 
    def get_all_dataflow_refresh_history(self):
        """
        Get all dataflow refresh history from Power BI.
        """
        # Get all dataflows
        df_get_all_dataflows = self.get_all_dataflows()
        # Get dataflow refresh history
        df_get_all_dataflows_refresh_history = pd.DataFrame()
        list_of_dataflows = df_get_all_dataflows['objectId']
 
        # Loop through dataflow
        for dataflow_id in list_of_dataflows:
            try:
                # Get workspace id
                workspace_id = df_get_all_dataflows.query('objectId == "{0}"'.format(dataflow_id))["workspaceId"].iloc[0]
                # Get workspace name
                workspace_name = df_get_all_dataflows.query('objectId == "{0}"'.format(dataflow_id))["workspaceName"].iloc[0]
                # Get dataflow name
                dataflow_name = df_get_all_dataflows.query('objectId == "{0}"'.format(dataflow_id))["name"].iloc[0]
                # Send API to get data
                result = self.get_dataflow_refresh_history_by_id(workspace_id, dataflow_id)
                # If api_call success then proceed:
                if result.status_code == 200:
                    # Parse data from json output
                    df = pd.DataFrame.from_dict(result.json()['value'], orient='columns')
                    # Add column
                    df['dataflowId'] = dataflow_id
                    # Add column
                    df['dataflowName'] = dataflow_name
                    # Add column
                    df['workspaceId'] = workspace_id
                    # Add column
                    df['workspaceName'] = workspace_name
                    # Convert all columns to string type (optional)
                    df = df.astype('str')
                    # Append data
                    df_get_all_dataflows_refresh_history = pd.concat([df_get_all_dataflows_refresh_history, df])
            except Exception as e:
                continue
               
        return df_get_all_dataflows_refresh_history
 
    def get_all_dataset_users(self):
        """
        Get all dataset users from Power BI.
        """
        # Get all datasets
        df_get_all_datasets = self.get_all_datasets()
        # Filter Usage Report dataset
        df_get_all_datasets = df_get_all_datasets[~df_get_all_datasets['name'].str.contains('Usage Metrics')]
        # Get report list
        dataset_id_list = df_get_all_datasets['id']
        # Define an empty dataframe
        df_get_all_dataset_users = pd.DataFrame()
        # Loop through dataset
        for dataset_id in dataset_id_list:
            try:
                workspace_id = df_get_all_datasets.query(f'id == "{dataset_id}"')["workspaceId"].iloc[0]
                workspace_name = df_get_all_datasets.query(f'id == "{dataset_id}"')["workspaceName"].iloc[0]
                dataset_name = df_get_all_datasets.query(f'id == "{dataset_id}"')["name"].iloc[0]
                # Send API call to get data
                result = self.get_dataset_users_by_id(workspace_id, dataset_id)
                # If result success then proceed:
                if result.status_code == 200:
                    # Create dataframe to store data
                    df = pd.DataFrame.from_dict(result.json()['value'], orient='columns')
                    # Add workspace name column
                    df['workspaceId'] = workspace_id
                    df['workspaceName'] = workspace_name
                    df['datasetId'] = dataset_id
                    df['datasetName'] = dataset_name
                    # Convert all columns to string type (optional)
                    df = df.astype('str')
                    # Append data
                    df_get_all_dataset_users = pd.concat([df_get_all_dataset_users, df])
            except Exception as e:
                continue
 
        return df_get_all_dataset_users
   
    def get_all_dataset_sources(self):
        """
        Get all dataset data sources from Power BI.
        """
        # Filter Usage Report dataset
        df_get_all_datasets = self.get_all_datasets()
        df_get_all_datasets = df_get_all_datasets[~df_get_all_datasets['name'].str.contains('Usage Metrics')]
        # Get report list
        dataset_id_list = df_get_all_datasets['id']
        # Define an empty dataframe
        df_get_all_dataset_sources = pd.DataFrame()
 
            # Loop through dataset
        for dataset_id in dataset_id_list:
            try:
                workspace_id= df_get_all_datasets.query(f'id == "{dataset_id}"')["workspaceId"].iloc[0]
                workspace_name = df_get_all_datasets.query(f'id == "{dataset_id}"')["workspaceName"].iloc[0]
                dataset_name = df_get_all_datasets.query(f'id == "{dataset_id}"')["name"].iloc[0]
                # Send API call to get data
                result = self.get_dataset_sources_by_id(workspace_id, dataset_id)
                # If result success then proceed:
                if result.status_code == 200:
                    # Create dataframe to store data
                    df = pd.DataFrame(result.json()['value'])
                    # Add workspace name column
                    df['workspaceId'] = workspace_id
                    df['workspaceName'] = workspace_name
                    df['datasetId'] = dataset_id
                    df['datasetName'] = dataset_name
                    # Extract more useful columns
                    df[['server', 'database', 'connectionString', 'url', 'path']] = df['connectionDetails'].apply(extract_connection_details)
                    # Convert all columns to string type (optional)
                    df = df.astype('str')
                    # Append data
                    df_get_all_dataset_sources = pd.concat([df_get_all_dataset_sources,df])
            except Exception as e:
                continue
 
        return df_get_all_dataset_sources
 
    def get_all_dataflow_sources(self):
        """
        Get all dataflow data sources from Power BI.
        """
        # Get all dataflows
        df_get_all_dataflows = self.get_all_dataflows()
        # Get report list
        dataflow_id_list = df_get_all_dataflows['objectId']
        # Define an empty dataframe
        df_get_all_dataflow_sources = pd.DataFrame()
        # Loop through dataset
        for dataflow_id in dataflow_id_list:
            workspace_id= df_get_all_dataflows.query(f'objectId == "{dataflow_id}"')["workspaceId"].iloc[0]
            workspace_name = df_get_all_dataflows.query(f'objectId == "{dataflow_id}"')["workspaceName"].iloc[0]
            dataflow_name = df_get_all_dataflows.query(f'objectId == "{dataflow_id}"')["name"].iloc[0]
 
            result = self.get_dataflow_sources_by_id(workspace_id, dataflow_id)
            # If result success then proceed:
            if result.status_code == 200:
                try:
                    # Create dataframe to store data
                    df = pd.DataFrame(result.json()['value'])
                    # Add workspace name column
                    df['workspaceId'] = workspace_id
                    df['workspaceName'] = workspace_name
                    df['dataflowId'] = dataflow_id
                    df['dataflowName'] = dataflow_name
                    # Extract more useful columns
                    df[['server', 'database', 'connectionString', 'url', 'path']] = df['connectionDetails'].apply(self.extract_connection_details)
                    # Convert all columns to string type (optional)
                    df = df.astype('str')
                    # Append data
                    df_get_all_dataflow_sources = pd.concat([df_get_all_dataflow_sources,df])
                except Exception as e:
                    continue
 
        return df_get_all_dataflow_sources