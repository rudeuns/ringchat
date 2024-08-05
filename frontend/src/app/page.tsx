import { SmallLogo, LargeLogo } from "@/components/common/Logos"
import { ServiceDesc } from "@/components/common/Descriptions"
import LoginButton from '@/components/buttons/LoginButton';
import SignupButton from '@/components/buttons/SignupButton';

export default function RootPage() {
  return (
    <div className="full-container">
      <div className="sidebar-container">
        <div className="sidebar-guest">
          <SmallLogo />
          <p>로그인이 필요한 서비스입니다.</p>
        </div>
      </div>
      <div className="main-container">
        <div className="h-11" />
        <div className="logo-desc">
          <LargeLogo />
          <ServiceDesc />
        </div>
        <div className='login-nav'>
          <LoginButton />
          <SignupButton />
        </div>
      </div>
    </div>
  )
}
