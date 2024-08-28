from flask import Blueprint, jsonify, abort

card_bp = Blueprint('cards', __name__)

cards = [
    {
        "ID": 0,
        "Title": "來者網站發布",
        "Description": "为北美的留学生、职业青年、年轻家庭（简称 “美漂”）量身打造的社群媒体平台。平台每周推播注册会员的原创内容，欢迎加入我们！",
        "ContentURL": "https://www.afcdrc.org/en/younghub",
        "Author": "心怡",
        "PictureURL": "https://younghubstorage.blob.core.windows.net/home/younghub_intro.png"
    },
    {
        "ID": 1,
        "Title": "另一篇文章",
        "Description": "这是一篇示例文章的描述。",
        "ContentURL": "https://www.example.com/article2",
        "Author": "作者名",
        "PictureURL": "https://example.com/image2.png"
    }
    # Add more cards as needed
]


@card_bp.route('/card/<int:id>')
def get_card(id):
    # Find the card with the matching ID
    card = next((card for card in cards if card["ID"] == id), None)

    if card is not None:
        return jsonify(card)
    else:
        # Return a 404 error if the card is not found
        abort(404, description="Card not found")
