"use client";

import { useState } from "react";
import LoginForm from "@/components/auth/LoginForm";
import SignupForm from "@/components/auth/SignupForm";

export default function AuthForm() {
  const [showLoginForm, setShowLoginForm] = useState(true);
  const [showSignupForm, setShowSignupForm] = useState(false);

  const handleShowLoginForm = () => {
    setShowLoginForm(true);
    setShowSignupForm(false);
  };

  const handleShowSignupForm = () => {
    setShowSignupForm(true);
    setShowLoginForm(false);
  };

  // TODO: 비밀번호 찾기 구현
  const handleFindPassword = () => {};

  return (
    <div className="flex flex-col self-center w-[32rem] space-y-8 px-12 py-5 rounded-lg shadow-lg">
      <div className="flex flex-row divide-x-2 divide-muted">
        <button
          className={showLoginForm ? "btn-auth-active" : "btn-auth-inactive"}
          onClick={handleShowLoginForm}
        >
          로그인
        </button>
        <button
          className={showSignupForm ? "btn-auth-active" : "btn-auth-inactive"}
          onClick={handleShowSignupForm}
        >
          회원가입
        </button>
      </div>
      {showLoginForm && <LoginForm />}
      {showSignupForm && <SignupForm />}
      <button
        className="self-center text-sm text-primary hover:underline hover:underline-offset-4"
        onClick={handleFindPassword}
      >
        비밀번호 찾기
      </button>
    </div>
  );
}
