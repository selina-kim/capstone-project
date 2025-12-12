const lightTheme = {
  background: "#FFFCF9",
  icon: {
    outlinePrimary: "#8D481C",
    outlineSecondary: "#FFBA26",
    fillPrimary: "#FFFCF9",
    fillSecondary: "#FFF5DB",
  },
  text: {
    primary: "#5C2C0E",
    secondary: "#8D481C",
  },
  accent: {
    primary: "#FFBA26",
    secondary: "#399BEB",
    delete: "#D41605",
  },
} as const;

export const THEMES = {
  light: lightTheme,
} as const;

// temporary for now
export const COLORS = THEMES.light;
