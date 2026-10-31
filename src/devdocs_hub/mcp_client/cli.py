import anyio
from mcp import Client

from devdocs_hub.settings import settings

async def main() -> None:
    while True:
        command = input("> ")
        command = command.strip()
        
        match command:
            case "devdocs-mcp tools":
                async with Client(f"http://{settings.api_host}:{settings.api_port}/mcp") as client:
                    result = await client.list_tools()
                    for tool in result.tools:
                        print(f'name: {tool.name}')
                        print(f' title: {tool.title}')
                        print(f' description: {tool.description}')
                        print(f' input_schema: {tool.input_schema}')
            case "exit":
                print("Quitting...")
                break
            case _:
                print(f"Unknown command: {command}")

if __name__ == '__main__':
    anyio.run(main)

