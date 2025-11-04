@description('Name prefix for resources')
param namePrefix string = 'lowlightenhancer'

@description('Location for all resources')
param location string = resourceGroup().location

@description('App Service SKU')
param sku string = 'P0V3'

//
// Generate a globally unique suffix for names
//
var uniqueSuffix    = toLower(uniqueString(resourceGroup().id, location))
var appServiceName  = '${namePrefix}-web-${uniqueSuffix}'
var appServicePlanName = '${namePrefix}-plan'

//
// App Service Plan (Linux)
//
resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  sku: {
    name: sku
    tier: 'PremiumV3'
    capacity: 1
  }
  properties: {
    reserved: true
  }
}


//
// Web App via appservice.bicep module
//
module web './core/host/appservice.bicep' = {
  name: 'web'
  params: {
    name: appServiceName
    location: location
    appServicePlanId: appServicePlan.id
    runtimeName: 'python'
    runtimeVersion: '3.13'
    scmDoBuildDuringDeployment: true
    tags: {
      'azd-service-name': 'web'
    }
  }
}


//
// Configure App Settings
//
resource appSettings 'Microsoft.Web/sites/config@2023-12-01' = {
  name: '${appServiceName}/appsettings'
  properties: {
    SCM_DO_BUILD_DURING_DEPLOYMENT: true
  }
  dependsOn: [
    web
  ]
}


//
// Outputs
//
output appServiceUrl string     = web.outputs.url
