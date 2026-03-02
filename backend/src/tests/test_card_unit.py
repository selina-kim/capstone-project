"""Unit tests for CardService.

Tests the card service logic with mocked dependencies:
- URL validation helper
- Deck ownership verification
- Card CRUD operations (create, read, update, delete)
- Deck-level card queries (pagination, review cards)
- MinIO storage operations (skeleton tests)
- TTS generation (skeleton tests)

Run this test file:
    docker compose exec backend pytest src/tests/test_card_unit.py -v

Run with coverage:
    docker compose exec backend pytest src/tests/test_card_unit.py --cov=services.card_service
"""

import pytest
from unittest.mock import patch, MagicMock
from services.card_service import (
    CardService,
    CardNotFoundError,
    DeckNotFoundError,
    UnauthorizedError,
    DatabaseError
)


@pytest.fixture
def card_service():
    """Create CardService instance with mocked MinIO."""
    with patch.object(CardService, '_init_minio'):
        service = CardService()
        service.minio_client = None
        return service


@pytest.fixture
def sample_card_data():
    """Sample card data for testing."""
    return {
        "d_id": 1,
        "word": "hola",
        "translation": "hello",
        "word_roman": "oh-lah",
        "definition": "A greeting",
        "word_example": "Hola, ¿cómo estás?",
        "trans_example": "Hello, how are you?",
        "trans_roman": None,
        "image": None
    }


@pytest.fixture
def sample_card_response():
    """Sample card response from database."""
    return {
        "c_id": 1,
        "d_id": 1,
        "word": "hola",
        "translation": "hello",
        "definition": "A greeting",
        "word_example": "Hola, ¿cómo estás?",
        "trans_example": "Hello, how are you?",
        "word_roman": "oh-lah",
        "trans_roman": None,
        "image": None,
        "word_audio": None,
        "trans_audio": None
    }


class TestIsUrl:
    """Tests for _is_url static method."""
    
    def test_http_url(self):
        assert CardService._is_url("http://example.com/image.jpg") is True
    
    def test_https_url(self):
        assert CardService._is_url("https://example.com/image.jpg") is True
    
    def test_not_url_path(self):
        assert CardService._is_url("/path/to/image.jpg") is False
    
    def test_not_url_empty(self):
        assert CardService._is_url("") is False
    
    def test_not_url_none(self):
        assert CardService._is_url(None) is False
    
    def test_not_url_relative(self):
        assert CardService._is_url("images/photo.jpg") is False


class TestMinIOSkeletons:
    """Skeleton tests for MinIO-dependent methods."""
    # TODO: Implement when MinIO is integrated
    
    def test_download_and_store_image_placeholder(self, card_service):
        """Test image download and storage."""
        # TODO: Implement when MinIO is configured
        # Should download image from URL, upload to MinIO, return object ID
        pass
    
    def test_download_and_store_image_invalid_url(self, card_service):
        """Test with invalid URL returns None."""
        result = card_service._download_and_store_image("not-a-url", 1)
        assert result is None
    
    def test_download_and_store_image_empty(self, card_service):
        """Test with empty URL returns None."""
        result = card_service._download_and_store_image("", 1)
        assert result is None
    
    def test_download_and_store_image_none(self, card_service):
        """Test with None URL returns None."""
        result = card_service._download_and_store_image(None, 1)
        assert result is None
    
    def test_delete_from_minio_empty(self, card_service):
        """Test delete with empty object_id."""
        result = card_service._delete_from_minio("")
        assert result is True
    
    def test_delete_from_minio_none(self, card_service):
        """Test delete with None object_id."""
        result = card_service._delete_from_minio(None)
        assert result is True
    
    def test_delete_from_minio_placeholder(self, card_service):
        """Test actual MinIO deletion."""
        # TODO: Implement when MinIO is configured
        # Should remove object from MinIO bucket
        pass


