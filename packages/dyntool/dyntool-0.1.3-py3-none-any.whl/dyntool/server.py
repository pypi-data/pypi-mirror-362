import logging
from typing import Sequence
from mcp.server import Server
from mcp.server.session import ServerSession
from mcp.server.stdio import stdio_server
from mcp.types import (
    ClientCapabilities,
    TextContent,
    Tool,
    ListRootsResult,
    RootsCapability,
)
from enum import Enum
from pydantic import BaseModel
import click
import sys
import os
import fitz  # PyMuPDF

class InternsTool(str, Enum):
    GET_INTERNS = "get_adobe_interns"
    LIST_DIRECTORY = "list_directory"
    TEXT_TO_PDF = "text_to_pdf"

class GetInternsInput(BaseModel):
    year: int

class ListDirectoryInput(BaseModel):
    path: str

class TextToPdfInput(BaseModel):
    text: str
    output_path: str

def get_adobe_interns(year: int) -> list[str]:
    """Return a list of current interns at Adobe for a given year"""
    # Example: hardcoded data for demonstration
    interns_by_year = {
        2023: [
            "Ajay Paliwal",
            "Abhijeet Agarwal",
            "Siddhartha Rajeev",
            "Shrey Patel"
        ],
        2022: [
            "Jane Doe",
            "John Smith"
        ]
    }
    with open("./interns.txt", "a") as file:
        file.write(f"Requested interns for year {year} \n, interns: {interns_by_year.get(year, [])}\n")
    return interns_by_year.get(year, [])

def list_directory(path: str) -> list[str]:
    """Return a list of files and directories at the given path"""
    try:
        return os.listdir(path)
    except (FileNotFoundError, PermissionError) as e:
        return [f"Error: {str(e)}"]
        
def text_to_pdf(text: str, output_path: str) -> str:
    """Convert text to PDF and save it to the specified location using PyMuPDF"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create a new PDF document
        doc = fitz.open()
        page = doc.new_page()
        
        # Add text to the page
        text_instance = fitz.Text(page.rect)
        text_instance.append_text(text)
        page.insert_text(fitz.Point(50, 50), text, fontsize=11)
        
        # Save the document
        doc.save(output_path)
        doc.close()
        
        return f"PDF successfully created at {output_path}"
    except Exception as e:
        return f"Error creating PDF: {str(e)}"

async def serve() -> None:
    print({"message": "Starting latest DynamicWF MCP server with tools"})
    logger = logging.getLogger(__name__)
    logger.info("Starting DynamicWF MCP server")

    server = Server("dynamicwf")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=InternsTool.GET_INTERNS,
                description="Get a list of all current Adobe interns for a given year",
                inputSchema=GetInternsInput.schema(),
            ),
            Tool(
                name=InternsTool.LIST_DIRECTORY,
                description="List files and directories at the given path",
                inputSchema=ListDirectoryInput.schema(),
            ),
            Tool(
                name=InternsTool.TEXT_TO_PDF,
                description="Convert text to PDF and save it to the specified location",
                inputSchema=TextToPdfInput.schema(),
            ),
        ]

    async def list_roots() -> Sequence[str]:
        if not isinstance(server.request_context.session, ServerSession):
            raise TypeError("server.request_context.session must be a ServerSession")

        if not server.request_context.session.check_client_capability(
            ClientCapabilities(roots=RootsCapability())
        ):
            return []

        roots_result: ListRootsResult = await server.request_context.session.list_roots()
        logger.debug(f"Roots result: {roots_result}")
        return []

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        match name:
            case InternsTool.GET_INTERNS:
                input_data = GetInternsInput(**arguments)
                interns = get_adobe_interns(input_data.year)
                return [TextContent(
                    type="text",
                    text=f"Current Adobe interns for {input_data.year}:\n" +
                        ("\n".join(f"- {intern}" for intern in interns) if interns else "No data available.")
                )]
            case InternsTool.LIST_DIRECTORY:
                input_data = ListDirectoryInput(**arguments)
                files = list_directory(input_data.path)
                return [TextContent(
                    type="text",
                    text=f"Contents of {input_data.path}:\n" +
                        ("\n".join(f"- {file}" for file in files) if files else "No files found or directory is empty.")
                )]
            case InternsTool.TEXT_TO_PDF:
                input_data = TextToPdfInput(**arguments)
                result = text_to_pdf(input_data.text, input_data.output_path)
                return [TextContent(
                    type="text",
                    text=result
                )]
            case _:
                raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

@click.command()
@click.option("-v", "--verbose", count=True)
def main(verbose: bool) -> None:
    """DynamicWF MCP Server - Intern information for MCP"""
    import asyncio

    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    asyncio.run(serve())

# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(serve())