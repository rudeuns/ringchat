import { PiSpinnerGapBold } from "react-icons/pi";

export default function LoadingRootPage() {
  return (
    <div className="flex flex-center w-full h-full">
      <PiSpinnerGapBold className="icon-base size-8 text-primary animate-spin" />
    </div>
  );
}