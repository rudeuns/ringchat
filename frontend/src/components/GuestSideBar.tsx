import { LogoSmall } from '@/components/Logo';

export default function GuestSideBar() {
  return (
    <div className="sb-logo-container-g">
      <LogoSmall />
      <p className="text-base">로그인이 필요한 서비스입니다.</p>
    </div>
  );
}
