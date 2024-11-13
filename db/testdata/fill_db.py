import os

from vk_api import VkApi, VkUpload

from db.testdata.testdata import categories
from services.category_service import CategoryService
from services.product_service import ProductService

pics_path = "./db/testdata/pics/"

vk_session = VkApi(token=os.getenv("API_TOKEN"))
vk = vk_session.get_api()
upload = VkUpload(vk)


async def upload_image_to_vk(image_path: str) -> str:
    """
    Uploads an image to VK and returns the URL of the uploaded image.
    Args:
        image_path (str): The path to the image file.
    Returns:
        str: The URL of the uploaded image.
    """
    photo = upload.photo_messages(photos=image_path)[0]
    return f"photo{photo['owner_id']}_{photo['id']}"


async def fill_db() -> None:
    """
    Fills the database with categories and products from the test data.
    """
    category_service = CategoryService()
    product_service = ProductService()

    for category_name, products in categories.items():
        await category_service.add_category(category_name=category_name)

        for product in products:
            product_name = product["name"]
            product_description = product["description"]
            product_image = product["image"]

            image_url = await upload_image_to_vk(f"{pics_path}{product_image}")

            await product_service.add_product(
                name=product_name,
                description=product_description,
                category_name=category_name,
                image_url=image_url,
            )


if __name__ == "__main__":
    import asyncio

    asyncio.run(fill_db())
