import { Stack } from "expo-router";
import { COLORS } from "@/constants/colors";
import { AppLogo } from "@/assets/AppLogo";
import { View } from "react-native";
import { ProfileIcon } from "@/assets/icons/ProfileIcon";

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: {
          backgroundColor: COLORS.accent.primary,
        },
        headerTintColor: COLORS.text.primary,
        headerShadowVisible: false,
        headerTitle: () => <AppLogo width={100} />,
        headerRight: () => (
          <View style={{ marginHorizontal: 15 }}>
            <ProfileIcon />
          </View>
        ),
      }}
    >
      <Stack.Screen name="(tabs)" options={{ headerShown: true }} />
      <Stack.Screen name="(auth)" options={{ headerShown: false }} />
    </Stack>
  );
}
