from httpx import AsyncClient
from bs4 import BeautifulSoup
from telegraph.aio import Telegraph


async def katbin_paste(text: str) -> str:
    """
    paste the text in katb.in website.
    """

    katbin_url = "https://katb.in/api/paste"
    client = AsyncClient()
    try:
        paste_post = await client.post(
            katbin_url,
            json={"paste": {"content": f"{text}"}}).json()
        
        output_url = "https://katb.in/{}".format(paste_post["id"])
        
        await client.aclose()
        return output_url
    except:
        return "something went wrong while pasting text in katb.in."


async def telegraph_paste(content: str, title="UsenetBot") -> str:
    """
    paste the text in telegra.ph (graph.org) website (text should follow proper html tags).
    """

    telegraph = Telegraph(domain="graph.org")

    await telegraph.create_account(short_name=title)
    html_content = content.replace("\n", "<br>")
    try:
        response = await telegraph.create_page(
            title="Usenet Bot search result -", html_content=html_content)
        response = response["url"]
    except:
        response = await katbin_paste(content)

    try:
        await telegraph.revoke_access_token()
    except: pass
    return response
