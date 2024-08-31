"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { fetchClient } from "@/lib/fetch";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();

  const handleChangeEmail = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setEmail(value);
  };

  const handleChangePassword = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setPassword(value);
  };

  const handleShowPassword = () => {
    setShowPassword((prevState) => !prevState);
  };

  const handleSubmitForm = async () => {
    if (!email) {
      alert("이메일을 입력해 주세요.");
      return;
    }
    if (!password) {
      alert("비밀번호를 입력해 주세요.");
      return;
    }

    try {
      const res = await fetchClient("/auth/login", {
        method: "POST",
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      if (res.ok) {
        router.push("/main");
        return;
      }

      const result = await res.json();
      switch (result.code) {
        case "INVALID_EMAIL":
          alert(
            "입력하신 이메일로 등록된 계정이 없습니다. 이메일을 다시 확인해 주세요.",
          );
          break;
        case "INVALID_PWD":
          alert("비밀번호가 일치하지 않습니다. 다시 입력해 주세요.");
          break;
        default:
          alert("로그인 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.");
          console.log(`Error occurred while logging in: ${result.code}`);
          break;
      }
    } catch (error) {
      alert(
        "로그인 중 예기치 않은 오류가 발생했습니다. 관리자에게 문의하시거나 잠시 후 다시 시도해 주세요.",
      );
      console.log(`Unexpected error occurred while logging in: ${error}`);
    }
  };

  return (
    <>
      <div className="flex flex-col">
        <input
          className="input-base"
          type="email"
          placeholder="이메일"
          name="email"
          value={email}
          onChange={handleChangeEmail}
        />
        <input
          className="input-base sy-auth-input"
          type={showPassword ? "text" : "password"}
          placeholder="비밀번호"
          name="password"
          value={password}
          onChange={handleChangePassword}
          autoComplete="off"
        />
        <div className="container-check-visible">
          <input
            type="checkbox"
            id="show-password"
            checked={showPassword}
            onChange={handleShowPassword}
          />
          <label className="text-sm" htmlFor="show-password">
            비밀번호 표시
          </label>
        </div>
      </div>
      <button className="btn-fill" onClick={handleSubmitForm}>
        로그인
      </button>
    </>
  );
}
