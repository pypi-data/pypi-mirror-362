import asyncio

import boto3
from utils.constants import Q_BUSINESS_APP_NAME


class AsyncBedrockClient:
    """Async wrapper for Bedrock client operations"""
    
    def __init__(self, region='us-east-1'):
        self.region = region
        self.client = boto3.client('bedrock', region_name=region)
        self.runtime_client = boto3.client('bedrock-runtime', region_name=region)
    
    async def setup_inference_profile(self, profile_name, base_model_arn, tags=None):
        """Async wrapper for setting up an inference profile"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._setup_inference_profile,
            profile_name,
            base_model_arn,
            tags
        )
    
    def _setup_inference_profile(self, profile_name, base_model_arn, tags=None):
        """Synchronous implementation for setup_inference_profile"""
        try:
            existing_profiles = self.client.list_inference_profiles(
                typeEquals="APPLICATION"
            )
            profile_exists = any(p['inferenceProfileName'] == profile_name 
                              for p in existing_profiles.get('inferenceProfileSummaries', []))
            
            if not profile_exists:
                profile = self.client.create_inference_profile(
                    inferenceProfileName=profile_name,
                    description="test",
                    modelSource={'copyFrom': base_model_arn},
                    tags=tags or []
                )
                profile_arn = profile['inferenceProfileArn']
            else:
                # Get existing profile ARN
                profile_arn = next(p['inferenceProfileArn'] 
                                for p in existing_profiles['inferenceProfileSummaries'] 
                                if p['inferenceProfileName'] == profile_name)
            
            return profile_arn
        except Exception as e:
            print(f"Error checking/creating profile: {str(e)}")
            raise
    
    async def query_model(self, model_id, query, system_prompt, context=None):
        """Async wrapper for querying a Bedrock model"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._query_model,
            model_id,
            query,
            system_prompt,
            context
        )
    
    def _query_model(self, model_id, query, system_prompt, context=None):
        """Synchronous implementation for query_model"""
        # Prepare message content based on whether context is provided
        if context:
            message_text = f"Given the full context: {context}\n\nAnswer this question accurately: {query}"
        else:
            message_text = query
        
        # Prepare messages for the API call
        messages = [
            {
                "role": "user",
                "content": [
                    {"text": message_text}
                ]
            }
        ]
        
        # Prepare parameters for the API call
        converse_params = {
            "modelId": model_id,
            "messages": messages,
            "system": [{"text": system_prompt}]
        }
        
        # Call the API and return the response
        response = self.runtime_client.converse(**converse_params)
        return response['output']['message']['content'][0]['text']

class AsyncQBusinessClient:
    """Async wrapper for Q Business client operations"""
    
    def __init__(self, region='us-east-1', credentials=None):
        if credentials:
            self.client = boto3.client("qbusiness", region_name=region, **credentials)
        else:
            self.client = boto3.client('qbusiness', region_name=region)
    
    async def get_app_and_retriever_ids(self):
        """Async wrapper for getting app and retriever IDs"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._get_app_and_retriever_ids
        )
    
    def _get_app_and_retriever_ids(self):
        """Synchronous implementation for get_app_and_retriever_ids"""
        app_id = ""
        retriever_id = ""
        
        # Get application ID
        response_app = self.client.list_applications()
        for app in response_app["applications"]:
            if Q_BUSINESS_APP_NAME in app['displayName']:
                app_id = app['applicationId']
                break
        
        # Get retriever ID if app ID was found
        if app_id:
            response_ret = self.client.list_retrievers(applicationId=app_id)
            retriever_id = response_ret['retrievers'][0]['retrieverId']
        
        return app_id, retriever_id
    
    async def call_search_relevant_content(self, app_id, retriever_id, query_text, max_results=5):
        """Async wrapper for searching relevant content"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._call_search_relevant_content,
            app_id,
            retriever_id,
            query_text,
            max_results
        )
    
    def _call_search_relevant_content(self, app_id, retriever_id, query_text, max_results):
        """Synchronous implementation for call_search_relevant_content"""
        search_params = {
            'applicationId': app_id, 
            'contentSource': {
                'retriever': { 
                    'retrieverId': retriever_id 
                }
            }, 
            'queryText': query_text, 
            'maxResults': max_results
        }
        
        try:
            search_response = self.client.search_relevant_content(**search_params)
            return search_response['relevantContent']
        except Exception as e:
            print(e)
            return None