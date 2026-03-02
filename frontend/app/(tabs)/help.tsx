import { DecksIcon } from "@/assets/icons/DecksIcon";
import { PlusFilledIcon } from "@/assets/icons/PlusFilledIcon";
import { PlayIcon } from "@/assets/icons/PlayIcon";
import { OpenBookIcon } from "@/assets/icons/OpenBookIcon";
import { CText } from "@/components/common/CText";
import { InfoContainer} from "@/components/features/help/InfoContainer";
import { StepContainer} from "@/components/features/help/StepContainer";
import { TipsContainer } from "@/components/features/help/TipsContainer";
import { FAQ } from "@/components/features/help/FAQ";
import { ScrollView } from "react-native";

type LabelProps = {
  text: string;
}

const Label = ({ text }: LabelProps) => (
  <CText
    style={{
      textAlign: "left",
      paddingHorizontal: 25,
      paddingTop: 25,
      paddingBottom: 5,
    }}
    bold
  >
    {text}
  </CText>
);

const FAQ_DATA = [
  {
    question: "What is spaced repetition?",
    answer: "Spaced repetition is a learning technique that involves reviewing information at increasing intervals to improve long-term retention.",
  },
  {
    question: "How should I rate my answers?",
    answer: "Rate your answer based on how easily you were able to recall the information:\n\nEasy: you recalled it effortlessly\nGood: you recalled it with some effort\nHard: you recall it with difficulty\nAgain: you could not recall it at all",
  },
  {
    question: "How many cards should I add to a deck?",
    answer: "As many as you want!\n\nIt is recommended to add 5-10 cards per day to avoid overwhelming yourself during reviews.\n\nConsistency is key, so find a pace that works for you and stick to it.",
  },
  {
    question: "How often should I review?",
    answer: "Daily review is recommended. The system will space cards automatically for optimal retention.",
  },
  {
    question: "Can I edit cards after creating them?",
    answer: "Yes. You can edit or delete cards at any time.\n\nTo edit or delete a card, go to the deck page, view the deck that contains card you want to edit, locate the card, and then select the edit or delete icon.",
  },
];

export default function Help() {
  return (
    <ScrollView
      style={{
        flex: 1,
        padding: 10,
      }}
    >
      <InfoContainer />
      <Label text="Getting Started" />
      <StepContainer
        title="Create a Deck"
        step="Step 1"
        description="Start by creating a new deck for the language you want to learn. Choose a name, select your target language, and add a description."
        Icon={DecksIcon}
        iconStyle={{
          transform: [{ scale: 0.8 }],
        }}
      />
      <StepContainer
        title="Add Cards"
        step="Step 2"
        description="Add flashcards to your deck. The front will hold the word in your target language, and the back will hold the translation."
        Icon={PlusFilledIcon}
        iconStyle={{
          marginTop: 12,
          marginLeft: 12,
          transform: [{ scale: 1.3 }],
        }}
      />
      <StepContainer
        title="Start Reviewing"
        step="Step 3"
        description="Begin your review session. Look at each card's content, try to remember the translation, then flip the card to check."
        Icon={PlayIcon}
        iconStyle={{
          transform: [{ scale: 1.6 }],
        }}
      />
      <StepContainer
        title="Rate Your Memory"
        step="Step 4"
        description="After checking the translation, rate how easily you remembered it. This helps the algorithm schedule the card's next appearance."
        Icon={OpenBookIcon}
        iconStyle={{
          marginTop: 4,
          transform: [{ scale: 0.7 }],
        }}
      />
      <Label text="Frequently Asked Questions" />
      <FAQ faqs={FAQ_DATA} />
      <TipsContainer
        tips={[
          {
            title: "Be consistent:",
            description: "Review daily, even if just for a few minutes.",
          },
          {
            title: "Stay honest:",
            description: "Rate your answers accurately for the algorithm to work effectively.",
          },
          {
            title: "Add context:",
            description: "Include example sentences or images to make cards more memorable.",
          },
          {
            title: "Keep it simple",
            description: "One concept per card words best for effective learning.",
          },
          {
            title: "Review before bed:",
            description: "Sleep helps consolidate memories, so reviewing before sleep can enhance retention.",
          },
        ]}
      />
    </ScrollView>
  );
}
