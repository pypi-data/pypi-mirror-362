import sys
import asyncio
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, List, Dict
from grabba import (
    Grabba, Job, JobResult, JobStats, GetJobResponse, GetJobsResponse,
    JobExecutionStatus, GetJobResultResponse, JobExecutionResponse,
    JobCreationResponse, JobEstimatedCostResponse, PuppetRegion,
    JobStatsResponse,
    CreateKnowledgeBaseResponse, GetKnowledgeBasesResponse, GetKnowledgeBaseResponse,
    StoreContextResponse, FetchContextResponse, UpdateContextResponse, GatherContextResponse,
    BaseResponse
)


class ServerConfig(BaseSettings):
    PORT: int = Field(8283, description="The PORT the MCP server should run on.")
    API_KEY: str = Field(None, description="The API key for accessing the Grabba python SDK.")
    MCP_SERVER_TRANSPORT: str = Field("stdio", description="The transport protocol for the MCP mcp.")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

class GrabbaService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API Key cannot be empty.")
        self.grabba = Grabba(api_key)

    async def fetch_stats_data(self) -> tuple[str, Optional[JobStats]]:
        """Fetch usage stats and user token balance"""
        try:
            result: JobStatsResponse = self.grabba.get_stats()
            return result.message, result.job_stats
        except Exception as err:
            return f"Error fetching usage stats: {str(err)}", None

    async def estimate_job_cost(self, extraction_data: Job) -> tuple[str, Optional[List[Job]]]:
        """Get the estimated cost of a job before creating or scheduling it"""
        try:
            result: JobEstimatedCostResponse = self.grabba.estimate_job_cost(job=extraction_data)
            return result.message, result.job_estimated_cost
        except Exception as err:
            return f"Error estimating job cost: {str(err)}", None

    async def extract_data(self, extraction_data: Job) -> tuple[str, Optional[Dict]]:
        """Schedule a new data extraction job. [Web Search Tool - used with markdown tasks]"""
        try:
            result: JobExecutionResponse = self.grabba.extract(job=extraction_data)
            if result.status == JobExecutionStatus.SUCCESS:
                job_result: JobResult = result.job_result
                return result.message, job_result
            return result.message, result.job_result
        except Exception as err:
            return f"Error scheduling job: {str(err)}", None

    async def create_job(self, extraction_data: Job) -> tuple[str, Optional[Job]]:
        """Create a new data extraction job (Without scheduling it)"""
        try:
            result: JobCreationResponse = self.grabba.create_job(job=extraction_data)
            return result.message, result.job
        except Exception as err:
            return f"Error creating job: {str(err)}", None
        
    async def schedule_job(self, job_id: str) -> tuple[str, Optional[Dict]]:
        """Schedule an existing job to run immediately"""
        try:
            result: JobExecutionResponse = self.grabba.schedule_job(job_id=job_id)
            return result.message, result.job_result
        except Exception as err:
            return f"Error scheduling job: {str(err)}", None

    async def fetch_jobs_data(self) -> tuple[str, Optional[List[Job]]]:
        """Fetch all jobs for the current user"""
        try:
            result: GetJobsResponse = self.grabba.get_jobs()
            return result.message, result.jobs
        except Exception as err:
            return f"Error fetching jobs: {str(err)}", None

    async def fetch_job_data(self, job_id: str) -> tuple[str, Optional[Job]]:
        """Fetch details of a specific job"""
        try:
            result: GetJobResponse = self.grabba.get_job(job_id)
            return result.message, result.job
        except Exception as err:
            return f"Error fetching job: {str(err)}", None

    async def delete_job_data(self, job_id: str) -> tuple[str, None]:
        """Delete a specific job"""
        try:
            self.grabba.delete_job(job_id)
            return f"Successfully deleted job {job_id}", None
        except Exception as err:
            return f"Error deleting job: {str(err)}", None

    async def fetch_job_result_data(self, job_result_id: str) -> tuple[str, Optional[Dict]]:
        """Fetch results of a completed job"""
        try:
            result: GetJobResultResponse = self.grabba.get_job_result(job_result_id)
            return result.message, result.job_result
        except Exception as err:
            return f"Error fetching job results: {str(err)}", None

    async def delete_job_result_data(self, job_result_id: str) -> tuple[str, None]:
        """Delete results of a completed job"""
        try:
            self.grabba.delete_job_result(job_result_id)
            return f"Successfully deleted job result {job_result_id}", None
        except Exception as err:
            return f"Error deleting job results: {str(err)}", None

    async def fetch_available_regions(self) -> tuple[str, Optional[List[Dict[str, PuppetRegion]]]]:
        """Fetch all available puppet (web agent) regions for scheduling web data extractions."""
        try:
            return "Fetched available regions successfully", self.grabba.get_available_regions()
        except Exception as err:
            return f"Error fetching jobs: {str(err)}", None

    async def create_knowledge_base(self, name: str, description: Optional[str] = None) -> tuple[str, Optional[CreateKnowledgeBaseResponse]]:
        """Create a new knowledge base."""
        try:
            result: CreateKnowledgeBaseResponse = self.grabba.create_knowledge_base(name=name, description=description)
            return result.message, result
        except Exception as err:
            return f"Error creating knowledge base: {str(err)}", None

    async def get_knowledge_bases(self) -> tuple[str, Optional[List[GetKnowledgeBasesResponse]]]:
        """Get all knowledge bases."""
        try:
            result: GetKnowledgeBasesResponse = self.grabba.get_knowledge_bases()
            return result.message, result.knowledge_bases
        except Exception as err:
            return f"Error fetching knowledge bases: {str(err)}", None

    async def get_knowledge_base(self, kb_id: str) -> tuple[str, Optional[GetKnowledgeBaseResponse]]:
        """Get a specific knowledge base by ID."""
        try:
            result: GetKnowledgeBaseResponse = self.grabba.get_knowledge_base(kb_id=kb_id)
            return result.message, result.knowledge_base
        except Exception as err:
            return f"Error fetching knowledge base: {str(err)}", None

    async def delete_knowledge_base(self, kb_id: str) -> tuple[str, None]:
        """Delete a knowledge base by ID."""
        try:
            result: BaseResponse = self.grabba.delete_knowledge_base(kb_id=kb_id)
            return result.message, None
        except Exception as err:
            return f"Error deleting knowledge base: {str(err)}", None

    async def store_context(self, kb_id: str, context: str, metadata: Optional[Dict] = None) -> tuple[str, Optional[StoreContextResponse]]:
        """Store context in a knowledge base."""
        try:
            result: StoreContextResponse = self.grabba.store_context(kb_id=kb_id, context=context, metadata=metadata)
            return result.message, result
        except Exception as err:
            return f"Error storing context: {str(err)}", None

    async def fetch_context(self, kb_id: str, query: str, options: Optional[Dict] = None) -> tuple[str, Optional[FetchContextResponse]]:
        """Fetch context from a knowledge base."""
        try:
            result: FetchContextResponse = self.grabba.fetch_context(kb_id=kb_id, query=query, options=options)
            return result.message, result
        except Exception as err:
            return f"Error fetching context: {str(err)}", None

    async def update_context(self, context_id: str, content: Optional[str] = None, metadata: Optional[Dict] = None) -> tuple[str, Optional[UpdateContextResponse]]:
        """Update context in a knowledge base."""
        try:
            result: UpdateContextResponse = self.grabba.update_context(context_id=context_id, content=content, metadata=metadata)
            return result.message, result
        except Exception as err:
            return f"Error updating context: {str(err)}", None

    async def delete_context(self, context_id: str) -> tuple[str, None]:
        """Delete context from a knowledge base."""
        try:
            result: BaseResponse = self.grabba.delete_context(context_id=context_id)
            return result.message, None
        except Exception as err:
            return f"Error deleting context: {str(err)}", None

    async def gather_context(self, kb_id: str) -> tuple[str, Optional[GatherContextResponse]]:
        """Gather context for a knowledge base."""
        try:
            result: GatherContextResponse = self.grabba.gather_context(kb_id=kb_id)
            return result.message, result
        except Exception as err:
            return f"Error gathering context: {str(err)}", None


