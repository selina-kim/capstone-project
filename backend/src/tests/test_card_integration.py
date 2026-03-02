"""Integration tests for card routes.

Tests the card management endpoints with actual HTTP requests and responses.
These tests verify the complete request/response cycle including:
- Card CRUD operations (create, read, update, delete)
- Deck-level card queries with pagination
- Authentication and authorization
- Database interactions
- Input validation and error handling

All tests in this file are marked as integration tests.

Run this test file:
    docker compose exec backend pytest src/tests/test_card_integration.py -v -m integration

Run with coverage:
    docker compose exec backend pytest src/tests/test_card_integration.py --cov=routes.cards -m integration
"""

import pytest
import json

pytestmark = pytest.mark.integration


def test_create_card_success(client, auth_headers):
    """Test successful card creation."""
    card_data = {
        "word": "adios",
        "translation": "goodbye",
        "word_roman": "ah-dee-ohs",
        "definition": "A farewell greeting",
        "word_example": "Adios, amigo!",
        "trans_example": "Goodbye, friend!"
    }
    
    response = client.post(
        "/decks/1/card",
        data=json.dumps(card_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 201
    result = json.loads(response.data)
    assert "card" in result
    assert result["card"]["word"] == "adios"
    assert result["card"]["translation"] == "goodbye"


def test_create_card_missing_word(client, auth_headers):
    """Test card creation fails without required word field."""
    card_data = {
        "translation": "goodbye",
        "word_roman": "ah-dee-ohs"
    }
    
    response = client.post(
        "/decks/1/card",
        data=json.dumps(card_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 400
    result = json.loads(response.data)
    assert "Missing required field" in result["error"]


def test_create_card_missing_translation(client, auth_headers):
    """Test card creation fails without required translation field."""
    card_data = {
        "word": "adios",
        "word_roman": "ah-dee-ohs"
    }
    
    response = client.post(
        "/decks/1/card",
        data=json.dumps(card_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 400
    result = json.loads(response.data)
    assert "Missing required field" in result["error"]


def test_create_card_missing_word_roman(client, auth_headers):
    """Test card creation fails without required word_roman field."""
    card_data = {
        "word": "adios",
        "translation": "goodbye"
    }
    
    response = client.post(
        "/decks/1/card",
        data=json.dumps(card_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 400
    result = json.loads(response.data)
    assert "Missing required field" in result["error"]


def test_create_card_no_data(client, auth_headers):
    """Test card creation fails with no data."""
    response = client.post(
        "/decks/1/card",
        data="",
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 400
    result = json.loads(response.data)
    assert "No data provided" in result["error"]


def test_create_card_deck_not_found(client, auth_headers):
    """Test card creation fails for non-existent deck."""
    card_data = {
        "word": "adios",
        "translation": "goodbye",
        "word_roman": "ah-dee-ohs"
    }
    
    response = client.post(
        "/decks/9999/card",
        data=json.dumps(card_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 404


def test_create_card_unauthorized(client):
    """Test card creation fails without auth token."""
    card_data = {
        "word": "adios",
        "translation": "goodbye",
        "word_roman": "ah-dee-ohs"
    }
    
    response = client.post(
        "/decks/1/card",
        data=json.dumps(card_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401


def test_get_card_success(client, auth_headers):
    """Test successful card retrieval."""
    response = client.get("/decks/1/cards/1", headers=auth_headers)
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["word"] == "hola"
    assert result["translation"] == "hello"


def test_get_card_not_found(client, auth_headers):
    """Test card retrieval for non-existent card."""
    response = client.get("/decks/1/cards/9999", headers=auth_headers)
    
    assert response.status_code == 404


def test_get_card_wrong_deck(client, auth_headers):
    """Test card retrieval with wrong deck ID."""
    response = client.get("/decks/9999/cards/1", headers=auth_headers)
    
    assert response.status_code == 404


def test_get_card_unauthorized(client):
    """Test card retrieval fails without auth token."""
    response = client.get("/decks/1/cards/1")
    
    assert response.status_code == 401


def test_update_card_success(client, auth_headers):
    """Test successful card update."""
    update_data = {
        "definition": "Updated definition"
    }
    
    response = client.post(
        "/decks/1/cards/1",
        data=json.dumps(update_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["card"]["definition"] == "Updated definition"


def test_update_card_word(client, auth_headers):
    """Test updating card word field."""
    update_data = {
        "word": "buenos dias"
    }
    
    response = client.post(
        "/decks/1/cards/1",
        data=json.dumps(update_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["card"]["word"] == "buenos dias"


def test_update_card_not_found(client, auth_headers):
    """Test update for non-existent card."""
    update_data = {
        "definition": "Updated"
    }
    
    response = client.post(
        "/decks/1/cards/9999",
        data=json.dumps(update_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 404


def test_update_card_no_data(client, auth_headers):
    """Test update with no data."""
    response = client.post(
        "/decks/1/cards/1",
        data="",
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 400
    result = json.loads(response.data)
    assert "No data provided" in result["error"]


def test_update_card_unauthorized(client):
    """Test update fails without auth token."""
    update_data = {
        "definition": "Updated"
    }
    
    response = client.post(
        "/decks/1/cards/1",
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401


def test_delete_card_success(client, auth_headers):
    """Test successful card deletion."""
    # First create a card to delete
    card_data = {
        "word": "test",
        "translation": "test",
        "word_roman": "test"
    }
    
    create_response = client.post(
        "/decks/1/card",
        data=json.dumps(card_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert create_response.status_code == 201
    card_id = json.loads(create_response.data)["card"]["c_id"]
    
    # Now delete it
    response = client.delete(f"/decks/1/cards/{card_id}", headers=auth_headers)
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert "deleted" in result["message"].lower()
    
    # Verify it's gone
    get_response = client.get(f"/decks/1/cards/{card_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_delete_card_not_found(client, auth_headers):
    """Test delete for non-existent card."""
    response = client.delete("/decks/1/cards/9999", headers=auth_headers)
    
    assert response.status_code == 404


def test_delete_card_unauthorized(client):
    """Test delete fails without auth token."""
    response = client.delete("/decks/1/cards/1")
    
    assert response.status_code == 401


def test_get_deck_cards_success(client, auth_headers):
    """Test successful retrieval of all cards in a deck."""
    response = client.get("/decks/1/cards", headers=auth_headers)
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert "cards" in result
    assert "pagination" in result
    assert len(result["cards"]) >= 1


def test_get_deck_cards_pagination(client, auth_headers):
    """Test pagination parameters for deck cards."""
    response = client.get("/decks/1/cards?page=1&per_page=10", headers=auth_headers)
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["pagination"]["page"] == 1
    assert result["pagination"]["per_page"] == 10


def test_get_deck_cards_deck_not_found(client, auth_headers):
    """Test cards retrieval for non-existent deck."""
    response = client.get("/decks/9999/cards", headers=auth_headers)
    
    assert response.status_code == 404


def test_get_deck_cards_unauthorized(client):
    """Test cards retrieval fails without auth token."""
    response = client.get("/decks/1/cards")
    
    assert response.status_code == 401


def test_create_multiple_cards(client, auth_headers):
    """Test creating multiple cards in a deck."""
    cards = [
        {"word": "uno", "translation": "one", "word_roman": "oo-no"},
        {"word": "dos", "translation": "two", "word_roman": "dohs"},
        {"word": "tres", "translation": "three", "word_roman": "trehs"}
    ]
    
    for card_data in cards:
        response = client.post(
            "/decks/1/card",
            data=json.dumps(card_data),
            content_type='application/json',
            headers=auth_headers
        )
        assert response.status_code == 201
    
    # Verify all cards are in the deck
    response = client.get("/decks/1/cards", headers=auth_headers)
    result = json.loads(response.data)
    assert result["pagination"]["total"] >= 4  # 1 from setup + 3 new


def test_card_fields_preserved(client, auth_headers):
    """Test that all optional fields are preserved."""
    card_data = {
        "word": "gato",
        "translation": "cat",
        "word_roman": "gah-toh",
        "definition": "A small feline",
        "word_example": "El gato es negro",
        "trans_example": "The cat is black",
        "trans_roman": "kat"
    }
    
    response = client.post(
        "/decks/1/card",
        data=json.dumps(card_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 201
    result = json.loads(response.data)
    card = result["card"]
    
    assert card["word"] == "gato"
    assert card["translation"] == "cat"
    assert card["word_roman"] == "gah-toh"
    assert card["definition"] == "A small feline"
    assert card["word_example"] == "El gato es negro"
    assert card["trans_example"] == "The cat is black"
    assert card["trans_roman"] == "kat"


def test_update_multiple_fields(client, auth_headers):
    """Test updating multiple fields at once."""
    update_data = {
        "word": "ciao",
        "translation": "hi/bye",
        "definition": "Italian greeting"
    }
    
    response = client.post(
        "/decks/1/cards/1",
        data=json.dumps(update_data),
        content_type='application/json',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    result = json.loads(response.data)
    card = result["card"]
    
    assert card["word"] == "ciao"
    assert card["translation"] == "hi/bye"
    assert card["definition"] == "Italian greeting"


# ==================== MinIO/TTS Integration Skeletons ====================
# TODO: Implement when MinIO and TTS services are configured

class TestImageIntegration:
    """Skeleton tests for image upload integration."""
    
    def test_create_card_with_image_url_placeholder(self, client, auth_headers):
        """Test card creation with image URL."""
        # TODO: Implement when MinIO is configured
        # Should download image from URL and store in MinIO
        pass
    
    def test_update_card_image_placeholder(self, client, auth_headers):
        """Test updating card image."""
        # TODO: Implement when MinIO is configured
        # Should delete old image and store new one
        pass
    
    def test_delete_card_removes_image_placeholder(self, client, auth_headers):
        """Test that deleting card removes image from MinIO."""
        # TODO: Implement when MinIO is configured
        pass


class TestTTSIntegration:
    """Skeleton tests for TTS integration."""
    
    def test_create_card_generates_tts_placeholder(self, client, auth_headers):
        """Test card creation auto-generates TTS."""
        # TODO: Implement when TTS service is configured
        # Should generate audio for word and translation
        pass
    
    def test_update_card_regenerates_tts_placeholder(self, client, auth_headers):
        """Test updating word/translation regenerates TTS."""
        # TODO: Implement when TTS service is configured
        # Should delete old audio and generate new
        pass
    
    def test_delete_card_removes_audio_placeholder(self, client, auth_headers):
        """Test that deleting card removes audio from MinIO."""
        # TODO: Implement when TTS/MinIO is configured
        pass


class TestFSRSIntegration:
    """Skeleton tests for FSRS scheduling fields."""
    
    def test_card_has_fsrs_fields(self, client, auth_headers):
        """Test that card response includes FSRS scheduling fields."""
        response = client.get("/decks/1/cards/1", headers=auth_headers)
        
        assert response.status_code == 200
        result = json.loads(response.data)
        
        # FSRS fields should be present
        assert "learning_state" in result
        assert "step" in result
        assert "difficulty" in result
        assert "stability" in result
        assert "due_date" in result
    
    def test_new_card_default_fsrs_values(self, client, auth_headers):
        """Test that new cards have default FSRS values."""
        card_data = {
            "word": "nuevo",
            "translation": "new",
            "word_roman": "nweh-vo"
        }
        
        response = client.post(
            "/decks/1/card",
            data=json.dumps(card_data),
            content_type='application/json',
            headers=auth_headers
        )
        
        assert response.status_code == 201
        # Note: FSRS fields may not be in create response depending on implementation
        # Fetch the card to verify defaults
        card_id = json.loads(response.data)["card"]["c_id"]
        
        get_response = client.get(f"/decks/1/cards/{card_id}", headers=auth_headers)
        result = json.loads(get_response.data)
        
        # New card should have New state and no due_date
        assert result["learning_state"] == 0  # New state
