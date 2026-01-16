import { DecksIcon } from "@/assets/icons/DecksIcon";
import { PlusIcon } from "@/assets/icons/PlusIcon";
import { COLORS } from "@/constants/colors";
import { Pressable, Text, View } from "react-native";

export const NoDecksBanner = () => (
  <View style={{ width: "100%", height: "100%" }}>
    <View
      style={{
        display: "flex",
        rowGap: "10px",
        paddingVertical: 30,
      }}
    >
      <View style={{ width: 64, marginHorizontal: "auto" }}>
        <DecksIcon />
      </View>
      <Text
        style={{
          color: COLORS.text.primary,
          fontWeight: "bold",
          textAlign: "center",
        }}
      >
        No Decks Yet
      </Text>
      <Text style={{ color: COLORS.text.secondary, textAlign: "center" }}>
        Create your first deck to start learning!
      </Text>
      <Pressable
        style={{
          backgroundColor: COLORS.accent.primary,
          padding: 10,
          borderRadius: 8,
          display: "flex",
          flexDirection: "row",
          marginHorizontal: "auto",
          marginTop: 20,
          columnGap: 5,
          alignItems: "center",
        }}
      >
        <View style={{ minWidth: "auto" }}>
          <PlusIcon />
        </View>
        <Text
          style={{
            color: COLORS.text.primary,
            fontWeight: "bold",
            textAlign: "center",
            width: "100%",
          }}
        >
          Create Your First Deck
        </Text>
      </Pressable>
    </View>
  </View>
);
