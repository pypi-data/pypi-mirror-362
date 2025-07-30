from abs_nosql_integration_core.service.provider_services import SharepointIntegrationService, GoogleIntegrationService, DocusignIntegrationService

providers_mapping = {
    "sharepoint": SharepointIntegrationService,
    "google": GoogleIntegrationService,
    "docusign": DocusignIntegrationService,
}


def create_provider_service(provider_name: str, **kwargs):
    return providers_mapping[provider_name](provider_name=provider_name,**kwargs)
