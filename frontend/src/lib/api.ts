import { ErrorCode, fetchServer } from "@/lib/fetch";

export async function fetchEmail({ accessToken }: { accessToken: string }) {
  try {
    const res = await fetchServer("/me", {
      method: "GET",
      headers: {
        Cookie: `access_token=${accessToken}`,
      },
    });

    const result = await res.json();
    if (res.ok) {
      return result.email;
    } else if (res.status == 401) {
      throw new ErrorCode(result.detail, result.code);
    } else {
      return "Failed to load email";
    }
  } catch (error) {
    console.log("Error occurred while fetching email.");
    throw error;
  }
}

export async function fetchFolders({ accessToken }: { accessToken: string }) {
  try {
    const res = await fetchServer("/folders", {
      method: "GET",
      headers: {
        Cookie: `access_token=${accessToken}`,
      },
    });

    const result = await res.json();
    if (res.ok) {
      return result.folders;
    } else {
      throw new ErrorCode(result.detail, result.code);
    }
  } catch (error) {
    console.log("Error occurred while fetching folders.");
    throw error;
  }
}

export async function fetchNoFolderChatRooms({
  accessToken,
}: {
  accessToken: string;
}) {
  try {
    const res = await fetchServer("/chatrooms?folderId=0", {
      method: "GET",
      headers: {
        Cookie: `access_token=${accessToken}`,
      },
    });

    const result = await res.json();
    if (res.ok) {
      return result.chat_rooms;
    } else {
      throw new ErrorCode(result.detail, result.code);
    }
  } catch (error) {
    console.log("Error occurred while fetching chat rooms.");
    throw error;
  }
}
