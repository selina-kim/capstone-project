import { CText } from "@/components/common/CText";
import { COLORS } from "@/constants/colors";
import { useState } from "react";
import { Pressable, View } from "react-native";

interface FAQItem {
  question: string;
  answer: string;
}

interface FAQProps {
  faqs: FAQItem[];
}

export const FAQ = ({ faqs }: FAQProps) => {
  const [openIndexes, setOpenIndexes] = useState<number[]>([]);

  const toggle = (index: number) => {
    setOpenIndexes((prev) =>
      prev.includes(index)
        ? prev.filter((i) => i !== index)
        : [...prev, index]
    );
  };

  return (
    <View style={{ width: "100%" }}>
      <View
        style={{
          paddingBottom: 25,
          paddingHorizontal: 25,
        }}
      >
        {faqs.map((item, index) => {
          const isOpen = openIndexes.includes(index);

          return (
            <View
              key={index}
              style={{
                borderBottomWidth: 1,
                borderBottomColor: COLORS.icon.outlinePrimary,
                paddingVertical: 16,
              }}
            >
              <Pressable
                onPress={() => toggle(index)}
                style={{
                  flexDirection: "row",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <CText>{item.question}</CText>

                <CText
                  style={{
                    color: COLORS.text.secondary,
                    fontSize: 18,
                  }}
                >
                  {isOpen ? "−" : "+"}
                </CText>
              </Pressable>

              {isOpen && (
                <View style={{ marginTop: 10 }}>
                  <CText style={{ color: COLORS.text.secondary }}>
                    {item.answer}
                  </CText>
                </View>
              )}
            </View>
          );
        })}
      </View>
    </View>
  );
};