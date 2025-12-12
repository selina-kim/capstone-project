import { Stack } from "expo-router";
import { COLORS } from "@/constants/colors";

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: {
          backgroundColor: COLORS.accent.primary,
        },
        headerTintColor: COLORS.text.primary,
        headerShadowVisible: false,
        headerTitle: "Languine",
        contentStyle: {
          backgroundColor: "red",
        },
      }}
    >
      <Stack.Screen name="(tabs)" options={{ headerShown: true }} />
      <Stack.Screen name="(auth)" options={{ headerShown: false }} />
    </Stack>
  );
}
