export interface Deck {
  card_count: number;
  creation_date: string;
  d_id: string;
  deck_name: string;
  description?: string;
  is_public: boolean;
  last_reviewed: string | null;
  trans_lang: string;
  word_lang: string;
}

export interface CreateDeckRequestPayload {
  deck_name: string;
  word_lang: string;
  trans_lang: string;
  description?: string;
  is_public?: boolean;
  link?: string;
}
