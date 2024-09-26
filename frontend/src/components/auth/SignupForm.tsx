"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { fetchClient } from "@/lib/fetch";

export default function SignupForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
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

  const handleChangeConfirmPassword = (
    e: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const { value } = e.target;
    setConfirmPassword(value);
  };

  const handleShowPassword = () => {
    setShowPassword((prevState) => !prevState);
  };

  const handleSubmitForm = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!email) {
      alert("이메일을 입력해 주세요.");
      return;
    }
    if (!emailRegex.test(email)) {
      alert("이메일 형식이 올바르지 않습니다. 다시 입력해 주세요.");
      return;
    }
    if (!password) {
      alert("비밀번호를 입력해 주세요.");
      return;
    }
    if (password !== confirmPassword) {
      alert("비밀번호가 일치하지 않습니다. 다시 입력해 주세요.");
      return;
    }

    try {
      const res = await fetchClient("/auth/signup", {
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
        case "EMAIL_EXISTS":
          alert("이미 사용 중인 이메일입니다. 다른 이메일을 사용해 주세요.");
          break;
        case "TOKEN_CREATE_ERROR":
          alert("회원가입이 완료되었습니다. 다시 로그인해 주세요.");
          window.location.reload();
          break;
        default:
          alert("회원가입 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.");
          break;
      }
    } catch (error) {
      alert(
        "회원가입 중 예기치 않은 오류가 발생했습니다. 관리자에게 문의하시거나 잠시 후 다시 시도해 주세요.",
      );
      console.log(`Unexpected error occurred while signing up: ${error}`);
    }
  };

  return (
    <form className="flex flex-col" onSubmit={handleSubmitForm}>
      <div className="flex flex-col">
        <input
          className="input-base"
          type="email"
          placeholder="이메일"
          name="email"
          value={email}
          onChange={handleChangeEmail}
          autoComplete="off"
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
        <input
          className="input-base sy-auth-input"
          type={showPassword ? "text" : "password"}
          placeholder="비밀번호 확인"
          name="confirmPassword"
          value={confirmPassword}
          onChange={handleChangeConfirmPassword}
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
      <button className="btn-fill sy-auth-input" type="submit">
        회원가입
      </button>
    </form>
  );
}