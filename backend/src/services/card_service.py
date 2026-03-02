"""
Card service - handles card CRUD and media storage (MinIO).
"""

import os
import uuid
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from db import get_db_cursor
import psycopg2


class CardNotFoundError(Exception):
    pass


class DeckNotFoundError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class DatabaseError(Exception):
    pass


class MinIOError(Exception):
    pass


class CardService:
    
    def __init__(self):
        self.minio_client = None
        self.bucket_name = os.getenv("MINIO_BUCKET", "flashcards")
        self._init_minio()
    
    def _init_minio(self):
        """
        TODO: Set up MinIO client
        Env vars: MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET
        """
        # Skeleton: MinIO initialization
        # from minio import Minio
        # 
        # try:
        #     self.minio_client = Minio(
        #         os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        #         access_key=os.getenv("MINIO_ACCESS_KEY"),
        #         secret_key=os.getenv("MINIO_SECRET_KEY"),
        #         secure=os.getenv("MINIO_SECURE", "false").lower() == "true"
        #     )
        #     
        #     # Ensure bucket exists
        #     if not self.minio_client.bucket_exists(self.bucket_name):
        #         self.minio_client.make_bucket(self.bucket_name)
        # except Exception as e:
        #     print(f"Warning: MinIO initialization failed: {e}")
        #     self.minio_client = None
        pass
    
    # ==================== MinIO Storage ====================
    
    def _download_and_store_image(self, image_url: str, card_id: int) -> Optional[str]:
        """
        Download image from URL, store in MinIO, return object ID.
        TODO: Implement actual MinIO upload
        """
        # Skeleton implementation
        if not image_url or not self._is_url(image_url):
            return None
        
        try:
            # Step 1: Download image from URL
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            image_data = response.content
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            
            # Determine file extension from content type
            ext_map = {
                'image/jpeg': 'jpg',
                'image/png': 'png',
                'image/gif': 'gif',
                'image/webp': 'webp'
            }
            extension = ext_map.get(content_type, 'jpg')
            
            # Step 2: Generate unique object ID
            object_id = f"images/{card_id}/{uuid.uuid4()}.{extension}"
            
            # Step 3: Upload to MinIO
            # TODO: Implement actual MinIO upload
            # from io import BytesIO
            # self.minio_client.put_object(
            #     self.bucket_name,
            #     object_id,
            #     BytesIO(image_data),
            #     length=len(image_data),
            #     content_type=content_type
            # )
            
            # For now, return the object_id as placeholder
            # In production, this would only return after successful MinIO upload
            print(f"[Skeleton] Would store image at: {object_id}")
            return object_id
            
        except Exception as e:
            print(f"Failed to download/store image: {e}")
            return None
    
    def _delete_from_minio(self, object_id: str) -> bool:
        """Delete object from MinIO. TODO: Implement actual deletion."""
        if not object_id:
            return True
        
        try:
            # TODO: Implement actual MinIO deletion
            # self.minio_client.remove_object(self.bucket_name, object_id)
            print(f"[Skeleton] Would delete from MinIO: {object_id}")
            return True
        except Exception as e:
            print(f"Failed to delete from MinIO: {e}")
            return False
    
    def _generate_and_store_tts(
        self, 
        text: str, 
        language: str, 
        card_id: int, 
        field_type: str = "word"
    ) -> Optional[str]:
        """
        Generate TTS audio, store in MinIO, return object ID.
        TODO: Implement TTS generation and MinIO upload
        """
        if not text:
            return None
        
        try:
            # Step 1: Generate TTS audio
            # TODO: Import and use TTSService
            # from services.tts_service import TTSService
            # tts_service = TTSService()
            # audio_data = tts_service.generate_speech(text, language)
            
            # Step 2: Generate unique object ID
            object_id = f"audio/{card_id}/{field_type}_{uuid.uuid4()}.wav"
            
            # Step 3: Upload to MinIO
            # TODO: Implement actual MinIO upload
            # from io import BytesIO
            # from scipy.io import wavfile
            # 
            # buffer = BytesIO()
            # wavfile.write(buffer, 22050, audio_data)
            # buffer.seek(0)
            # 
            # self.minio_client.put_object(
            #     self.bucket_name,
            #     object_id,
            #     buffer,
            #     length=buffer.getbuffer().nbytes,
            #     content_type='audio/wav'
            # )
            
            print(f"[Skeleton] Would generate TTS and store at: {object_id}")
            return object_id
            
        except Exception as e:
            print(f"Failed to generate/store TTS: {e}")
            return None
    
    @staticmethod
    def _is_url(value: str) -> bool:
        if not value:
            return False
        return value.startswith(('http://', 'https://'))
    
    # ==================== Card CRUD ====================
    
    def create_card(self, user_id: str, card_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new card. Auto-generates TTS if word_audio/trans_audio not provided.
        Downloads and stores image if URL is provided.
        """
        deck_id = card_data.get("d_id")
        
        if not self._verify_deck_ownership(user_id, deck_id):
            raise DeckNotFoundError("Deck not found or access denied")
        
        deck_info = self._get_deck_info(deck_id)
        word_lang = deck_info.get("word_lang", "en") if deck_info else "en"
        trans_lang = deck_info.get("trans_lang", "en") if deck_info else "en"
        
        # Create card first to get c_id, then handle image/TTS
        
        try:
            with get_db_cursor(commit=True) as cursor:
                # Insert card without image/audio first
                cursor.execute(
                    """
                    INSERT INTO Cards (
                        d_id, word, translation, definition, word_example,
                        trans_example, word_roman, trans_roman
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING c_id, d_id, word, translation, definition,
                              word_example, trans_example, word_roman, trans_roman,
                              image, word_audio, trans_audio
                    """,
                    (
                        deck_id,
                        card_data.get("word", "").strip(),
                        card_data.get("translation", "").strip(),
                        card_data.get("definition", "").strip() or None,
                        card_data.get("word_example", "").strip() or None,
                        card_data.get("trans_example", "").strip() or None,
                        card_data.get("word_roman", "").strip(),
                        card_data.get("trans_roman", "").strip() or None
                    )
                )
                card = dict(cursor.fetchone())
                card_id = card["c_id"]
        
        except psycopg2.Error as e:
            raise DatabaseError(f"Failed to create card: {str(e)}")
        
        image_object_id = None
        word_audio_id = None
        trans_audio_id = None
        
        # Download and store image if URL provided
        image_url = card_data.get("image")
        if image_url and self._is_url(image_url):
            image_object_id = self._download_and_store_image(image_url, card_id)
        
        # Generate TTS if not provided
        if not card_data.get("word_audio"):
            word_audio_id = self._generate_and_store_tts(
                card_data.get("word", ""),
                word_lang,
                card_id,
                "word"
            )
        if not card_data.get("trans_audio"):
            trans_audio_id = self._generate_and_store_tts(
                card_data.get("translation", ""),
                trans_lang,
                card_id,
                "translation"
            )
        
        # Update card with generated media object IDs
        if any([image_object_id, word_audio_id, trans_audio_id]):
            try:
                with get_db_cursor(commit=True) as cursor:
                    cursor.execute(
                        """
                        UPDATE Cards
                        SET image = COALESCE(%s, image),
                            word_audio = COALESCE(%s, word_audio),
                            trans_audio = COALESCE(%s, trans_audio)
                        WHERE c_id = %s
                        RETURNING c_id, d_id, word, translation, definition,
                                  word_example, trans_example, word_roman, trans_roman,
                                  image, word_audio, trans_audio
                        """,
                        (image_object_id, word_audio_id, trans_audio_id, card_id)
                    )
                    card = dict(cursor.fetchone())
            except psycopg2.Error as e:
                print(f"Warning: Media storage update failed: {e}")
        
        return card
    
    def get_card(self, user_id: str, card_id: int, deck_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Get card by ID. Returns None if not found or unauthorized."""
        with get_db_cursor() as cursor:
            if deck_id:
                cursor.execute(
                    """
                    SELECT c.c_id, c.d_id, c.word, c.translation, c.definition,
                           c.image, c.word_example, c.trans_example,
                           c.word_audio, c.trans_audio, c.word_roman, c.trans_roman,
                           c.learning_state, c.step, c.difficulty, c.stability,
                           c.due_date, c.last_review, c.successful_reps, c.fail_count
                    FROM Cards c
                    JOIN Decks d ON c.d_id = d.d_id
                    WHERE c.c_id = %s AND c.d_id = %s AND d.u_id = %s
                    """,
                    (card_id, deck_id, user_id)
                )
            else:
                cursor.execute(
                    """
                    SELECT c.c_id, c.d_id, c.word, c.translation, c.definition,
                           c.image, c.word_example, c.trans_example,
                           c.word_audio, c.trans_audio, c.word_roman, c.trans_roman,
                           c.learning_state, c.step, c.difficulty, c.stability,
                           c.due_date, c.last_review, c.successful_reps, c.fail_count
                    FROM Cards c
                    JOIN Decks d ON c.d_id = d.d_id
                    WHERE c.c_id = %s AND d.u_id = %s
                    """,
                    (card_id, user_id)
                )
            card = cursor.fetchone()
            
            return dict(card) if card else None
    
    def update_card(self, user_id: str, card_id: int, update_data: Dict[str, Any], deck_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Update card fields. Re-downloads image if URL changes.
        Regenerates TTS if word/translation changes.
        """
        current_card = self.get_card(user_id, card_id, deck_id)
        if not current_card:
            raise CardNotFoundError("Card not found or access denied")
        
        deck_id = current_card["d_id"]
        deck_info = self._get_deck_info(deck_id)
        word_lang = deck_info.get("word_lang", "en") if deck_info else "en"
        trans_lang = deck_info.get("trans_lang", "en") if deck_info else "en"
        
        # Handle image - delete old, download new if URL
        new_image_id = None
        image_value = update_data.get("image")
        if image_value and self._is_url(image_value):
            old_image_id = current_card.get("image")
            if old_image_id:
                self._delete_from_minio(old_image_id)
            new_image_id = self._download_and_store_image(image_value, card_id)
        
        new_word_audio = None
        new_trans_audio = None
        new_word = update_data.get("word", "").strip()
        new_translation = update_data.get("translation", "").strip()
        
        # Regenerate TTS if text changed
        if new_word and new_word != current_card.get("word"):
            old_audio_id = current_card.get("word_audio")
            if old_audio_id:
                self._delete_from_minio(old_audio_id)
            new_word_audio = self._generate_and_store_tts(new_word, word_lang, card_id, "word")
        
        if new_translation and new_translation != current_card.get("translation"):
            old_audio_id = current_card.get("trans_audio")
            if old_audio_id:
                self._delete_from_minio(old_audio_id)
            new_trans_audio = self._generate_and_store_tts(new_translation, trans_lang, card_id, "translation")
        
        updates = []
        params = []
        
        field_mapping = {
            "word": "word",
            "translation": "translation",
            "definition": "definition",
            "word_example": "word_example",
            "trans_example": "trans_example",
            "word_roman": "word_roman",
            "trans_roman": "trans_roman"
        }
        
        for data_key, db_col in field_mapping.items():
            if data_key in update_data:
                updates.append(f"{db_col} = %s")
                params.append(update_data[data_key].strip() if update_data[data_key] else None)
        
        if new_image_id:
            updates.append("image = %s")
            params.append(new_image_id)
        
        if new_word_audio:
            updates.append("word_audio = %s")
            params.append(new_word_audio)
        
        if new_trans_audio:
            updates.append("trans_audio = %s")
            params.append(new_trans_audio)
        
        if not updates:
            return current_card  # Nothing to update
        
        params.append(card_id)
        
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    f"""
                    UPDATE Cards
                    SET {", ".join(updates)}
                    WHERE c_id = %s
                    RETURNING c_id, d_id, word, translation, definition,
                              word_example, trans_example, word_roman, trans_roman,
                              image, word_audio, trans_audio, learning_state,
                              difficulty, stability, due_date
                    """,
                    tuple(params)
                )
                card = cursor.fetchone()
                return dict(card)
        
        except psycopg2.Error as e:
            raise DatabaseError(f"Failed to update card: {str(e)}")
    
    def delete_card(self, user_id: str, card_id: int, deck_id: Optional[int] = None) -> bool:
        """Delete card and its MinIO objects (image, audio)."""
        card = self.get_card(user_id, card_id, deck_id)
        if not card:
            raise CardNotFoundError("Card not found or access denied")
        
        # Clean up MinIO
        if card.get("image"):
            self._delete_from_minio(card["image"])
        if card.get("word_audio"):
            self._delete_from_minio(card["word_audio"])
        if card.get("trans_audio"):
            self._delete_from_minio(card["trans_audio"])
        
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    """
                    DELETE FROM Cards
                    WHERE c_id = %s
                    """,
                    (card_id,)
                )
                return True
        
        except psycopg2.Error as e:
            raise DatabaseError(f"Failed to delete card: {str(e)}")
    
    # ==================== Deck-level Queries ====================
    
    def get_cards_for_deck(
        self, 
        user_id: str, 
        deck_id: int, 
        page: int = 1, 
        per_page: int = 50
    ) -> Optional[Dict[str, Any]]:
        """Get paginated cards for a deck."""
        if not self._verify_deck_ownership(user_id, deck_id):
            return None
        
        offset = (page - 1) * per_page
        
        with get_db_cursor() as cursor:
            # Get total count
            cursor.execute(
                "SELECT COUNT(*) as total FROM Cards WHERE d_id = %s",
                (deck_id,)
            )
            total = cursor.fetchone()["total"]
            
            cursor.execute(
                """
                SELECT c_id, d_id, word, translation, definition,
                       image, word_example, trans_example,
                       word_audio, trans_audio, word_roman, trans_roman,
                       learning_state, step, difficulty, stability,
                       due_date, last_review, successful_reps, fail_count
                FROM Cards
                WHERE d_id = %s
                ORDER BY c_id
                LIMIT %s OFFSET %s
                """,
                (deck_id, per_page, offset)
            )
            cards = cursor.fetchall()
            
            return {
                "cards": [dict(card) for card in cards],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "total_pages": (total + per_page - 1) // per_page
                }
            }
    
    def get_cards_for_review(
        self, 
        user_id: str, 
        deck_id: int, 
        limit: int = 20,
        include_new: bool = True
    ) -> Optional[List[Dict[str, Any]]]:
        """Get cards due for review (due_date <= now or new cards)."""
        if not self._verify_deck_ownership(user_id, deck_id):
            return None
        
        now = datetime.now(timezone.utc)
        
        with get_db_cursor() as cursor:
            if include_new:
                cursor.execute(
                    """
                    SELECT c_id, d_id, word, translation, definition,
                           image, word_example, trans_example,
                           word_audio, trans_audio, word_roman, trans_roman,
                           learning_state, step, difficulty, stability,
                           due_date, last_review, successful_reps, fail_count
                    FROM Cards
                    WHERE d_id = %s
                      AND (due_date IS NULL OR due_date <= %s)
                    ORDER BY 
                        CASE WHEN due_date IS NULL THEN 1 ELSE 0 END,
                        due_date ASC
                    LIMIT %s
                    """,
                    (deck_id, now, limit)
                )
            else:
                cursor.execute(
                    """
                    SELECT c_id, d_id, word, translation, definition,
                           image, word_example, trans_example,
                           word_audio, trans_audio, word_roman, trans_roman,
                           learning_state, step, difficulty, stability,
                           due_date, last_review, successful_reps, fail_count
                    FROM Cards
                    WHERE d_id = %s
                      AND due_date IS NOT NULL
                      AND due_date <= %s
                    ORDER BY due_date ASC
                    LIMIT %s
                    """,
                    (deck_id, now, limit)
                )
            
            cards = cursor.fetchall()
            return [dict(card) for card in cards]
    
    def get_decks_with_due_cards(self, user_id: str) -> List[Dict[str, Any]]:
        """Get decks that have cards needing review."""
        now = datetime.now(timezone.utc)
        
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT d.d_id, d.deck_name, d.word_lang, d.trans_lang,
                       d.last_reviewed,
                       COUNT(CASE WHEN c.due_date IS NULL OR c.due_date <= %s THEN 1 END) as due_count,
                       COUNT(c.c_id) as total_cards
                FROM Decks d
                LEFT JOIN Cards c ON d.d_id = c.d_id
                WHERE d.u_id = %s
                GROUP BY d.d_id, d.deck_name, d.word_lang, d.trans_lang, d.last_reviewed
                HAVING COUNT(CASE WHEN c.due_date IS NULL OR c.due_date <= %s THEN 1 END) > 0
                ORDER BY due_count DESC
                """,
                (now, user_id, now)
            )
            decks = cursor.fetchall()
            return [dict(deck) for deck in decks]
    
    def get_recent_decks(self, user_id: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Get most recently reviewed decks."""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT d.d_id, d.deck_name, d.word_lang, d.trans_lang,
                       d.description, d.last_reviewed,
                       COUNT(c.c_id) as card_count
                FROM Decks d
                LEFT JOIN Cards c ON d.d_id = c.d_id
                WHERE d.u_id = %s AND d.last_reviewed IS NOT NULL
                GROUP BY d.d_id, d.deck_name, d.word_lang, d.trans_lang,
                         d.description, d.last_reviewed
                ORDER BY d.last_reviewed DESC
                LIMIT %s
                """,
                (user_id, limit)
            )
            decks = cursor.fetchall()
            return [dict(deck) for deck in decks]
    
    # ==================== Helpers ====================
    
    def _verify_deck_ownership(self, user_id: str, deck_id: int) -> bool:
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT d_id FROM Decks WHERE d_id = %s AND u_id = %s",
                (deck_id, user_id)
            )
            return cursor.fetchone() is not None
    
    def _get_deck_info(self, deck_id: int) -> Optional[Dict[str, Any]]:
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT d_id, deck_name, word_lang, trans_lang
                FROM Decks
                WHERE d_id = %s
                """,
                (deck_id,)
            )
            deck = cursor.fetchone()
            return dict(deck) if deck else None
