@description('Name of the App Service')
param name string

@description('Location for the App Service')
param location string

@description('App Service Plan ID')
param appServicePlanId string

@description('Runtime name (e.g. python, node, dotnet)')
param runtimeName string = 'python'

@description('Runtime version (e.g. 3.13)')
param runtimeVersion string = '3.13'

@description('Enable Oryx build')
param scmDoBuildDuringDeployment bool = true

@description('Optional startup command')
param startupCommand string = ''

@description('Tags for the App Service')
param tags object = {}

resource appService 'Microsoft.Web/sites@2023-12-01' = {
  name: name
  location: location
  kind: 'app,linux'
  identity: {
    type: 'SystemAssigned'
  }
  tags: tags
  properties: {
    serverFarmId: appServicePlanId
    siteConfig: {
      linuxFxVersion: '${toUpper(runtimeName)}|${runtimeVersion}'
      scmDoBuildDuringDeployment: scmDoBuildDuringDeployment
      appCommandLine: empty(startupCommand) ? '' : startupCommand
    }
  }
}

output url string = 'https://${name}.azurewebsites.net'
output identityPrincipalId string = appService.identity.principalId
