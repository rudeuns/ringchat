import { PiSpinnerGapBold } from "react-icons/pi";

export default function LoadingMainPage() {
  return (
    <div className="flex flex-center flex-1">
      <PiSpinnerGapBold className="icon-base size-8 text-primary animate-spin" />
    </div>
  );
}
