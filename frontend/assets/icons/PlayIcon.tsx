import { COLORS } from "@/constants/colors";
import React from "react";
import Svg, { Path } from "react-native-svg";

export const PlayIcon: React.FC<{
  stroke?: string;
  fill?: string;
}> = ({
  stroke = COLORS.icon.outlinePrimary,
  fill = COLORS.icon.fillPrimary,
}) => (
  <Svg width="16" height="16" viewBox="0 0 16 16" fill="none">
    <Path 
      d="M5 3V17L17 10L7 3H5Z" 
      fill={fill} 
      stroke={fill} 
      stroke-linecap="round"
    />
    <Path 
      d="M4.1655 4.16547C4.16541 3.8723 4.24268 3.58429 4.3895 3.33053C4.53633 3.07677 4.74751 2.86624 5.00172 2.72021C5.25593 2.57417 5.54418 2.49779 5.83735 2.49879C6.13052 2.49978 6.41824 2.57812 6.67146 2.72588L16.6661 8.5559C16.9184 8.70226 17.1278 8.91226 17.2734 9.1649C17.4191 9.41755 17.4959 9.70399 17.4961 9.99561C17.4964 10.2872 17.4201 10.5738 17.2749 10.8267C17.1297 11.0796 16.9206 11.29 16.6686 11L"
      stroke={stroke} 
      stroke-width="1.6662" 
      stroke-linecap="round" 
      stroke-linejoin="round"
    />
  </Svg>
);