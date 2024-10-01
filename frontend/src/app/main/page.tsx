import { LargeLogoDesc } from "@/components/common/Texts";
import LinkModalNav from "@/components/link/LinkModalNav";
import LinkForm from "@/components/link/LinkForm";

export default function MainPage() {
  return (
    <div className="container-main">
      <LargeLogoDesc />
      <div className="relative flex flex-col self-center w-2/3 min-w-[32rem]">
        <LinkModalNav />
        <LinkForm />
      </div>
    </div>
  );
}
