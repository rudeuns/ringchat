import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { LargeLogoDesc } from "@/components/common/Texts";
import AuthForm from "@/components/auth/AuthForm";

export default function RootPage() {
  const accessToken = cookies().get("access_token")?.value;
  if (accessToken) {
    redirect("/main");
  }

  return (
    <div className="flex flex-col h-full">
      <div className="h-topbar" />
      <div className="container-main">
        <LargeLogoDesc />
        <AuthForm />
      </div>
    </div>
  );
}
