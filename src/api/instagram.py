import api


async def request(
    session: "api.Request",
    url: str
) -> dict:
    response: dict = await session.request(
        "GET",
        "https://rubigram.ir/apis/instagram.php?url={}".format(url),
        "JSON"
    )

    if not response or not response.get("fetch"):
        return None

    data: dict[str, list] = {}

    if "video" in response:
        data["videos"] = [item["video"] for item in response["video"]]

    if "image" in response:
        data["images"] = response["image"]

    return data