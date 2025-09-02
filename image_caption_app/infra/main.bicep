@description('Azure Developer environment name (passed from azd). Used for naming and tags.')
param azdEnvName string

@description('Name prefix for resources (optional). Defaults to azdEnvName if not provided')
@allowed([
  ''
])
param namePrefix string = ''

@description('Location for all resources')
param location string = resourceGroup().location

@description('App Service Plan SKU. Use B1/B3 for Linux Basic or P*v3 for PremiumV3.')
@allowed([
  'B1'
  'B3'
  'P0v3'
  'P1v3'
  'P2v3'
])
param planSku string = 'B3'

@description('Azure AI Foundry model deployment name')
param aiFoundryModelName string = 'gpt-4o-mini'

@description('Azure OpenAI API version for SDK calls')
param openaiApiVersion string = '2024-12-01-preview'

@description('Whether to deploy Azure AI Foundry resources. Set to false if your subscription lacks AIServices quota and provide an existing endpoint below.')
param deployFoundry bool = true

@description('Existing Azure AI (Foundry/OpenAI) endpoint to use when deployFoundry = false, e.g., https://<your-ai>.openai.azure.com')
param existingFoundryEndpoint string = ''

//
// Derived naming
//
var prefix        = toLower(empty(namePrefix) ? azdEnvName : namePrefix)
var uniqueSuffix  = toLower(uniqueString(resourceGroup().id, prefix, location))
var appServiceName = '${prefix}-web-${uniqueSuffix}'
var appServicePlanName = '${prefix}-plan'
var aiFoundryName = '${prefix}-aifoundry-${uniqueSuffix}'
var aiFoundryProj = '${prefix}-proj-${uniqueSuffix}'
var visionName    = '${prefix}-cv-${uniqueSuffix}'
var planTier      =  'Basic'

//
// App Service Plan (Linux)
//
resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  sku: {
    name: planSku
  tier: planTier
    capacity: 1
  }
  properties: {
    reserved: true
  }
  tags: {
    'azd-env-name': azdEnvName
  }
}

//
// Azure AI Foundry Account
//
resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = if (deployFoundry) {
  name: aiFoundryName
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    apiProperties: {}
    customSubDomainName: aiFoundryName
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    allowProjectManagement: true
    defaultProject: aiFoundryProj
    associatedProjects: [
      aiFoundryProj
    ]
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
  tags: {
    'azd-env-name': azdEnvName
  }
}

//
// Default Project for AI Foundry
//
resource aiFoundryProject 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = if (deployFoundry) {
  name: aiFoundryProj
  parent: aiFoundry
  location: location
  kind: 'AIServices'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {}
}

//
// GPT-4o-mini Foundry Deployment
//
resource aiFoundryDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = if (deployFoundry) {
  name: aiFoundryModelName
  parent: aiFoundry
  sku: {
    name: 'GlobalStandard'
    capacity: 1
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o-mini'
      version: '2024-07-18'
    }
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
    raiPolicyName: 'Microsoft.DefaultV2'
  }
}

//
// Computer Vision (Cognitive Services)
//
resource vision 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: visionName
  location: location
  sku: {
    name: 'S1'
  }
  kind: 'ComputerVision'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: visionName
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    allowProjectManagement: false
    publicNetworkAccess: 'Enabled'
  }
  tags: {
    'azd-env-name': azdEnvName
  }
}

//
// Web App via local module
//
module web '../core/host/appservice.bicep' = {
  name: 'web'
  params: {
    name: appServiceName
    location: location
    appServicePlanId: appServicePlan.id
    runtimeName: 'python'
    runtimeVersion: '3.13'
    scmDoBuildDuringDeployment: true
  // Run directly from the mounted package without relying on a script file
  startupCommand: 'streamlit run app.py --server.port 8000 --server.address 0.0.0.0'
    tags: {
      'azd-service-name': 'web'
      'azd-env-name': azdEnvName
    }
  }
}

//
// Role assignments: Grant the Web App MI access to Cognitive Services
//
// Cognitive Services User
resource roleCognitiveUserFoundry 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (deployFoundry) {
  name: guid(resourceGroup().id, 'foundry-cog-user', appServiceName)
  scope: aiFoundry
  properties: {
    principalId: web.outputs.identityPrincipalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'a97b65f3-24c7-4388-baec-2e87135dc908') // Cognitive Services User
    principalType: 'ServicePrincipal'
  }
}

// Cognitive Services OpenAI User (for Foundry/OpenAI access)
resource roleOpenAIUserFoundry 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (deployFoundry) {
  name: guid(resourceGroup().id, 'foundry-openai-user', appServiceName)
  scope: aiFoundry
  properties: {
    principalId: web.outputs.identityPrincipalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd') // Cognitive Services OpenAI User
    principalType: 'ServicePrincipal'
  }
}

// Cognitive Services User on the Vision account
resource roleCognitiveUserVision 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, 'vision-cog-user', appServiceName)
  scope: vision
  properties: {
    principalId: web.outputs.identityPrincipalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'a97b65f3-24c7-4388-baec-2e87135dc908') // Cognitive Services User
    principalType: 'ServicePrincipal'
  }
}

//
// Configure App Settings for the Web App
//
resource appSettings 'Microsoft.Web/sites/config@2023-12-01' = {
  name: '${appServiceName}/appsettings'
  properties: {
    ENDPOINT_URL: deployFoundry ? aiFoundry.properties.endpoint : existingFoundryEndpoint
    OPENAI_API_VERSION: openaiApiVersion
    DEPLOYMENT_NAME: aiFoundryModelName
    VISION_ENDPOINT: vision.properties.endpoint
  WEBSITES_PORT: '8000'
    // Optional: expose azd env name for diagnostics
    AZD_ENV_NAME: azdEnvName
  }
  dependsOn: [
    web
    vision
  ]
}

//
// Outputs
//
output appServiceUrl string = web.outputs.url
output aiFoundryEndpoint string = deployFoundry ? aiFoundry.properties.endpoint : existingFoundryEndpoint
output visionEndpoint string = vision.properties.endpoint
