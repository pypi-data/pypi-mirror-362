from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import requests
import json
import os

mcp = FastMCP("ms_image_gen_mcp")


# @mcp.tool()
# def list_api_available_text_to_image_models(page_size=30, page_number=1) -> list[TextContent]:
#     """
#     List all api-inference available text-to-image models on ModelScope.
#     """

#     url = 'https://placeholder.modelscope.cn/openapi/v1/models'
#     token = os.environ.get("MODELSCOPE_API_KEY")

#     params = {
#         "page_size": page_size,
#         "page_number": page_number,
#         "inference.backend": "ollama"
#     }

#     # params = {
#     #     "filter.task": "text-to-image-synthesis",
#     #     "inference.backend": "ollama"
#     # }

#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json'
#     }

#     try:
#         response = requests.get(url, headers=headers, params=params)
#         response_data = response.json()

#         if response_data['code'] == 200:
#             total_count = response_data['data']['total_count']
#             models = response_data['data']['models']
#             info = f"Found {total_count} text-to-image models available for API inference. Showing page {page_number} with {page_size} models per page:"
#             res = info + ','.join(["Model ID:{}, name: {}, description:{}".format(model['id'], model['display_name'], model['description']) for model in models])
#         else:
#             res = str(response_data)

#     except Exception as e:
#         res = "error:" + str(e)
#         print(f"Error: {e}")
#     return [TextContent(type="text", text=res)]


@mcp.tool()
def generate_image_url_from_text(description : str,
                                 model: str = "MusePublic/489_ckpt_FLUX_1"
                                 ) -> list[TextContent]:
    """Generate an image from the input description using ModelScope API, it returns the image URL.

    Args:
        description: the description of the image to be generated, containing the desired elements and visual features.
        model: the model name to be used for image generation, default is "MusePublic/489_ckpt_FLUX_1".
    """


    url = 'https://api-inference.modelscope.cn/v1/images/generations'
    token = os.environ.get("MODELSCOPE_API_KEY")
    payload = {
        'model': model,  # ModelScope Model-Id, 必填项
        'prompt': description  # 必填项
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url,
                                 data=json.dumps(
                                     payload, ensure_ascii=False).encode('utf-8'),
                                 headers=headers)

        response_data = response.json()
        if 'images' in response_data.keys():
            res= response_data['images'][0]['url']
        else:
            res = str(response_data)

    except Exception as e:
        res = "error:" + str(e)
        print(f"Error: {e}")
    return [TextContent(type="text", text=res)]


@mcp.tool()
def generate_image_url_from_text_and_image_url(description : str,
                                               image_url : str,
                                 model: str = "black-forest-labs/FLUX.1-Kontext-dev"
                                 ) -> list[TextContent]:
    """Generate an image from the input description and input image_url using ModelScope API, it returns the image URL.

    Args:
        description: the description of the image to be generated, containing the desired elements and visual features.
        image_url: the image URL to be used as the input image for image generation.
        model: the model name to be used for image generation, default is "black-forest-labs/FLUX.1-Kontext-dev".
    """


    url = 'https://api-inference.modelscope.cn/v1/images/generations'
    token = os.environ.get("MODELSCOPE_API_KEY")
    payload = {
        'model': model,  # ModelScope Model-Id, 必填项
        'prompt': description,  # 必填项
        'image_url': image_url
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url,
                                 data=json.dumps(
                                     payload, ensure_ascii=False).encode('utf-8'),
                                 headers=headers)

        response_data = response.json()
        if 'images' in response_data.keys():
            res= response_data['images'][0]['url']
        else:
            res = str(response_data)

    except Exception as e:
        res = "error:" + str(e)
        print(f"Error: {e}")
    return [TextContent(type="text", text=res)]





if __name__ == "__main__":
    mcp.run(transport='stdio')

