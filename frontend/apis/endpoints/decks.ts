import { CreateDeckRequestPayload, Deck } from "@/types/decks";
import client from "@/apis/client";

export const getDecks = (): Promise<{
  data: { decks: Deck[] };
  error: string | null;
}> => client.get(`/decks`);

export const createDeck = (data: CreateDeckRequestPayload) =>
  client.post(`/decks/new`, JSON.stringify(data));

export default { getDecks, createDeck };
