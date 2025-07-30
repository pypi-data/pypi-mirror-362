REPORT_DEFINITION = """{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/1.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byConnection": {
      "connectionString": "Data Source=powerbi://api.powerbi.com/v1.0/myorg/#{workspace_name}#;initial catalog=#{semantic_model_name}#;integrated security=ClaimsToken",
      "pbiServiceModelId": null,
      "pbiModelVirtualServerName": "sobe_wowvirtualserver",
      "pbiModelDatabaseName": "#{semantic_model_id}#",
      "name": "EntityDataSource",
      "connectionType": "pbiServiceXmlaStyleLive"
    }
  }
}"""
