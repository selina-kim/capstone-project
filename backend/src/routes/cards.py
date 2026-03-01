"""
Card API endpoints for CRUD operations on flashcards.
"""

import json
from flask import Blueprint, request, Response
from services.card_service import (
    CardService, 
    CardNotFoundError, 
    DeckNotFoundError, 
    UnauthorizedError,
    DatabaseError
)
from flask_jwt_extended import jwt_required, get_jwt_identity

cards_bp = Blueprint("cards", __name__)
card_service = CardService()


def json_response(data, status=200, ensure_ascii=False):
    return Response(
        json.dumps(data, default=str, ensure_ascii=ensure_ascii),
        status=status,
        mimetype="application/json; charset=utf-8" if not ensure_ascii else "application/json"
    )


def error_response(message, status=500):
    return json_response({"error": message}, status=status)


@cards_bp.route("/decks/<int:deck_id>/card", methods=["POST"])
@jwt_required()
def create_card(deck_id: int):
    """
    POST /decks/:d_id/card
    Body: word, translation, word_roman (required); definition, word_example, 
          trans_example, image, word_audio, trans_audio, trans_roman (optional)
    """
    data = request.get_json(silent=True)
    if not data:
        return error_response("No data provided", status=400)
    
    data["d_id"] = deck_id
    
    required_fields = ["word", "translation", "word_roman"]
    for field in required_fields:
        if field not in data or not str(data.get(field, "")).strip():
            return error_response(f"Missing required field: {field}", status=400)
    
    user_id = get_jwt_identity()
    
    try:
        card = card_service.create_card(user_id, data)
        
        return json_response({
            "message": "Card created successfully",
            "card": card
        }, status=201)
    
    except DeckNotFoundError as e:
        return error_response(str(e) or "Deck not found or access denied", status=404)
    
    except UnauthorizedError as e:
        return error_response(str(e) or "Unauthorized", status=403)
    
    except DatabaseError as e:
        return error_response(str(e) or "Database error", status=500)
    
    except Exception as e:
        return error_response(f"Failed to create card: {str(e)}")


@cards_bp.route("/decks/<int:deck_id>/cards/<int:card_id>", methods=["GET"])
@jwt_required()
def get_card(deck_id: int, card_id: int):
    """GET /decks/:d_id/cards/:c_id - returns card data"""
    user_id = get_jwt_identity()
    
    try:
        card = card_service.get_card(user_id, card_id, deck_id)
        
        if not card:
            return error_response("Card not found or access denied", status=404)
        
        return json_response(card)
    
    except Exception as e:
        return error_response(f"Database error: {str(e)}")


@cards_bp.route("/decks/<int:deck_id>/cards/<int:card_id>", methods=["POST"])
@jwt_required()
def update_card(deck_id: int, card_id: int):
    """
    POST /decks/:d_id/cards/:c_id - edit card
    Any field can be updated. TTS regenerated if word/translation changes.
    Image re-downloaded if URL provided.
    """
    data = request.get_json(silent=True)
    if not data:
        return error_response("No data provided", status=400)
    
    user_id = get_jwt_identity()
    
    try:
        card = card_service.update_card(user_id, card_id, data, deck_id)
        
        return json_response({
            "message": "Card updated successfully",
            "card": card
        })
    
    except CardNotFoundError as e:
        return error_response(str(e) or "Card not found or access denied", status=404)
    
    except UnauthorizedError as e:
        return error_response(str(e) or "Unauthorized", status=403)
    
    except DatabaseError as e:
        return error_response(str(e) or "Database error", status=500)
    
    except Exception as e:
        return error_response(f"Failed to update card: {str(e)}")


@cards_bp.route("/decks/<int:deck_id>/cards/<int:card_id>", methods=["DELETE"])
@jwt_required()
def delete_card(deck_id: int, card_id: int):
    """DELETE /decks/:d_id/cards/:c_id - also removes MinIO objects"""
    user_id = get_jwt_identity()
    
    try:
        card_service.delete_card(user_id, card_id, deck_id)
        
        return json_response({"message": "Card deleted successfully"})
    
    except CardNotFoundError as e:
        return error_response(str(e) or "Card not found or access denied", status=404)
    
    except UnauthorizedError as e:
        return error_response(str(e) or "Unauthorized", status=403)
    
    except Exception as e:
        return error_response(f"Failed to delete card: {str(e)}")


@cards_bp.route("/decks/<int:deck_id>/cards", methods=["GET"])
@jwt_required()
def get_deck_cards(deck_id: int):
    """GET /decks/:d_id/cards?page=1&per_page=50"""
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)
    
    try:
        result = card_service.get_cards_for_deck(user_id, deck_id, page, per_page)
        
        if result is None:
            return error_response("Deck not found or access denied", status=404)
        
        return json_response(result)
    
    except Exception as e:
        return error_response(f"Database error: {str(e)}")