# Load environment variables from .env file
load_dotenv()

# Instantiate ServerConfig
server_config = ServerConfig()

# === ARGUMENT PARSING LOGIC ===
if len(sys.argv) > 1:
    transport = sys.argv[1]
    # Check if the first argument is a known transport type
    valid_transports = ["stdio", "streamable-http", "sse"]
    if transport in valid_transports:
        server_config.MCP_SERVER_TRANSPORT = transport
        print(f"Overriding transport protocol from command line: {server_config.MCP_SERVER_TRANSPORT}")


# Initialize the MCP server
mcp = FastMCP(name="grabba-agent")

# Helper function to get GrabbaService instance within tool
async def _get_grabba_service_instance() -> GrabbaService:
    """
    Resolves the GrabbaService dependency.
    This is called by each tool to get an authenticated GrabbaService instance.
    """
    headers = get_http_headers()
    # Get API_KEY from headers
    api_key = headers.get("api_key") or server_config.API_KEY 
    if not api_key:
        raise ValueError("API Key is missing. Provide it via API_KEY header or API_KEY env var.")
    return GrabbaService(api_key=api_key)


#############################
#   Tools SPecifications    #
#############################


@mcp.tool(
    name="fetch_stats_data",
    description="Fetches usage statistics and current user token balance for Grabba. Takes no parameters.",
    tags={"billing", "usage"}
)
async def fetch_stats_data_tool() -> tuple[str, Optional[JobStats]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.fetch_stats_data()


@mcp.tool(
    name="estimate_job_cost",
    description="Estimates the cost of a Grabba job before creation or scheduling. Requires a 'Job' object detailing the extraction tasks.",
    tags={"billing"}
)
async def estimate_job_cost_tool(extraction_data: Job) -> tuple[str, Optional[Dict]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.estimate_job_cost(extraction_data)


@mcp.tool(
    name="create_job",
    description="Creates a new data extraction job in Grabba without immediately scheduling it for execution. Requires a 'Job' object detailing the extraction tasks.",
    tags={"management"}
)
async def create_job_tool(extraction_data: Job) -> tuple[str, Optional[Job]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.create_job(extraction_data)


@mcp.tool(
    name="extract_data",
    description="Schedules a new data extraction job with Grabba. Requires a 'Job' object detailing the extraction tasks.",
    tags={"catalog", "search"},
)
async def extract_data_tool(extraction_data: Job) -> tuple[str, Optional[Dict]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.extract_data(extraction_data)


@mcp.tool(
    name="schedule_existing_job",
    description="Schedules an existing Grabba job to run immediately. Requires the 'job_id' of the existing job."
)
async def schedule_job_tool(job_id: str) -> tuple[str, Optional[Dict]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.schedule_job(job_id)


@mcp.tool(
    name="fetch_all_jobs",
    description="Fetches all Grabba jobs for the current user. Takes no parameters."
)
async def fetch_jobs_data_tool() -> tuple[str, Optional[List[Job]]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.fetch_jobs_data()


@mcp.tool(
    name="fetch_specific_job",
    description="Fetches details of a specific Grabba job by its ID. Requires the 'job_id' of the job."
)
async def fetch_job_data_tool(job_id: str) -> tuple[str, Optional[Job]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.fetch_job_data(job_id)


@mcp.tool(
    name="delete_job",
    description="Deletes a specific Grabba job. Requires the 'job_id' of the job to delete."
)
async def delete_job_data_tool(job_id: str) -> tuple[str, None]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.delete_job_data(job_id)


@mcp.tool(
    name="fetch_job_result",
    description="Fetches results of a completed Grabba job by its result ID. Requires the 'job_result_id' of the result."
)
async def fetch_job_result_data_tool(job_result_id: str) -> tuple[str, Optional[Dict]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.fetch_job_result_data(job_result_id)


@mcp.tool(
    name="delete_job_result",
    description="Deletes results of a completed Grabba job. Requires the 'job_result_id' of the result to delete."
)
async def delete_job_result_data_tool(job_result_id: str) -> tuple[str, None]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.delete_job_result_data(job_result_id)


@mcp.tool(
    name="fetch_available_regions",
    description="Fetches a list of all available puppet (web agent) regions that can be used for scheduling web data extractions. Takes no parameters.",
    tags={"configuration"}
)
async def fetch_available_regions_tool() -> tuple[str, Optional[List[PuppetRegion]]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.fetch_available_regions()


@mcp.tool(
    name="create_knowledge_base",
    description="Creates a new knowledge base with a given name and optional description.",
    tags={"knowledge_base"}
)
async def create_knowledge_base_tool(name: str, description: Optional[str] = None) -> tuple[str, Optional[CreateKnowledgeBaseResponse]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.create_knowledge_base(name=name, description=description)


@mcp.tool(
    name="get_knowledge_bases",
    description="Retrieves a list of all knowledge bases.",
    tags={"knowledge_base"}
)
async def get_knowledge_bases_tool() -> tuple[str, Optional[List[GetKnowledgeBasesResponse]]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.get_knowledge_bases()


@mcp.tool(
    name="get_knowledge_base",
    description="Retrieves a specific knowledge base by its ID.",
    tags={"knowledge_base"}
)
async def get_knowledge_base_tool(kb_id: str) -> tuple[str, Optional[GetKnowledgeBaseResponse]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.get_knowledge_base(kb_id=kb_id)


@mcp.tool(
    name="delete_knowledge_base",
    description="Deletes a knowledge base by its ID.",
    tags={"knowledge_base"}
)
async def delete_knowledge_base_tool(kb_id: str) -> tuple[str, None]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.delete_knowledge_base(kb_id=kb_id)


@mcp.tool(
    name="store_context",
    description="Stores context (text content) within a specified knowledge base.",
    tags={"knowledge_base"}
)
async def store_context_tool(kb_id: str, context: str, metadata: Optional[Dict] = None) -> tuple[str, Optional[StoreContextResponse]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.store_context(kb_id=kb_id, context=context, metadata=metadata)


@mcp.tool(
    name="fetch_context",
    description="Fetches relevant context from a knowledge base based on a query.",
    tags={"knowledge_base"}
)
async def fetch_context_tool(kb_id: str, query: str, options: Optional[Dict] = None) -> tuple[str, Optional[FetchContextResponse]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.fetch_context(kb_id=kb_id, query=query, options=options)


@mcp.tool(
    name="update_context",
    description="Updates existing context within a knowledge base.",
    tags={"knowledge_base"}
)
async def update_context_tool(context_id: str, content: Optional[str] = None, metadata: Optional[Dict] = None) -> tuple[str, Optional[UpdateContextResponse]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.update_context(context_id=context_id, content=content, metadata=metadata)


@mcp.tool(
    name="delete_context",
    description="Deletes context from a knowledge base by its ID.",
    tags={"knowledge_base"}
)
async def delete_context_tool(context_id: str) -> tuple[str, None]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.delete_context(context_id=context_id)


@mcp.tool(
    name="gather_context",
    description="Gathers and processes context for a knowledge base.",
    tags={"knowledge_base"}
)
async def gather_context_tool(kb_id: str) -> tuple[str, Optional[GatherContextResponse]]:
    grabba_service = await _get_grabba_service_instance()
    return await grabba_service.gather_context(kb_id=kb_id)


def main():
    if server_config.MCP_SERVER_TRANSPORT == "streamable-http":        
        # Start the MCP server using FastMCP's built-in run method
        # This will handle HTTP communication protocol (e.g., streamable-http)
        print("Starting Grabba MCP server (streamable-http transport)...")
        asyncio.run(mcp.run_streamable_http_async(
            host="0.0.0.0", 
            port=server_config.PORT, 
            path="/"
        ))

    elif server_config.MCP_SERVER_TRANSPORT == "sse":
        # Start the MCP server using FastMCP's built-in run method
        # This will handle SSE communication protocol
        print("Starting Grabba MCP server (sse transport)...")
        asyncio.run(mcp.run_sse_async(
            host="0.0.0.0", 
            port=server_config.PORT, 
            path="/"
        ))

    else:
        if not server_config.API_KEY:
            raise ValueError("API Key required for stdio transport.")
        # Start the MCP server using StdioTransport
        print("Starting Grabba MCP server (stdio transport)...")
        asyncio.run(mcp.run_stdio_async())

if __name__ == "__main__":
    main()