class TestTTSSkeletons:
    """Skeleton tests for TTS-dependent methods."""
    # TODO: Implement when TTS is integrated
    
    def test_generate_and_store_tts_placeholder(self, card_service):
        """Test TTS generation and storage."""
        # TODO: Implement when TTS service is configured
        # Should generate audio, upload to MinIO, return object ID
        pass
    
    def test_generate_and_store_tts_empty_text(self, card_service):
        """Test TTS with empty text returns None."""
        result = card_service._generate_and_store_tts("", "en", 1, "word")
        assert result is None
    
    def test_generate_and_store_tts_none_text(self, card_service):
        """Test TTS with None text returns None."""
        result = card_service._generate_and_store_tts(None, "en", 1, "word")
        assert result is None


class TestVerifyDeckOwnership:
    """Tests for _verify_deck_ownership helper."""
    
    def test_verify_deck_ownership_success(self, card_service):
        """Test deck ownership verification with valid owner."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"d_id": 1}
        
        with patch('services.card_service.get_db_cursor') as mock_db:
            mock_db.return_value.__enter__.return_value = mock_cursor
            result = card_service._verify_deck_ownership("user-123", 1)
        
        assert result is True
    
    def test_verify_deck_ownership_not_owner(self, card_service):
        """Test deck ownership verification with non-owner."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        with patch('services.card_service.get_db_cursor') as mock_db:
            mock_db.return_value.__enter__.return_value = mock_cursor
            result = card_service._verify_deck_ownership("user-123", 999)
        
        assert result is False


class TestGetDeckInfo:
    """Tests for _get_deck_info helper."""
    
    def test_get_deck_info_found(self, card_service):
        """Test getting deck info for existing deck."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {
            "d_id": 1,
            "deck_name": "Spanish",
            "word_lang": "es",
            "trans_lang": "en"
        }
        
        with patch('services.card_service.get_db_cursor') as mock_db:
            mock_db.return_value.__enter__.return_value = mock_cursor
            result = card_service._get_deck_info(1)
        
        assert result["deck_name"] == "Spanish"
        assert result["word_lang"] == "es"
    
    def test_get_deck_info_not_found(self, card_service):
        """Test getting deck info for non-existent deck."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        with patch('services.card_service.get_db_cursor') as mock_db:
            mock_db.return_value.__enter__.return_value = mock_cursor
            result = card_service._get_deck_info(999)
        
        assert result is None


class TestCreateCard:
    """Tests for create_card method."""
    
    def test_create_card_deck_not_found(self, card_service, sample_card_data):
        """Test card creation fails when deck doesn't exist."""
        with patch.object(card_service, '_verify_deck_ownership', return_value=False):
            with pytest.raises(DeckNotFoundError):
                card_service.create_card("user-123", sample_card_data)
    
    def test_create_card_success(self, card_service, sample_card_data, sample_card_response):
        """Test successful card creation."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = sample_card_response
        
        with patch.object(card_service, '_verify_deck_ownership', return_value=True):
            with patch.object(card_service, '_get_deck_info', return_value={"word_lang": "es", "trans_lang": "en"}):
                with patch('services.card_service.get_db_cursor') as mock_db:
                    mock_db.return_value.__enter__.return_value = mock_cursor
                    result = card_service.create_card("user-123", sample_card_data)
        
        assert result["word"] == "hola"
        assert result["translation"] == "hello"


class TestGetCard:
    """Tests for get_card method."""
    
    def test_get_card_success(self, card_service, sample_card_response):
        """Test successful card retrieval."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = sample_card_response
        
        with patch('services.card_service.get_db_cursor') as mock_db:
            mock_db.return_value.__enter__.return_value = mock_cursor
            result = card_service.get_card("user-123", 1, 1)
        
        assert result["c_id"] == 1
        assert result["word"] == "hola"
    
    def test_get_card_not_found(self, card_service):
        """Test card retrieval when card doesn't exist."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        with patch('services.card_service.get_db_cursor') as mock_db:
            mock_db.return_value.__enter__.return_value = mock_cursor
            result = card_service.get_card("user-123", 999, 1)
        
        assert result is None
    
    def test_get_card_without_deck_id(self, card_service, sample_card_response):
        """Test card retrieval without specifying deck_id."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = sample_card_response
        
        with patch('services.card_service.get_db_cursor') as mock_db:
            mock_db.return_value.__enter__.return_value = mock_cursor
            result = card_service.get_card("user-123", 1)
        
        assert result is not None


