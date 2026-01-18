import { Modal } from "@/components/common/Modal";
import { Text } from "react-native";

interface CreateNewDeckModalProps {
  visible: boolean;
  onClose: () => void;
}

export const CreateNewDeckModal = ({
  visible,
  onClose,
}: CreateNewDeckModalProps) => {
  const onCreateDeck = () => {};

  return (
    <Modal
      visible={visible}
      header="Create New Deck"
      subheader="Add a new flashcard deck for language learning"
      onSubmit={onCreateDeck}
      submitLabel="Create Deck"
      onClose={onClose}
      closeLabel="Cancel"
    >
      <Text>Content TODO</Text>
    </Modal>
  );
};
