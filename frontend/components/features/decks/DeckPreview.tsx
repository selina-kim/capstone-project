import { CButton } from "@/components/common/CButton";
import { CText } from "@/components/common/CText";
import { COLORS } from "@/constants/colors";
import { View } from "react-native";

interface DeckPreviewProps {
  deckName: string;
  description?: string;
  language: string;
  cardCount: number;
  onReview: () => void;
}

export const DeckPreview = ({
  deckName,
  description,
  language,
  cardCount,
  onReview,
}: DeckPreviewProps) => {
  const hasDescription = description && description.trim() !== "";

  return (
    <View
      style={{
        padding: 20,
        borderColor: COLORS.text.primary,
        borderWidth: 2,
        borderRadius: 14,
        width: "100%",
        backgroundColor: COLORS.background.secondary,
      }}
    >
      <CText
        style={{
          fontSize: 22,
          lineHeight: 28,
        }}
        bold
      >
        {deckName}
      </CText>
      <CText
        style={{ color: COLORS.text.language, fontSize: 16, lineHeight: 24 }}
        special
      >
        {language.toUpperCase()}
      </CText>
      {hasDescription && (
        <CText
          style={{
            marginTop: 15,
          }}
        >
          {description}
        </CText>
      )}
      <CText
        style={{
          marginTop: 15,
          marginBottom: 15,
        }}
      >
        {cardCount} cards
      </CText>
      <CButton onPress={onReview} variant="primary" label="View Deck" />
    </View>
  );
};
