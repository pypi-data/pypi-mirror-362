from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from maintainer.ai.model.registry_mcp_info import Repository, ServerVersionDetail


class McpCapability(Enum):
	TOOL = "TOOL"
	PROMPT = "PROMPT"
	RESOURCE = "RESOURCE"


class McpEndpointInfo(BaseModel):
	address: Optional[str]=None
	port: Optional[int]=None
	path: Optional[str]=None


class McpServiceRef(BaseModel):
	namespaceId: Optional[str]=None
	groupName: Optional[str]=None
	serviceName: Optional[str]=None


class McpEndpointSpec(BaseModel):
	type: Optional[str]=None
	data: Optional[Dict[str, str]]=None


class McpServerRemoteServiceConfig(BaseModel):
	serviceRef: Optional[McpServiceRef]=None
	exportPath: Optional[str]=None


class McpServerBasicInfo(BaseModel):
	id: Optional[str]=None
	name: Optional[str]=None
	protocol: Optional[str]=None
	frontProtocol: Optional[str]=None
	description: Optional[str]=None
	repository: Optional[Repository]=None
	versionDetail: Optional[ServerVersionDetail]=None
	version: Optional[str]=None
	remoteServerConfig: Optional[McpServerRemoteServiceConfig]=None
	localServerConfig: Optional[Dict[str, Any]]=None
	enabled: Optional[bool]=None
	capabilities: Optional[List[McpCapability]]=None


class McpServerVersionInfo(McpServerBasicInfo):
	latestPublishedVersion: Optional[str]=None
	versionDetails: Optional[List[ServerVersionDetail]]=None


class McpTool(BaseModel):
	name: Optional[str]=None
	description: Optional[str]=None
	inputSchema: Optional[Dict[str, Any]]=None


class McpToolMeta(BaseModel):
	invokeContext: Optional[Dict[str, Any]]=None
	enabled: Optional[bool]=None
	templates: Optional[Dict[str, Any]]=None


class McpToolSpecification(BaseModel):
	tools: Optional[List[McpTool]]=None
	toolsMeta: Optional[Dict[str, McpToolMeta]]=None


class McpServerDetailInfo(McpServerBasicInfo):
	backendEndpoints: Optional[List[McpEndpointInfo]]=None
	toolSpec: Optional[McpToolSpecification]=None
	allVersions: Optional[List[ServerVersionDetail]]=None
	namespaceId: Optional[str]=None
