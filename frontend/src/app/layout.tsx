import type { Metadata } from 'next';
import { Noto_Sans_KR } from 'next/font/google';
import { AuthProvider } from '@/context/AuthContext';
import Sidebar from '@/components/SideBar';
import '@/styles/globals.css';

const noto = Noto_Sans_KR({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'RingChat',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className={noto.className}>
        <AuthProvider>
          <div className="full-container">
            <Sidebar />
            <main>{children}</main>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
