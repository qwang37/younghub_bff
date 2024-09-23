from flask import Blueprint, jsonify, abort
from app.util.azure_cosmos_util import AzureCosmosUtil

card_bp = Blueprint('cards', __name__)

read_article_list = AzureCosmosUtil()

@card_bp.route('/cards')
def get_card():
    return read_article_list.read_article_list()
