import requests


class ImagesProvider:
    __slots__ = ()

    API_TOKEN = "21775110-0daaf3eef48f15b280160a679"
    URL = "https://pixabay.com/api/"
    QUERY = "red+cars"
    PER_PAGE = 21

    @classmethod
    def load_images(cls):
        query_string = (
            f"{cls.URL}?key={cls.API_TOKEN}&q={cls.QUERY}"
            f"&image_type=photo&per_page={cls.PER_PAGE}"
        )
        json_response = requests.get(query_string).json()

        images_links = []
        print(len(json_response["hits"]))
        for json_img in json_response["hits"]:
            images_links.append(json_img["webformatURL"])
        return images_links