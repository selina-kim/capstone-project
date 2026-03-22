import { EditIcon } from "@/assets/icons/EditIcon";
import { TrashIcon } from "@/assets/icons/TrashIcon";
import { CText } from "@/components/common/CText";
import { COLORS } from "@/constants/colors";
import { Card } from "@/types/decks";
import { Pressable, View } from "react-native";

export const CardsList = ({ cards }: { cards: Card[] }) => {
  const CardButtons = () => (
    <View
      style={{
        position: "absolute",
        top: 20,
        right: 20,
        display: "flex",
        flexDirection: "row",
        columnGap: 20,
      }}
    >
      <Pressable
        style={{
          padding: 1,
          width: 20,
          height: 20,
        }}
        onPress={() => console.log("edit clicked")} // TODO
      >
        <EditIcon />
      </Pressable>
      <Pressable
        style={{
          width: 20,
          height: 20,
        }}
        onPress={() => console.log("delete clicked")} // TODO
      >
        <TrashIcon />
      </Pressable>
    </View>
  );

  return (
    <View
      style={{
        width: "100%",
        rowGap: 15,
      }}
    >
      {cards.map((card) => (
        <View
          key={`card_${card.c_id}`}
          style={{
            padding: 20,
            borderRadius: 14,
            borderColor: COLORS.text.primary,
            borderWidth: 2,
            width: "100%",
          }}
        >
          <View
            style={{
              width: "100%",
              display: "flex",
              paddingBottom: 16,
              marginBottom: 16,
              borderBottomColor: COLORS.text.secondary,
              borderBottomWidth: 1,
            }}
          >
            <CText
              style={{
                color: COLORS.text.secondary,
                marginBottom: 4,
              }}
              bold
            >
              Front
            </CText>
            <CText>{card.word}</CText>
            {card.word_example && (
              <CText
                style={{
                  marginTop: 14,
                }}
              >
                {card.word_example}
              </CText>
            )}
          </View>
          <View
            style={{
              width: "100%",
              display: "flex",
            }}
          >
            <CText
              style={{
                color: COLORS.text.secondary,
                marginBottom: 4,
              }}
              bold
            >
              Back
            </CText>
            <CText>{card.translation}</CText>
            {card.word_example && (
              <CText
                style={{
                  marginTop: 14,
                }}
              >
                {card.trans_example}
              </CText>
            )}
          </View>
          <CardButtons />
        </View>
      ))}
    </View>
  );
};
