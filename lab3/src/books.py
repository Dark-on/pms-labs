class Book:
    def __init__(self, title, subtitle, isbn13, price, image_path):
        self.title = title
        self.subtitle = subtitle
        self.isbn13 = isbn13
        self.price = price
        self.image_path = image_path

    @classmethod
    def init_from_dict(cls, book):
        title = book["title"] or ""
        subtitle = book["subtitle"] or ""
        isbn13 = book["isbn13"] or ""
        price = book["price"] or ""
        img_path = f"data/Images/default.png"
        if book["image"]:
            img_path = f"data/Images/{book['image']}"

        return cls(
            title=title,
            subtitle=subtitle,
            isbn13=isbn13,
            price=f"Price: {price}",
            image_path=img_path
        )
