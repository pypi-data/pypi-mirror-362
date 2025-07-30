from mcp.server.fastmcp import FastMCP, Context
import requests
import os
from importlib import resources
import base64
from mixpanel import Mixpanel

mcp = FastMCP("Figma→Compose with Tool Calls")
mp = Mixpanel("89ee15e05d11c3010c90e4713e25e7b5")

# Tool B: Fetches Figma node JSON
@mcp.tool()
async def get_figma_node(file_key: str, node_id: str) -> dict:
    """
    Fetches Figma node JSON

    Args:
        file_key: figma node file key
        node_id: figma node id
    """
    token = os.environ.get("FIGMA_TOKEN")
    node_id = node_id.replace('-', ':')
    url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}"
    res = requests.get(url, headers={"X-Figma-Token": token})
    res.raise_for_status()
    mp.track(hash(token), 'get_figma_node')
    return res.json()["nodes"][node_id]

# Tool C: Fetches SVG for a node
@mcp.tool()
async def get_figma_svg(file_key: str, node_id: str) -> str:
    """
    Fetches SVG for a node

    Args:
        file_key: figma node file key
        node_id: figma node id
    """
    token = os.environ.get("FIGMA_TOKEN")
    node_id = node_id.replace('-', ':')
    url = f"https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=svg"
    res = requests.get(url, headers={"X-Figma-Token": token})
    res.raise_for_status()
    img_url = res.json()["images"][node_id]
    mp.track(hash(token), 'get_figma_svg')
    return requests.get(img_url).text

# Tool A: Generates Compose prompt by calling Tools B and C
@mcp.tool()
async def generate_compose_code(
    file_key: str,
    node_id: str,
    ctx: Context
) -> str:
    """Generates jetpack compose code from figma link can have alias jc

    Args:
        file_key: figma node file key
        node_id: figma node id
        ctx: context
    """
    # Get token from environment
    token = os.environ.get("FIGMA_TOKEN")
    if not token:
        return "Error: FIGMA_TOKEN environment variable not set."

    # Call get_figma_node
    await ctx.info("Invoking get_figma_node…")
    node_json = await mcp.call_tool(
        "get_figma_node",
        {"file_key": file_key, "node_id": node_id, "token": token}
    )

    # Read the prompt template from package resources
    prompt_template = resources.read_text("figma_compose", "prompt.txt")

    # Build prompt text
    prompt = (
        f"{prompt_template}\n\n"
        f"Figma JSON:\n{node_json}\n\n"
    )

    mp.track(hash(token), 'generate_compose_code')

    return prompt

# @mcp.tool()
# async def get_figma_png(file_key: str, node_id: str, ctx: Context) -> str:
#     """Get figma png image

#     Args:
#         file_key: figma node file key
#         node_id: figma node id
#     """
#     token = os.environ.get("FIGMA_TOKEN")
#     node_id = node_id.replace('-', ':')
#     url = f"https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=png"
#     await ctx.info(f"Downloading image json from {url}…")
#     res = requests.get(url, headers={"X-Figma-Token": token})
#     res.raise_for_status()
#     await ctx.info(f"Downloading image json {res.json()}")
#     img_url = res.json()["images"][node_id]
#     await ctx.info(f"Downloading image from {img_url}…")
#     img_res = requests.get(img_url)
#     await ctx.info(f"Image downloaded")
#     img_res.raise_for_status()
#     return base64.b64encode(img_res.content).decode("utf-8")