class TestUpdateCard:
    """Tests for update_card method."""
    
    def test_update_card_not_found(self, card_service):
        """Test update fails when card doesn't exist."""
        with patch.object(card_service, 'get_card', return_value=None):
            with pytest.raises(CardNotFoundError):
                card_service.update_card("user-123", 999, {"word": "nuevo"})
    
    def test_update_card_no_changes(self, card_service, sample_card_response):
        """Test update with no changes returns current card."""
        with patch.object(card_service, 'get_card', return_value=sample_card_response):
            with patch.object(card_service, '_get_deck_info', return_value={"word_lang": "es", "trans_lang": "en"}):
                result = card_service.update_card("user-123", 1, {})
        
        assert result["word"] == "hola"
    
    def test_update_card_success(self, card_service, sample_card_response):
        """Test successful card update."""
        updated_response = {**sample_card_response, "word": "nuevo"}
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = updated_response
        
        with patch.object(card_service, 'get_card', return_value=sample_card_response):
            with patch.object(card_service, '_get_deck_info', return_value={"word_lang": "es", "trans_lang": "en"}):
                with patch('services.card_service.get_db_cursor') as mock_db:
                    mock_db.return_value.__enter__.return_value = mock_cursor
                    result = card_service.update_card("user-123", 1, {"word": "nuevo"})
        
        assert result["word"] == "nuevo"


class TestDeleteCard:
    """Tests for delete_card method."""
    
    def test_delete_card_not_found(self, card_service):
        """Test delete fails when card doesn't exist."""
        with patch.object(card_service, 'get_card', return_value=None):
            with pytest.raises(CardNotFoundError):
                card_service.delete_card("user-123", 999)
    
    def test_delete_card_success(self, card_service, sample_card_response):
        """Test successful card deletion."""
        mock_cursor = MagicMock()
        
        with patch.object(card_service, 'get_card', return_value=sample_card_response):
            with patch.object(card_service, '_delete_from_minio', return_value=True):
                with patch('services.card_service.get_db_cursor') as mock_db:
                    mock_db.return_value.__enter__.return_value = mock_cursor
                    result = card_service.delete_card("user-123", 1)
        
        assert result is True
    
    def test_delete_card_cleans_up_minio(self, card_service):
        """Test that delete cleans up MinIO objects."""
        card_with_media = {
            "c_id": 1,
            "d_id": 1,
            "word": "test",
            "translation": "test",
            "image": "images/1/test.jpg",
            "word_audio": "audio/1/word.wav",
            "trans_audio": "audio/1/trans.wav"
        }
        
        mock_cursor = MagicMock()
        delete_calls = []
        
        def track_delete(object_id):
            delete_calls.append(object_id)
            return True
        
        with patch.object(card_service, 'get_card', return_value=card_with_media):
            with patch.object(card_service, '_delete_from_minio', side_effect=track_delete):
                with patch('services.card_service.get_db_cursor') as mock_db:
                    mock_db.return_value.__enter__.return_value = mock_cursor
                    card_service.delete_card("user-123", 1)
        
        assert "images/1/test.jpg" in delete_calls
        assert "audio/1/word.wav" in delete_calls
        assert "audio/1/trans.wav" in delete_calls


