from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="complusory field.")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="complusory field.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'item exists'}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        item.save_to_db()
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item Deleted'}
        return {'message': 'Item cannot be found'}

    def put(self, name):
        # global items
        # data = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            #can change store id

        item.save_to_db()

        return item.json()


class ItemsList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
