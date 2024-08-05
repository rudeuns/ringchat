import type { Metadata } from 'next';
import { Noto_Sans_KR } from 'next/font/google';
import { AuthProvider } from '@/context/AuthContext';
import '@/styles/globals.css';
import '@/styles/sidebar.css';
import '@/styles/modal.css';

const notoSansKR = Noto_Sans_KR({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'RingChat',
  icons: {
    icon: '/favicon.svg'
  }
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className={notoSansKR.className}>
        <AuthProvider>
          <main>{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}