class TestGetCardsForDeck:
    """Tests for get_cards_for_deck method."""
    
    def test_get_cards_for_deck_unauthorized(self, card_service):
        """Test returns None when user doesn't own deck."""
        with patch.object(card_service, '_verify_deck_ownership', return_value=False):
            result = card_service.get_cards_for_deck("user-123", 999)
        
        assert result is None
    
    def test_get_cards_for_deck_success(self, card_service, sample_card_response):
        """Test successful pagination of cards."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"total": 1}
        mock_cursor.fetchall.return_value = [sample_card_response]
        
        with patch.object(card_service, '_verify_deck_ownership', return_value=True):
            with patch('services.card_service.get_db_cursor') as mock_db:
                mock_db.return_value.__enter__.return_value = mock_cursor
                result = card_service.get_cards_for_deck("user-123", 1)
        
        assert "cards" in result
        assert "pagination" in result
        assert result["pagination"]["total"] == 1
    
    def test_get_cards_for_deck_pagination(self, card_service):
        """Test pagination parameters."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"total": 100}
        mock_cursor.fetchall.return_value = []
        
        with patch.object(card_service, '_verify_deck_ownership', return_value=True):
            with patch('services.card_service.get_db_cursor') as mock_db:
                mock_db.return_value.__enter__.return_value = mock_cursor
                result = card_service.get_cards_for_deck("user-123", 1, page=2, per_page=20)
        
        assert result["pagination"]["page"] == 2
        assert result["pagination"]["per_page"] == 20
        assert result["pagination"]["total_pages"] == 5


class TestGetCardsForReview:
    """Tests for get_cards_for_review method."""
    
    def test_get_cards_for_review_unauthorized(self, card_service):
        """Test returns None when user doesn't own deck."""
        with patch.object(card_service, '_verify_deck_ownership', return_value=False):
            result = card_service.get_cards_for_review("user-123", 999)
        
        assert result is None
    
    def test_get_cards_for_review_success(self, card_service, sample_card_response):
        """Test successful retrieval of due cards."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [sample_card_response]
        
        with patch.object(card_service, '_verify_deck_ownership', return_value=True):
            with patch('services.card_service.get_db_cursor') as mock_db:
                mock_db.return_value.__enter__.return_value = mock_cursor
                result = card_service.get_cards_for_review("user-123", 1)
        
        assert len(result) == 1
    
    def test_get_cards_for_review_exclude_new(self, card_service):
        """Test excluding new cards from review."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        
        with patch.object(card_service, '_verify_deck_ownership', return_value=True):
            with patch('services.card_service.get_db_cursor') as mock_db:
                mock_db.return_value.__enter__.return_value = mock_cursor
                result = card_service.get_cards_for_review("user-123", 1, include_new=False)
        
        assert result == []


class TestGetDecksWithDueCards:
    """Tests for get_decks_with_due_cards method."""
    
    def test_get_decks_with_due_cards_success(self, card_service):
        """Test retrieval of decks with due cards."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"d_id": 1, "deck_name": "Spanish", "due_count": 5, "total_cards": 10}
        ]
        
        with patch('services.card_service.get_db_cursor') as mock_db:
            mock_db.return_value.__enter__.return_value = mock_cursor
            result = card_service.get_decks_with_due_cards("user-123")
        
        assert len(result) == 1
        assert result[0]["due_count"] == 5


class TestGetRecentDecks:
    """Tests for get_recent_decks method."""
    
    def test_get_recent_decks_success(self, card_service):
        """Test retrieval of recently reviewed decks."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"d_id": 1, "deck_name": "Spanish", "card_count": 10}
        ]
        
        with patch('services.card_service.get_db_cursor') as mock_db:
            mock_db.return_value.__enter__.return_value = mock_cursor
            result = card_service.get_recent_decks("user-123")
        
        assert len(result) == 1
    
    def test_get_recent_decks_with_limit(self, card_service):
        """Test limit parameter for recent decks."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        
        with patch('services.card_service.get_db_cursor') as mock_db:
            mock_db.return_value.__enter__.return_value = mock_cursor
            card_service.get_recent_decks("user-123", limit=5)
        
        # Verify the query was called (we check it doesn't error)
        assert mock_cursor.execute.called
