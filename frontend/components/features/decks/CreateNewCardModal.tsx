import { createDeck } from "@/apis/endpoints/decks";
import { CText } from "@/components/common/CText";
import { CTextInput } from "@/components/common/CTextInput";
import { Modal } from "@/components/common/Modal";
import { useEffect, useState } from "react";
import { View } from "react-native";

interface CreateNewCardModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CreateNewCardModal = ({
  isOpen,
  onClose,
}: CreateNewCardModalProps) => {
  const [deckName, setDeckName] = useState("");
  const [language, setLanguage] = useState<string | null>(null);
  const [description, setDescription] = useState("");

  const [deckNameInputError, setDeckNameInputError] = useState<string>();
  const [languageInputError, setLanguageInputError] = useState<string>();

  const onCreateDeck = async () => {
    setDeckNameInputError(undefined);
    setLanguageInputError(undefined);

    const isDeckNameEmpty = deckName.trim() === "";

    if (isDeckNameEmpty || !language) {
      if (isDeckNameEmpty) {
        setDeckNameInputError("Deck name cannot be empty");
      }

      if (!language) {
        setLanguageInputError("Language must be selected");
      }

      return;
    }

    const { error } = await createDeck({
      deck_name: deckName,
      word_lang: language,
      trans_lang: "en",
      description: description,
      is_public: false,
    });

    if (!error) {
      onClose();
    } else {
      setDeckNameInputError(error);
    }
  };

  useEffect(() => {
    if (!isOpen) {
      setDeckName("");
      setLanguage(null);
      setDescription("");
      setDeckNameInputError(undefined);
      setLanguageInputError(undefined);
    }
  }, [isOpen]);

  return (
    <Modal
      visible={isOpen}
      header="Add New Card"
      subheader="Create a new flashcard for this deck"
      onSubmit={onCreateDeck}
      submitLabel="Create Deck"
      onClose={onClose}
      closeLabel="Cancel"
    >
      <View style={{ gap: 14, marginBottom: 16 }}>
        <CTextInput
          label="Word"
          sublabel="ENGLISH"
          value={deckName}
          onChangeText={setDeckName}
          placeholder="e.g., Spanish Basics"
        />
        {deckNameInputError && (
          <CText variant="inputError">{deckNameInputError}</CText>
        )}
      </View>
    </Modal>
  );
};
