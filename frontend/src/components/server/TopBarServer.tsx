import { cookies } from "next/headers";
import { fetchServer } from "@/lib/fetch";
import TopBar from "@/components/topbar/TopBar";

export default async function TopBarServer() {
  let email: string;

  try {
    const accessToken = cookies().get("access_token");
    if (!accessToken) {
      return null;
    }

    const res = await fetchServer("/user/email", {
      method: "GET",
      headers: {
        Cookie: `access_token=${accessToken.value}`,
      },
    });

    const result = await res.json();
    if (res.ok) {
      email = result.data.email;
    } else {
      console.log(`Error occurred while fetching user email: ${result.code}`);
      return null;
    }
  } catch {
    throw new Error("Unexpected error occurred while fetching user email.");
  }

  return <TopBar email={email} />;
}
