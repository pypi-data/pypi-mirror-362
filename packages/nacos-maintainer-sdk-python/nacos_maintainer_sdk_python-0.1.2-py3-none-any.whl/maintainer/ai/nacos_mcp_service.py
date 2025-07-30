import json
from typing import List

from pydantic import TypeAdapter

from maintainer.common.ai_maintainer_client_config import AIMaintainerClientConfig
from maintainer.common.auth import RequestResource
from maintainer.common.constants import Constants
from maintainer.ai.model.nacos_mcp_info import McpServerBasicInfo, \
	McpServerDetailInfo, McpToolSpecification, McpEndpointSpec
from maintainer.nacos_maintainer_client import NacosMaintainerClient
from maintainer.transport.client_http_proxy import ClientHttpProxy, HttpRequest


class NacosAIMaintainerService(NacosMaintainerClient):

	def __init__(self, ai_client_config: AIMaintainerClientConfig):
		super().__init__(ai_client_config, Constants.MCP_MODULE)
		self.http_proxy = ClientHttpProxy(self.logger, ai_client_config, self.http_agent)

	@staticmethod
	async def create_mcp_service(client_config: AIMaintainerClientConfig):
		mcp_service = NacosAIMaintainerService(client_config)
		return mcp_service

	async def list_mcp_servers(self, namespace_id:str, mcp_name:str, page_no:int, page_size:int) -> (int, int, int, List[McpServerBasicInfo]):
		if namespace_id is None or len(namespace_id) == 0:
			namespace_id = Constants.DEFAULT_NAMESPACE_ID

		params = {
			'pageNo': page_no,
			'pageSize': page_size,
			'namespaceId': namespace_id,
			'mcpName': mcp_name,
			'search': "accurate"
		}
		request_resource = RequestResource(Constants.MCP_MODULE, namespace_id, '', mcp_name)
		request = HttpRequest(path='/nacos/v3/admin/ai/mcp/list', method='GET', request_resource=request_resource, params=params)
		result = await self.http_proxy.request(request)
		if result['code'] != 0:
			self.logger.error("list ai servers failed",result)
			raise Exception(result['message'])

		result_data = result['data']
		total_count = result_data['totalCount']
		page_number = result_data['pageNumber']
		page_available = result_data['pagesAvailable']
		page_items = result_data['pageItems']
		try:
			adapter = TypeAdapter(List[McpServerBasicInfo])
			mcp_servers:List[McpServerBasicInfo] = adapter.validate_python(page_items)
		except Exception as e:
			self.logger.error(e)
			raise

		return total_count, page_number, page_available, mcp_servers

	async def search_mcp_server(self,namespace_id:str, mcp_name:str, page_no:int, page_size:int) -> (int, int, int, List[McpServerBasicInfo]):
		if namespace_id is None or len(namespace_id) == 0:
			namespace_id = Constants.DEFAULT_NAMESPACE_ID

		params = {
			'pageNo': page_no,
			'pageSize': page_size,
			'namespaceId': namespace_id,
			'mcpName': mcp_name,
			'search': "blur"
		}
		request_resource = RequestResource(Constants.MCP_MODULE, namespace_id, '', mcp_name)
		request = HttpRequest(path='/nacos/v3/admin/ai/mcp/list', method='GET', request_resource=request_resource, params=params)
		result = await self.http_proxy.request(request)
		if result['code'] != 0:
			self.logger.error("search ai server failed",result)
			raise Exception(result['message'])

		result_data = result['data']
		total_count = result_data['totalCount']
		page_number = result_data['pageNumber']
		page_available = result_data['pagesAvailable']
		page_items = result_data['pageItems']
		try:
			adapter = TypeAdapter(List[McpServerBasicInfo])
			mcp_servers:List[McpServerBasicInfo] = adapter.validate_python(page_items)
		except Exception as e:
			self.logger.error(e)
			raise
		return total_count, page_number, page_available, mcp_servers

	async def get_mcp_server_detail(self, namespace_id:str, mcp_name:str, version:str) -> McpServerDetailInfo:
		if namespace_id is None or len(namespace_id) == 0:
			namespace_id = Constants.DEFAULT_NAMESPACE_ID

		params = {
			'namespaceId': namespace_id,
			'mcpName': mcp_name,
			'version': version
		}
		request_resource = RequestResource(Constants.MCP_MODULE, namespace_id, '', mcp_name)
		request = HttpRequest(path='/nacos/v3/admin/ai/mcp', method='GET', request_resource=request_resource, params=params)
		result = await self.http_proxy.request(request)
		if result['code'] != 0:
			self.logger.error("get mcp server detail failed",result)
			raise Exception(result['message'])

		result_data = result['data']
		try:
			adapter = TypeAdapter(McpServerDetailInfo)
			mcp_server:McpServerDetailInfo = adapter.validate_python(result_data)
		except Exception as e:
			self.logger.error(e)
			raise
		return mcp_server

	async def create_mcp_server(self,namespace_id:str, mcp_name:str, server_spec: McpServerBasicInfo,
		tool_spec: McpToolSpecification, endpoint_spec: McpEndpointSpec) -> bool:
		if namespace_id is None or len(namespace_id) == 0:
			namespace_id = Constants.DEFAULT_NAMESPACE_ID

		params = {
			'namespaceId': namespace_id,
			'mcpName': mcp_name,
			'serverSpecification': server_spec.model_dump_json(exclude_none=True),
		}
		if tool_spec is not None:
			params['toolSpecification'] = tool_spec.model_dump_json(exclude_none=True)
		if endpoint_spec is not None:
			params['endpointSpecification'] = endpoint_spec.model_dump_json(exclude_none=True)

		request_resource = RequestResource(Constants.MCP_MODULE, namespace_id, '', mcp_name)
		request = HttpRequest(path='/nacos/v3/admin/ai/mcp', method='POST', request_resource=request_resource, data=params)
		result = await self.http_proxy.request(request)
		if result['code'] != 0:
			self.logger.error("create mcp server failed",result)
			return False

		return True

	async def update_mcp_server(self, namespace_id:str, mcp_name:str, is_latest:bool, server_spec: McpServerBasicInfo,
		tool_spec: McpToolSpecification, endpoint_spec: McpEndpointSpec):
		if namespace_id is None or len(namespace_id) == 0:
			namespace_id = Constants.DEFAULT_NAMESPACE_ID

		params = {
			'namespaceId': namespace_id,
			'mcpName': mcp_name,
			'latest': is_latest,
			'serverSpecification': server_spec.model_dump_json(exclude_none=True)
		}
		if tool_spec is not None:
			params['toolSpecification'] = tool_spec.model_dump_json(exclude_none=True)
		if endpoint_spec is not None:
			params['endpointSpecification'] = endpoint_spec.model_dump_json(exclude_none=True)

		request_resource = RequestResource(Constants.MCP_MODULE, namespace_id, '', mcp_name)
		request = HttpRequest(path='/nacos/v3/admin/ai/mcp', method='PUT', request_resource=request_resource, data=params)
		result = await self.http_proxy.request(request)
		if result['code'] != 0:
			self.logger.error("update mcp server failed",result)
			return False

		return True

	async def delete_mcp_server(self, namespace_id:str, mcp_name:str) -> bool:
		if namespace_id is None or len(namespace_id) == 0:
			namespace_id = Constants.DEFAULT_NAMESPACE_ID

		params = {
			'namespaceId': namespace_id,
			'mcpName': mcp_name
		}
		request_resource = RequestResource(Constants.MCP_MODULE, namespace_id, '', mcp_name)
		request = HttpRequest(path='/nacos/v3/admin/ai/mcp', method='DELETE', request_resource=request_resource, params=params)
		result = await self.http_proxy.request(request)
		if result['code'] != 0:
			self.logger.error("delete mcp server failed",result)
			return False

		return True