import { CText } from "@/components/common/CText";
import { COLORS } from "@/constants/colors";
import { RelativePathString, useRouter } from "expo-router";
import { useState } from "react";
import { Pressable, View } from "react-native";

type RouteButtonProps = {
  text: string;
  route: "index" | "decks" | "revision" | "help" | "settings";
};

export const RouteButton = ({ text, route }: RouteButtonProps) => {
  const router = useRouter();
  const [modalVisible, setModalVisible] = useState(false);

  const buildRoute = (page: string): RelativePathString => {
    return `${page}` as RelativePathString;
  };

  return (
    <View style={{ width: "100%", height: "100%" }}>
      <View
        style={{
          display: "flex",
          rowGap: "10px",
        }}
      >
        <Pressable
          onPress={() => router.push(buildRoute(route))}
          style={{
            backgroundColor: COLORS.accent.primary,
            padding: 10,
            borderRadius: 8,
            display: "flex",
            flexDirection: "row",
            marginTop: 20,
            columnGap: 5,
            alignItems: "center",
          }}
        >
          <CText
            style={{
              textAlign: "center",
              width: "100%",
            }}
            bold
          >
            {text}
          </CText>
        </Pressable>
      </View>
    </View>
  );
};
