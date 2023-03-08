from httpx import AsyncClient
from bs4 import BeautifulSoup
from telegraph.aio import Telegraph


async def katbin_paste(text: str) -> str:
	"""
	paste the text in katb.in website.
	"""

	katbin_url = "https://katb.in"
	client = AsyncClient()
	response = await client.get(katbin_url)
	soup = BeautifulSoup(response.content, "html.parser")
	csrf_token = soup.find("input", {"name": "_csrf_token"}).get("value")
	try:
		paste_post = await client.post(
			katbin_url,
			data={"_csrf_token": csrf_token, "paste[content]": text},
			follow_redirects=False)
		output_url = f"{katbin_url}{paste_post.headers['location']}"
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
	html_content = "<p>" + content.replace("\n", "<br>") + "</p>"
	try:
		response = await telegraph.create_page(title="Usenet Bot search result -", html_content=html_content)
		response = response["url"]
	except:
		response = await katbin_paste(content)

	try: await telegraph.revoke_access_token()
	except: pass
	return response



